import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ROOT = Path(os.getenv('DEVFORGE_ROOT', getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[2])))
DATA = Path(os.getenv('DEVFORGE_DATA_DIR', str(ROOT / 'data')))
DATA.mkdir(exist_ok=True, parents=True)
engine = create_engine(os.getenv('DEVFORGE_DB', f'sqlite:///{DATA / "devforge.db"}'), connect_args={'check_same_thread': False})

@event.listens_for(engine, 'connect')
def configure_sqlite(connection, _):
    connection.execute('PRAGMA foreign_keys=ON')
    connection.execute('PRAGMA busy_timeout=5000')

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(engine, expire_on_commit=False)

def session():
    with SessionLocal() as db:
        yield db
