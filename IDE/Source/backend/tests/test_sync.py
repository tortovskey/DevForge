import copy
import sqlite3
from uuid import uuid4
import pytest
from app.content import BY_ID
from app.sync import checksum


def export(client):
    response = client.get('/api/sync/export')
    assert response.status_code == 200
    return response.json()


def signed(bundle):
    bundle['checksum'] = checksum(bundle['data'])
    return bundle


def register_other(client):
    assert client.post('/api/auth/register', json={
        'username': 'other', 'displayName': 'Other', 'password': 'Password42'
    }).status_code == 201


def test_release_1_reads_legacy_05_backups(client):
    bundle = export(client)
    assert bundle['version'] == '1.0.0'
    bundle['version'] = '0.5.0'
    result = client.post('/api/sync/import', json={'bundle': bundle})
    assert result.status_code == 200, result.text


def create_attempt(client):
    lesson = BY_ID['python-first-print']
    body = {'id': str(uuid4()), 'lesson_id': lesson['id'],
            'results': [{'id': t['id'], 'actual': t['expected']} for t in lesson['tests']]}
    assert client.post('/api/progress/attempts', json=body).status_code == 200


def test_sync_roundtrip_settings_drafts_assessments_and_scores(client, tmp_path):
    assert client.get('/api/platform').json()['platform'] in ('web', 'desktop')
    assert client.put('/api/settings', json={'theme': 'light', 'minimap': True}).status_code == 200
    client.put('/api/drafts/python-first-print', json={'code': 'print("saved")'})
    questions = client.get('/api/assessment/python').json()
    client.post('/api/assessment/python', json={'answers': {q['id']: -1 for q in questions}})
    create_attempt(client)
    bundle = export(client)
    assert bundle['data']['settings']['minimap'] is True
    assert bundle['checksum'] == checksum(bundle['data'])
    register_other(client)
    result = client.post('/api/sync/import', json={'bundle': bundle})
    assert result.status_code == 200, result.text
    assert client.get('/api/settings').json()['theme'] == 'light'
    assert client.get('/api/drafts/python-first-print').json()['code'] == 'print("saved")'
    assert client.get('/api/learning-plan').json()['courses'][0]['assessment']['score'] == 0
    assert client.get('/api/progress').json()['xp'] == BY_ID['python-first-print']['xp']
    backup = tmp_path / 'backups' / result.json()['backup_created']
    with sqlite3.connect(backup) as db:
        assert db.execute('SELECT COUNT(*) FROM v2_accounts').fetchone()[0] == 2
        assert db.execute('SELECT COUNT(*) FROM v2_completions').fetchone()[0] == 1
    assert client.get('/api/sync/backups').json()[0]['name'] == backup.name


def test_sync_cross_account_ids_remap_and_repeat_is_idempotent(client):
    project = client.post('/api/projects', json={'name': 'Original', 'language': 'python',
        'files': [{'name': 'main.py', 'content': 'print(42)'}]}).json()
    create_attempt(client)
    bundle = export(client)
    register_other(client)
    first = client.post('/api/sync/import', json={'bundle': bundle})
    assert first.status_code == 200, first.text
    own = client.get('/api/projects').json()
    assert len(own) == 1 and own[0]['id'] != project['id']
    again = client.post('/api/sync/import', json={'bundle': bundle})
    assert again.status_code == 200 and again.json()['imported_projects'] == 0
    assert client.get('/api/progress').json()['attemptCount'] == 1
    assert client.get('/api/projects/' + project['id']).status_code == 404
    client.post('/api/auth/login', json={'username': 'tester', 'password': 'TestPassword42'})
    assert client.get('/api/projects/' + project['id']).json() == project


@pytest.mark.parametrize('kind', ['checksum', 'missing_checksum', 'unknown_lesson', 'traversal',
                                 'duplicate', 'settings', 'timestamp', 'version', 'oversized_code'])
