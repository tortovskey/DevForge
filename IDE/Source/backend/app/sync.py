"""Validated, transactional account transfers with backups of the active database."""
import hashlib
import json
import os
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Literal
from uuid import NAMESPACE_URL, uuid4, uuid5
from fastapi import APIRouter, Depends, HTTPException
from pydantic import AfterValidator, Field, ValidationError, field_validator, model_validator
from sqlalchemy import select
from sqlalchemy.orm import Session
from .accounts import Account, Assessment, Attempt, Completion, Draft, Project, Setting, current_account
from .content import BY_ID
from .database import DATA, session
from .learning import QUESTIONS, assessment_value
from .models import now
from .schemas import DraftIn, ProjectIn, ResultIn, SettingsIn, StrictModel

router = APIRouter(prefix='/api/sync', tags=['sync'])


def known_lesson(value: str) -> str:
    if value not in BY_ID:
        raise ValueError('Unknown lesson')
    return value


def valid_timestamp(value: str) -> str:
    datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value


LessonId = Annotated[str, Field(max_length=80), AfterValidator(known_lesson)]
Timestamp = Annotated[str, Field(max_length=50), AfterValidator(valid_timestamp)]
RecordId = Annotated[str, Field(min_length=1, max_length=128)]


class CompletionData(StrictModel):
    lesson_id: LessonId
    xp: int = Field(ge=0, le=1_000_000)
    created_at: Timestamp


class AttemptData(StrictModel):
    id: RecordId
    lesson_id: LessonId
    passed: int = Field(ge=0, le=20)
    total: int = Field(ge=1, le=20)
    results: list[ResultIn] = Field(max_length=20)
    created_at: Timestamp

    @model_validator(mode='after')
    def validate_results(self):
        expected = {t['id']: t['expected'] for t in BY_ID[self.lesson_id]['tests']}
        if len(self.results) != len(expected) or {r.id for r in self.results} != set(expected):
            raise ValueError('All unique test results are required')
        self.total = len(expected)
        self.passed = sum(r.error is None and r.actual == expected[r.id] for r in self.results)
        return self


class DraftData(DraftIn):
    lesson_id: LessonId


class ProjectData(ProjectIn):
    id: RecordId
    updated_at: Timestamp


class AssessmentAnswer(StrictModel):
    id: str = Field(max_length=80)
    tag: str = Field(max_length=80)
    correct: bool
    answer: int = Field(ge=-1, le=100)
    expected: int = Field(ge=0, le=100)
    explanation: str = Field(max_length=10000)


class AssessmentValue(StrictModel):
    language: str = Field(max_length=30)
    score: int = Field(ge=0, le=30)
    total: int = Field(ge=1, le=30)
    level: str = Field(max_length=40)
    results: list[AssessmentAnswer] = Field(max_length=30)
    createdAt: Timestamp
    preliminary: Literal[True]


class AssessmentData(StrictModel):
    language: str = Field(max_length=30)
    value: AssessmentValue

    @model_validator(mode='after')
    def validate_answers(self):
        entries = [q for q in QUESTIONS if q['language'] == self.language]
        answers = {r.id: r.answer for r in self.value.results}
        if (not entries or self.value.language != self.language or len(answers) != len(self.value.results)
                or set(answers) != {q['id'] for q in entries}
                or any(not -1 <= answers[q['id']] < len(q['options']) for q in entries)):
            raise ValueError('Invalid assessment answers')
        return self


class SyncData(StrictModel):
    completions: list[CompletionData] = Field(default_factory=list, max_length=1000)
    attempts: list[AttemptData] = Field(default_factory=list, max_length=10000)
    drafts: list[DraftData] = Field(default_factory=list, max_length=1000)
    projects: list[ProjectData] = Field(default_factory=list, max_length=1000)
    settings: SettingsIn = Field(default_factory=SettingsIn)
    assessments: list[AssessmentData] = Field(default_factory=list, max_length=30)

    @field_validator('settings')
    @classmethod
    def validate_settings(cls, value):
        if value.lastLesson:
            known_lesson(value.lastLesson)
        return value

    @model_validator(mode='after')
    def unique_records(self):
        for rows, key in ((self.completions, 'lesson_id'), (self.drafts, 'lesson_id'),
                          (self.attempts, 'id'), (self.projects, 'id'), (self.assessments, 'language')):
            if len({getattr(row, key) for row in rows}) != len(rows):
                raise ValueError('Duplicate records in sync bundle')
        return self


class ImportRequest(StrictModel):
    bundle: dict
    mode: Literal['merge', 'overwrite'] = 'merge'


def checksum(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, allow_nan=False).encode('utf-8')).hexdigest()


def database_file(db: Session) -> Path | None:
    bind = db.get_bind()
    name = bind.url.database
    return Path(name).resolve() if bind.dialect.name == 'sqlite' and name and name != ':memory:' else None


def get_backup_dir(db: Session) -> Path:
    source = database_file(db)
    folder = (source.parent if source else DATA) / 'backups'
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def create_db_backup(db: Session) -> str:
    source = database_file(db)
    if source is None:
        raise HTTPException(503, 'Невозможно создать резервную копию этой базы данных')
    name = f'devforge_pre_import_{datetime.now(timezone.utc):%Y%m%d_%H%M%S_%f}_{uuid4().hex[:8]}.db'
    target = get_backup_dir(db) / name
    try:
        with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(target) as dst:
            src.backup(dst)
    except (OSError, sqlite3.Error) as exc:
        target.unlink(missing_ok=True)
        raise HTTPException(503, 'Резервная копия не создана. Импорт отменён.') from exc
    return name


