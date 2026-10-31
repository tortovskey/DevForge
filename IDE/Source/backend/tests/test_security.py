import asyncio
import json
from unittest.mock import patch
import pytest
from app.security import LocalSecurityMiddleware, MAX_BODY


@pytest.mark.parametrize('host', ['evil.test', '127.0.0.1@evil.test', 'localhost/forged',
                                  'localhost?x=', 'localhost#x', 'localhost:99999'])
def test_raw_host_is_validated(client, host):
    assert client.get('/api/health', headers={'Host': host}).status_code == 403


@pytest.mark.parametrize('path', ['/assets/%5C%5Cattacker.invalid%5Cshare', '/runtimes/C:%5Cwindows', '/workers/a%00.js'])
def test_windows_paths_rejected_before_static_file_lookup(client, path):
    with patch('starlette.staticfiles.StaticFiles.get_response', side_effect=AssertionError('unsafe filesystem lookup')):
        assert client.get(path).status_code == 400


def test_headers_and_worker_network_policy(client):
    response = client.get('/api/settings')
    assert response.headers['cache-control'] == 'no-store'
    assert response.headers['x-frame-options'] == 'DENY'
    assert response.headers['cross-origin-opener-policy'] == 'same-origin'
    response = client.get('/workers/javascript.js')
    policy = response.headers['content-security-policy']
    connect = next(part for part in policy.split(';') if part.strip().startswith('connect-src'))
    assert '/runtimes/' in connect and '/api/' not in connect and "'self'" not in connect


def test_native_java_never_starts_process_or_writes_file(client, tmp_path):
    with patch('subprocess.run', side_effect=AssertionError('host process execution')):
        response = client.post('/api/runner/java', json={'filename': str(tmp_path / 'outside.java'), 'code': 'untrusted'})
    assert response.status_code == 200 and response.json() == {'available': False}
    assert not (tmp_path / 'outside.java').exists()
    client.post('/api/auth/logout')
    assert client.post('/api/runner/java', json={}).status_code == 401


def test_body_limit_counts_streamed_bytes():
    called = False
    async def downstream(scope, receive, send):
        nonlocal called
        called = True
    async def run():
        messages = []
        async def receive():
            return {'type': 'http.request', 'body': b'x' * 1_000_001, 'more_body': True}
        async def send(message):
            messages.append(message)
        await LocalSecurityMiddleware(downstream)({'type': 'http', 'scheme': 'http', 'method': 'POST',
            'path': '/api/sync/import', 'headers': [(b'host', b'localhost')]}, receive, send)
        assert messages[0]['status'] == 413
    asyncio.run(run())
    assert not called


def test_auth_throttle_and_session_rotation(client):
    old = client.cookies.get('devforge_session')
    assert client.post('/api/auth/login', json={'username': 'tester', 'password': 'TestPassword42'}).status_code == 200
    token = client.cookies.get('devforge_session')
    assert token != old
    assert client.get('/api/auth/me', headers={'Cookie': f'devforge_session={old}'}).status_code == 401
    for _ in range(9):
        assert client.post('/api/auth/login', json={'username': 'tester', 'password': 'wrong'}).status_code == 401
    response = client.post('/api/auth/login', json={'username': 'tester', 'password': 'wrong'})
    assert response.status_code == 429 and response.headers['retry-after'] == '60'


def test_minimap_setting_persists(client):
    assert client.put('/api/settings', json={'minimap': True}).status_code == 200
    assert client.get('/api/settings').json()['minimap'] is True


def test_guest_does_not_take_over_registered_developer(client):
    assert client.post('/api/auth/register',json={'username':'developer','displayName':'Private','password':'Password42'}).status_code==201
    project=client.post('/api/projects',json={'name':'Private','language':'python','files':[{'name':'main.py','content':'secret'}]}).json()
    response=client.post('/api/auth/guest',json={})
    assert response.status_code==200 and response.json()['id']=='dev-local-user'
    assert client.get('/api/projects/'+project['id']).status_code==404


def test_allow_all_hosts_environment_cannot_disable_security(client,monkeypatch):
    monkeypatch.setenv('DEVFORGE_ALLOW_ALL_HOSTS','1')
    assert client.get('/api/health',headers={'Host':'evil.test'}).status_code==403


def test_logo_is_served_as_an_image(client):
    response=client.get('/forge.svg')
    assert response.status_code==200 and response.headers['content-type'].startswith('image/svg+xml')
    assert '<svg' in response.text


def test_project_documentation_and_data_files_are_supported(client):
    response=client.post('/api/projects',json={'name':'Documented project','language':'python','files':[
        {'name':'main.py','content':'print(42)'},{'name':'README.md','content':'# Project'},
        {'name':'config.json','content':'{}'}]})
    assert response.status_code==201 and len(response.json()['files'])==3