def test_sync_rejects_corruption_before_backup_or_writes(client, tmp_path, kind):
    bundle = export(client)
    if kind == 'checksum':
        bundle['checksum'] = '0' * 64
    elif kind == 'missing_checksum':
        del bundle['checksum']
    else:
        if kind == 'unknown_lesson':
            bundle['data']['completions'] = [{'lesson_id': 'missing', 'xp': 100, 'created_at': '2026-01-01T00:00:00Z'}]
        elif kind == 'traversal':
            bundle['data']['projects'] = [{'id': 'unsafe', 'name': 'Unsafe', 'language': 'python',
                'files': [{'name': '../escape.py', 'content': ''}], 'revision': 1, 'updated_at': '2026-01-01T00:00:00Z'}]
        elif kind in ('duplicate', 'oversized_code'):
            bundle['data']['drafts'] = [{'lesson_id': 'python-first-print', 'code': 'x' * (200001 if kind == 'oversized_code' else 1)}]
            if kind == 'duplicate':
                bundle['data']['drafts'] *= 2
        elif kind == 'settings':
            bundle['data']['settings'] = {'aiPort': 80}
        elif kind == 'timestamp':
            bundle['data']['completions'] = [{'lesson_id': 'python-first-print', 'xp': 10, 'created_at': 'broken'}]
        elif kind == 'version':
            bundle['version'] = '0.50.0'
        signed(bundle)
    before = export(client)
    response = client.post('/api/sync/import', json={'bundle': bundle})
    assert response.status_code == 400, response.text
    assert export(client)['data'] == before['data']
    assert not list((tmp_path / 'backups').glob('*.db'))


def test_sync_merge_overwrite_and_stale_revision(client):
    project = client.post('/api/projects', json={'name': 'Old', 'language': 'python',
        'files': [{'name': 'main.py', 'content': 'old'}]}).json()
    client.put('/api/drafts/python-first-print', json={'code': 'old'})
    client.put('/api/settings', json={'theme': 'light'})
    bundle = export(client)
    changed = {k: project[k] for k in ('name', 'language', 'files', 'revision')}
    changed['name'] = 'New'
    client.put('/api/projects/' + project['id'], json=changed)
    client.put('/api/drafts/python-first-print', json={'code': 'new'})
    client.put('/api/settings', json={'theme': 'dark'})
    assert client.post('/api/sync/import', json={'bundle': bundle}).status_code == 200
    assert client.get('/api/drafts/python-first-print').json()['code'] == 'new'
    assert client.get('/api/settings').json()['theme'] == 'dark'
    response = client.post('/api/sync/import', json={'bundle': bundle, 'mode': 'overwrite'})
    assert response.status_code == 200, response.text
    restored = client.get('/api/projects/' + project['id']).json()
    assert restored['name'] == 'Old' and restored['revision'] == 3
    assert client.get('/api/drafts/python-first-print').json()['code'] == 'old'
    assert client.get('/api/settings').json()['theme'] == 'light'
    assert client.put('/api/projects/' + project['id'], json=changed).status_code == 409
    assert client.post('/api/sync/import', json={'bundle': bundle, 'mode': 'bad'}).status_code == 422


def test_sync_backup_failure_is_fail_closed(client, monkeypatch):
    from app import sync
    bundle = export(client)
    bundle['data']['drafts'] = [{'lesson_id': 'python-first-print', 'code': 'must not save'}]
    signed(bundle)
    def fail(*args, **kwargs):
        raise sqlite3.OperationalError('disk full')
    monkeypatch.setattr(sync.sqlite3, 'connect', fail)
    assert client.post('/api/sync/import', json={'bundle': bundle}).status_code == 503
    assert client.get('/api/drafts/python-first-print').json()['code'] != 'must not save'


def test_sync_recomputes_xp_and_attempt_scores(client):
    create_attempt(client)
    bundle = export(client)
    bundle['data']['completions'][0]['xp'] = 999999
    item = bundle['data']['attempts'][0]
    item['passed'] = 20
    for result in item['results']:
        result['error'] = 'Execution failed'
    signed(bundle)
    register_other(client)
    assert client.post('/api/sync/import', json={'bundle': bundle}).status_code == 200
    progress = client.get('/api/progress').json()
    assert progress['xp'] == BY_ID['python-first-print']['xp']
    assert progress['attempts'][0]['passed'] == 0
