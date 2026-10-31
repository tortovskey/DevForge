"""Local identities and scoped v0.2 storage. Legacy v0.1 tables remain untouched."""
import hashlib
import secrets
import time
from collections import OrderedDict, deque
from threading import Lock
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import Field, field_validator
from sqlalchemy import JSON, Integer, String, Text, select, func, delete
from sqlalchemy.orm import Mapped, mapped_column, Session
from .database import Base, session
from .schemas import StrictModel
from .models import now

class Account(Base):
    __tablename__='v2_accounts'
    id: Mapped[str]=mapped_column(String,primary_key=True)
    username: Mapped[str]=mapped_column(String,unique=True)
    display_name: Mapped[str]=mapped_column(String)
    password_hash: Mapped[str]=mapped_column(String)
    created_at: Mapped[str]=mapped_column(String,default=now)

class AuthSession(Base):
    __tablename__='v2_sessions'
    digest: Mapped[str]=mapped_column(String,primary_key=True)
    owner_id: Mapped[str]=mapped_column(String,index=True)
    expires: Mapped[int]=mapped_column(Integer)

class Project(Base):
    __tablename__='v2_projects'
    id: Mapped[str]=mapped_column(String,primary_key=True)
    owner_id: Mapped[str]=mapped_column(String,index=True)
    name: Mapped[str]=mapped_column(String)
    language: Mapped[str]=mapped_column(String)
    files: Mapped[list]=mapped_column(JSON)
    revision: Mapped[int]=mapped_column(Integer,default=1)
    updated_at: Mapped[str]=mapped_column(String,default=now)

class Attempt(Base):
    __tablename__='v2_attempts'
    id: Mapped[str]=mapped_column(String,primary_key=True)
    owner_id: Mapped[str]=mapped_column(String,index=True)
    lesson_id: Mapped[str]=mapped_column(String)
    results: Mapped[list]=mapped_column(JSON)
    passed: Mapped[int]=mapped_column(Integer)
    total: Mapped[int]=mapped_column(Integer)
    created_at: Mapped[str]=mapped_column(String,default=now)

class Completion(Base):
    __tablename__='v2_completions'
    owner_id: Mapped[str]=mapped_column(String,primary_key=True)
    lesson_id: Mapped[str]=mapped_column(String,primary_key=True)
    xp: Mapped[int]=mapped_column(Integer)
    created_at: Mapped[str]=mapped_column(String,default=now)

class Setting(Base):
    __tablename__='v2_settings'
    owner_id: Mapped[str]=mapped_column(String,primary_key=True)
    value: Mapped[dict]=mapped_column(JSON)

class Draft(Base):
    __tablename__='v2_drafts'
    owner_id: Mapped[str]=mapped_column(String,primary_key=True)
    lesson_id: Mapped[str]=mapped_column(String,primary_key=True)
    code: Mapped[str]=mapped_column(Text)

class Assessment(Base):
    __tablename__='v2_assessments'
    owner_id: Mapped[str]=mapped_column(String,primary_key=True)
    language: Mapped[str]=mapped_column(String,primary_key=True)
    value: Mapped[dict]=mapped_column(JSON)

class Registration(StrictModel):
    username:str=Field(min_length=3,max_length=32,pattern=r'^[a-zA-Z0-9_]+$')
    displayName:str=Field(min_length=1,max_length=60)
    password:str=Field(min_length=8,max_length=128)
    @field_validator('displayName')
    @classmethod
    def nonblank(cls,value):
        if not value.strip():raise ValueError('Введите имя')
        return value.strip()

class Login(StrictModel):
    username:str=Field(min_length=1,max_length=32)
    password:str=Field(min_length=1,max_length=128)

def hash_password(password:str,salt:str|None=None)->str:
    salt=salt or secrets.token_hex(16)
    digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),600_000).hex()
    return salt+':'+digest

def get_or_create_default_developer_account(db: Session) -> Account:
    # A guest must never inherit a registered user's account by matching its name.
    dev = db.get(Account, 'dev-local-user')
    if not dev:
        db.connection().exec_driver_sql('BEGIN IMMEDIATE')
        dev = db.get(Account, 'dev-local-user',populate_existing=True)
        if dev:return dev
        dev = Account(
            id='dev-local-user',
            username='__devforge_guest',
            display_name='Developer',
            password_hash=hash_password(secrets.token_hex(16)),
        )
        first=not db.scalar(select(func.count()).select_from(Account))
        db.add(dev)
        db.flush()
        if first:migrate_legacy(db,dev.id)
        db.commit()
        db.refresh(dev)
    return dev

def public(account:Account):
    return {'id':account.id,'username':account.username,'displayName':account.display_name}

def current_account(request:Request,db:Session=Depends(session))->Account:
    import os
    token=request.cookies.get('devforge_session','')
    record=db.get(AuthSession,hashlib.sha256(token.encode()).hexdigest()) if token else None
    if not record or record.expires<=int(time.time()):
        if os.environ.get('DEVFORGE_MODE') == 'ide':
            return get_or_create_default_developer_account(db)
        raise HTTPException(401,'Войдите в локальный аккаунт')
    account=db.get(Account,record.owner_id)
    if not account:
        if os.environ.get('DEVFORGE_MODE') == 'ide':
            return get_or_create_default_developer_account(db)
        raise HTTPException(401,'Аккаунт не найден')
    return account