@router.get('/export')
def export_data(account: Account = Depends(current_account), db: Session = Depends(session)):
    def rows(model):
        return db.scalars(select(model).where(model.owner_id == account.id)).all()

    setting = db.get(Setting, account.id)
    data = {
        'completions': [{k: getattr(c, k) for k in ('lesson_id', 'xp', 'created_at')} for c in rows(Completion)],
        'attempts': [{k: getattr(a, k) for k in ('id', 'lesson_id', 'passed', 'total', 'results', 'created_at')} for a in rows(Attempt)],
        'drafts': [{'lesson_id': d.lesson_id, 'code': d.code} for d in rows(Draft)],
        'projects': [{k: getattr(p, k) for k in ('id', 'name', 'language', 'files', 'revision', 'updated_at')} for p in rows(Project)],
        'settings': SettingsIn(**setting.value).model_dump() if setting else {},
        'assessments': [{'language': a.language, 'value': a.value} for a in rows(Assessment)],
    }
    return {'format': 'devforge-sync', 'version': '1.0.1', 'exported_at': now(),
            'platform': 'desktop' if os.environ.get('DEVFORGE_DESKTOP') else 'web',
            'account': {'username': account.username, 'displayName': account.display_name},
            'data': data, 'checksum': checksum(data)}


def scoped_id(db: Session, model, identifier: str, owner: str) -> str:
    """Stable remapping makes repeated transfers between accounts idempotent."""
    candidate = identifier
    while True:
        row = db.get(model, candidate)
        if row is None or row.owner_id == owner:
            return candidate
        candidate = str(uuid5(NAMESPACE_URL, f'devforge:{model.__tablename__}:{owner}:{candidate}'))


@router.post('/import')
def import_data(req: ImportRequest, account: Account = Depends(current_account), db: Session = Depends(session)):
    bundle = req.bundle
    if bundle.get('format') != 'devforge-sync':
        raise HTTPException(400, 'Некорректный формат файла синхронизации DevForge')
    if not re.fullmatch(r'(?:0\.[45]\.[0-9]+|1\.0\.[0-9]+)', str(bundle.get('version', ''))):
        raise HTTPException(400, 'Неподдерживаемая версия данных')
    payload = bundle.get('data')
    supplied = bundle.get('checksum')
    try:
        if not isinstance(payload, dict) or not isinstance(supplied, str) or not secrets.compare_digest(checksum(payload), supplied):
            raise ValueError('Checksum mismatch')
        data = SyncData.model_validate(payload)
    except (ValidationError, ValueError, TypeError) as exc:
        raise HTTPException(400, 'Файл повреждён или содержит некорректные данные. Импорт отменён.') from exc

    backup_name = create_db_backup(db)
    counts = {'completions': 0, 'projects': 0, 'drafts': 0}
    try:
        for c in data.completions:
            if db.get(Completion, (account.id, c.lesson_id)) is None:
                db.add(Completion(owner_id=account.id, lesson_id=c.lesson_id, xp=BY_ID[c.lesson_id]['xp'], created_at=c.created_at))
                counts['completions'] += 1
        for a in data.attempts:
            identifier = scoped_id(db, Attempt, a.id, account.id)
            if db.get(Attempt, identifier) is None:
                db.add(Attempt(owner_id=account.id, **{**a.model_dump(), 'id': identifier}))
        for d in data.drafts:
            row = db.get(Draft, (account.id, d.lesson_id))
            if row is None:
                db.add(Draft(owner_id=account.id, **d.model_dump()))
                counts['drafts'] += 1
            elif req.mode == 'overwrite':
                row.code = d.code
                counts['drafts'] += 1
        for p in data.projects:
            identifier = scoped_id(db, Project, p.id, account.id)
            row = db.get(Project, identifier)
            if row is None:
                db.add(Project(owner_id=account.id, **{**p.model_dump(), 'id': identifier}))
                counts['projects'] += 1
            elif req.mode == 'overwrite':
                row.name, row.language, row.files = p.name, p.language, [f.model_dump() for f in p.files]
                row.revision += 1
                row.updated_at = now()
                counts['projects'] += 1
        if payload.get('settings'):
            row = db.get(Setting, account.id)
            if row is None:
                db.add(Setting(owner_id=account.id, value=data.settings.model_dump()))
            elif req.mode == 'overwrite':
                row.value = data.settings.model_dump()
        for a in data.assessments:
            row = db.get(Assessment, (account.id, a.language))
            value = assessment_value(a.language, {r.id: r.answer for r in a.value.results}, a.value.createdAt)
            if row is None:
                db.add(Assessment(owner_id=account.id, language=a.language, value=value))
            elif req.mode == 'overwrite':
                row.value = value
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {'status': 'ok', 'message': 'Синхронизация завершена',
            **{f'imported_{k}': v for k, v in counts.items()}, 'backup_created': backup_name}


@router.get('/backups')
def list_backups(account: Account = Depends(current_account), db: Session = Depends(session)):
    backups = []
    for path in get_backup_dir(db).glob('*.db'):
        stat = path.stat()
        backups.append({'name': path.name, 'size': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()})
    return sorted(backups, key=lambda b: b['created_at'], reverse=True)
