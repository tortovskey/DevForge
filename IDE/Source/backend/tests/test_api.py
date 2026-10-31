from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, session
from app.main import app
from app.content import BY_ID

@pytest.fixture
def client(tmp_path):
    engine = create_engine(f'sqlite:///{tmp_path / "test.db"}', connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    sessions = sessionmaker(engine)
    def isolated():
        with sessions() as db:
            yield db
    app.dependency_overrides[session] = isolated
    with TestClient(app) as http:
        assert http.post('/api/auth/register',json={'username':'tester','displayName':'Tester','password':'TestPassword42'}).status_code==201
        yield http
    app.dependency_overrides.clear()
    engine.dispose()

def project_body():
    return {'name': 'Laboratory', 'language': 'python', 'files': [{'name': 'main.py', 'content': 'print(8)'}]}

def attempt_body(lesson_id='python-functions', valid=True):
    return {'id': str(uuid4()), 'lesson_id': lesson_id, 'results': [{'id': t['id'], 'actual': t['expected'] if valid else 'wrong'} for t in BY_ID[lesson_id]['tests']]}

def test_health_content_and_no_cloud(client):
    assert client.get('/api/health').json()['execution'] == 'browser-workers'
    courses = client.get('/api/courses').json()
    assert len(courses) == 15
    assert sum(len(c['lessons']) for c in courses) == 377
    assert len(client.get('/api/documentation').json()) >= 20
    assert len(client.get('/api/documentation?q=функц').json()) >= 1
    languages = client.get('/api/languages').json()
    assert {l['id'] for l in languages if l['status'] == 'available'} == {'python', 'sql', 'postgresql', 'html-css', 'c', 'javascript', 'typescript', 'java', 'cpp', 'csharp', 'objc', 'rust', '1c', 'lua', 'assembly'}
    assert client.get('/api/lessons/missing').status_code == 404

def test_c_projects_diagnostic_and_curriculum_integrity(client):
    body={'name':'C modules','language':'c','files':[{'name':'main.c','content':'#include "helper.h"\nint main(void){return 0;}'},{'name':'helper.h','content':'int add(int,int);'}]}
    result=client.post('/api/projects',json=body)
    assert result.status_code==201
    assert client.get('/api/projects/'+result.json()['id']).json()['files']==body['files']
    questions=client.get('/api/assessment/c').json()
    assert len(questions)==8
    result=client.post('/api/assessment/c',json={'answers':{q['id']:-1 for q in questions}})
    assert result.status_code==200 and result.json()['score']==0
    courses=client.get('/api/courses').json()
    ids={l['id'] for c in courses for l in c['lessons']}
    assert len(ids) == 377
    for course in courses:
        assert [l['order'] for l in course['lessons']]==list(range(1,len(course['lessons'])+1))
        for lesson in course['lessons']:
            assert lesson['tests'] and len({t['id'] for t in lesson['tests']})==len(lesson['tests'])
            assert all(p in ids for p in lesson['prerequisites'])
            assert all(BY_ID[p]['order']<lesson['order'] for p in lesson['prerequisites'])
            assert all(r['url'].startswith('https://') for r in lesson['resources'])

def test_new_languages_projects_and_runner(client):
    js_proj = client.post('/api/projects', json={
        'name': 'JS Project',
        'language': 'javascript',
        'files': [{'name': 'index.js', 'content': 'console.log("Hello JS");'}]
    })
    assert js_proj.status_code == 201

    ts_proj = client.post('/api/projects', json={
        'name': 'TS Project',
        'language': 'typescript',
        'files': [{'name': 'index.ts', 'content': 'const x: number = 42;'}]
    })
    assert ts_proj.status_code == 201

    java_proj = client.post('/api/projects', json={
        'name': 'Java Project',
        'language': 'java',
        'files': [{'name': 'Main.java', 'content': 'public class Main { public static void main(String[] args) { System.out.println("Java OK"); } }'}]
    })
    assert java_proj.status_code == 201

    cpp_proj = client.post('/api/projects', json={
        'name': 'C++ Project',
        'language': 'cpp',
        'files': [{'name': 'main.cpp', 'content': '#include <iostream>\nint main() { return 0; }'}]
    })
    assert cpp_proj.status_code == 201

    cs_proj = client.post('/api/projects', json={
        'name': 'C# Project',
        'language': 'csharp',
        'files': [{'name': 'Program.cs', 'content': 'class Program { static void Main() {} }'}]
    })
    assert cs_proj.status_code == 201

    objc_proj = client.post('/api/projects', json={
        'name': 'Obj-C Project',
        'language': 'objc',
        'files': [{'name': 'main.m', 'content': 'int main() { return 0; }'}]
    })
    assert objc_proj.status_code == 201

    rust_proj = client.post('/api/projects', json={
        'name': 'Rust Project',
        'language': 'rust',
        'files': [{'name': 'main.rs', 'content': 'fn main() {}'}]
    })
    assert rust_proj.status_code == 201

    ones_proj = client.post('/api/projects', json={
        'name': '1C Project',
        'language': '1c',
        'files': [{'name': 'Module.bsl', 'content': 'Сообщить("Старт");'}]
    })
    assert ones_proj.status_code == 201

    for lang in ('javascript', 'typescript', 'java', 'cpp', 'csharp', 'objc', 'rust', '1c'):
        qs = client.get(f'/api/assessment/{lang}').json()
        assert len(qs) == 8
        score_res = client.post(f'/api/assessment/{lang}', json={'answers': {q['id']: 0 for q in qs}})
        assert score_res.status_code == 200

    java_run = client.post('/api/runner/java', json={
        'code': 'public class Main { public static void main(String[] args) { System.out.println("Native Java Test"); } }',
        'stdin': ''
    })
    assert java_run.status_code == 200
    res = java_run.json()
    assert 'available' in res
    if res['available']:
        assert 'Native Java Test' in res['result']['stdout']


def test_project_crud_and_revisions(client):
    response = client.post('/api/projects', json=project_body())
    assert response.status_code == 201
    project = response.json()
    pid = project['id']
    assert client.get(f'/api/projects/{pid}').json()['files'][0]['content'] == 'print(8)'
    body = {k: project[k] for k in ('name', 'language', 'files', 'revision')}
    body['files'][0]['name'] = 'renamed.py'
    body['files'].append({'name':'utils.py', 'content':'VALUE = 42'})
    saved = client.put(f'/api/projects/{pid}', json=body)
    assert saved.status_code == 200
    assert saved.json()['revision'] == 2
    assert client.put(f'/api/projects/{pid}', json=body).status_code == 409
    assert client.get('/api/projects').json()[0]['files'][1]['content'] == 'VALUE = 42'
    assert client.delete(f'/api/projects/{pid}').status_code == 204
    assert client.get(f'/api/projects/{pid}').status_code == 404

@pytest.mark.parametrize('name', ['../escape.py', 'C:\\secret.py', '/tmp/file.py', 'foo/../main.py', 'name.exe', '..py'])
def test_path_traversal_rejected(client, name):
    body = project_body()
    body['files'][0]['name'] = name
    assert client.post('/api/projects', json=body).status_code == 422

def test_unsupported_and_duplicate_files(client):
    body = project_body()
    body['language'] = 'ruby'
    assert client.post('/api/projects', json=body).status_code == 422
    body = project_body()
    body['files'].append({'name':'MAIN.py', 'content':''})
    assert client.post('/api/projects', json=body).status_code == 422

def test_progress_rejects_wrong_results_and_awards_once(client):
    bad = client.post('/api/progress/attempts', json=attempt_body(valid=False)).json()
    assert bad['passed'] == 0
    assert bad['progress']['xp'] == 0
    body = attempt_body()
    good = client.post('/api/progress/attempts', json=body).json()
    assert good['passed'] == 3
    assert good['progress']['xp'] == 60
    client.post('/api/progress/attempts', json=body)  # idempotent retry
    client.post('/api/progress/attempts', json=attempt_body())
    stored = client.get('/api/progress').json()
    assert stored['xp'] == 60
    assert stored['completed'] == ['python-functions']
    assert stored['attemptCount'] == 3

def test_errors_do_not_pass_null_expected_and_missing_tests(client):
    body = attempt_body('python-exceptions')
    for result in body['results']:
        result['error'] = 'NameError'
    assert client.post('/api/progress/attempts', json=body).json()['passed'] == 0
    body['results'].pop()
    assert client.post('/api/progress/attempts', json=body).status_code == 422
    body = attempt_body()
    body['results'][1]['id'] = body['results'][0]['id']
    assert client.post('/api/progress/attempts', json=body).status_code == 422

def test_settings_drafts_and_local_origin(client):
    settings = {'theme':'light', 'fontSize':18, 'mode':'developer', 'lastLesson':'python-functions'}
    assert client.put('/api/settings', json=settings).status_code == 200
    assert all(client.get('/api/settings').json()[k]==v for k,v in settings.items())
    assert client.put('/api/settings', json={**settings, 'fontSize':99}).status_code == 422
    code = "print('persistent')"
    client.put('/api/drafts/python-functions', json={'code':code})
    assert client.get('/api/drafts/python-functions').json()['code'] == code
    assert client.post('/api/projects', json=project_body(), headers={'Origin':'https://example.org'}).status_code == 403
    assert client.get('/api/health', headers={'Host':'attacker.example'}).status_code == 403

def test_storage_survives_new_connection(client):
    pid = client.post('/api/projects', json=project_body()).json()['id']
    client.post('/api/progress/attempts', json=attempt_body('sql-select'))
    # Every dependency opens a new SQLite session and connection lifecycle.
    assert client.get(f'/api/projects/{pid}').json()['name'] == 'Laboratory'
    assert client.get('/api/progress').json()['completed'] == ['sql-select']

def test_account_isolation_and_logout(client):
    project=client.post('/api/projects',json=project_body()).json()
    client.put('/api/drafts/python-functions',json={'code':'secret=42'})
    client.post('/api/progress/attempts',json=attempt_body())
    token=client.cookies.get('devforge_session')
    response=client.post('/api/auth/register',json={'username':'second','displayName':'Second','password':'OtherPassword42'})
    assert response.status_code==201
    assert 'HttpOnly' in response.headers['set-cookie'] and 'SameSite=strict' in response.headers['set-cookie']
    assert client.get('/api/projects').json()==[]
    assert client.get('/api/progress').json()['xp']==0
    assert client.get('/api/drafts/python-functions').json()['code']!='secret=42'
    assert client.get('/api/projects/'+project['id']).status_code==404
    assert client.delete('/api/projects/'+project['id']).status_code==404
    assert client.put('/api/projects/'+project['id'],json=project_body()).status_code==404
    client.post('/api/auth/logout')
    assert client.get('/api/progress').status_code==401
    assert client.post('/api/auth/login',json={'username':'tester','password':'wrong'}).status_code==401
    assert client.post('/api/auth/login',json={'username':'TESTER','password':'TestPassword42'}).status_code==200
    assert client.get('/api/projects').json()[0]['id']==project['id']

def test_placement_and_plan(client):
    from app.learning import QUESTIONS
    questions=client.get('/api/assessment/python').json()
    assert len(questions)==8 and all('correct' not in q for q in questions)
    answers={q['id']:-1 for q in questions}
    assert client.post('/api/assessment/python',json={'answers':{}}).status_code==422
    result=client.post('/api/assessment/python',json={'answers':answers}).json()
    assert result['level']=='С нуля' and result['score']==0
    plan=client.get('/api/learning-plan').json()['courses'][0]
    assert plan['nextLesson']=='python-first-print' and len(plan['recommended'])==66
    answers={q['id']:q['correct'] for q in QUESTIONS if q['language']=='python'}
    result=client.post('/api/assessment/python',json={'answers':answers}).json()
    assert result['score']==8
    plan=client.get('/api/learning-plan').json()['courses'][0]
    assert len(plan['review'])>0 and len(plan['recommended'])<35
    assert client.get('/api/progress').json()['xp']==0

def test_ai_local_only_and_validation(client):
    assert client.get('/api/ai/models').status_code==409
    assert client.put('/api/settings',json={'aiProvider':'cloud'}).status_code==422
    assert client.put('/api/settings',json={'aiPort':80}).status_code==422
    assert client.put('/api/settings',json={'aiProvider':'ollama','aiModel':'remote-cloud'}).status_code==200
    assert client.post('/api/ai/generate',json={'code':'print(1)'}).status_code==409
    assert client.post('/api/ai/generate',json={'url':'https://example.org'}).status_code==422

def test_ai_completion_removes_repeated_prefix_and_next_function(client,monkeypatch):
    from app import ai
    async def provider(port,path,body=None,timeout=15):
        assert port==11434 and path in {'/api/tags','/api/generate'}
        return {'models':[{'name':'test-coder'}]} if path=='/api/tags' else {'response':'def add(a, b):\n    return a + b\n\ndef subtract(a, b):'}
    monkeypatch.setattr(ai,'local_call',provider)
    client.put('/api/settings',json={'aiProvider':'ollama','aiPort':11434,'aiModel':'test-coder'})
    response=client.post('/api/ai/generate',json={'mode':'complete','code':'def add(a, b):\n    return a +','suffix':'\n'})
    assert response.status_code==200 and response.json()['text']==' b'

def test_legacy_migration_once(tmp_path):
    from app.models import Project as LegacyProject,Completion as LegacyCompletion
    from app.accounts import Account,Project as NewProject
    engine=create_engine(f'sqlite:///{tmp_path / "legacy.db"}',connect_args={'check_same_thread':False})
    Base.metadata.create_all(engine)
    sessions=sessionmaker(engine)
    with sessions() as db:
        db.add(LegacyProject(id='old-project',name='Legacy',language='python',files=[{'name':'main.py','content':'print(42)'}],revision=3))
        db.add(LegacyCompletion(lesson_id='python-functions',xp=60));db.commit()
    def isolated():
        with sessions() as db:yield db
    app.dependency_overrides[session]=isolated
    try:
        with TestClient(app) as http:
            assert http.post('/api/auth/register',json={'username':'first','displayName':'First','password':'password42'}).status_code==201
            assert http.get('/api/projects').json()[0]['revision']==3
            assert http.get('/api/progress').json()['xp']==60
            http.post('/api/auth/register',json={'username':'second','displayName':'Second','password':'password42'})
            assert http.get('/api/projects').json()==[]
        with sessions() as db:assert db.get(LegacyProject,'old-project') is not None
    finally:app.dependency_overrides.clear();engine.dispose()



def test_tracks_api(client):
    res = client.get('/api/tracks')
    assert res.status_code == 200
    tracks = res.json()
    assert len(tracks) == 3
    track_ids = {t['id'] for t in tracks}
    assert track_ids == {'backend-development', 'frontend-development', 'java-development'}
    for t in tracks:
        assert t['modules'] and len(t['modules']) >= 5
        assert t['capstone'] and 'id' in t['capstone']
    single = client.get('/api/tracks/backend-development').json()
    assert single['id'] == 'backend-development'
    assert client.get('/api/tracks/unknown').status_code == 404