def start_session(db:Session,response:Response,account:Account,previous_token:str=''):
    db.execute(delete(AuthSession).where(AuthSession.expires<=int(time.time())))
    if previous_token:
        db.execute(delete(AuthSession).where(AuthSession.digest==hashlib.sha256(previous_token.encode()).hexdigest()))
    token=secrets.token_urlsafe(32)
    db.add(AuthSession(digest=hashlib.sha256(token.encode()).hexdigest(),owner_id=account.id,expires=int(time.time())+7*86400))
    db.commit()
    response.set_cookie('devforge_session',token,httponly=True,samesite='strict',max_age=7*86400,path='/')
    return public(account)

router=APIRouter(prefix='/api/auth')

class AuthLimiter:
    """Bound memory and reserve attempts atomically, before expensive password hashing."""
    def __init__(self):
        self.entries=OrderedDict()
        self.lock=Lock()

    def clear(self):
        with self.lock:self.entries.clear()

    def check(self,keys):
        moment=time.monotonic()
        with self.lock:
            for key,limit in keys:
                queue=self.entries.setdefault(key,deque())
                while queue and moment-queue[0]>=60:queue.popleft()
                self.entries.move_to_end(key)
                if len(queue)>=limit:
                    raise HTTPException(429,'Слишком много попыток. Повторите через минуту.',headers={'Retry-After':'60'})
            for key,_ in keys:self.entries[key].append(moment)
            while len(self.entries)>4096:self.entries.popitem(last=False)

auth_limiter=AuthLimiter()

@router.get('/status')
def status(db:Session=Depends(session)):
    import os
    is_ide = os.environ.get('DEVFORGE_MODE') == 'ide'
    return {
        'hasAccounts': bool(db.scalar(select(func.count()).select_from(Account))),
        'localOnly': True,
        'isIde': is_ide,
        'authOptional': is_ide
    }

@router.post('/guest')
def guest_login(request: Request, response: Response, db: Session = Depends(session)):
    dev = get_or_create_default_developer_account(db)
    return start_session(db, response, dev, request.cookies.get('devforge_session', ''))

@router.get('/me')
def me(account:Account=Depends(current_account)):
    return public(account)

@router.post('/register',status_code=201)
def register(body:Registration,request:Request,response:Response,db:Session=Depends(session)):
    from sqlalchemy.exc import IntegrityError
    peer=request.client.host if request.client else 'local'
    auth_limiter.check([(f'register:{peer}',20)])
    if body.username.casefold()=='__devforge_guest':raise HTTPException(409,'Этот логин зарезервирован')
    account=Account(id=secrets.token_hex(16),username=body.username.casefold(),display_name=body.displayName,password_hash=hash_password(body.password))
    # A single SQLite write transaction claims legacy data for the first account.
    db.connection().exec_driver_sql('BEGIN IMMEDIATE')
    first=not db.scalar(select(func.count()).select_from(Account))
    db.add(account)
    try:
        db.flush()
        if first: migrate_legacy(db,account.id)
        return start_session(db,response,account,request.cookies.get('devforge_session',''))
    except IntegrityError:
        db.rollback()
        raise HTTPException(409,'Такой логин уже существует')

@router.post('/login')
def login(body:Login,request:Request,response:Response,db:Session=Depends(session)):
    peer=request.client.host if request.client else 'local'
    auth_limiter.check([(f'login-peer:{peer}',60),(f'login-user:{body.username.casefold()}',10)])
    account=db.scalar(select(Account).where(Account.username==body.username.casefold()))
    candidate=hash_password(body.password,account.password_hash.split(':')[0] if account else '00'*16)
    if not account or not secrets.compare_digest(candidate,account.password_hash):
        raise HTTPException(401,'Неверный логин или пароль')
    return start_session(db,response,account,request.cookies.get('devforge_session',''))

@router.post('/logout')
def logout(request:Request,response:Response,db:Session=Depends(session)):
    token=request.cookies.get('devforge_session','')
    row=db.get(AuthSession,hashlib.sha256(token.encode()).hexdigest())
    if row:db.delete(row)
    db.commit();response.delete_cookie('devforge_session',path='/')
    return {'ok':True}

def migrate_legacy(db:Session,owner_id:str):
    from . import models as legacy
    for row in db.scalars(select(legacy.Project)):
        db.add(Project(owner_id=owner_id,**{k:getattr(row,k) for k in ('id','name','language','files','revision','updated_at')}))
    for row in db.scalars(select(legacy.Attempt)):
        db.add(Attempt(owner_id=owner_id,**{k:getattr(row,k) for k in ('id','lesson_id','results','passed','total','created_at')}))
    for row in db.scalars(select(legacy.Completion)):
        db.add(Completion(owner_id=owner_id,lesson_id=row.lesson_id,xp=row.xp,created_at=row.created_at))
    for row in db.scalars(select(legacy.Draft)):
        db.add(Draft(owner_id=owner_id,lesson_id=row.lesson_id,code=row.code))
    setting=db.get(legacy.Setting,'profile')
    if setting:db.add(Setting(owner_id=owner_id,value=setting.value))
