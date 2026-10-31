import copy
import pytest


def profile():
    return {'format': 'devforge.ide-profile', 'version': 1, 'profile': {
        'id': 'work', 'name': 'My workbench', 'preferences': {
            'theme': 'light', 'fontSize': 18, 'minimap': True,
            'ide': {'theme': 'paper', 'sidebarSide': 'right', 'panelPosition': 'right',
                    'fontFamily': 'jetbrains', 'tabSize': 2, 'keymap': 'jetbrains',
                    'shortcuts': {'save': 'Ctrl+Alt+S', 'settings': 'Ctrl+Comma'},
                    'colors': {'editor': '#fefefe'}}}}}


def test_legacy_settings_gain_independent_workbench_defaults(client):
    old = {'theme': 'light', 'fontSize': 16, 'minimap': True}
    result = client.put('/api/settings', json=old)
    assert result.status_code == 200
    settings = client.get('/api/settings').json()
    assert settings['theme'] == 'light' and settings['fontSize'] == 16
    assert settings['ide']['theme'] == 'inherit'
    assert settings['ide']['sidebarWidth'] == 248
    assert settings['ideProfiles'] == []


def test_profiles_validate_without_mutation_and_survive_save_and_sync(client):
    before = client.get('/api/settings').json()
    validated = client.post('/api/ide/validate-profile', json=profile())
    assert validated.status_code == 200, validated.text
    assert client.get('/api/settings').json() == before
    p = validated.json()['profile']
    settings = {**before, **p['preferences'], 'ideProfiles': [p]}
    assert client.put('/api/settings', json=settings).status_code == 200
    assert client.get('/api/settings').json() == settings
    bundle = client.get('/api/sync/export').json()
    client.post('/api/auth/register', json={'username': 'profile_other', 'displayName': 'Other', 'password': 'Password42'})
    assert client.get('/api/settings').json()['ideProfiles'] == []
    imported = client.post('/api/sync/import', json={'bundle': bundle})
    assert imported.status_code == 200, imported.text
    assert client.get('/api/settings').json() == settings


@pytest.mark.parametrize('patch', [
    {'sidebarWidth': -1}, {'panelHeight': 999999}, {'tabSize': 3},
    {'lineHeight': 5}, {'accent': 'url(https://evil.invalid)'},
    {'colors': {'editor': '#fff;display:none'}}, {'colors': {'unknown': '#ffffff'}},
    {'shortcuts': {'eval': 'Ctrl+E'}}, {'shortcuts': {'save': 'Ctrl+P'}},
    {'shortcuts': {'save': 'Ctrl+W'}}, {'shortcuts': {'save': 'F1'}},
    {'shortcuts': {'save': 'Ctrl+Shift+Alt+S'}}, {'shortcuts': {'save': 'S'}},
    {'activityBar': 'false'}, {'fontFamily': 'https://evil.invalid/font'},
    {'theme': 'unknown'}, {'css': 'body{display:none}'}
])
def test_invalid_preferences_rejected_atomically(client, patch):
    before = client.get('/api/settings').json()
    result = client.put('/api/settings', json={**before, 'ide': {**before['ide'], **patch}})
    assert result.status_code == 422, result.text
    assert client.get('/api/settings').json() == before


def test_profile_documents_and_collection_are_bounded(client):
    valid = profile()
    for mutate in [lambda p: p.update(version=2),
                   lambda p: p.update(script='alert(1)'),
                   lambda p: p['profile'].update(name='  '),
                   lambda p: p['profile'].update(id='../../file')]:
        invalid = copy.deepcopy(valid)
        mutate(invalid)
        assert client.post('/api/ide/validate-profile', json=invalid).status_code == 422
    p = client.post('/api/ide/validate-profile', json=valid).json()['profile']
    settings = client.get('/api/settings').json()
    for profiles in [[p, p], [{**p, 'id': str(i), 'name': str(i)} for i in range(13)]]:
        assert client.put('/api/settings', json={**settings, 'ideProfiles': profiles}).status_code == 422
    schema = client.get('/api/ide/profile-schema').json()
    assert schema['additionalProperties'] is False
    assert 'IDEPreferences' in schema['$defs']


def test_unbound_command_and_both_keymaps_are_supported(client):
    for keymap in ['code', 'jetbrains']:
        result = client.put('/api/settings', json={'ide': {'keymap': keymap, 'shortcuts': {'save': ''}}})
        assert result.status_code == 200, result.text
        assert result.json()['ide']['shortcuts']['save'] == ''
