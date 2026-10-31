"""DevForge Builtin Backend Libraries for Pyodide (FastAPI, Pydantic, SQLAlchemy, Pytest)."""
import inspect
import json
import os
import re
import sqlite3
import sys
import types

# =====================================================================
# PYDANTIC
# =====================================================================
class FieldInfo:
    def __init__(self, default=..., min_length=None, max_length=None, ge=None, le=None, description=""):
        self.default = default
        self.min_length = min_length
        self.max_length = max_length
        self.ge = ge
        self.le = le
        self.description = description

def Field(default=..., **kwargs):
    return FieldInfo(default=default, **kwargs)

class ValidationError(ValueError):
    pass

class BaseModel:
    def __init__(self, **kwargs):
        cls = self.__class__
        annotations = getattr(cls, '__annotations__', {})
        for field_name, field_type in annotations.items():
            field_def = getattr(cls, field_name, ...)
            default_val = field_def.default if isinstance(field_def, FieldInfo) else field_def
            
            if field_name in kwargs:
                val = kwargs[field_name]
            elif default_val is not ...:
                val = default_val
            else:
                raise ValidationError(f"Обязательное поле '{field_name}' не передано")

            if val is not None and field_type in (int, str, float, bool, list, dict):
                if not isinstance(val, field_type):
                    try:
                        val = field_type(val)
                    except Exception:
                        raise ValidationError(f"Некорректный тип для '{field_name}': ожидается {field_type.__name__}, получено {type(val).__name__}")

            if isinstance(field_def, FieldInfo):
                if field_def.min_length is not None and len(str(val)) < field_def.min_length:
                    raise ValidationError(f"Поле '{field_name}' короче минимальной длины {field_def.min_length}")
                if field_def.max_length is not None and len(str(val)) > field_def.max_length:
                    raise ValidationError(f"Поле '{field_name}' превышает максимальную длину {field_def.max_length}")
                if field_def.ge is not None and val < field_def.ge:
                    raise ValidationError(f"Значение '{field_name}' должно быть >= {field_def.ge}")
                if field_def.le is not None and val > field_def.le:
                    raise ValidationError(f"Значение '{field_name}' должно быть <= {field_def.le}")

            setattr(self, field_name, val)

    def model_dump(self):
        cls = self.__class__
        annotations = getattr(cls, '__annotations__', {})
        res = {}
        for k in annotations:
            v = getattr(self, k, None)
            if isinstance(v, BaseModel):
                res[k] = v.model_dump()
            elif isinstance(v, list):
                res[k] = [x.model_dump() if isinstance(x, BaseModel) else x for x in v]
            else:
                res[k] = v
        return res

    dict = model_dump

pydantic_mod = types.ModuleType('pydantic')
pydantic_mod.BaseModel = BaseModel
pydantic_mod.Field = Field
pydantic_mod.ValidationError = ValidationError
sys.modules['pydantic'] = pydantic_mod


# =====================================================================
# FASTAPI
# =====================================================================
class status:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_500_INTERNAL_SERVER_ERROR = 500

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")

class Depends:
    def __init__(self, dependency):
        self.dependency = dependency

class Response:
    def __init__(self, status_code: int, json_data: any, text: str = ""):
        self.status_code = status_code
        self._json = json_data
        self.text = text
    def json(self):
        return self._json

