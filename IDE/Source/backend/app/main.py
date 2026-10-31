import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, update, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from .database import Base, ROOT, engine, session
from .models import now
from .accounts import Account, Attempt, Completion, Draft, Project, Setting, current_account, router as auth_router
from .schemas import AttemptIn, DraftIn, ProjectIn, SettingsIn
from .ide_settings import IDEProfileDocument
from .content import BY_ID, DOCS, LANGUAGES, LESSONS, TRACKS
from .security import LocalSecurityMiddleware, ORIGINS

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title='DevForge local API', version='1.0.0', lifespan=lifespan)
app.include_router(auth_router)
from .learning import router as learning_router
from .ai import router as ai_router
from .sync import router as sync_router
app.include_router(learning_router)
app.include_router(ai_router)
app.include_router(sync_router)

app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type'])

app.add_middleware(LocalSecurityMiddleware)

@app.exception_handler(Exception)
async def unexpected(_request: Request, exc: Exception):
    logging.exception('Unhandled API error', exc_info=exc)
    return JSONResponse({'detail': 'Ошибка хранилища. Повторите действие; подробности в журнале сервера.'}, status_code=500)

def lesson_or_404(lesson_id: str):
    if lesson_id not in BY_ID:
        raise HTTPException(404, 'Lesson not found')
    return BY_ID[lesson_id]

@app.get('/api/health')
def health():
    return {'status': 'ok', 'version': '1.0.0', 'execution': 'browser-workers'}

@app.get('/api/platform')
def platform_info():
    is_desktop = bool(os.environ.get('DEVFORGE_DESKTOP'))
    mode = os.environ.get('DEVFORGE_MODE', 'full')
    return {
        'platform': 'desktop' if is_desktop else 'web',
        'mode': mode,
        'version': '1.0.0',
        'standalone': True,
        'storage': str(ROOT)
    }

@app.get('/api/languages')
def languages():
    return LANGUAGES

@app.get('/api/courses')
def courses():
    return [{'id': lang['id'], 'name': lang['name'], 'lessons': sorted([l for l in LESSONS if l['language'] == lang['id']],key=lambda l:l['order'])} for lang in LANGUAGES if lang['status']=='available']

@app.get('/api/courses/{course_id}')
def course(course_id: str):
    result = next((c for c in courses() if c['id'] == course_id), None)
    if result is None:
        raise HTTPException(404, 'Course not found')
    return result

@app.get('/api/tracks')
def tracks():
    return TRACKS

@app.get('/api/tracks/{track_id}')
def track(track_id: str):
    result = next((t for t in TRACKS if t['id'] == track_id), None)
    if result is None:
        raise HTTPException(404, 'Track not found')
    return result

@app.get('/api/lessons/{lesson_id}')
def lesson(lesson_id: str):
    return lesson_or_404(lesson_id)

@app.get('/api/documentation')
def documentation(q: str = ''):
    return [doc for doc in DOCS if q.casefold() in ' '.join([doc['title'], doc['explanation'], doc['language']]).casefold()]

@app.get('/api/progress')
def progress(db: Session = Depends(session), account: Account = Depends(current_account)):
    completed = db.scalars(select(Completion).where(Completion.owner_id == account.id)).all()
    attempts = db.scalars(select(Attempt).where(Attempt.owner_id == account.id).order_by(Attempt.created_at.desc()).limit(50)).all()
    count = db.scalar(select(func.count()).select_from(Attempt).where(Attempt.owner_id == account.id))
    return {'completed': [c.lesson_id for c in completed], 'xp': sum(c.xp for c in completed), 'attemptCount': count, 'attempts': [{'id': a.id, 'lesson_id': a.lesson_id, 'passed': a.passed, 'total': a.total, 'created_at': a.created_at} for a in attempts]}

@app.post('/api/progress/attempts')
def attempt(body: AttemptIn, db: Session = Depends(session), account: Account = Depends(current_account)):
    lesson = lesson_or_404(body.lesson_id)
    expected = {t['id']: t['expected'] for t in lesson['tests']}
    if len(body.results) != len(expected) or {r.id for r in body.results} != set(expected):
        raise HTTPException(422, 'All unique test results are required')
    passed = sum(r.error is None and r.actual == expected[r.id] for r in body.results)
    existing=db.get(Attempt,str(body.id))
    if existing and (existing.owner_id != account.id or existing.lesson_id != body.lesson_id):
        raise HTTPException(409,'Attempt ID already used')
    values = dict(owner_id=account.id, id=str(body.id), lesson_id=body.lesson_id, results=[r.model_dump() for r in body.results], passed=passed, total=len(expected), created_at=now())
    created = db.execute(insert(Attempt).values(**values).on_conflict_do_nothing(index_elements=['id'])).rowcount
    if created and passed == len(expected):
        db.execute(insert(Completion).values(owner_id=account.id, lesson_id=body.lesson_id, xp=lesson['xp'], created_at=now()).on_conflict_do_nothing(index_elements=['owner_id','lesson_id']))
    db.commit()
    saved = db.get(Attempt, str(body.id))
    return {'passed': saved.passed, 'total': saved.total, 'progress': progress(db,account)}

