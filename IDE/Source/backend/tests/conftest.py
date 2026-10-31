import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, session
from app.main import app

@pytest.fixture(autouse=True)
def isolate_auth_limits():
    from app.accounts import auth_limiter
    auth_limiter.clear()
    yield
    auth_limiter.clear()

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
        assert http.post('/api/auth/register', json={'username': 'tester', 'displayName': 'Tester', 'password': 'TestPassword42'}).status_code == 201
        yield http
    app.dependency_overrides.clear()
    engine.dispose()