class TestClient:
    def __init__(self, app):
        self.app = app

    def _request(self, method: str, url: str, json_data=None, params=None, headers=None):
        path = url.split("?")[0]
        query = params or {}
        if "?" in url:
            from urllib.parse import parse_qs
            qs = parse_qs(url.split("?", 1)[1])
            for k, v in qs.items():
                query[k] = v[0] if len(v) == 1 else v

        handler_info = None
        path_params = {}
        for (m, p), info in self.app.routes.items():
            if m != method:
                continue
            pattern = re.sub(r"\{([a-zA-Z_]\w*)\}", r"(?P<\1>[^/]+)", p)
            match = re.fullmatch(pattern, path)
            if match:
                handler_info = info
                path_params = match.groupdict()
                break

        if not handler_info:
            return Response(404, {"detail": f"Route {method} {path} not found"})

        func = handler_info["func"]
        expected_status = handler_info["status"]
        sig = inspect.signature(func)
        kwargs = {}

        try:
            for param_name, param in sig.parameters.items():
                if isinstance(param.default, Depends):
                    dep_fn = param.default.dependency
                    dep_sig = inspect.signature(dep_fn)
                    dep_kwargs = {}
                    for dp_name, dp_param in dep_sig.parameters.items():
                        if dp_name in query:
                            val = query[dp_name]
                            if dp_param.annotation == int: val = int(val)
                            elif dp_param.annotation == float: val = float(val)
                            dep_kwargs[dp_name] = val
                        elif dp_param.default is not inspect.Parameter.empty:
                            dep_kwargs[dp_name] = dp_param.default
                    if inspect.isgeneratorfunction(dep_fn):
                        gen = dep_fn(**dep_kwargs)
                        kwargs[param_name] = next(gen)
                    else:
                        kwargs[param_name] = dep_fn(**dep_kwargs)
                elif param_name in path_params:
                    val = path_params[param_name]
                    if param.annotation == int: val = int(val)
                    elif param.annotation == float: val = float(val)
                    kwargs[param_name] = val
                elif param_name in query:
                    val = query[param_name]
                    if param.annotation == int: val = int(val)
                    elif param.annotation == float: val = float(val)
                    kwargs[param_name] = val
                elif json_data is not None and isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
                    kwargs[param_name] = param.annotation(**json_data)
                elif param.default is not inspect.Parameter.empty:
                    kwargs[param_name] = param.default

            res = func(**kwargs)
            if isinstance(res, BaseModel):
                res = res.model_dump()
            return Response(expected_status, res)
        except HTTPException as e:
            return Response(e.status_code, {"detail": e.detail})
        except ValidationError as e:
            return Response(422, {"detail": str(e)})

    def get(self, url: str, **kwargs): return self._request("GET", url, **kwargs)
    def post(self, url: str, **kwargs): return self._request("POST", url, **kwargs)
    def put(self, url: str, **kwargs): return self._request("PUT", url, **kwargs)
    def delete(self, url: str, **kwargs): return self._request("DELETE", url, **kwargs)

class FastAPI:
    def __init__(self, title: str = "DevForge App", version: str = "0.1.0"):
        self.title = title
        self.version = version
        self.routes = {}

    def _register(self, method: str, path: str, func, status_code: int):
        self.routes[(method, path)] = {"func": func, "status": status_code}

    def get(self, path: str, status_code: int = 200):
        def decorator(f):
            self._register("GET", path, f, status_code)
            return f
        return decorator

    def post(self, path: str, status_code: int = 200):
        def decorator(f):
            self._register("POST", path, f, status_code)
            return f
        return decorator

    def put(self, path: str, status_code: int = 200):
        def decorator(f):
            self._register("PUT", path, f, status_code)
            return f
        return decorator

    def delete(self, path: str, status_code: int = 200):
        def decorator(f):
            self._register("DELETE", path, f, status_code)
            return f
        return decorator

fastapi_mod = types.ModuleType('fastapi')
fastapi_mod.FastAPI = FastAPI
fastapi_mod.HTTPException = HTTPException
fastapi_mod.Depends = Depends
fastapi_mod.status = status
fastapi_mod.Response = Response
fastapi_mod.TestClient = TestClient
sys.modules['fastapi'] = fastapi_mod

testclient_mod = types.ModuleType('fastapi.testclient')
testclient_mod.TestClient = TestClient
sys.modules['fastapi.testclient'] = testclient_mod


# =====================================================================
# SQLALCHEMY 2.0 (Lightweight SQLite ORM wrapper)
# =====================================================================
class Column:
    def __init__(self, col_type, primary_key=False, nullable=True, default=None):
        self.type = col_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.name = None

    def __eq__(self, other): return ("eq", self, other)
    def __gt__(self, other): return ("gt", self, other)

class DeclarativeMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        if hasattr(cls, '__tablename__'):
            cls._columns = {k: v for k, v in dct.items() if isinstance(v, Column)}
        return cls

class DeclarativeBase(metaclass=DeclarativeMeta):
    __tablename__ = None
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def declarative_base():
    class Base(DeclarativeBase):
        pass
    return Base

class Integer: pass
class String:
    def __init__(self, length=255): self.length = length
class Float: pass

class SelectQuery:
    def __init__(self, entity):
        self.entity = entity
        self.conditions = []

    def where(self, condition):
        self.conditions.append(condition)
        return self

def select(entity):
    return SelectQuery(entity)

class Engine:
    def __init__(self, url):
        self.url = url
        path = url.replace("sqlite:///", "") if url.startswith("sqlite:///") else ":memory:"
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

class Session:
    def __init__(self, engine):
        self.engine = engine
        self.conn = engine.conn
        self._new = []

    def add(self, obj):
        self._new.append(obj)

    def commit(self):
        cursor = self.conn.cursor()
        for obj in self._new:
            cls = obj.__class__
            tbl = getattr(cls, '__tablename__')
            cols = []
            vals = []
            for k, v in cls._columns.items():
                val = getattr(obj, k, None)
                if isinstance(val, Column): val = None
                if v.primary_key and val is None: continue
                cols.append(k)
                vals.append(val)
            placeholders = ", ".join(["?"] * len(cols))
            col_names = ", ".join(cols)
            cursor.execute(f"INSERT INTO {tbl} ({col_names}) VALUES ({placeholders})", vals)
            for k, v in cls._columns.items():
                if v.primary_key and getattr(obj, k, None) is None:
                    setattr(obj, k, cursor.lastrowid)
        self.conn.commit()
        self._new.clear()

    def rollback(self):
        self.conn.rollback()
        self._new.clear()

    def scalars(self, query):
        cursor = self.conn.cursor()
        tbl = query.entity.__tablename__
        sql = f"SELECT * FROM {tbl}"
        params = []
        if query.conditions:
            clauses = []
            for op, col, val in query.conditions:
                col_name = [k for k, v in query.entity._columns.items() if v is col][0]
                if op == "eq": clauses.append(f"{col_name} = ?")
                elif op == "gt": clauses.append(f"{col_name} > ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(clauses)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        objs = []
        for r in rows:
            obj = query.entity()
            for k in r.keys():
                setattr(obj, k, r[k])
            objs.append(obj)
        return ScalarResult(objs)

    def close(self):
        pass

class ScalarResult:
    def __init__(self, items): self.items = items
    def all(self): return self.items
    def first(self): return self.items[0] if self.items else None

def create_engine(url): return Engine(url)
def sessionmaker(bind=None): return lambda: Session(bind)

sqlalchemy_mod = types.ModuleType('sqlalchemy')
sqlalchemy_mod.create_engine = create_engine
sqlalchemy_mod.declarative_base = declarative_base
sqlalchemy_mod.DeclarativeBase = DeclarativeBase
sqlalchemy_mod.Column = Column
sqlalchemy_mod.Integer = Integer
sqlalchemy_mod.String = String
sqlalchemy_mod.Float = Float
sqlalchemy_mod.select = select
sqlalchemy_mod.Session = Session
sqlalchemy_mod.sessionmaker = sessionmaker
sys.modules['sqlalchemy'] = sqlalchemy_mod


# =====================================================================
# PYTEST
# =====================================================================
class Pytest:
    @staticmethod
    def fixture(fn): return fn

    @staticmethod
    def raises(expected_exc):
        class RaisesContext:
            def __enter__(self): pass
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    raise AssertionError(f"Expected {expected_exc.__name__} but no exception was raised")
                return issubclass(exc_type, expected_exc)
        return RaisesContext()

pytest_mod = types.ModuleType('pytest')
pytest_mod.fixture = Pytest.fixture
pytest_mod.raises = Pytest.raises
sys.modules['pytest'] = pytest_mod

print("DevForge Backend Pack initialized (fastapi, pydantic, sqlalchemy, pytest).")