@app.get('/api/settings')
def settings(db: Session = Depends(session), account: Account = Depends(current_account)):
    row = db.get(Setting, account.id)
    return SettingsIn(**row.value).model_dump() if row else SettingsIn().model_dump()

@app.get('/api/ide/profile-schema')
def ide_profile_schema(account: Account = Depends(current_account)):
    return IDEProfileDocument.model_json_schema()

@app.post('/api/ide/validate-profile')
def validate_ide_profile(body: IDEProfileDocument, account: Account = Depends(current_account)):
    # Validation has no side effects. Applying a profile is an explicit settings save.
    return body

@app.put('/api/settings')
def save_settings(body: SettingsIn, db: Session = Depends(session), account: Account = Depends(current_account)):
    if body.lastLesson:
        lesson_or_404(body.lastLesson)
    db.merge(Setting(owner_id=account.id, value=body.model_dump()))
    db.commit()
    return body

@app.get('/api/drafts/{lesson_id}')
def draft(lesson_id: str, db: Session = Depends(session), account: Account = Depends(current_account)):
    lesson = lesson_or_404(lesson_id)
    row = db.get(Draft, (account.id,lesson_id))
    return {'code': row.code if row else lesson['starterCode']}

@app.put('/api/drafts/{lesson_id}')
def save_draft(lesson_id: str, body: DraftIn, db: Session = Depends(session), account: Account = Depends(current_account)):
    lesson_or_404(lesson_id)
    db.merge(Draft(owner_id=account.id,lesson_id=lesson_id, code=body.code))
    db.commit()
    return body

def project_dict(row: Project):
    return {key: getattr(row, key) for key in ('id', 'name', 'language', 'files', 'revision', 'updated_at')}

@app.get('/api/projects')
def projects(db: Session = Depends(session), account: Account = Depends(current_account)):
    return [project_dict(row) for row in db.scalars(select(Project).where(Project.owner_id == account.id).order_by(Project.updated_at.desc())).all()]

@app.post('/api/projects', status_code=201)
def create_project(body: ProjectIn, db: Session = Depends(session), account: Account = Depends(current_account)):
    row = Project(owner_id=account.id,id=str(uuid4()), **body.model_dump(exclude={'revision'}), revision=1)
    db.add(row)
    db.commit()
    return project_dict(row)

@app.get('/api/projects/{project_id}')
def project(project_id: str, db: Session = Depends(session), account: Account = Depends(current_account)):
    row = db.get(Project, project_id)
    if not row or row.owner_id != account.id:
        raise HTTPException(404, 'Project not found')
    return project_dict(row)

@app.put('/api/projects/{project_id}')
def save_project(project_id: str, body: ProjectIn, db: Session = Depends(session), account: Account = Depends(current_account)):
    project(project_id, db, account)
    changed = db.execute(update(Project).where(Project.id == project_id, Project.owner_id == account.id, Project.revision == body.revision).values(**body.model_dump(exclude={'revision'}), revision=body.revision + 1, updated_at=now())).rowcount
    if not changed:
        raise HTTPException(409, 'Проект изменён в другой вкладке. Скопируйте код и откройте проект заново.')
    db.commit()
    return project(project_id, db, account)

@app.delete('/api/projects/{project_id}', status_code=204)
def delete_project(project_id: str, db: Session = Depends(session), account: Account = Depends(current_account)):
    row = db.get(Project, project_id)
    if not row or row.owner_id != account.id:
        raise HTTPException(404, 'Project not found')
    db.delete(row)
    db.commit()

@app.post('/api/runner/java')
def runner_java(account: Account = Depends(current_account)):
    # A host JVM is not a sandbox. Java uses the same disposable Worker as other languages.
    return {'available': False}

DIST = ROOT / 'frontend' / 'dist'
if DIST.exists():
    app.mount('/assets', StaticFiles(directory=DIST / 'assets'), name='assets')
    app.mount('/runtimes', StaticFiles(directory=DIST / 'runtimes'), name='runtimes')
    app.mount('/workers', StaticFiles(directory=DIST / 'workers'), name='workers')

    @app.get('/{path:path}')
    def frontend(path: str):
        if path.startswith('api/'):
            raise HTTPException(404, 'Endpoint not found')
        if path in {'forge.svg', 'favicon.ico'}:
            asset = DIST / path
            if not asset.is_file():raise HTTPException(404, 'Asset not found')
            return FileResponse(asset)
        return FileResponse(DIST / 'index.html')
