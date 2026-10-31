"""
Curriculum for Professional Tracks (Backend, Frontend, Java Development)
for DevForge 0.5.0
Adhering strictly to the 8-point pedagogical standard.
"""

def make_guide(lesson_title, topic, solution_code, sample_code=None, walkthrough=None):
    return {
        "version": 1,
        "idea": f"Освоение ключевого практического навыка направления: {lesson_title}. Разбираем архитектурный подход и типовой шаблон реализации в реальных проектах.",
        "steps": [
            f"Изучите теоретическую концепцию темы: {topic}.",
            "Разберите пример исходного кода и проследите поток выполнения данных.",
            "Напишите решение задачи в редакторе и проверьте его автоматическими тестами."
        ],
        "experiment": "Попробуйте изменить входные параметры и граничные условия, чтобы увидеть поведение системы в нештатных ситуациях.",
        "terms": [
            {"term": lesson_title.split(":")[0], "meaning": topic}
        ],
        "solution": solution_code,
        "taskSteps": walkthrough or [f"Реализуйте функционал для темы: {lesson_title}"],
        "checklist": [
            "Код компилируется и выполняется без синтаксических ошибок",
            "Реализованы все заявленные методы и требования сигнатуры",
            "Обработаны граничные условия и возможные исключения"
        ],
        "taskTables": [],
        "example": {
            "code": sample_code or solution_code,
            "expected": "",
            "setupSql": "",
            "kind": "output",
            "tables": []
        }
    }


BACKEND_LESSONS = [
    {
        "id": "backend-http-rest",
        "language": "python",
        "title": "HTTP, REST и коды ответов: клиент-серверная архитектура",
        "topic": "HTTP методы, статус-коды и заголовки",
        "section": "Backend: Архитектура и HTTP",
        "order": 48,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "Клиент-серверное взаимодействие в веб-разработке строится на протоколе HTTP. "
            "Клиент отправляет текстовый запрос, состоящий из стартовой строки (метод, путь, версия), "
            "заголовков (метаданных: Host, Content-Type, Authorization) и опционального тела (body, чаще всего JSON).\n\n"
            "Ключевые методы REST API:\n"
            "• GET — безопасное чтение данных без изменения состояния на сервере.\n"
            "• POST — создание нового ресурса.\n"
            "• PUT / PATCH — полное или частичное обновление ресурса.\n"
            "• DELETE — удаление ресурса.\n\n"
            "Статус-коды сервера делятся на группы:\n"
            "• 2xx (Успех): 200 OK, 201 Created, 204 No Content.\n"
            "• 4xx (Ошибка клиента): 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity.\n"
            "• 5xx (Ошибка сервера): 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable."
        ),
        "syntax": (
            "# Формат HTTP-запроса:\n"
            "METHOD /path HTTP/1.1\\r\\n\n"
            "Header-Name: header-value\\r\\n\n"
            "\\r\\n\n"
            "{\"optional\": \"body\"}"
        ),
        "examples": [
            (
                "def parse_simple_headers(header_lines):\n"
                "    headers = {}\n"
                "    for line in header_lines:\n"
                "        if ': ' in line:\n"
                "            key, val = line.split(': ', 1)\n"
                "            headers[key] = val\n"
                "    return headers"
            )
        ],
        "task": (
            "Напишите функцию `parse_http_request(raw_request: str) -> dict`.\n"
            "Она должна принимать сырую строку HTTP-запроса, разделять заголовки и тело по пустой строке `\\r\\n\\r\\n` (или `\\n\\n`), "
            "парсить первую строку на `method` и `path`, извлекать словарь `headers` и возвращать словарь вида:\n"
            "{\n"
            "    'method': str,\n"
            "    'path': str,\n"
            "    'status_code': 200,\n"
            "    'headers': dict[str, str],\n"
            "    'body': str\n"
            "}\n"
            "Если запрос пуст или некорректен, возвращайте `{'status_code': 400, 'error': 'Bad Request'}`."
        ),
        "starterCode": (
            "def parse_http_request(raw_request: str) -> dict:\n"
            "    # Ваш код здесь\n"
            "    pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Парсинг стандартного GET-запроса",
                "expression": "parse_http_request('GET /api/v1/users HTTP/1.1\\r\\nHost: api.devforge.ru\\r\\n\\r\\n')",
                "expected": {
                    "method": "GET",
                    "path": "/api/v1/users",
                    "status_code": 200,
                    "headers": {"Host": "api.devforge.ru"},
                    "body": ""
                }
            },
            {
                "id": "t2",
                "label": "Парсинг POST-запроса с JSON телом",
                "expression": "parse_http_request('POST /api/v1/login HTTP/1.1\\r\\nHost: api.devforge.ru\\r\\nContent-Type: application/json\\r\\n\\r\\n{\"user\":\"admin\"}')",
                "expected": {
                    "method": "POST",
                    "path": "/api/v1/login",
                    "status_code": 200,
                    "headers": {"Host": "api.devforge.ru", "Content-Type": "application/json"},
                    "body": "{\"user\":\"admin\"}"
                }
            },
            {
                "id": "t3",
                "label": "Пустой запрос возвращает 400 Bad Request",
                "expression": "parse_http_request('')",
                "expected": {"status_code": 400, "error": "Bad Request"}
            }
        ],
        "hints": [
            "Направление: разделите весь текст на две части по границе '\\r\\n\\r\\n' или '\\n\\n'.",
            "Подход: первая часть содержит стартовую строку и заголовки, вторая часть — это тело запроса.",
            "Детали: разбейте первую строку через `.split(' ')` чтобы получить [method, path, version]."
        ],
        "commonMistakes": (
            "Забывание о том, что перевод строки в HTTP стандарте — это \\r\\n, "
            "а заголовки могут содержать двоеточие в значении (используйте split(': ', 1))."
        ),
        "solutionExplanation": (
            "Мы проверяем непустоту строки, разделяем заголовки и тело по двойному переводу строки, "
            "извлекаем стартовую строку и парсим каждый заголовок в словарь."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["HTTP", "REST", "Headers", "Status Codes"],
        "walkthrough": [
            "Проверьте входящую строку на пустоту",
            "Разделите текст на блок заголовков и тело",
            "Разберите первую строку на метод и путь",
            "Соберите словарь заголовков и верните итоговую структуру"
        ],
        "prerequisites": ["python-functions", "python-strings", "python-dictionaries"],
        "resources": [{"title": "MDN: Overview of HTTP", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", "language": "python"}],
        "lifeExample": "Как почтовый конверт: адрес получателя и отправителя — это заголовки, а письмо внутри — тело запроса.",
        "guide": make_guide(
            "HTTP, REST и коды ответов",
            "HTTP методы, статус-коды и заголовки",
            (
                "def parse_http_request(raw_request: str) -> dict:\n"
                "    if not raw_request or not raw_request.strip():\n"
                "        return {'status_code': 400, 'error': 'Bad Request'}\n"
                "    sep = '\\r\\n\\r\\n' if '\\r\\n\\r\\n' in raw_request else '\\n\\n'\n"
                "    parts = raw_request.split(sep, 1)\n"
                "    head = parts[0]\n"
                "    body = parts[1] if len(parts) > 1 else ''\n"
                "    lines = head.replace('\\r', '').split('\\n')\n"
                "    start_tokens = lines[0].split(' ')\n"
                "    if len(start_tokens) < 2:\n"
                "        return {'status_code': 400, 'error': 'Bad Request'}\n"
                "    method, path = start_tokens[0], start_tokens[1]\n"
                "    headers = {}\n"
                "    for line in lines[1:]:\n"
                "        if ': ' in line:\n"
                "            k, v = line.split(': ', 1)\n"
                "            headers[k] = v\n"
                "    return {'method': method, 'path': path, 'status_code': 200, 'headers': headers, 'body': body}\n"
            )
        )
    },
    {
        "id": "backend-fastapi-models",
        "language": "python",
        "title": "FastAPI и валидация данных: Pydantic схемы",
        "topic": "Строгая валидация входящих JSON, типы и ограничения",
        "section": "Backend: FastAPI и валидация",
        "order": 49,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "В современных веб-фреймворках (FastAPI) входящие данные автоматически проверяются библиотекой Pydantic. "
            "Pydantic гарантирует, что если эндпоинт ожидает число, строку определённой длины или валидный email, "
            "то некорректный запрос будет отклонён с кодом 422 до попадания в бизнес-логику.\n\n"
            "Принципы валидации схем:\n"
            "1. Проверка обязательных полей (отсутствие поля вызывает ошибку).\n"
            "2. Приведение и проверка типов (int, str, bool, float).\n"
            "3. Бизнес-ограничения: минимальная/максимальная длина, регулярные выражения, числовые диапазоны."
        ),
        "syntax": (
            "from pydantic import BaseModel, Field, EmailStr\n\n"
            "class UserCreate(BaseModel):\n"
            "    username: str = Field(min_length=3, max_length=30)\n"
            "    email: str\n"
            "    age: int = Field(ge=18)"
        ),
        "examples": [
            (
                "def check_field_type(val, expected_type, name):\n"
                "    if not isinstance(val, expected_type):\n"
                "        raise ValueError(f'{name} must be {expected_type.__name__}')"
            )
        ],
        "task": (
            "Реализуйте функцию `validate_user_schema(payload: dict) -> tuple[bool, str | dict]`.\n"
            "Требования к валидации:\n"
            "1. Обязательные поля: `username` (строка, от 3 до 20 символов), `email` (строка, содержит '@' и '.'), `age` (целое число, >= 18).\n"
            "2. Если все правила соблюдены, функция возвращает `(True, cleaned_dict)`, где `cleaned_dict` содержит только эти три поля с приведенными типами.\n"
            "3. При ошибке валидации возвращайте `(False, 'error description')` с указанием причины (например: 'Invalid age', 'Invalid email', 'Invalid username', 'Missing required field')."
        ),
        "starterCode": (
            "def validate_user_schema(payload: dict) -> tuple[bool, str | dict]:\n"
            "    # Ваш код здесь\n"
            "    pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Корректные данные пользователя",
                "expression": "validate_user_schema({'username': 'alex', 'email': 'alex@devforge.ru', 'age': 25})",
                "expected": [True, {"username": "alex", "email": "alex@devforge.ru", "age": 25}]
            },
            {
                "id": "t2",
                "label": "Возраст меньше 18 лет",
                "expression": "validate_user_schema({'username': 'alex', 'email': 'alex@devforge.ru', 'age': 16})[0]",
                "expected": False
            },
            {
                "id": "t3",
                "label": "Некорректный email без точки",
                "expression": "validate_user_schema({'username': 'alex', 'email': 'bad_email@com', 'age': 20})[0]",
                "expected": False
            },
            {
                "id": "t4",
                "label": "Слишком короткий username",
                "expression": "validate_user_schema({'username': 'al', 'email': 'al@test.ru', 'age': 20})[0]",
                "expected": False
            }
        ],
        "hints": [
            "Направление: проверьте наличие всех трех ключей в payload: 'username', 'email', 'age'.",
            "Подход: проверьте типы isinstance(age, int) и age >= 18.",
            "Детали: проверьте email: isinstance(email, str) and '@' in email and '.' in email.split('@')[-1]."
        ],
        "commonMistakes": (
            "Считать boolean за int (в Python True является экземпляром int: `isinstance(True, int) == True`). "
            "Используйте `type(age) is int` или `isinstance(age, int) and not isinstance(age, bool)`."
        ),
        "solutionExplanation": (
            "Мы проверяем наличие обязательных полей, их типы (исключая bool для целых чисел), "
            "длину имени и структуру почтового адреса."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Validation", "Pydantic", "FastAPI", "Type Safety"],
        "walkthrough": [
            "Проверьте наличие ключей 'username', 'email', 'age'",
            "Проверьте, что username — строка от 3 до 20 символов",
            "Проверьте валидность email",
            "Проверьте возраст (целое число >= 18)",
            "Верните (True, cleaned_dict) или (False, error)"
        ],
        "prerequisites": ["python-functions", "python-dictionaries", "python-exceptions"],
        "resources": [{"title": "FastAPI Request Body & Pydantic", "url": "https://fastapi.tiangolo.com/tutorial/body/", "language": "python"}],
        "lifeExample": "Служба паспортного контроля: если в анкете возраст < 18 или подпись отсутствует, документы не принимаются к рассмотрению.",
        "guide": make_guide(
            "FastAPI и валидация данных",
            "Pydantic схемы и проверка типов",
            (
                "def validate_user_schema(payload: dict) -> tuple[bool, str | dict]:\n"
                "    if not isinstance(payload, dict):\n"
                "        return False, 'Payload must be a dictionary'\n"
                "    for key in ['username', 'email', 'age']:\n"
                "        if key not in payload:\n"
                "            return False, f'Missing required field: {key}'\n"
                "    username = payload['username']\n"
                "    email = payload['email']\n"
                "    age = payload['age']\n"
                "    if not isinstance(username, str) or len(username) < 3 or len(username) > 20:\n"
                "        return False, 'Invalid username: must be 3-20 chars'\n"
                "    if not isinstance(email, str) or '@' not in email or '.' not in email.split('@')[-1]:\n"
                "        return False, 'Invalid email format'\n"
                "    if type(age) is not int or age < 18:\n"
                "        return False, 'Invalid age: must be int >= 18'\n"
                "    return True, {'username': username, 'email': email, 'age': age}\n"
            )
        )
    },
    {
        "id": "backend-fastapi-routes",
        "language": "python",
        "title": "FastAPI: маршрутизация, параметры и ошибки",
        "topic": "Маршруты, Query/Path параметры и HTTPException",
        "section": "Backend: Маршрутизация",
        "order": 50,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "В REST сервисах маршрутизатор сопоставляет HTTP-метод и путь с функцией-обработчиком. "
            "Параметры пути (/items/{id}) идентифицируют конкретный ресурс, а параметры запроса (/items?limit=10) "
            "используются для фильтрации, пагинации и сортировки.\n\n"
            "Если ресурс не найден, сервер должен выбрасывать HTTPException со статусом 404, "
            "а не возвращать пустую страницу со статусом 200."
        ),
        "syntax": (
            "from fastapi import FastAPI, HTTPException\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/items/{item_id}')\n"
            "def read_item(item_id: int):\n"
            "    if item_id not in DB:\n"
            "        raise HTTPException(status_code=404, detail='Item not found')\n"
            "    return DB[item_id]"
        ),
        "examples": [
            (
                "class SimpleRouter:\n"
                "    def __init__(self):\n"
                "        self.routes = {}\n"
                "    def add(self, method, path, handler):\n"
                "        self.routes[(method, path)] = handler"
            )
        ],
        "task": (
            "Создайте класс `MiniApiRouter` со следующими методами:\n"
            "1. `register(method: str, path: str, handler: callable)` — регистрирует обработчик.\n"
            "2. `dispatch(method: str, path: str, params: dict = None) -> dict` — вызывает зарегистрированный обработчик, передавая params (если они есть).\n"
            "   • Если маршрут найден и функция отработала штатно: возвращает `{'status': 200, 'data': result}`.\n"
            "   • Если маршрут не найден: возвращает `{'status': 404, 'error': 'Not Found'}`.\n"
            "   • Если обработчик выбросил ValueError или исключение: возвращает `{'status': 400, 'error': str(e)}`."
        ),
        "starterCode": (
            "class MiniApiRouter:\n"
            "    def __init__(self):\n"
            "        # инициализация\n"
            "        pass\n"
            "\n"
            "    def register(self, method: str, path: str, handler):\n"
            "        pass\n"
            "\n"
            "    def dispatch(self, method: str, path: str, params: dict = None) -> dict:\n"
            "        pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успешный вызов зарегистрированного маршрута",
                "expression": (
                    "r = MiniApiRouter()\n"
                    "r.register('GET', '/users', lambda params: [{'id': 1, 'name': 'Ann'}])\n"
                    "r.dispatch('GET', '/users')"
                ),
                "expected": {"status": 200, "data": [{"id": 1, "name": "Ann"}]}
            },
            {
                "id": "t2",
                "label": "Маршрут не найден — 404 Not Found",
                "expression": (
                    "r = MiniApiRouter()\n"
                    "r.dispatch('GET', '/unknown')"
                ),
                "expected": {"status": 404, "error": "Not Found"}
            },
            {
                "id": "t3",
                "label": "Ошибка валидации в обработчике — 400 Bad Request",
                "expression": (
                    "def fail(p): raise ValueError('Invalid limit')\n"
                    "r = MiniApiRouter()\n"
                    "r.register('GET', '/items', fail)\n"
                    "r.dispatch('GET', '/items')"
                ),
                "expected": {"status": 400, "error": "Invalid limit"}
            }
        ],
        "hints": [
            "Направление: сохраняйте маршруты в словаре с ключом (method.upper(), path).",
            "Подход: в dispatch проверяйте наличие ключа, оборачивайте вызов в try-except Exception as e.",
            "Детали: если params is None, передавайте пустой словарь {} или вызывайте handler(params or {})."
        ],
        "commonMistakes": (
            "Забывать приводить метод к верхнему регистру (GET vs get). "
            "Не перехватывать исключения обработчика."
        ),
        "solutionExplanation": (
            "Класс маршрутизатора сохраняет обработчики в словаре и при dispatch безопасно выполняет функцию, "
            "оборачивая ответ в структурированный статус-код."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Routing", "FastAPI", "HTTPException", "Error Handling"],
        "walkthrough": [
            "Создайте словарь routes в __init__",
            "Реализуйте метод register(method, path, handler)",
            "В dispatch найдите нужный handler по (method.upper(), path)",
            "Вызовите handler в блоке try-except и сформируйте ответ"
        ],
        "prerequisites": ["backend-http-rest", "python-exceptions", "python-classes"],
        "resources": [{"title": "FastAPI Path Parameters", "url": "https://fastapi.tiangolo.com/tutorial/path-params/", "language": "python"}],
        "lifeExample": "Диспетчер такси: определяет нужную улицу и направляет вызов конкретному водителю, а если адреса нет на карте — сообщает об ошибке.",
        "guide": make_guide(
            "FastAPI: маршрутизация и ошибки",
            "Маршруты и HTTPException",
            (
                "class MiniApiRouter:\n"
                "    def __init__(self):\n"
                "        self._routes = {}\n"
                "    def register(self, method: str, path: str, handler):\n"
                "        self._routes[(method.upper(), path)] = handler\n"
                "    def dispatch(self, method: str, path: str, params: dict = None) -> dict:\n"
                "        key = (method.upper(), path)\n"
                "        if key not in self._routes:\n"
                "            return {'status': 404, 'error': 'Not Found'}\n"
                "        handler = self._routes[key]\n"
                "        try:\n"
                "            result = handler(params or {})\n"
                "            return {'status': 200, 'data': result}\n"
                "        except Exception as e:\n"
                "            return {'status': 400, 'error': str(e)}\n"
            )
        )
    },
    {
        "id": "backend-fastapi-depends",
        "language": "python",
        "title": "FastAPI: Dependency Injection (Depends) и аутентификация",
        "topic": "Внедрение зависимостей, валидация токенов и защита эндпоинтов",
        "section": "Backend: Внедрение зависимостей",
        "order": 51,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "Dependency Injection (DI) в FastAPI позволяет разделять бизнес-логику и вспомогательный код: "
            "проверку токенов авторизации, получение сессии базы данных или проверку прав пользователя.\n\n"
            "Зависимость — это обычная функция, которую фреймворк выполняет перед вызовом эндпоинта. "
            "Если зависимость бросает HTTPException (например 401 Unauthorized), эндпоинт даже не начинает выполняться."
        ),
        "syntax": (
            "from fastapi import Depends, HTTPException, Header\n\n"
            "def get_current_user(authorization: str = Header(...)):\n"
            "    if not authorization.startswith('Bearer '):\n"
            "        raise HTTPException(401, 'Invalid auth header')\n"
            "    token = authorization.split(' ')[1]\n"
            "    return verify_token(token)\n\n"
            "@app.get('/profile')\n"
            "def get_profile(user = Depends(get_current_user)):\n"
            "    return {'user': user}"
        ),
        "examples": [
            (
                "TOKEN_DB = {'sec-token-123': {'id': 1, 'role': 'admin'}}\n"
                "def authenticate(token):\n"
                "    if token not in TOKEN_DB:\n"
                "        return None\n"
                "    return TOKEN_DB[token]"
            )
        ],
        "task": (
            "Реализуйте функцию `resolve_auth_dependency(auth_header: str | None, users_db: dict) -> dict`.\n"
            "Правила проверки:\n"
            "1. Если `auth_header` отсутствует (None) или пустой: возвращайте `{'status': 401, 'error': 'Missing authorization header'}`.\n"
            "2. Заголовок должен начинаться с `'Bearer '`. Если префикс отсутствует: `{'status': 401, 'error': 'Invalid token schema'}`.\n"
            "3. Извлеките токен (часть после `'Bearer '`). Проверьте наличие токена в `users_db` (словарь вида `{token: user_data}`).\n"
            "4. Если токен найден: возвращайте `{'status': 200, 'user': user_data}`.\n"
            "5. Если токен не найден в БД: возвращайте `{'status': 401, 'error': 'Invalid or expired token'}`."
        ),
        "starterCode": (
            "def resolve_auth_dependency(auth_header: str | None, users_db: dict) -> dict:\n"
            "    # Ваш код здесь\n"
            "    pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успешная авторизация по валидному Bearer токену",
                "expression": (
                    "db = {'token-abc': {'id': 10, 'username': 'dmitry'}}\n"
                    "resolve_auth_dependency('Bearer token-abc', db)"
                ),
                "expected": {"status": 200, "user": {"id": 10, "username": "dmitry"}}
            },
            {
                "id": "t2",
                "label": "Отсутствие заголовка авторизации",
                "expression": "resolve_auth_dependency(None, {})",
                "expected": {"status": 401, "error": "Missing authorization header"}
            },
            {
                "id": "t3",
                "label": "Неверная схема токена (нет Bearer)",
                "expression": "resolve_auth_dependency('Basic dXNlcjpwYXNz', {})",
                "expected": {"status": 401, "error": "Invalid token schema"}
            },
            {
                "id": "t4",
                "label": "Токен не найден в базе данных",
                "expression": "resolve_auth_dependency('Bearer expired-token', {'valid': {'id': 1}})",
                "expected": {"status": 401, "error": "Invalid or expired token"}
            }
        ],
        "hints": [
            "Направление: проверьте `if not auth_header:` в первую очередь.",
            "Подход: используйте `.startswith('Bearer ')` для проверки схемы.",
            "Детали: извлеките токен через `auth_header[7:].strip()` и выполните поиск `token in users_db`."
        ],
        "commonMistakes": (
            "Забывать удалять пробелы вокруг токена или вызывать .startswith() на значении None."
        ),
        "solutionExplanation": (
            "Мы последовательно проверяем наличие заголовка, соответствие стандарту Bearer токенов "
            "и сверяем токен с базой активных сессий."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["FastAPI", "Depends", "Authentication", "Bearer Token"],
        "walkthrough": [
            "Проверьте auth_header на None и пустоту",
            "Проверьте префикс Bearer",
            "Извлеките токен",
            "Проверьте токен в словаре пользователей",
            "Верните статус 200 с пользователем или 401 с ошибкой"
        ],
        "prerequisites": ["backend-fastapi-routes", "python-dictionaries"],
        "resources": [{"title": "FastAPI Dependencies", "url": "https://fastapi.tiangolo.com/tutorial/dependencies/", "language": "python"}],
        "lifeExample": "Электронный пропуск на турникете: считыватель проверяет формат карты и валидность чипа в базе службы безопасности.",
        "guide": make_guide(
            "FastAPI: Dependency Injection",
            "Depends и Bearer аутентификация",
            (
                "def resolve_auth_dependency(auth_header: str | None, users_db: dict) -> dict:\n"
                "    if not auth_header or not auth_header.strip():\n"
                "        return {'status': 401, 'error': 'Missing authorization header'}\n"
                "    if not auth_header.startswith('Bearer '):\n"
                "        return {'status': 401, 'error': 'Invalid token schema'}\n"
                "    token = auth_header[7:].strip()\n"
                "    if not token or token not in users_db:\n"
                "        return {'status': 401, 'error': 'Invalid or expired token'}\n"
                "    return {'status': 200, 'user': users_db[token]}\n"
            )
        )
    },
    {
        "id": "backend-sqlalchemy-orm",
        "language": "python",
        "title": "SQLAlchemy: ORM-модели, сессии и CRUD",
        "topic": "Объектно-реляционное отображение, сущности и репозиторий",
        "section": "Backend: SQLAlchemy ORM",
        "order": 52,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "ORM (Object-Relational Mapping) позволяет работать с таблицами реляционной БД как с классами Python. "
            "Каждая строка таблицы — это объект класса, а колонки — свойства объекта.\n\n"
            "Преимущества ORM:\n"
            "• Безопасность: автоматическое экранирование параметров предотвращает SQL Injection.\n"
            "• Типизация: подсказки редактора и проверка соответствия типов.\n"
            "• Независимость от СУБД: переносимость между SQLite, PostgreSQL, MySQL."
        ),
        "syntax": (
            "from sqlalchemy import Column, Integer, String\n"
            "from sqlalchemy.orm import declarative_base, Session\n\n"
            "Base = declarative_base()\n\n"
            "class Account(Base):\n"
            "    __tablename__ = 'accounts'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    owner = Column(String(50), nullable=False)\n"
            "    balance_cents = Column(Integer, default=0)"
        ),
        "examples": [
            (
                "class AccountRepo:\n"
                "    def __init__(self, session):\n"
                "        self.session = session\n"
                "    def save(self, acc):\n"
                "        self.session.add(acc)\n"
                "        self.session.commit()"
            )
        ],
        "task": (
            "Создайте класс репозитория `AccountRepository` для управления счетами пользователей.\n"
            "Он должен хранить счета в словаре `{account_id: account_dict}` и реализовывать методы:\n"
            "1. `create_account(owner: str, currency: str = 'RUB', initial_cents: int = 0) -> dict`:\n"
            "   • генерирует уникальный автоинкрементный `id` (начиная с 1);\n"
            "   • сохраняет и возвращает словарь `{'id': id, 'owner': owner, 'currency': currency, 'balance_cents': initial_cents, 'is_active': True}`.\n"
            "2. `get_by_id(account_id: int) -> dict | None`: возвращает счет или None.\n"
            "3. `update_balance(account_id: int, delta_cents: int) -> dict`:\n"
            "   • увеличивает баланс на `delta_cents` (или уменьшает, если число отрицательное);\n"
            "   • если счет не найден: бросает `KeyError('Account not found')`;\n"
            "   • если результирующий баланс меньше 0: бросает `ValueError('Insufficient funds')` и не меняет баланс;\n"
            "   • возвращает обновленный счет."
        ),
        "starterCode": (
            "class AccountRepository:\n"
            "    def __init__(self):\n"
            "        pass\n"
            "\n"
            "    def create_account(self, owner: str, currency: str = 'RUB', initial_cents: int = 0) -> dict:\n"
            "        pass\n"
            "\n"
            "    def get_by_id(self, account_id: int) -> dict | None:\n"
            "        pass\n"
            "\n"
            "    def update_balance(self, account_id: int, delta_cents: int) -> dict:\n"
            "        pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Создание счета и чтение по ID",
                "expression": (
                    "repo = AccountRepository()\n"
                    "acc = repo.create_account('Иван', 'RUB', 1000)\n"
                    "repo.get_by_id(acc['id'])"
                ),
                "expected": {"id": 1, "owner": "Иван", "currency": "RUB", "balance_cents": 1000, "is_active": True}
            },
            {
                "id": "t2",
                "label": "Пополнение и списание средств",
                "expression": (
                    "repo = AccountRepository()\n"
                    "acc = repo.create_account('Анна', 'RUB', 500)\n"
                    "repo.update_balance(acc['id'], 300)\n"
                    "repo.update_balance(acc['id'], -200)"
                ),
                "expected": {"id": 1, "owner": "Анна", "currency": "RUB", "balance_cents": 600, "is_active": True}
            },
            {
                "id": "t3",
                "label": "Ошибка при нехватке средств (баланс не меняется)",
                "expression": (
                    "repo = AccountRepository()\n"
                    "acc = repo.create_account('Ольга', 'RUB', 200)\n"
                    "try:\n"
                    "    repo.update_balance(acc['id'], -300)\n"
                    "    res = 'no-error'\n"
                    "except ValueError as e:\n"
                    "    res = str(e)\n"
                    "res, repo.get_by_id(acc['id'])['balance_cents']"
                ),
                "expected": ["Insufficient funds", 200]
            }
        ],
        "hints": [
            "Направление: используйте словарь `self._db = {}` и счетчик `self._next_id = 1`.",
            "Подход: в create_account инкрементируйте счетчик и сохраняйте копию объекта.",
            "Детали: в update_balance проверьте `new_balance = acc['balance_cents'] + delta_cents < 0` перед записью."
        ],
        "commonMistakes": (
            "Мутация баланса до проверки условия `< 0`. Из-за этого при ошибке баланс оказывается испорченным."
        ),
        "solutionExplanation": (
            "Репозиторий инкапсулирует операции со счетами и гарантирует инвариант: баланс не может стать отрицательным."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["SQLAlchemy", "ORM", "Repository Pattern", "CRUD"],
        "walkthrough": [
            "Инициализируйте хранилище и счетчик ID",
            "Реализуйте метод create_account",
            "Реализуйте метод get_by_id",
            "Реализуйте метод update_balance с проверкой условий"
        ],
        "prerequisites": ["python-classes", "python-dictionaries", "python-exceptions"],
        "resources": [{"title": "SQLAlchemy ORM Quick Start", "url": "https://docs.sqlalchemy.org/en/20/orm/quickstart.html", "language": "python"}],
        "lifeExample": "Банковский сейф: чтобы положить или забрать деньги, кассир проверяет номер ячейки и не дает выдать больше, чем в ней лежит.",
        "guide": make_guide(
            "SQLAlchemy: ORM и CRUD",
            "Репозиторий сущностей и работа с балансом",
            (
                "class AccountRepository:\n"
                "    def __init__(self):\n"
                "        self._accounts = {}\n"
                "        self._next_id = 1\n"
                "\n"
                "    def create_account(self, owner: str, currency: str = 'RUB', initial_cents: int = 0) -> dict:\n"
                "        acc_id = self._next_id\n"
                "        self._next_id += 1\n"
                "        acc = {'id': acc_id, 'owner': owner, 'currency': currency, 'balance_cents': initial_cents, 'is_active': True}\n"
                "        self._accounts[acc_id] = acc\n"
                "        return dict(acc)\n"
                "\n"
                "    def get_by_id(self, account_id: int) -> dict | None:\n"
                "        acc = self._accounts.get(account_id)\n"
                "        return dict(acc) if acc else None\n"
                "\n"
                "    def update_balance(self, account_id: int, delta_cents: int) -> dict:\n"
                "        if account_id not in self._accounts:\n"
                "            raise KeyError('Account not found')\n"
                "        acc = self._accounts[account_id]\n"
                "        new_bal = acc['balance_cents'] + delta_cents\n"
                "        if new_bal < 0:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        acc['balance_cents'] = new_bal\n"
                "        return dict(acc)\n"
            )
        )
    },
    {
        "id": "backend-sqlalchemy-relations",
        "language": "python",
        "title": "SQLAlchemy: транзакции и межбанковские переводы",
        "topic": "Атомарные переводы между счетами, ACID и откат транзакций",
        "section": "Backend: Транзакции",
        "order": 53,
        "level": "Advanced",
        "minutes": 30,
        "theory": (
            "Перевод средств между счетами требует атомарности (буква 'A' в ACID): "
            "деньги должны быть списаны с одного счета и зачислены на другой либо операция не должна произойти вовсе.\n\n"
            "Если списание прошло успешно, а зачисление упало с ошибкой, транзакция должна быть полностью откатана (ROLLBACK). "
            "Ни копейки не должно потеряться или появиться из ниоткуда."
        ),
        "syntax": (
            "with session.begin():\n"
            "    from_acc.balance -= amount\n"
            "    to_acc.balance += amount\n"
            "    # commit происходит автоматически при выходе из блока with\n"
            "    # при ошибке происходит автоматический rollback"
        ),
        "examples": [
            (
                "def transfer_money(repo, from_id, to_id, amount):\n"
                "    # Проверяем оба счета до списания\n"
                "    repo.update_balance(from_id, -amount)\n"
                "    repo.update_balance(to_id, amount)"
            )
        ],
        "task": (
            "Создайте класс `TransferService`, принимающий `AccountRepository` в конструкторе, и реализуйте метод:\n"
            "`execute_transfer(from_id: int, to_id: int, amount_cents: int) -> dict`.\n"
            "Требования к выполнению:\n"
            "1. Сумма `amount_cents` должна быть строго больше 0 (иначе `ValueError('Invalid transfer amount')`).\n"
            "2. Перевод самому себе (`from_id == to_id`) запрещен (`ValueError('Cannot transfer to same account')`).\n"
            "3. Оба счета должны существовать. Если счет отправителя или получателя не найден — операция отклоняется (`KeyError('Account not found')`), балансы не меняются.\n"
            "4. У отправителя должно быть достаточно средств. Если средств недостаточно — бросается `ValueError('Insufficient funds')`, балансы обоих счетов не меняются.\n"
            "5. При успехе возвращается словарь:\n"
            "   `{'status': 'success', 'from_id': from_id, 'to_id': to_id, 'amount_cents': amount_cents, 'from_balance': new_from_bal, 'to_balance': new_to_bal}`."
        ),
        "starterCode": (
            "class TransferService:\n"
            "    def __init__(self, repo):\n"
            "        self.repo = repo\n"
            "\n"
            "    def execute_transfer(self, from_id: int, to_id: int, amount_cents: int) -> dict:\n"
            "        pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успешный межбанковский перевод",
                "expression": (
                    "class DummyRepo:\n"
                    "    def __init__(self):\n"
                    "        self.db = {1: {'id': 1, 'balance_cents': 1000}, 2: {'id': 2, 'balance_cents': 200}}\n"
                    "    def get_by_id(self, i): return self.db.get(i)\n"
                    "    def update_balance(self, i, d): self.db[i]['balance_cents'] += d; return self.db[i]\n"
                    "svc = TransferService(DummyRepo())\n"
                    "svc.execute_transfer(1, 2, 400)"
                ),
                "expected": {
                    "status": "success",
                    "from_id": 1,
                    "to_id": 2,
                    "amount_cents": 400,
                    "from_balance": 600,
                    "to_balance": 600
                }
            },
            {
                "id": "t2",
                "label": "Попытка перевода несуществующему получателю (откат списания)",
                "expression": (
                    "class DummyRepo:\n"
                    "    def __init__(self):\n"
                    "        self.db = {1: {'id': 1, 'balance_cents': 1000}}\n"
                    "    def get_by_id(self, i): return self.db.get(i)\n"
                    "    def update_balance(self, i, d): self.db[i]['balance_cents'] += d; return self.db[i]\n"
                    "repo = DummyRepo()\n"
                    "svc = TransferService(repo)\n"
                    "try:\n"
                    "    svc.execute_transfer(1, 999, 300)\n"
                    "except KeyError:\n"
                    "    pass\n"
                    "repo.get_by_id(1)['balance_cents']"
                ),
                "expected": 1000
            },
            {
                "id": "t3",
                "label": "Недостаточно средств у отправителя",
                "expression": (
                    "class DummyRepo:\n"
                    "    def __init__(self):\n"
                    "        self.db = {1: {'id': 1, 'balance_cents': 100}, 2: {'id': 2, 'balance_cents': 0}}\n"
                    "    def get_by_id(self, i): return self.db.get(i)\n"
                    "    def update_balance(self, i, d): self.db[i]['balance_cents'] += d; return self.db[i]\n"
                    "svc = TransferService(DummyRepo())\n"
                    "try:\n"
                    "    svc.execute_transfer(1, 2, 500)\n"
                    "    res = 'ok'\n"
                    "except ValueError as e:\n"
                    "    res = str(e)\n"
                    "res"
                ),
                "expected": "Insufficient funds"
            }
        ],
        "hints": [
            "Направление: проверьте аргументы: amount_cents > 0, from_id != to_id.",
            "Подход: сначала получите оба счета через get_by_id: убедитесь, что оба существуют и balance_cents >= amount_cents.",
            "Детали: только после проверки всех условий выполняйте списание и начисление."
        ],
        "commonMistakes": (
            "Списать деньги со счета отправителя ДО проверки существования счета получателя. "
            "Если получатель не существует, деньги исчезнут у отправителя."
        ),
        "solutionExplanation": (
            "Принцип валидации перед мутацией гарантирует атомарность: сначала проверяются оба счета и лимиты, "
            "и лишь затем производятся изменения."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["Transactions", "ACID", "Transfers", "Atomicity"],
        "walkthrough": [
            "Проверьте валидность суммы (> 0) и различие счетов",
            "Проверьте существование обоих счетов через repo.get_by_id",
            "Проверьте достаточность средств у отправителя",
            "Выполните списание и начисление",
            "Верните результат успешного перевода"
        ],
        "prerequisites": ["backend-sqlalchemy-orm"],
        "resources": [{"title": "PostgreSQL Transactions", "url": "https://www.postgresql.org/docs/current/tutorial-transactions.html", "language": "python"}],
        "lifeExample": "Перевод денег через СБП: сервер списывает деньги только после подтверждения банком получателя, что номер счета действителен.",
        "guide": make_guide(
            "SQLAlchemy: транзакции и переводы",
            "Атомарные переводы между счетами и ACID",
            (
                "class TransferService:\n"
                "    def __init__(self, repo):\n"
                "        self.repo = repo\n"
                "\n"
                "    def execute_transfer(self, from_id: int, to_id: int, amount_cents: int) -> dict:\n"
                "        if amount_cents <= 0:\n"
                "            raise ValueError('Invalid transfer amount')\n"
                "        if from_id == to_id:\n"
                "            raise ValueError('Cannot transfer to same account')\n"
                "        src = self.repo.get_by_id(from_id)\n"
                "        dst = self.repo.get_by_id(to_id)\n"
                "        if not src or not dst:\n"
                "            raise KeyError('Account not found')\n"
                "        if src['balance_cents'] < amount_cents:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        new_src = self.repo.update_balance(from_id, -amount_cents)\n"
                "        new_dst = self.repo.update_balance(to_id, amount_cents)\n"
                "        return {\n"
                "            'status': 'success',\n"
                "            'from_id': from_id,\n"
                "            'to_id': to_id,\n"
                "            'amount_cents': amount_cents,\n"
                "            'from_balance': new_src['balance_cents'],\n"
                "            'to_balance': new_dst['balance_cents']\n"
                "        }\n"
            )
        )
    },
    {
        "id": "backend-pytest-fixtures",
        "language": "python",
        "title": "Тестирование backend: pytest и тестовые фикстуры",
        "topic": "Изоляция тестов, фикстуры данных и проверка утверждений assert",
        "section": "Backend: Тестирование",
        "order": 54,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "pytest — промышленный стандарт тестирования в Python экосистеме. "
            "Фикстуры (@pytest.fixture) позволяют готовить чистое состояние базы данных, "
            "создавать тестовых пользователей и гарантировать, что один тест не влияет на результаты другого.\n\n"
            "Принципы надежных тестов:\n"
            "• Arrange: подготовка входных данных и зависимостей.\n"
            "• Act: вызов тестируемой функции или API эндпоинта.\n"
            "• Assert: проверка результата и инвариантов системы."
        ),
        "syntax": (
            "import pytest\n\n"
            "@pytest.fixture\n"
            "def test_account():\n"
            "    return {'id': 1, 'balance': 100}\n\n"
            "def test_deposit(test_account):\n"
            "    deposit(test_account, 50)\n"
            "    assert test_account['balance'] == 150"
        ),
        "examples": [
            (
                "def run_unit_test(test_fn):\n"
                "    try:\n"
                "        test_fn()\n"
                "        return {'passed': True, 'error': None}\n"
                "    except AssertionError as e:\n"
                "        return {'passed': False, 'error': str(e)}"
            )
        ],
        "task": (
            "Реализуйте мини-раннер тестов `run_test_suite(test_cases: list[callable]) -> dict`.\n"
            "Он принимает список функций-тестов без аргументов. Каждая функция выполняет проверки через `assert`.\n"
            "Функция должна запускать каждый тест и возвращать статистику:\n"
            "{\n"
            "    'total': int,\n"
            "    'passed': int,\n"
            "    'failed': int,\n"
            "    'errors': list[str]  # список сообщений об ошибках завалившихся тестов\n"
            "}\n"
            "Если тест вызвал AssertionError или любое другое исключение — он считается завалившимся ('failed')."
        ),
        "starterCode": (
            "def run_test_suite(test_cases: list) -> dict:\n"
            "    # Ваш код здесь\n"
            "    pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Все тесты успешны",
                "expression": (
                    "t1 = lambda: None\n"
                    "t2 = lambda: None\n"
                    "run_test_suite([t1, t2])"
                ),
                "expected": {"total": 2, "passed": 2, "failed": 0, "errors": []}
            },
            {
                "id": "t2",
                "label": "Тест упал по assert",
                "expression": (
                    "def t_pass(): assert 1 + 1 == 2\n"
                    "def t_fail(): assert 2 * 2 == 5, 'Math error'\n"
                    "run_test_suite([t_pass, t_fail])"
                ),
                "expected": {"total": 2, "passed": 1, "failed": 1, "errors": ["Math error"]}
            }
        ],
        "hints": [
            "Направление: переберите функции в цикле for test_fn in test_cases:.",
            "Подход: вызовите test_fn() внутри try-except Exception as e:.",
            "Детали: если e пустое, сообщение об ошибке можно взять как type(e).__name__ или str(e)."
        ],
        "commonMistakes": (
            "Ловить только AssertionError и пропускать TypeError или ValueError, которые также делают тест проваленным."
        ),
        "solutionExplanation": (
            "Тестовый раннер изолирует выполнение каждого тестового кейса и собирает сводную статистику."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["pytest", "Testing", "Unit Tests", "Assertions"],
        "walkthrough": [
            "Инициализируйте счетчики passed, failed и список errors",
            "Запустите каждый тест в блоке try-except",
            "При успехе увеличьте passed, при исключении увеличьте failed и добавьте ошибку",
            "Верните итоговый словарь"
        ],
        "prerequisites": ["python-testing", "python-exceptions"],
        "resources": [{"title": "pytest Documentation", "url": "https://docs.pytest.org/", "language": "python"}],
        "lifeExample": "Автоматическая линия контроля качества на заводе: проверяет размеры каждой детали перед выпуском партии в продажу.",
        "guide": make_guide(
            "Тестирование backend: pytest",
            "Изоляция тестов и запуск тестовых наборов",
            (
                "def run_test_suite(test_cases: list) -> dict:\n"
                "    total = len(test_cases)\n"
                "    passed = 0\n"
                "    failed = 0\n"
                "    errors = []\n"
                "    for fn in test_cases:\n"
                "        try:\n"
                "            fn()\n"
                "            passed += 1\n"
                "        except Exception as e:\n"
                "            failed += 1\n"
                "            msg = str(e) if str(e) else type(e).__name__\n"
                "            errors.append(msg)\n"
                "    return {'total': total, 'passed': passed, 'failed': failed, 'errors': errors}\n"
            )
        )
    },
    {
        "id": "backend-docker-compose",
        "language": "python",
        "title": "Контейнеризация: Dockerfile, переменные и Compose",
        "topic": "Изоляция окружения, docker-compose.yml и конфигурация сервисов",
        "section": "Backend: Деплой и контейнеризация",
        "order": 55,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "Контейнеризация в Docker позволяет упаковать приложение со всеми зависимостями и версией Python "
            "в неизменяемый образ (image), гарантируя, что код запустится одинаково на компьютере разработчика, "
            "сервере тестирования и в production-кластере.\n\n"
            "Инструмент `docker-compose` связывает в единую сеть несколько сервисов:\n"
            "1. Контейнер с приложением (FastAPI + uvicorn).\n"
            "2. Контейнер базы данных (PostgreSQL с persistent volume для данных).\n"
            "3. Переменные окружения (DATABASE_URL, SECRET_KEY) передаются через .env файл."
        ),
        "syntax": (
            "# Dockerfile:\n"
            "FROM python:3.11-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            "CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
        ),
        "examples": [
            (
                "def make_db_url(user, password, host, port, db_name):\n"
                "    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'"
            )
        ],
        "task": (
            "Реализуйте функцию `build_compose_config(app_port: int, db_port: int, db_name: str) -> dict`.\n"
            "Она должна формировать конфигурационный словарь, описывающий сервисы для docker-compose:\n"
            "{\n"
            "    'version': '3.8',\n"
            "    'services': {\n"
            "        'app': {\n"
            "            'build': '.',\n"
            "            'ports': [f'{app_port}:8000'],\n"
            "            'environment': {\n"
            "                'DATABASE_URL': f'postgresql://postgres:postgres@db:{db_port}/{db_name}'\n"
            "            },\n"
            "            'depends_on': ['db']\n"
            "        },\n"
            "        'db': {\n"
            "            'image': 'postgres:15-alpine',\n"
            "            'ports': [f'{db_port}:5432'],\n"
            "            'environment': {\n"
            "                'POSTGRES_DB': db_name,\n"
            "                'POSTGRES_USER': 'postgres',\n"
            "                'POSTGRES_PASSWORD': 'postgres'\n"
            "            },\n"
            "            'volumes': ['postgres_data:/var/lib/postgresql/data']\n"
            "        }\n"
            "    },\n"
            "    'volumes': {'postgres_data': None}\n"
            "}"
        ),
        "starterCode": (
            "def build_compose_config(app_port: int, db_port: int, db_name: str) -> dict:\n"
            "    # Ваш код здесь\n"
            "    pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Генерация конфигурации со стандартными портами",
                "expression": "build_compose_config(8000, 5432, 'devforge_db')",
                "expected": {
                    "version": "3.8",
                    "services": {
                        "app": {
                            "build": ".",
                            "ports": ["8000:8000"],
                            "environment": {
                                "DATABASE_URL": "postgresql://postgres:postgres@db:5432/devforge_db"
                            },
                            "depends_on": ["db"]
                        },
                        "db": {
                            "image": "postgres:15-alpine",
                            "ports": ["5432:5432"],
                            "environment": {
                                "POSTGRES_DB": "devforge_db",
                                "POSTGRES_USER": "postgres",
                                "POSTGRES_PASSWORD": "postgres"
                            },
                            "volumes": ["postgres_data:/var/lib/postgresql/data"]
                        }
                    },
                    "volumes": {"postgres_data": None}
                }
            }
        ],
        "hints": [
            "Направление: соберите вложенный словарь в точности по спецификации задачи.",
            "Подход: подставьте аргументы app_port, db_port, db_name в строки портов и переменных.",
            "Детали: обратите внимание на зависимость depends_on: ['db'] у сервиса app."
        ],
        "commonMistakes": (
            "Опечатки в именах ключей environment или неверный формат строки подключения к PostgreSQL."
        ),
        "solutionExplanation": (
            "Конфигурация docker-compose описывает согласованный запуск контейнера с бекендом и СУБД в общей сети."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Docker", "Docker Compose", "Containers", "DevOps"],
        "walkthrough": [
            "Сформируйте секцию app с портами и переменной DATABASE_URL",
            "Сформируйте секцию db с образом postgres:15-alpine и volume",
            "Добавьте том postgres_data в корень конфигурации"
        ],
        "prerequisites": ["backend-http-rest"],
        "resources": [{"title": "Docker Compose Specification", "url": "https://docs.docker.com/compose/", "language": "python"}],
        "lifeExample": "Стандартный морской контейнер: неважно, на какой корабль или поезд его поставят — содержимое надежно защищено и стандартизировано.",
        "guide": make_guide(
            "Контейнеризация: Docker Compose",
            "Декларативное описание мультисервисной архитектуры",
            (
                "def build_compose_config(app_port: int, db_port: int, db_name: str) -> dict:\n"
                "    return {\n"
                "        'version': '3.8',\n"
                "        'services': {\n"
                "            'app': {\n"
                "                'build': '.',\n"
                "                'ports': [f'{app_port}:8000'],\n"
                "                'environment': {\n"
                "                    'DATABASE_URL': f'postgresql://postgres:postgres@db:{db_port}/{db_name}'\n"
                "                },\n"
                "                'depends_on': ['db']\n"
                "            Client',\n"
                "            'db': {\n"
                "                'image': 'postgres:15-alpine',\n"
                "                'ports': [f'{db_port}:5432'],\n"
                "                'environment': {\n"
                "                    'POSTGRES_DB': db_name,\n"
                "                    'POSTGRES_USER': 'postgres',\n"
                "                    'POSTGRES_PASSWORD': 'postgres'\n"
                "                },\n"
                "                'volumes': ['postgres_data:/var/lib/postgresql/data']\n"
                "            }\n"
                "        },\n"
                "        'volumes': {'postgres_data': None}\n"
                "    }\n"
            )
        )
    },
    {
        "id": "backend-project-bank-api",
        "language": "python",
        "title": "Итоговый проект: API счетов, переводов и транзакций",
        "topic": "Комплексный Backend сервис: аутентификация, счета, переводы, пагинация",
        "section": "Backend: Итоговый проект",
        "order": 56,
        "level": "Advanced",
        "minutes": 45,
        "theory": (
            "Итоговый проект направления Backend Development объединяет все изученные технологии:\n"
            "• Клиент-серверное API со статусами и кодами ошибок.\n"
            "• Регистрация и аутентификация пользователей по Bearer токену.\n"
            "• Управление счетами и балансом в копейках (целочисленная арифметика).\n"
            "• Атомарные переводы между счетами с гарантией транзакционной целостности.\n"
            "• История операций с пагинацией и сортировкой от новых к старым."
        ),
        "syntax": (
            "class BankApplication:\n"
            "    def register_user(self, username, password):\n"
            "        ...\n"
            "    def create_account(self, token, initial_cents):\n"
            "        ...\n"
            "    def transfer(self, token, from_acc, to_acc, cents):\n"
            "        ...\n"
            "    def get_history(self, token, acc_id, page, page_size):\n"
            "        ..."
        ),
        "examples": [
            (
                "app = BankApplication()\n"
                "token = app.register_user('elena', 'pass123')\n"
                "acc_id = app.create_account(token, 5000)\n"
                "balance = app.get_balance(token, acc_id)"
            )
        ],
        "task": (
            "Реализуйте полноценный класс `BankApplication` со следующими методами:\n"
            "1. `register_user(username: str, password: str) -> str`:\n"
            "   • Если пользователь с таким именем уже существует или имя короче 3 символов — бросает `ValueError`.\n"
            "   • Генерирует и возвращает токен доступа: f'token_{username}'.\n"
            "2. `authenticate(username: str, password: str) -> str`:\n"
            "   • Проверяет имя и пароль, при ошибке бросает `PermissionError('Invalid credentials')`.\n"
            "   • Возвращает токен f'token_{username}'.\n"
            "3. `create_account(token: str, initial_cents: int = 0) -> int`:\n"
            "   • Проверяет токен (при невалидном токене бросает `PermissionError`).\n"
            "   • Создает счет с автоинкрементным id (начиная с 1) и возвращает `account_id`.\n"
            "4. `get_balance(token: str, account_id: int) -> int`:\n"
            "   • Возвращает баланс счета в копейках.\n"
            "   • Если счет не принадлежит пользователю или не существует — бросает `KeyError`.\n"
            "5. `transfer(token: str, from_id: int, to_id: int, amount_cents: int) -> dict`:\n"
            "   • Проверяет токен и принадлежность счета `from_id` пользователю.\n"
            "   • Проверяет `amount_cents > 0` и `from_id != to_id`.\n"
            "   • Проверяет достаточность средств (при нехватке — `ValueError('Insufficient funds')`).\n"
            "   • Атомарно списывает и начисляет средства, добавляет запись в историю обоих счетов.\n"
            "   • Возвращает `{'status': 'success', 'amount_cents': amount_cents}`.\n"
            "6. `get_history(token: str, account_id: int, page: int = 1, page_size: int = 5) -> list[dict]`:\n"
            "   • Возвращает срез истории операций по счету с пагинацией (1-based page)."
        ),
        "starterCode": (
            "class BankApplication:\n"
            "    def __init__(self):\n"
            "        pass\n"
            "\n"
            "    def register_user(self, username: str, password: str) -> str:\n"
            "        pass\n"
            "\n"
            "    def authenticate(self, username: str, password: str) -> str:\n"
            "        pass\n"
            "\n"
            "    def create_account(self, token: str, initial_cents: int = 0) -> int:\n"
            "        pass\n"
            "\n"
            "    def get_balance(self, token: str, account_id: int) -> int:\n"
            "        pass\n"
            "\n"
            "    def transfer(self, token: str, from_id: int, to_id: int, amount_cents: int) -> dict:\n"
            "        pass\n"
            "\n"
            "    def get_history(self, token: str, account_id: int, page: int = 1, page_size: int = 5) -> list[dict]:\n"
            "        pass\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Полный сценарий: регистрация, создание счета, перевод и баланс",
                "expression": (
                    "bank = BankApplication()\n"
                    "t1 = bank.register_user('alice', 'secret1')\n"
                    "t2 = bank.register_user('bob', 'secret2')\n"
                    "a1 = bank.create_account(t1, 1000)\n"
                    "a2 = bank.create_account(t2, 200)\n"
                    "res = bank.transfer(t1, a1, a2, 400)\n"
                    "[res['status'], bank.get_balance(t1, a1), bank.get_balance(t2, a2)]"
                ),
                "expected": ["success", 600, 600]
            },
            {
                "id": "t2",
                "label": "История операций и пагинация",
                "expression": (
                    "bank = BankApplication()\n"
                    "t1 = bank.register_user('victor', '123')\n"
                    "t2 = bank.register_user('anna', '456')\n"
                    "a1 = bank.create_account(t1, 500)\n"
                    "a2 = bank.create_account(t2, 0)\n"
                    "bank.transfer(t1, a1, a2, 100)\n"
                    "bank.transfer(t1, a1, a2, 50)\n"
                    "hist = bank.get_history(t1, a1, 1, 10)\n"
                    "len(hist)"
                ),
                "expected": 2
            },
            {
                "id": "t3",
                "label": "Защита от списания с чужого счета",
                "expression": (
                    "bank = BankApplication()\n"
                    "t1 = bank.register_user('user1', 'pass')\n"
                    "t2 = bank.register_user('user2', 'pass')\n"
                    "a1 = bank.create_account(t1, 1000)\n"
                    "a2 = bank.create_account(t2, 0)\n"
                    "try:\n"
                    "    bank.transfer(t2, a1, a2, 500) # user2 пытается списать со счета a1 (user1)\n"
                    "    ans = 'unauthorized'\n"
                    "except (PermissionError, KeyError):\n"
                    "    ans = 'denied'\n"
                    "ans"
                ),
                "expected": "denied"
            }
        ],
        "hints": [
            "Направление: структурируйте внутренние словари: self.users, self.tokens, self.accounts, self.history.",
            "Подход: в transfer проверьте, что token принадлежит владельцу счета from_id.",
            "Детали: для пагинации используйте срез списка: start = (page - 1) * page_size, end = start + page_size."
        ],
        "commonMistakes": (
            "Позволить пользователю списать деньги со счета, который ему не принадлежит, "
            "или не сохранить операцию в историю обоих участников перевода."
        ),
        "solutionExplanation": (
            "Итоговый проект реализует многопользовательский сервис с авторизацией, целостными переводами и аудитом."
        ),
        "xp": 100,
        "setupSql": "",
        "concepts": ["Backend Architecture", "FastAPI", "PostgreSQL", "Transactions", "Security"],
        "walkthrough": [
            "Реализуйте регистрацию и валидацию пользователей",
            "Реализуйте создание счетов с привязкой к пользователю",
            "Реализуйте транзакционный перевод с проверкой прав доступа",
            "Реализуйте историю операций с пагинацией"
        ],
        "prerequisites": ["backend-http-rest", "backend-fastapi-models", "backend-sqlalchemy-relations"],
        "resources": [{"title": "FastAPI Full Stack Architecture", "url": "https://fastapi.tiangolo.com/tutorial/", "language": "python"}],
        "lifeExample": "Архитектура ядра цифрового банка: обработка платежей, балансов и выписок миллионов клиентов.",
        "guide": make_guide(
            "Итоговый проект: API банковских счетов",
            "Комплексный Backend сервис с транзакциями и авторизацией",
            (
                "class BankApplication:\n"
                "    def __init__(self):\n"
                "        self.users = {} # username -> password\n"
                "        self.tokens = {} # token -> username\n"
                "        self.accounts = {} # acc_id -> dict\n"
                "        self.history = {} # acc_id -> list\n"
                "        self.next_acc_id = 1\n"
                "\n"
                "    def register_user(self, username: str, password: str) -> str:\n"
                "        if not username or len(username) < 3:\n"
                "            raise ValueError('Username too short')\n"
                "        if username in self.users:\n"
                "            raise ValueError('User already exists')\n"
                "        self.users[username] = password\n"
                "        token = f'token_{username}'\n"
                "        self.tokens[token] = username\n"
                "        return token\n"
                "\n"
                "    def authenticate(self, username: str, password: str) -> str:\n"
                "        if username not in self.users or self.users[username] != password:\n"
                "            raise PermissionError('Invalid credentials')\n"
                "        token = f'token_{username}'\n"
                "        self.tokens[token] = username\n"
                "        return token\n"
                "\n"
                "    def _get_user_from_token(self, token: str) -> str:\n"
                "        if token not in self.tokens:\n"
                "            raise PermissionError('Invalid token')\n"
                "        return self.tokens[token]\n"
                "\n"
                "    def create_account(self, token: str, initial_cents: int = 0) -> int:\n"
                "        user = self._get_user_from_token(token)\n"
                "        acc_id = self.next_acc_id\n"
                "        self.next_acc_id += 1\n"
                "        self.accounts[acc_id] = {'id': acc_id, 'owner': user, 'balance_cents': initial_cents}\n"
                "        self.history[acc_id] = []\n"
                "        return acc_id\n"
                "\n"
                "    def get_balance(self, token: str, account_id: int) -> int:\n"
                "        user = self._get_user_from_token(token)\n"
                "        if account_id not in self.accounts:\n"
                "            raise KeyError('Account not found')\n"
                "        acc = self.accounts[account_id]\n"
                "        if acc['owner'] != user:\n"
                "            raise KeyError('Account does not belong to user')\n"
                "        return acc['balance_cents']\n"
                "\n"
                "    def transfer(self, token: str, from_id: int, to_id: int, amount_cents: int) -> dict:\n"
                "        user = self._get_user_from_token(token)\n"
                "        if from_id not in self.accounts or to_id not in self.accounts:\n"
                "            raise KeyError('Account not found')\n"
                "        src = self.accounts[from_id]\n"
                "        dst = self.accounts[to_id]\n"
                "        if src['owner'] != user:\n"
                "            raise PermissionError('Unauthorized access to account')\n"
                "        if amount_cents <= 0 or from_id == to_id:\n"
                "            raise ValueError('Invalid transfer')\n"
                "        if src['balance_cents'] < amount_cents:\n"
                "            raise ValueError('Insufficient funds')\n"
                "        src['balance_cents'] -= amount_cents\n"
                "        dst['balance_cents'] += amount_cents\n"
                "        record = {'from_id': from_id, 'to_id': to_id, 'amount_cents': amount_cents}\n"
                "        self.history[from_id].append(record)\n"
                "        self.history[to_id].append(record)\n"
                "        return {'status': 'success', 'amount_cents': amount_cents}\n"
                "\n"
                "    def get_history(self, token: str, account_id: int, page: int = 1, page_size: int = 5) -> list[dict]:\n"
                "        user = self._get_user_from_token(token)\n"
                "        if account_id not in self.accounts or self.accounts[account_id]['owner'] != user:\n"
                "            raise KeyError('Account not accessible')\n"
                "        records = self.history.get(account_id, [])\n"
                "        start = (page - 1) * page_size\n"
                "        end = start + page_size\n"
                "        return records[start:end]\n"
            )
        )
    }
]


FRONTEND_LESSONS = [
{
        "id": "frontend-js-async-promises",
        "language": "javascript",
        "title": "JavaScript: Promises, async/await и микротаски",
        "topic": "Асинхронность, цепочки промисов и Event Loop",
        "section": "Frontend: Асинхронный JavaScript",
        "order": 21,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "Веб-интерфейсы взаимодействуют с сервером асинхронно: пока браузер ждёт ответ от API, "
            "пользовательский интерфейс не должен зависать. В JavaScript за это отвечает Event Loop и промисы (Promises).\n\n"
            "Состояния промиса:\n"
            "• pending — ожидание результата.\n"
            "• fulfilled — успешное завершение (вызов resolve).\n"
            "• rejected — ошибка (вызов reject).\n\n"
            "Синтаксис async/await позволяет писать асинхронный код линейно, перехватывая ошибки через привычный try...catch."
        ),
        "syntax": (
            "async function loadData(url) {\n"
            "  try {\n"
            "    const res = await fetch(url);\n"
            "    return await res.json();\n"
            "  } catch (err) {\n"
            "    console.error('Network error:', err);\n"
            "  }\n"
            "}"
        ),
        "examples": [
            (
                "function wait(ms) {\n"
                "  return new Promise(resolve => setTimeout(resolve, ms));\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте асинхронную функцию `retryOperation(operationFn, maxAttempts)`\n"
            "Она должна выполнять переданную функцию `operationFn()` (которая возвращает промис):\n"
            "1. Если операция выполнилась успешно — возвращать результат операции.\n"
            "2. Если операция выбросила ошибку, а количество сделанных попыток меньше `maxAttempts` — пробовать снова.\n"
            "3. Если попытки исчерпаны — пробрасывать последнюю ошибку наружу через throw."
        ),
        "starterCode": (
            "async function retryOperation(operationFn, maxAttempts) {\n"
            "  // Ваш код здесь\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успех с первой попытки",
                "expression": (
                    "let calls = 0;\n"
                    "const op = async () => { calls++; return 'success'; };\n"
                    "await retryOperation(op, 3)"
                ),
                "expected": "success"
            },
            {
                "id": "t2",
                "label": "Успех со второй попытки",
                "expression": (
                    "let calls = 0;\n"
                    "const op = async () => {\n"
                    "  calls++;\n"
                    "  if (calls < 2) throw new Error('Network glitch');\n"
                    "  return 'recovered';\n"
                    "};\n"
                    "await retryOperation(op, 3)"
                ),
                "expected": "recovered"
            }
        ],
        "hints": [
            "Направление: используйте цикл for (let attempt = 1; attempt <= maxAttempts; attempt++).",
            "Подход: вызовите await operationFn() внутри try-catch.",
            "Детали: если attempt === maxAttempts внутри блока catch — выполните throw error."
        ],
        "commonMistakes": (
            "Забывать писать await перед вызовом operationFn(), из-за чего блок catch не перехватывает ошибку промиса."
        ),
        "solutionExplanation": (
            "Функция выполняет цикл повторов, ожидая разрешения промиса в блоке try, и выбрасывает ошибку при исчерпании лимита."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Promises", "async/await", "Event Loop", "Error Handling"],
        "walkthrough": [
            "Создайте переменную для сохранения последней ошибки",
            "Организуйте цикл попыток от 1 до maxAttempts",
            "В блоке try вызовите await operationFn() и верните результат",
            "В блоке catch сохраните ошибку, а на последней итерации пробросьте её"
        ],
        "prerequisites": ["javascript-functions", "javascript-arrow"],
        "resources": [{"title": "MDN: Using Promises", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises", "language": "javascript"}],
        "lifeExample": "Повторный набор телефонного номера при сигнале 'занято'.",
        "guide": make_guide(
            "JavaScript: Promises и async/await",
            "Повторные сетевые запросы при сбоях",
            (
                "async function retryOperation(operationFn, maxAttempts) {\n"
                "  let lastError;\n"
                "  for (let attempt = 1; attempt <= maxAttempts; attempt++) {\n"
                "    try {\n"
                "      return await operationFn();\n"
                "    } catch (err) {\n"
                "      lastError = err;\n"
                "      if (attempt === maxAttempts) throw lastError;\n"
                "    }\n"
                "  }\n"
                "}\n"
            )
        )
    },
    {
        "id": "frontend-js-dom-events",
        "language": "javascript",
        "title": "DOM, события и делегирование в интерфейсах",
        "topic": "Event Delegation, target, bubbling и обработка динамических элементов",
        "section": "Frontend: DOM и события",
        "order": 22,
        "level": "Intermediate",
        "minutes": 25,
        "theory": (
            "Когда в интерфейсе много динамических элементов (например, десятки строк товаров в корзине), "
            "вешать отдельный слушатель на каждую кнопку затратно по памяти. "
            "Вместо этого используют паттерн Делегирование событий (Event Delegation): "
            "вешают один слушатель на родительский контейнер и определяют кликнутый элемент через `event.target`."
        ),
        "syntax": (
            "container.addEventListener('click', (event) => {\n"
            "  const btn = event.target.closest('[data-action]');\n"
            "  if (!btn) return;\n"
            "  const action = btn.dataset.action;\n"
            "  const id = btn.dataset.id;\n"
            "});"
        ),
        "examples": [
            (
                "function parseDataset(element) {\n"
                "  return element.dataset.action || null;\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте функцию `dispatchCartAction(eventTargetData, handlers)`:\n"
            "Она принимает объект кликнутого элемента `eventTargetData = { action: string, id: number, quantity?: number }` "
            "и объект с коллбэками `handlers = { onIncrease(id), onDecrease(id), onRemove(id) }`.\n"
            "• При action === 'increase' — вызывает `handlers.onIncrease(id)` и возвращает результат.\n"
            "• При action === 'decrease' — вызывает `handlers.onDecrease(id)` и возвращает результат.\n"
            "• При action === 'remove' — вызывает `handlers.onRemove(id)` и возвращает результат.\n"
            "• При неизвестном действии — возвращает null."
        ),
        "starterCode": (
            "function dispatchCartAction(targetData, handlers) {\n"
            "  // Ваш код здесь\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Увеличение количества товара",
                "expression": (
                    "let incId = null;\n"
                    "const h = { onIncrease: (id) => { incId = id; return 'inc-done'; } };\n"
                    "const res = dispatchCartAction({ action: 'increase', id: 42 }, h);\n"
                    "[res, incId]"
                ),
                "expected": ["inc-done", 42]
            },
            {
                "id": "t2",
                "label": "Удаление товара",
                "expression": (
                    "let remId = null;\n"
                    "const h = { onRemove: (id) => { remId = id; return 'rem-done'; } };\n"
                    "const res = dispatchCartAction({ action: 'remove', id: 99 }, h);\n"
                    "[res, remId]"
                ),
                "expected": ["rem-done", 99]
            }
        ],
        "hints": [
            "Направление: используйте конструкцию switch (targetData.action).",
            "Подход: проверяйте наличие соответствующей функции в объекте handlers перед вызовом.",
            "Детали: передавайте targetData.id аргументом в обработчик."
        ],
        "commonMistakes": (
            "Вызывать функцию, если она не передана в объекте handlers (проверяйте handlers[name])."
        ),
        "solutionExplanation": (
            "Диспетчер маршрутизирует событие по атрибуту action к нужному обработчику."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["DOM", "Events", "Delegation", "Event Loop"],
        "walkthrough": [
            "Проверьте наличие targetData и targetData.action",
            "Сопоставьте действие с коллбэком из handlers",
            "Вызовите функцию и верните результат"
        ],
        "prerequisites": ["javascript-objects", "javascript-functions"],
        "resources": [{"title": "MDN: Event Delegation", "url": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#event_delegation", "language": "javascript"}],
        "lifeExample": "Стойка ресепшен в отеле: все гости подходят к одному окну, а администратор перенаправляет запросы горничной или мастеру.",
        "guide": make_guide(
            "DOM и делегирование событий",
            "Маршрутизация кликов интерфейса",
            (
                "function dispatchCartAction(targetData, handlers) {\n"
                "  if (!targetData || !targetData.action) return null;\n"
                "  switch (targetData.action) {\n"
                "    case 'increase':\n"
                "      return handlers.onIncrease ? handlers.onIncrease(targetData.id) : null;\n"
                "    case 'decrease':\n"
                "      return handlers.onDecrease ? handlers.onDecrease(targetData.id) : null;\n"
                "    case 'remove':\n"
                "      return handlers.onRemove ? handlers.onRemove(targetData.id) : null;\n"
                "    default:\n"
                "      return null;\n"
                "  }\n"
                "}\n"
            )
        )
    },
    {
        "id": "frontend-react-hooks-state",
        "language": "javascript",
        "title": "React: управление состоянием формы и валидация",
        "topic": "useState, контролируемые компоненты и проверка ввода",
        "section": "Frontend: React и формы",
        "order": 23,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "В React состояние компонента управляется через хук `useState`. "
            "Контролируемые поля ввода (controlled components) связывают `value` с состоянием, "
            "а обновление происходит в обработчике `onChange`.\n\n"
            "Паттерн управления формой включает:\n"
            "• Объект значений `values`.\n"
            "• Объект ошибок `errors` (например `{ email: 'Некорректный email' }`).\n"
            "• Флаг готовности `isValid` (true, когда нет ошибок и все обязательные поля заполнены)."
        ),
        "syntax": (
            "const [values, setValues] = useState({ name: '', email: '' });\n"
            "const [errors, setErrors] = useState({});"
        ),
        "examples": [
            (
                "function validateEmail(email) {\n"
                "  return email.includes('@') && email.includes('.');\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `FormStateManager` для управления состоянием формы заказа:\n"
            "Конструктор принимает `initialValues: { name: string, email: string, address: string }`.\n"
            "Методы:\n"
            "1. `setValue(fieldName, value)`: обновляет значение поля и автоматически валидирует его.\n"
            "2. `getValues()`: возвращает текущий объект значений.\n"
            "3. `getErrors()`: возвращает текущий объект ошибок.\n"
            "4. `isValid()`: возвращает true, если ошибок нет и все три поля не пустые (после trim()).\n\n"
            "Правила валидации:\n"
            "• name: длина от 2 символов (иначе ошибка 'Имя слишком короткое').\n"
            "• email: содержит '@' и '.' (иначе 'Некорректный email').\n"
            "• address: длина от 5 символов (иначе 'Укажите полный адрес')."
        ),
        "starterCode": (
            "class FormStateManager {\n"
            "  constructor(initialValues) {\n"
            "    // Ваш код здесь\n"
            "  }\n"
            "  setValue(fieldName, value) {}\n"
            "  getValues() {}\n"
            "  getErrors() {}\n"
            "  isValid() {}\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Валидация корректной формы",
                "expression": (
                    "const f = new FormStateManager({ name: 'Анна', email: 'anna@mail.ru', address: 'ул. Ленина, 10' });\n"
                    "[f.isValid(), Object.keys(f.getErrors()).length]"
                ),
                "expected": [True, 0]
            },
            {
                "id": "t2",
                "label": "Обнаружение ошибки в email",
                "expression": (
                    "const f = new FormStateManager({ name: 'Иван', email: 'bad-email', address: 'г. Москва, Арбат' });\n"
                    "[f.isValid(), f.getErrors().email]"
                ),
                "expected": [False, "Некорректный email"]
            }
        ],
        "hints": [
            "Направление: храните this.values и this.errors.",
            "Подход: в setValue(fieldName, value) сначала обновите this.values[fieldName], затем вызовите валидацию.",
            "Детали: если валидация поля успешна, удаляйте ключ из this.errors через delete this.errors[fieldName]."
        ],
        "commonMistakes": (
            "Не удалять старую ошибку из объекта errors, когда пользователь исправил опечатку в поле."
        ),
        "solutionExplanation": (
            "Менеджер состояния синхронно проверяет введённые данные и гарантирует консистентность состояния формы."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["React", "useState", "Forms", "Validation"],
        "walkthrough": [
            "Инициализируйте values и errors в конструкторе",
            "Реализуйте метод валидации для каждого поля",
            "Реализуйте setValue с обновлением ошибок",
            "Реализуйте вычисление isValid"
        ],
        "prerequisites": ["javascript-classes", "javascript-objects"],
        "resources": [{"title": "React: Forms", "url": "https://react.dev/reference/react-dom/components/input", "language": "javascript"}],
        "lifeExample": "Электронный бланк отправки посылки: проверяет индекс и телефон прямо по ходу заполнения.",
        "guide": make_guide(
            "React: управление формами",
            "Валидация полей ввода и состояние",
            (
                "class FormStateManager {\n"
                "  constructor(initialValues = {}) {\n"
                "    this.values = { name: '', email: '', address: '', ...initialValues };\n"
                "    this.errors = {};\n"
                "    this.validateAll();\n"
                "  }\n"
                "  validateField(field, val) {\n"
                "    const v = (val || '').trim();\n"
                "    if (field === 'name') {\n"
                "      if (v.length < 2) return 'Имя слишком короткое';\n"
                "    } else if (field === 'email') {\n"
                "      if (!v.includes('@') || !v.includes('.')) return 'Некорректный email';\n"
                "    } else if (field === 'address') {\n"
                "      if (v.length < 5) return 'Укажите полный адрес';\n"
                "    }\n"
                "    return null;\n"
                "  }\n"
                "  validateAll() {\n"
                "    this.errors = {};\n"
                "    for (const f of ['name', 'email', 'address']) {\n"
                "      const err = this.validateField(f, this.values[f]);\n"
                "      if (err) this.errors[f] = err;\n"
                "    }\n"
                "  }\n"
                "  setValue(field, val) {\n"
                "    this.values[field] = val;\n"
                "    const err = this.validateField(field, val);\n"
                "    if (err) this.errors[field] = err;\n"
                "    else delete this.errors[field];\n"
                "  }\n"
                "  getValues() { return { ...this.values }; }\n"
                "  getErrors() { return { ...this.errors }; }\n"
                "  isValid() {\n"
                "    return Object.keys(this.errors).length === 0 &&\n"
                "      Boolean(this.values.name?.trim() && this.values.email?.trim() && this.values.address?.trim());\n"
                "  }\n"
                "}\n"
            )
        )
    },
    {
        "id": "frontend-react-hooks-advanced",
        "language": "javascript",
        "title": "Хуки React: состояние корзины и мемоизация",
        "topic": "useReducer, useMemo, расчет скидок и общих сумм",
        "section": "Frontend: Состояние корзины",
        "order": 24,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "Сложное состояние интернет-магазина (товары в корзине, промокоды, скидки, доставка) "
            "удобно инкапсулировать в отдельный модуль или редьюсер. "
            "Вычисления итоговых сумм не должны повторяться при каждом ререндере, если корзина не изменилась."
        ),
        "syntax": (
            "const totals = useMemo(() => {\n"
            "  return items.reduce((acc, item) => acc + item.price * item.quantity, 0);\n"
            "}, [items]);"
        ),
        "examples": [
            (
                "function sumItems(items) {\n"
                "  return items.reduce((sum, x) => sum + x.price * x.qty, 0);\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `CartManager` со следующими методами:\n"
            "1. `addItem(product: { id: number, name: string, price: number }, qty: number = 1)`:\n"
            "   • Если товар уже есть в корзине — увеличивает его количество `qty`.\n"
            "   • Если товара нет — добавляет `{ ...product, quantity: qty }`.\n"
            "2. `updateQuantity(productId: number, qty: number)`:\n"
            "   • Если `qty <= 0` — удаляет товар из корзины.\n"
            "   • Иначе устанавливает количество `quantity = qty`.\n"
            "3. `removeItem(productId: number)`: удаляет товар.\n"
            "4. `applyPromo(code: string)`: если code === 'DEVFORGE10' — активирует скидку 10% (0.10).\n"
            "5. `getSummary() -> { items: array, subtotal: number, discount: number, total: number }`:\n"
            "   • subtotal — сумма всех товаров (price * quantity).\n"
            "   • discount — величина скидки (subtotal * discountRate, округленная до целого Math.round).\n"
            "   • total — subtotal - discount."
        ),
        "starterCode": (
            "class CartManager {\n"
            "  constructor() {\n"
            "    // Ваш код здесь\n"
            "  }\n"
            "  addItem(product, qty = 1) {}\n"
            "  updateQuantity(id, qty) {}\n"
            "  removeItem(id) {}\n"
            "  applyPromo(code) {}\n"
            "  getSummary() {}\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Добавление и пересчет корзины",
                "expression": (
                    "const cart = new CartManager();\n"
                    "cart.addItem({ id: 1, name: 'Клавиатура', price: 3000 }, 1);\n"
                    "cart.addItem({ id: 1, name: 'Клавиатура', price: 3000 }, 1);\n"
                    "cart.addItem({ id: 2, name: 'Мышь', price: 1500 }, 1);\n"
                    "const s = cart.getSummary();\n"
                    "[s.items.length, s.subtotal, s.total]"
                ),
                "expected": [2, 7500, 7500]
            },
            {
                "id": "t2",
                "label": "Применение промокода на 10%",
                "expression": (
                    "const cart = new CartManager();\n"
                    "cart.addItem({ id: 1, name: 'Монитор', price: 20000 }, 1);\n"
                    "cart.applyPromo('DEVFORGE10');\n"
                    "const s = cart.getSummary();\n"
                    "[s.subtotal, s.discount, s.total]"
                ),
                "expected": [20000, 2000, 18000]
            }
        ],
        "hints": [
            "Направление: храните список товаров this.items = [] и ставку скидки this.discountRate = 0.",
            "Подход: при addItem ищите товар через this.items.find(x => x.id === product.id).",
            "Детали: в updateQuantity фильтруйте массив через this.items.filter(...) если qty <= 0."
        ],
        "commonMistakes": (
            "Мутировать объект товара напрямую без проверки его существования."
        ),
        "solutionExplanation": (
            "Класс объединяет бизнес-логику управления покупками и вычисляет финансовые итоги."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["State Management", "useReducer", "useMemo", "Shopping Cart"],
        "walkthrough": [
            "Инициализируйте массив товаров и скидку",
            "Реализуйте добавление с проверкой дубликатов",
            "Реализуйте обновление количества и удаление",
            "Реализуйте расчет стоимости с учетом промокода"
        ],
        "prerequisites": ["javascript-arrays", "javascript-reduce"],
        "resources": [{"title": "React: useReducer", "url": "https://react.dev/reference/react/useReducer", "language": "javascript"}],
        "lifeExample": "Калькулятор чека в супермаркете: сканирует штрихкоды, суммирует количество и применяет скидочную карту.",
        "guide": make_guide(
            "Хуки React: корзина и вычисления",
            "Менеджер корзины и расчет чека со скидкой",
            (
                "class CartManager {\n"
                "  constructor() {\n"
                "    this.items = [];\n"
                "    this.discountRate = 0;\n"
                "  }\n"
                "  addItem(product, qty = 1) {\n"
                "    const existing = this.items.find(x => x.id === product.id);\n"
                "    if (existing) {\n"
                "      existing.quantity += qty;\n"
                "    } else {\n"
                "      this.items.push({ ...product, quantity: qty });\n"
                "    }\n"
                "  }\n"
                "  updateQuantity(id, qty) {\n"
                "    if (qty <= 0) {\n"
                "      this.removeItem(id);\n"
                "    } else {\n"
                "      const it = this.items.find(x => x.id === id);\n"
                "      if (it) it.quantity = qty;\n"
                "    }\n"
                "  }\n"
                "  removeItem(id) {\n"
                "    this.items = this.items.filter(x => x.id !== id);\n"
                "  }\n"
                "  applyPromo(code) {\n"
                "    if (code === 'DEVFORGE10') this.discountRate = 0.10;\n"
                "  }\n"
                "  getSummary() {\n"
                "    const subtotal = this.items.reduce((sum, it) => sum + it.price * it.quantity, 0);\n"
                "    const discount = Math.round(subtotal * this.discountRate);\n"
                "    return {\n"
                "      items: this.items.map(it => ({ ...it })),\n"
                "      subtotal,\n"
                "      discount,\n"
                "      total: subtotal - discount\n"
                "    };\n"
                "  }\n"
                "}\n"
            )
        )
    },
    {
        "id": "frontend-project-catalog-cart",
        "language": "javascript",
        "title": "Итоговый проект: Каталог товаров, фильтры и оформление заказа",
        "topic": "Комплексное Frontend-приложение: каталог, корзина, пагинация, оформление заказа",
        "section": "Frontend: Итоговый проект",
        "order": 25,
        "level": "Advanced",
        "minutes": 45,
        "theory": (
            "Итоговый проект объединяет весь стек Frontend-разработки:\n"
            "• Интерактивный каталог товаров с поиском по названию и фильтрацией по категории.\n"
            "• Сортировка по цене (по возрастанию / убыванию) и пагинация страниц.\n"
            "• Полноценная корзина с изменением количества и удалением позиций.\n"
            "• Оформление заказа с валидацией контактных данных и адреса доставки.\n"
            "• Формирование готового объекта заказа для отправки на backend."
        ),
        "syntax": (
            "class StoreApp {\n"
            "  filterCatalog(query, category, sortOrder, page, pageSize) { ... }\n"
            "  addToCart(productId, qty) { ... }\n"
            "  checkout(customerData) { ... }\n"
            "}"
        ),
        "examples": [
            (
                "const app = new StoreApp(mockProducts);\n"
                "const catalogView = app.filterCatalog('ноутбук', 'all', 'price-asc', 1, 10);\n"
                "app.addToCart(1, 1);\n"
                "const order = app.checkout({ name: 'Иван', email: 'ivan@test.ru', address: 'Москва' });"
            )
        ],
        "task": (
            "Реализуйте полноценный класс `StoreApplication`:\n"
            "Конструктор принимает массив товаров `initialProducts = [{ id, name, category, price, inStock }]`.\n\n"
            "Методы:\n"
            "1. `queryCatalog({ search = '', category = 'all', sort = 'none', page = 1, pageSize = 5 }) -> { items, totalCount, totalPages, currentPage }`:\n"
            "   • search: нечувствителен к регистру (поиск подстроки в name).\n"
            "   • category: если не 'all', фильтрует по точному совпадению.\n"
            "   • sort: 'asc' — по возрастанию цены, 'desc' — по убыванию цены.\n"
            "   • пагинация: возвращает срез товаров для страницы `page`.\n"
            "2. `addToCart(productId, qty = 1)`: добавляет товар в корзину (если товар существует и inStock === true).\n"
            "3. `getCartSummary()`: возвращает `{ items, totalQty, totalCost }`.\n"
            "4. `submitOrder(customer)`:\n"
            "   • если корзина пуста — бросает Error('Cart is empty').\n"
            "   • валидирует customer (name: длина >= 2, email: содержит '@' и '.', address: длина >= 5). При ошибке — бросает Error('Validation failed').\n"
            "   • очищает корзину и возвращает `{ orderId: number, status: 'confirmed', total: totalCost, customer }`."
        ),
        "starterCode": (
            "class StoreApplication {\n"
            "  constructor(initialProducts) {\n"
            "    // Ваш код здесь\n"
            "  }\n"
            "  queryCatalog(params) {}\n"
            "  addToCart(productId, qty = 1) {}\n"
            "  getCartSummary() {}\n"
            "  submitOrder(customer) {}\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Поиск и сортировка в каталоге",
                "expression": (
                    "const products = [\n"
                    "  { id: 1, name: 'Apple iPhone 15', category: 'phones', price: 80000, inStock: true },\n"
                    "  { id: 2, name: 'Samsung Galaxy S24', category: 'phones', price: 75000, inStock: true },\n"
                    "  { id: 3, name: 'USB-C Cable', category: 'accessories', price: 1000, inStock: true }\n"
                    "];\n"
                    "const store = new StoreApplication(products);\n"
                    "const res = store.queryCatalog({ category: 'phones', sort: 'asc' });\n"
                    "[res.items.length, res.items[0].name]"
                ),
                "expected": [2, "Samsung Galaxy S24"]
            },
            {
                "id": "t2",
                "label": "Оформление заказа и очистка корзины",
                "expression": (
                    "const products = [{ id: 1, name: 'Наушники', category: 'audio', price: 5000, inStock: true }];\n"
                    "const store = new StoreApplication(products);\n"
                    "store.addToCart(1, 2);\n"
                    "const order = store.submitOrder({ name: 'Ольга', email: 'olga@test.ru', address: 'г. Казань, ул. Мира' });\n"
                    "[order.status, order.total, store.getCartSummary().totalQty]"
                ),
                "expected": ["confirmed", 10000, 0]
            }
        ],
        "hints": [
            "Направление: храните this.products и this.cart = [].",
            "Подход: в queryCatalog применяйте .filter() по поиску и категории, затем .sort(), затем .slice() для пагинации.",
            "Детали: сгенерируйте orderId через Date.now() или внутренний счетчик."
        ],
        "commonMistakes": (
            "Добавлять в корзину товар с inStock: false или не очищать корзину после успешного submitOrder."
        ),
        "solutionExplanation": (
            "Итоговый проект охватывает ключевой поток пользователя e-commerce: поиск, отбор, добавление в корзину и заказ."
        ),
        "xp": 100,
        "setupSql": "",
        "concepts": ["Frontend Architecture", "React", "State Management", "Catalog & Cart"],
        "walkthrough": [
            "Реализуйте каталог с поиском, фильтром по категориям и сортировкой",
            "Реализуйте пагинацию страниц",
            "Реализуйте корзину и расчет сумм",
            "Реализуйте валидацию заказа и генерацию чека"
        ],
        "prerequisites": ["frontend-js-async-promises", "frontend-react-hooks-state", "frontend-react-hooks-advanced"],
        "resources": [{"title": "React Architecture Patterns", "url": "https://react.dev/learn", "language": "javascript"}],
        "lifeExample": "Сайт любого современного маркетплейса: Ozon, Wildberries или Яндекс Маркет.",
        "guide": make_guide(
            "Итоговый проект: Каталог и Корзина",
            "Комплексное клиентское приложение интернет-магазина",
            (
                "class StoreApplication {\n"
                "  constructor(initialProducts = []) {\n"
                "    this.products = [...initialProducts];\n"
                "    this.cart = [];\n"
                "    this.nextOrderId = 1001;\n"
                "  }\n"
                "  queryCatalog({ search = '', category = 'all', sort = 'none', page = 1, pageSize = 5 } = {}) {\n"
                "    let res = this.products.filter(p => {\n"
                "      const matchSearch = !search || p.name.toLowerCase().includes(search.toLowerCase());\n"
                "      const matchCat = category === 'all' || p.category === category;\n"
                "      return matchSearch && matchCat;\n"
                "    });\n"
                "    if (sort === 'asc') res.sort((a, b) => a.price - b.price);\n"
                "    else if (sort === 'desc') res.sort((a, b) => b.price - a.price);\n"
                "    const totalCount = res.length;\n"
                "    const totalPages = Math.ceil(totalCount / pageSize) || 1;\n"
                "    const start = (page - 1) * pageSize;\n"
                "    const items = res.slice(start, start + pageSize);\n"
                "    return { items, totalCount, totalPages, currentPage: page };\n"
                "  }\n"
                "  addToCart(productId, qty = 1) {\n"
                "    const prod = this.products.find(p => p.id === productId);\n"
                "    if (!prod || !prod.inStock) return false;\n"
                "    const existing = this.cart.find(it => it.id === productId);\n"
                "    if (existing) existing.quantity += qty;\n"
                "    else this.cart.push({ ...prod, quantity: qty });\n"
                "    return true;\n"
                "  }\n"
                "  getCartSummary() {\n"
                "    const totalQty = this.cart.reduce((sum, it) => sum + it.quantity, 0);\n"
                "    const totalCost = this.cart.reduce((sum, it) => sum + it.price * it.quantity, 0);\n"
                "    return { items: [...this.cart], totalQty, totalCost };\n"
                "  }\n"
                "  submitOrder(customer) {\n"
                "    if (this.cart.length === 0) throw new Error('Cart is empty');\n"
                "    if (!customer || !customer.name || customer.name.trim().length < 2) throw new Error('Validation failed');\n"
                "    if (!customer.email || !customer.email.includes('@') || !customer.email.includes('.')) throw new Error('Validation failed');\n"
                "    if (!customer.address || customer.address.trim().length < 5) throw new Error('Validation failed');\n"
                "    const total = this.getCartSummary().totalCost;\n"
                "    const orderId = this.nextOrderId++;\n"
                "    this.cart = [];\n"
                "    return { orderId, status: 'confirmed', total, customer };\n"
                "  }\n"
                "}\n"
            )
        )
    },
{
        "id": "frontend-ts-frontend-props",
        "language": "typescript",
        "title": "TypeScript для Frontend: типизация Props и событий",
        "topic": "Интерфейсы компонентов, Generics и типобезопасные ответы API",
        "section": "Frontend: TypeScript во фронтенде",
        "order": 19,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "TypeScript во frontend разработке предотвращает ошибки передачи неправильных свойств (props) "
            "между компонентами и гарантирует, что данные, полученные с сервера, строго соответствуют контракту.\n\n"
            "Ключевые приёмы:\n"
            "• Описание контракта интерфейса: interface ButtonProps { label: string; onClick: () => void; disabled?: boolean; }\n"
            "• Обобщения (Generics): функция или контейнер может работать с любым типом данных, сохраняя проверку типов.\n"
            "• Сужение типов (Type Narrowing) через дискриминантные объединения (Discriminated Unions)."
        ),
        "syntax": (
            "interface ApiResponse<T> {\n"
            "  status: 'success' | 'error';\n"
            "  data?: T;\n"
            "  error?: string;\n"
            "}\n\n"
            "function handleResponse<T>(res: ApiResponse<T>): T | null {\n"
            "  if (res.status === 'success' && res.data) return res.data;\n"
            "  return null;\n"
            "}"
        ),
        "examples": [
            (
                "interface Item { id: number; name: string; }\n"
                "function findItem<T extends { id: number }>(items: T[], id: number): T | undefined {\n"
                "  return items.find(it => it.id === id);\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте функцию `filterAndSort<T extends { id: number; title: string; price: number }>(items: T[], minPrice: number, ascending: boolean): T[]`\n"
            "Требования:\n"
            "1. Отфильтровать элементы, оставив только те, у которых `price >= minPrice`.\n"
            "2. Отсортировать отфильтрованные элементы по полю `price`:\n"
            "   • если `ascending === true` — по возрастанию цены;\n"
            "   • если `ascending === false` — по убыванию цены.\n"
            "3. Не мутировать исходный массив (возвращать новый массив)."
        ),
        "starterCode": (
            "interface ProductItem {\n"
            "  id: number;\n"
            "  title: string;\n"
            "  price: number;\n"
            "}\n\n"
            "function filterAndSort<T extends ProductItem>(items: T[], minPrice: number, ascending: boolean): T[] {\n"
            "  // Ваш код здесь\n"
            "  return [];\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Фильтрация по минимальной цене и сортировка по возрастанию",
                "expression": (
                    "const data = [\n"
                    "  { id: 1, title: 'Книга', price: 500 },\n"
                    "  { id: 2, title: 'Блокнот', price: 200 },\n"
                    "  { id: 3, title: 'Ручка', price: 800 }\n"
                    "];\n"
                    "const res = filterAndSort(data, 300, true);\n"
                    "[res.length, res[0].price, res[1].price]"
                ),
                "expected": [2, 500, 800]
            }
        ],
        "hints": [
            "Направление: `items.filter(x => x.price >= minPrice)`",
            "Подход: `result.sort((a, b) => ascending ? a.price - b.price : b.price - a.price)`",
            "Детали: используйте `[...items.filter(...)]` перед сортировкой, чтобы не менять исходный массив."
        ],
        "commonMistakes": (
            "Мутировать исходный массив через вызов `.sort()` прямо на переданном параметре `items`."
        ),
        "solutionExplanation": (
            "Использование Generics с ограничением `extends ProductItem` обеспечивает строгую типизацию и гибкость."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["TypeScript", "Generics", "Props", "Type Safety"],
        "walkthrough": [
            "Отфильтруйте массив по условию price >= minPrice",
            "Создайте копию для сортировки",
            "Отсортируйте по флагу ascending",
            "Верните результат"
        ],
        "prerequisites": ["typescript-generics-interface"],
        "resources": [{"title": "TypeScript Handbook: Generics", "url": "https://www.typescriptlang.org/docs/handbook/2/generics.html", "language": "typescript"}],
        "lifeExample": "Сортировка товаров в каталоге интернет-магазина по ползунку минимальной цены.",
        "guide": make_guide(
            "TypeScript для Frontend: типизация Props",
            "Generic-фильтры и сортировка данных",
            (
                "function filterAndSort<T extends { id: number; title: string; price: number }>(items: T[], minPrice: number, ascending: boolean): T[] {\n"
                "  return items\n"
                "    .filter(it => it.price >= minPrice)\n"
                "    .sort((a, b) => ascending ? a.price - b.price : b.price - a.price);\n"
                "}\n"
            )
        )
    },
    {
        "id": "frontend-network-fetch",
        "language": "javascript",
        "title": "Сетевые запросы: fetch, AbortController и ошибки",
        "topic": "Загрузка данных с сервера, отмена устаревших запросов и обработка статусов",
        "section": "Frontend: Сетевые запросы",
        "order": 26,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "При разработке интерфейсов данные загружаются с backend через глобальную функцию `fetch`. "
            "Качественный фронтенд обязан учитывать все состояния запроса:\n"
            "• `loading: true` — отображение скелетона или спиннера.\n"
            "• `error: string` — вывод понятного сообщения, если сервер вернул 4xx/5xx статус или пропал интернет.\n"
            "• `data: T` — отображение готового контента.\n\n"
            "При быстром вводе в поле поиска предыдущие запросы нужно отменять с помощью `AbortController`, "
            "чтобы не допустить состояния гонки (race condition)."
        ),
        "syntax": (
            "const controller = new AbortController();\n"
            "fetch('/api/search?q=phone', { signal: controller.signal })\n"
            "  .then(res => res.json())\n"
            "  .catch(err => {\n"
            "    if (err.name === 'AbortError') console.log('Запрос отменен');\n"
            "  });\n"
            "// Для отмены:\n"
            "controller.abort();"
        ),
        "examples": [
            (
                "async function safeFetch(url) {\n"
                "  const res = await fetch(url);\n"
                "  if (!res.ok) throw new Error(`HTTP ${res.status}`);\n"
                "  return await res.json();\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `AsyncDataLoader`:\n"
            "Конструктор принимает функцию `fetcherFn(param: string): Promise<any>`.\n"
            "Методы:\n"
            "1. `load(param: string): Promise<any>`:\n"
            "   • переводит состояние в `{ status: 'loading', data: null, error: null }`;\n"
            "   • вызывает `fetcherFn(param)`;\n"
            "   • при успехе: сохраняет `{ status: 'success', data: result, error: null }` и возвращает результат;\n"
            "   • при ошибке: сохраняет `{ status: 'error', data: null, error: err.message || String(err) }` и пробрасывает ошибку;\n"
            "2. `getState()`: возвращает текущий объект состояния."
        ),
        "starterCode": (
            "class AsyncDataLoader {\n"
            "  constructor(fetcherFn) {\n"
            "    // Ваш код здесь\n"
            "  }\n"
            "  async load(param) {}\n"
            "  getState() {}\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успешная загрузка данных",
                "expression": (
                    "const mock = async (p) => ({ greeting: `Hello, ${p}` });\n"
                    "const loader = new AsyncDataLoader(mock);\n"
                    "await loader.load('World');\n"
                    "loader.getState()"
                ),
                "expected": {"status": "success", "data": {"greeting": "Hello, World"}, "error": None}
            },
            {
                "id": "t2",
                "label": "Обработка сетевой ошибки",
                "expression": (
                    "const mock = async () => { throw new Error('Network timeout'); };\n"
                    "const loader = new AsyncDataLoader(mock);\n"
                    "try { await loader.load('test'); } catch (e) {}\n"
                    "loader.getState()"
                ),
                "expected": {"status": "error", "data": None, "error": "Network timeout"}
            }
        ],
        "hints": [
            "Направление: инициализируйте state = { status: 'idle', data: null, error: null }.",
            "Подход: в load(param) сначала установите status: 'loading', затем в try-catch вызовите await fetcherFn(param).",
            "Детали: верните результат из блока try, а в catch обновите ошибку и выполните throw err."
        ],
        "commonMistakes": (
            "Забыть пробросить ошибку наружу через throw в catch блоке."
        ),
        "solutionExplanation": (
            "Класс реализует паттерн машины состояний для асинхронных операций (idle -> loading -> success | error)."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["fetch", "Async", "State Machine", "Error Handling"],
        "walkthrough": [
            "Инициализируйте состояние загрузчика",
            "Обновите статус на loading перед сетевым вызовом",
            "При успехе запишите data и верните значение",
            "При сбое запишите error и пробросьте исключение"
        ],
        "prerequisites": ["frontend-js-async-promises"],
        "resources": [{"title": "MDN: Fetch API", "url": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API", "language": "javascript"}],
        "lifeExample": "Индикатор загрузки в банковском приложении: показывает крутящееся кольцо, а при сбое выводит понятную кнопку 'Повторить попытку'.",
        "guide": make_guide(
            "Сетевые запросы: fetch и состояния",
            "Управление жизненным циклом асинхронной загрузки",
            (
                "class AsyncDataLoader {\n"
                "  constructor(fetcherFn) {\n"
                "    this.fetcherFn = fetcherFn;\n"
                "    this.state = { status: 'idle', data: null, error: null };\n"
                "  }\n"
                "  async load(param) {\n"
                "    this.state = { status: 'loading', data: null, error: null };\n"
                "    try {\n"
                "      const result = await this.fetcherFn(param);\n"
                "      this.state = { status: 'success', data: result, error: null };\n"
                "      return result;\n"
                "    } catch (err) {\n"
                "      const msg = err.message || String(err);\n"
                "      this.state = { status: 'error', data: null, error: msg };\n"
                "      throw err;\n"
                "    }\n"
                "  }\n"
                "  getState() {\n"
                "    return { ...this.state };\n"
                "  }\n"
                "}\n"
            )
        )
    }
]



JAVA_LESSONS = [
{
        "id": "java-collections-list-map",
        "language": "java",
        "title": "Коллекции в Java: List, Set, Map и дженерики",
        "topic": "ArrayList, HashMap, HashSet и эффективный поиск данных",
        "section": "Java: Коллекции и Generics",
        "order": 19,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "Фреймворк коллекций Java (Java Collections Framework) предоставляет готовые структуры данных:\n"
            "• List (ArrayList, LinkedList) — упорядоченные списки с доступом по индексу.\n"
            "• Set (HashSet, TreeSet) — коллекции уникальных элементов без дубликатов.\n"
            "• Map (HashMap, TreeMap) — ассоциативные массивы пар 'ключ-значение'. "
            "Поиск по ключу в HashMap выполняется за константное время O(1).\n\n"
            "Дженерики (Generics, например List<String>, Map<Long, User>) гарантируют проверку типов на этапе компиляции."
        ),
        "syntax": (
            "import java.util.Map;\n"
            "import java.util.HashMap;\n"
            "import java.util.List;\n"
            "import java.util.ArrayList;\n\n"
            "Map<String, Integer> map = new HashMap<>();\n"
            "map.put(\"apple\", 10);\n"
            "int count = map.getOrDefault(\"apple\", 0);"
        ),
        "examples": [
            (
                "Map<String, Integer> counts = new HashMap<>();\n"
                "for (String word : words) {\n"
                "    counts.put(word, counts.getOrDefault(word, 0) + 1);\n"
                "}"
            )
        ],
        "task": (
            "Напишите класс `ProductCatalog` со следующими методами:\n"
            "1. `void addProduct(String category, String name, int price)` — добавляет товар в каталог.\n"
            "2. `int getProductCount(String category)` — возвращает количество товаров в указанной категории (или 0, если категория не найдена).\n"
            "3. `int getTotalPrice(String category)` — возвращает суммарную стоимость всех товаров в указанной категории.\n\n"
            "Проверьте работу в методе `main`."
        ),
        "starterCode": (
            "import java.util.*;\n\n"
            "public class Main {\n"
            "    public static class ProductCatalog {\n"
            "        // Объявите структуры данных\n"
            "        public void addProduct(String category, String name, int price) {}\n"
            "        public int getProductCount(String category) { return 0; }\n"
            "        public int getTotalPrice(String category) { return 0; }\n"
            "    }\n"
            "    public static void main(String[] args) {\n"
            "        ProductCatalog cat = new ProductCatalog();\n"
            "        cat.addProduct(\"food\", \"bread\", 50);\n"
            "        cat.addProduct(\"food\", \"cheese\", 250);\n"
            "        System.out.println(cat.getProductCount(\"food\"));\n"
            "        System.out.println(cat.getTotalPrice(\"food\"));\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Подсчет количества и суммы в категории",
                "expected": "2\n300"
            }
        ],
        "hints": [
            "Направление: используйте `Map<String, List<Integer>> pricesByCategory = new HashMap<>();`",
            "Подход: в addProduct делайте `pricesByCategory.computeIfAbsent(category, k -> new ArrayList<>()).add(price);`",
            "Детали: в getTotalPrice просуммируйте список цен для категории."
        ],
        "commonMistakes": (
            "Бросать NullPointerException при вызове getProductCount для несуществующей категории."
        ),
        "solutionExplanation": (
            "Использование HashMap со списками позволяет группировать данные по категории с мгновенным доступом."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Java Collections", "HashMap", "ArrayList", "Generics"],
        "walkthrough": [
            "Создайте мапу категорий и списков цен",
            "Реализуйте добавление цены в список нужной категории",
            "Реализуйте подсчет количества элементов",
            "Реализуйте подсчет суммарной стоимости"
        ],
        "prerequisites": ["java-classes", "java-methods"],
        "resources": [{"title": "Oracle Java: Collections", "url": "https://docs.oracle.com/javase/tutorial/collections/", "language": "java"}],
        "lifeExample": "Складской учет: товары группируются по отделам, и завскладом может мгновенно узнать общую стоимость отдела.",
        "guide": make_guide(
            "Java Collections: List и Map",
            "Группировка данных и подсчет сумм",
            (
                "import java.util.*;\n\n"
                "public class Main {\n"
                "    public static class ProductCatalog {\n"
                "        private Map<String, List<Integer>> items = new HashMap<>();\n"
                "        public void addProduct(String category, String name, int price) {\n"
                "            if (!items.containsKey(category)) {\n"
                "                items.put(category, new ArrayList<>());\n"
                "            }\n"
                "            items.get(category).add(price);\n"
                "        }\n"
                "        public int getProductCount(String category) {\n"
                "            return items.containsKey(category) ? items.get(category).size() : 0;\n"
                "        }\n"
                "        public int getTotalPrice(String category) {\n"
                "            if (!items.containsKey(category)) return 0;\n"
                "            int sum = 0;\n"
                "            for (int p : items.get(category)) sum += p;\n"
                "            return sum;\n"
                "        }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        ProductCatalog cat = new ProductCatalog();\n"
                "        cat.addProduct(\"food\", \"bread\", 50);\n"
                "        cat.addProduct(\"food\", \"cheese\", 250);\n"
                "        System.out.println(cat.getProductCount(\"food\"));\n"
                "        System.out.println(cat.getTotalPrice(\"food\"));\n"
                "    }\n"
                "}\n"
            )
        )
    },
    {
        "id": "java-stream-api",
        "language": "java",
        "title": "Java Stream API и функциональное программирование",
        "topic": "filter, map, sorted, collect и лямбда-выражения",
        "section": "Java: Stream API",
        "order": 20,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "Java Stream API (появившееся в Java 8) кардинально изменило работу с данными в Java, "
            "позволив писать декларативный код без громоздких циклов и промежуточных списков.\n\n"
            "Поток (Stream) обрабатывает элементы через цепочку операций:\n"
            "• Промежуточные (Intermediate): `filter()` (отбор), `map()` (преобразование), `sorted()` (сортировка).\n"
            "• Терминальные (Terminal): `collect()` (сбор в коллекцию), `count()`, `reduce()`, `findFirst()`. "
            "Пока не вызвана терминальная операция, поток не выполняет вычислений (ленивость)."
        ),
        "syntax": (
            "List<String> result = names.stream()\n"
            "    .filter(name -> name.startsWith(\"A\"))\n"
            "    .map(String::toUpperCase)\n"
            "    .sorted()\n"
            "    .collect(Collectors.toList());"
        ),
        "examples": [
            (
                "int sum = numbers.stream()\n"
                "    .filter(n -> n > 0)\n"
                "    .mapToInt(Integer::intValue)\n"
                "    .sum();"
            )
        ],
        "task": (
            "Напишите класс `TaskFilter` со статическим методом:\n"
            "`List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority)`\n"
            "Каждый объект `Task` имеет методы `getTitle()` (String) и `getPriority()` (int).\n\n"
            "Метод должен с помощью Stream API:\n"
            "1. Отфильтровать задачи, чей приоритет >= `minPriority`.\n"
            "2. Преобразовать каждую задачу в верхний регистр названия (`getTitle().toUpperCase()`).\n"
            "3. Отсортировать названия по алфавиту.\n"
            "4. Собрать и вернуть в виде `List<String>`.\n\n"
            "Выведите результат работы в консоль через разделитель запятая."
        ),
        "starterCode": (
            "import java.util.*;\n"
            "import java.util.stream.*;\n\n"
            "public class Main {\n"
            "    public static class Task {\n"
            "        private String title;\n"
            "        private int priority;\n"
            "        public Task(String title, int priority) { this.title = title; this.priority = priority; }\n"
            "        public String getTitle() { return title; }\n"
            "        public int getPriority() { return priority; }\n"
            "    }\n\n"
            "    public static List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority) {\n"
            "        // Stream API конвейер здесь\n"
            "        return null;\n"
            "    }\n\n"
            "    public static void main(String[] args) {\n"
            "        List<Task> list = Arrays.asList(\n"
            "            new Task(\"deploy\", 10),\n"
            "            new Task(\"refactor\", 3),\n"
            "            new Task(\"backup\", 8)\n"
            "        );\n"
            "        List<String> res = getUrgentTaskTitles(list, 5);\n"
            "        System.out.println(String.join(\", \", res));\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Фильтрация, регистр и сортировка задач",
                "expected": "BACKUP, DEPLOY"
            }
        ],
        "hints": [
            "Направление: `tasks.stream().filter(t -> t.getPriority() >= minPriority)...`",
            "Подход: вызовите `.map(t -> t.getTitle().toUpperCase()).sorted().collect(Collectors.toList())`.",
            "Детали: проверьте, что `Collectors` импортирован из `java.util.stream.Collectors`."
        ],
        "commonMistakes": (
            "Забыть вызвать `.sorted()` перед `.collect()`."
        ),
        "solutionExplanation": (
            "Стрим лаконично фильтрует задачи по приоритету, маппит в заглавные строки и сортирует."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["Stream API", "Lambdas", "filter", "map", "Collectors"],
        "walkthrough": [
            "Откройте стрим из списка tasks",
            "Примените filter по приоритету",
            "Примените map для извлечения названия в верхнем регистре",
            "Примените sorted() и соберите через collect(Collectors.toList())"
        ],
        "prerequisites": ["java-collections-list-map"],
        "resources": [{"title": "Oracle: Package java.util.stream", "url": "https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html", "language": "java"}],
        "lifeExample": "Конвейерная сортировочная лента посылок: сенсор отсекает лёгкие, сканер читает штрихкод, робот выстраивает по адресам.",
        "guide": make_guide(
            "Java Stream API",
            "Конвейерная обработка коллекций",
            (
                "import java.util.*;\n"
                "import java.util.stream.*;\n\n"
                "public class Main {\n"
                "    public static class Task {\n"
                "        private String title;\n"
                "        private int priority;\n"
                "        public Task(String title, int priority) { this.title = title; this.priority = priority; }\n"
                "        public String getTitle() { return title; }\n"
                "        public int getPriority() { return priority; }\n"
                "    }\n\n"
                "    public static List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority) {\n"
                "        return tasks.stream()\n"
                "            .filter(t -> t.getPriority() >= minPriority)\n"
                "            .map(t -> t.getTitle().toUpperCase())\n"
                "            .sorted()\n"
                "            .collect(Collectors.toList());\n"
                "    }\n\n"
                "    public static void main(String[] args) {\n"
                "        List<Task> list = Arrays.asList(\n"
                "            new Task(\"deploy\", 10),\n"
                "            new Task(\"refactor\", 3),\n"
                "            new Task(\"backup\", 8)\n"
                "        );\n"
                "        List<String> res = getUrgentTaskTitles(list, 5);\n"
                "        System.out.println(String.join(\", \", res));\n"
                "    }\n"
                "}\n"
            )
        )
    },
    {
        "id": "java-spring-boot-controller",
        "language": "java",
        "title": "Spring Boot: REST-контроллеры и Dependency Injection",
        "topic": "@RestController, @GetMapping, @PostMapping и архитектура слоёв",
        "section": "Java: Spring Boot Backend",
        "order": 21,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "Spring Boot — ведущий промышленный фреймворк для создания корпоративных web-приложений на Java. "
            "Архитектура Spring строится на трёх основных слоях:\n"
            "1. Controller (@RestController) — принимает HTTP-запросы, валидирует входные данные и возвращает ответы (обычно JSON).\n"
            "2. Service (@Service) — содержит бизнес-логику приложения.\n"
            "3. Repository (@Repository) — отвечает за сохранение и загрузку данных из БД.\n\n"
            "Внедрение зависимостей (Inversion of Control / DI) связывает компоненты автоматически через конструкторы."
        ),
        "syntax": (
            "@RestController\n"
            "@RequestMapping(\"/api/tasks\")\n"
            "public class TaskController {\n"
            "    private final TaskService taskService;\n"
            "    public TaskController(TaskService service) {\n"
            "        this.taskService = service;\n"
            "    }\n"
            "    @GetMapping\n"
            "    public List<Task> getAll() {\n"
            "        return taskService.findAll();\n"
            "    }\n"
            "}"
        ),
        "examples": [
            (
                "public class ApiResponse<T> {\n"
                "    public int status;\n"
                "    public T data;\n"
                "    public ApiResponse(int status, T data) {\n"
                "        this.status = status; this.data = data;\n"
                "    }\n"
                "}"
            )
        ],
        "task": (
            "Смоделируйте логику Spring REST-контроллера в классе `TaskApiController`:\n"
            "Конструктор принимает `TaskService service`.\n"
            "Методы контроллера:\n"
            "1. `ApiResponse handleGetById(long id)`: если задача найдена — возвращает `{ status: 200, data: task }`, если нет — `{ status: 404, error: \"Task not found\" }`.\n"
            "2. `ApiResponse handleCreate(String title, int priority)`: если title пустой или priority < 1 — возвращает `{ status: 400, error: \"Validation failed\" }`, иначе создает задачу и возвращает `{ status: 201, data: task }`.\n\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\n\n"
            "public class Main {\n"
            "    public static class Task {\n"
            "        public long id;\n"
            "        public String title;\n"
            "        public int priority;\n"
            "        public Task(long id, String title, int priority) {\n"
            "            this.id = id; this.title = title; this.priority = priority;\n"
            "        }\n"
            "    }\n"
            "    public static class ApiResponse {\n"
            "        public int status;\n"
            "        public Object data;\n"
            "        public String error;\n"
            "        public ApiResponse(int s, Object d, String e) { status = s; data = d; error = e; }\n"
            "    }\n"
            "    public static class TaskService {\n"
            "        private Map<Long, Task> db = new HashMap<>();\n"
            "        private long nextId = 1;\n"
            "        public Task findById(long id) { return db.get(id); }\n"
            "        public Task create(String title, int priority) {\n"
            "            Task t = new Task(nextId++, title, priority);\n"
            "            db.put(t.id, t);\n"
            "            return t;\n"
            "        }\n"
            "    }\n"
            "    public static class TaskApiController {\n"
            "        private TaskService service;\n"
            "        public TaskApiController(TaskService s) { this.service = s; }\n"
            "        public ApiResponse handleGetById(long id) { return null; }\n"
            "        public ApiResponse handleCreate(String title, int priority) { return null; }\n"
            "    }\n"
            "    public static void main(String[] args) {\n"
            "        TaskService s = new TaskService();\n"
            "        TaskApiController c = new TaskApiController(s);\n"
            "        ApiResponse r1 = c.handleCreate(\"Init DB\", 5);\n"
            "        ApiResponse r2 = c.handleGetById(999);\n"
            "        System.out.println(r1.status + \" \" + ((Task)r1.data).title);\n"
            "        System.out.println(r2.status + \" \" + r2.error);\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Статусы ответов 201 Created и 404 Not Found",
                "expected": "201 Init DB\n404 Task not found"
            }
        ],
        "hints": [
            "Направление: в handleGetById проверьте `Task t = service.findById(id); if (t == null) return new ApiResponse(404, null, \"Task not found\");`",
            "Подход: в handleCreate проверьте `if (title == null || title.trim().isEmpty() || priority < 1)`."
        ],
        "commonMistakes": (
            "Возвращать статус 200 вместо 201 при успешном создании ресурса по стандарту REST."
        ),
        "solutionExplanation": (
            "Контроллер изолирует обработку HTTP запросов от сервиса, валидирует ввод и формирует структурированные ответы."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["Spring Boot", "REST Controller", "Dependency Injection", "Validation"],
        "walkthrough": [
            "Сохраните service в конструкторе",
            "Реализуйте handleGetById с проверкой на null",
            "Реализуйте handleCreate с проверкой валидности полей"
        ],
        "prerequisites": ["java-stream-api"],
        "resources": [{"title": "Spring Boot Reference Documentation", "url": "https://docs.spring.io/spring-boot/docs/current/reference/html/", "language": "java"}],
        "lifeExample": "Служба обработки заказов в ресторане: официант (контроллер) принимает заказ и передает шеф-повару (сервису).",
        "guide": make_guide(
            "Spring Boot: REST-контроллеры",
            "Обработка эндпоинтов и статус-кодов",
            (
                "import java.util.*;\n\n"
                "public class Main {\n"
                "    public static class Task {\n"
                "        public long id;\n"
                "        public String title;\n"
                "        public int priority;\n"
                "        public Task(long id, String title, int priority) {\n"
                "            this.id = id; this.title = title; this.priority = priority;\n"
                "        }\n"
                "    }\n"
                "    public static class ApiResponse {\n"
                "        public int status;\n"
                "        public Object data;\n"
                "        public String error;\n"
                "        public ApiResponse(int s, Object d, String e) { status = s; data = d; error = e; }\n"
                "    }\n"
                "    public static class TaskService {\n"
                "        private Map<Long, Task> db = new HashMap<>();\n"
                "        private long nextId = 1;\n"
                "        public Task findById(long id) { return db.get(id); }\n"
                "        public Task create(String title, int priority) {\n"
                "            Task t = new Task(nextId++, title, priority);\n"
                "            db.put(t.id, t);\n"
                "            return t;\n"
                "        }\n"
                "    }\n"
                "    public static class TaskApiController {\n"
                "        private TaskService service;\n"
                "        public TaskApiController(TaskService s) { this.service = s; }\n"
                "        public ApiResponse handleGetById(long id) {\n"
                "            Task t = service.findById(id);\n"
                "            if (t == null) return new ApiResponse(404, null, \"Task not found\");\n"
                "            return new ApiResponse(200, t, null);\n"
                "        }\n"
                "        public ApiResponse handleCreate(String title, int priority) {\n"
                "            if (title == null || title.trim().isEmpty() || priority < 1) {\n"
                "                return new ApiResponse(400, null, \"Validation failed\");\n"
                "            }\n"
                "            Task t = service.create(title, priority);\n"
                "            return new ApiResponse(201, t, null);\n"
                "        }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        TaskService s = new TaskService();\n"
                "        TaskApiController c = new TaskApiController(s);\n"
                "        ApiResponse r1 = c.handleCreate(\"Init DB\", 5);\n"
                "        ApiResponse r2 = c.handleGetById(999);\n"
                "        System.out.println(r1.status + \" \" + ((Task)r1.data).title);\n"
                "        System.out.println(r2.status + \" \" + r2.error);\n"
                "    }\n"
                "}\n"
            )
        )
    },
    {
        "id": "java-project-enterprise-api",
        "language": "java",
        "title": "Итоговый проект: Enterprise REST API сервиса ресурсов",
        "topic": "Комплексный Spring Boot сервис: модели, валидация, пагинация, ошибки",
        "section": "Java: Итоговый проект",
        "order": 22,
        "level": "Advanced",
        "minutes": 45,
        "theory": (
            "Итоговый проект направления Java Development моделирует работу промышленного Enterprise API:\n"
            "• Управление ресурсами и задачами с уникальными идентификаторами.\n"
            "• Строгая валидация входящих данных (@Valid, минимальная длина, статус).\n"
            "• Фильтрация по статусу (NEW, IN_PROGRESS, COMPLETED) и поиск по подстроке.\n"
            "• Пагинация выдачи (page, size) для эффективной работы с большими объёмами данных.\n"
            "• Единообразная обработка ошибок (400 Bad Request, 404 Not Found)."
        ),
        "syntax": (
            "public class EnterpriseTaskManager {\n"
            "    public Task create(TaskCreateDto dto) { ... }\n"
            "    public Task updateStatus(long id, String newStatus) { ... }\n"
            "    public PageResult<Task> search(String query, String status, int page, int size) { ... }\n"
            "}"
        ),
        "examples": [
            (
                "EnterpriseTaskManager manager = new EnterpriseTaskManager();\n"
                "Task task = manager.create(\"Database Migration\", \"Backend\", 10);\n"
                "manager.updateStatus(task.id, \"IN_PROGRESS\");"
            )
        ],
        "task": (
            "Реализуйте полноценный класс `EnterpriseTaskManager`:\n"
            "Класс `Task` имеет поля: `long id`, `String title`, `String status` (по умолчанию \"NEW\"), `int priority`.\n\n"
            "Методы менеджера:\n"
            "1. `Task createTask(String title, int priority)`:\n"
            "   • Если title == null или длина < 3, или priority < 1 — бросает `IllegalArgumentException(\"Invalid task data\")`.\n"
            "   • Генерирует автоинкрементный id и сохраняет задачу со статусом \"NEW\".\n"
            "2. `Task updateStatus(long id, String newStatus)`:\n"
            "   • Если задача не найдена — бросает `NoSuchElementException(\"Task not found\")`.\n"
            "   • Допустимые статусы: \"NEW\", \"IN_PROGRESS\", \"COMPLETED\". При недопустимом статусе — `IllegalArgumentException`.\n"
            "3. `List<Task> searchTasks(String status, int page, int pageSize)`:\n"
            "   • Фильтрует по статусу (если status равен null или \"ALL\" — возвращает задачи с любым статусом).\n"
            "   • Применяет пагинацию: пропускает (page - 1) * pageSize и берет pageSize элементов.\n\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\n\n"
            "public class Main {\n"
            "    public static class Task {\n"
            "        public long id;\n"
            "        public String title;\n"
            "        public String status;\n"
            "        public int priority;\n"
            "        public Task(long id, String title, int priority) {\n"
            "            this.id = id; this.title = title; this.priority = priority; this.status = \"NEW\";\n"
            "        }\n"
            "    }\n"
            "    public static class EnterpriseTaskManager {\n"
            "        // Реализация здесь\n"
            "    }\n"
            "    public static void main(String[] args) {\n"
            "        EnterpriseTaskManager m = new EnterpriseTaskManager();\n"
            "        Task t1 = m.createTask(\"Setup CI/CD\", 5);\n"
            "        Task t2 = m.createTask(\"Security Audit\", 10);\n"
            "        m.updateStatus(t1.id, \"IN_PROGRESS\");\n"
            "        List<Task> res = m.searchTasks(\"IN_PROGRESS\", 1, 10);\n"
            "        System.out.println(res.size() + \" \" + res.get(0).title + \" \" + res.get(0).status);\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Создание, обновление статуса и поиск с фильтрацией",
                "expected": "1 Setup CI/CD IN_PROGRESS"
            }
        ],
        "hints": [
            "Направление: храните `Map<Long, Task> tasks = new LinkedHashMap<>();`",
            "Подход: в searchTasks отфильтруйте задачи через stream: `.filter(t -> status == null || \"ALL\".equals(status) || t.status.equals(status))`",
            "Детали: используйте `.skip((long)(page - 1) * pageSize).limit(pageSize).collect(Collectors.toList())`."
        ],
        "commonMistakes": (
            "Не проверять допустимость статуса при updateStatus (разрешены только NEW, IN_PROGRESS, COMPLETED)."
        ),
        "solutionExplanation": (
            "Итоговый проект на Java демонстрирует архитектуру корпоративного сервиса с валидацией, пагинацией и проверкой целостности."
        ),
        "xp": 100,
        "setupSql": "",
        "concepts": ["Enterprise Java", "Spring Boot", "REST API", "Pagination", "Validation"],
        "walkthrough": [
            "Создайте класс Task и коллекцию хранения",
            "Реализуйте createTask с валидацией",
            "Реализуйте updateStatus с проверкой допустимых значений",
            "Реализуйте searchTasks с фильтрацией и пагинацией"
        ],
        "prerequisites": ["java-spring-boot-controller", "java-stream-api"],
        "resources": [{"title": "Spring Data JPA Repository", "url": "https://spring.io/projects/spring-data-jpa", "language": "java"}],
        "lifeExample": "Корпоративная система управления проектами (Jira, Asana, Kaiten): трекинг задач, спринтов и релизов.",
        "guide": make_guide(
            "Итоговый проект: Enterprise REST API",
            "Комплексный сервис управления задачами и ресурсами",
            (
                "import java.util.*;\n"
                "import java.util.stream.*;\n\n"
                "public class Main {\n"
                "    public static class Task {\n"
                "        public long id;\n"
                "        public String title;\n"
                "        public String status;\n"
                "        public int priority;\n"
                "        public Task(long id, String title, int priority) {\n"
                "            this.id = id; this.title = title; this.priority = priority; this.status = \"NEW\";\n"
                "        }\n"
                "    }\n"
                "    public static class EnterpriseTaskManager {\n"
                "        private Map<Long, Task> db = new LinkedHashMap<>();\n"
                "        private long nextId = 1;\n"
                "        private Set<String> validStatuses = new HashSet<>(Arrays.asList(\"NEW\", \"IN_PROGRESS\", \"COMPLETED\"));\n\n"
                "        public Task createTask(String title, int priority) {\n"
                "            if (title == null || title.trim().length() < 3 || priority < 1) {\n"
                "                throw new IllegalArgumentException(\"Invalid task data\");\n"
                "            }\n"
                "            Task t = new Task(nextId++, title, priority);\n"
                "            db.put(t.id, t);\n"
                "            return t;\n"
                "        }\n\n"
                "        public Task updateStatus(long id, String newStatus) {\n"
                "            if (!db.containsKey(id)) throw new NoSuchElementException(\"Task not found\");\n"
                "            if (!validStatuses.contains(newStatus)) throw new IllegalArgumentException(\"Invalid status\");\n"
                "            Task t = db.get(id);\n"
                "            t.status = newStatus;\n"
                "            return t;\n"
                "        }\n\n"
                "        public List<Task> searchTasks(String status, int page, int pageSize) {\n"
                "            return db.values().stream()\n"
                "                .filter(t -> status == null || \"ALL\".equals(status) || t.status.equals(status))\n"
                "                .skip((long)(page - 1) * pageSize)\n"
                "                .limit(pageSize)\n"
                "                .collect(Collectors.toList());\n"
                "        }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        EnterpriseTaskManager m = new EnterpriseTaskManager();\n"
                "        Task t1 = m.createTask(\"Setup CI/CD\", 5);\n"
                "        Task t2 = m.createTask(\"Security Audit\", 10);\n"
                "        m.updateStatus(t1.id, \"IN_PROGRESS\");\n"
                "        List<Task> res = m.searchTasks(\"IN_PROGRESS\", 1, 10);\n"
                "        System.out.println(res.size() + \" \" + res.get(0).title + \" \" + res.get(0).status);\n"
                "    }\n"
                "}\n"
            )
        )
    },
{
        "id": "java-exceptions-try-resources",
        "language": "java",
        "title": "Исключения в Java: try-with-resources и кастомные типы",
        "topic": "Иерархия Throwable, Checked vs Unchecked, AutoCloseable",
        "section": "Java: Надежность и исключения",
        "order": 23,
        "level": "Intermediate",
        "minutes": 30,
        "theory": (
            "Обработка ошибок в Java строится на классах исключений (Exceptions):\n"
            "• Checked (проверяемые, наследники Exception) — компилятор требует явно обработать через try-catch "
            "или объявить в сигнатуре метода через throws (например IOException, SQLException).\n"
            "• Unchecked (непроверяемые, наследники RuntimeException) — ошибки логики программы (NullPointerException, IllegalArgumentException).\n\n"
            "Конструкция `try-with-resources` гарантирует автоматическое закрытие ресурсов (файлы, сетевые сокеты, соединения с БД), "
            "реализующих интерфейс `AutoCloseable`, даже если внутри блока возникла критическая ошибка."
        ),
        "syntax": (
            "public class InsufficientFundsException extends Exception {\n"
            "    public InsufficientFundsException(String msg) { super(msg); }\n"
            "}\n\n"
            "try (Connection conn = dataSource.getConnection()) {\n"
            "    // ресурс conn закроется автоматически при выходе из блока\n"
            "}"
        ),
        "examples": [
            (
                "public void validateAge(int age) {\n"
                "    if (age < 18) throw new IllegalArgumentException(\"Too young\");\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `SafeBankVault` со следующими возможностями:\n"
            "1. Создайте проверяемое исключение `public static class OverdraftException extends Exception`.\n"
            "2. В классе `SafeBankVault` реализуйте приватное поле `int balanceCents`. Конструктор принимает начальный баланс.\n"
            "3. Метод `void withdraw(int amount) throws OverdraftException`:\n"
            "   • если `amount <= 0` — бросает `IllegalArgumentException(\"Amount must be positive\")`;\n"
            "   • если `balanceCents < amount` — бросает `OverdraftException(\"Not enough balance\")`;\n"
            "   • иначе уменьшает баланс на `amount`.\n"
            "4. Метод `int getBalance()`: возвращает текущий баланс.\n\n"
            "Проверьте работу в `main`, перехватив `OverdraftException` и выведя сообщение ошибки."
        ),
        "starterCode": (
            "public class Main {\n"
            "    public static class OverdraftException extends Exception {\n"
            "        public OverdraftException(String msg) { super(msg); }\n"
            "    }\n"
            "    public static class SafeBankVault {\n"
            "        private int balanceCents;\n"
            "        public SafeBankVault(int initial) { this.balanceCents = initial; }\n"
            "        public void withdraw(int amount) throws OverdraftException {\n"
            "            // реализация\n"
            "        }\n"
            "        public int getBalance() { return balanceCents; }\n"
            "    }\n"
            "    public static void main(String[] args) {\n"
            "        SafeBankVault vault = new SafeBankVault(500);\n"
            "        try {\n"
            "            vault.withdraw(300);\n"
            "            vault.withdraw(400); // вызовет OverdraftException\n"
            "        } catch (OverdraftException e) {\n"
            "            System.out.println(e.getMessage());\n"
            "        }\n"
            "        System.out.println(vault.getBalance());\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Перехват OverdraftException и сохранение баланса",
                "expected": "Not enough balance\n200"
            }
        ],
        "hints": [
            "Направление: проверьте amount <= 0 в первую очередь.",
            "Подход: проверьте balanceCents < amount перед списанием.",
            "Детали: убедитесь, что withdraw объявлен с `throws OverdraftException`."
        ],
        "commonMistakes": (
            "Уменьшить баланс ДО проверки, из-за чего при ошибке баланс станет отрицательным."
        ),
        "solutionExplanation": (
            "Кастомное проверяемое исключение четко информирует вызывающий код о бизнес-ошибке списания."
        ),
        "xp": 35,
        "setupSql": "",
        "concepts": ["Java Exceptions", "try-catch", "Checked Exceptions", "AutoCloseable"],
        "walkthrough": [
            "Объявите класс исключения OverdraftException",
            "Реализуйте метод withdraw с проверкой условий",
            "Перехватите исключение в main и выведите сообщение"
        ],
        "prerequisites": ["java-classes", "java-methods"],
        "resources": [{"title": "Oracle: Exceptions", "url": "https://docs.oracle.com/javase/tutorial/essential/exceptions/", "language": "java"}],
        "lifeExample": "Банкомат: если клиент пытается снять больше денег, чем есть на карте, банкомат отклоняет операцию и возвращает карту.",
        "guide": make_guide(
            "Исключения в Java",
            "Кастомные исключения и защита целостности данных",
            (
                "public class Main {\n"
                "    public static class OverdraftException extends Exception {\n"
                "        public OverdraftException(String msg) { super(msg); }\n"
                "    }\n"
                "    public static class SafeBankVault {\n"
                "        private int balanceCents;\n"
                "        public SafeBankVault(int initial) { this.balanceCents = initial; }\n"
                "        public void withdraw(int amount) throws OverdraftException {\n"
                "            if (amount <= 0) throw new IllegalArgumentException(\"Amount must be positive\");\n"
                "            if (balanceCents < amount) throw new OverdraftException(\"Not enough balance\");\n"
                "            balanceCents -= amount;\n"
                "        }\n"
                "        public int getBalance() { return balanceCents; }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        SafeBankVault vault = new SafeBankVault(500);\n"
                "        try {\n"
                "            vault.withdraw(300);\n"
                "            vault.withdraw(400);\n"
                "        } catch (OverdraftException e) {\n"
                "            System.out.println(e.getMessage());\n"
                "        }\n"
                "        System.out.println(vault.getBalance());\n"
                "    }\n"
                "}\n"
            )
        )
    },
    {
        "id": "java-spring-data-jpa",
        "language": "java",
        "title": "Spring Data JPA: сущности @Entity и JpaRepository",
        "topic": "Объектно-реляционное отображение в Java, @Id, @Table и автогенерация запросов",
        "section": "Java: Базы данных и ORM",
        "order": 24,
        "level": "Advanced",
        "minutes": 35,
        "theory": (
            "Spring Data JPA упрощает работу с базами данных до минимума: разработчик описывает сущность (@Entity) "
            "и объявляет интерфейс репозитория, наследующий `JpaRepository<Entity, IdType>`. "
            "Spring автоматически генерирует реализации всех стандартных CRUD-методов (save, findById, findAll, delete), "
            "а также позволяет объявлять методы по соглашению об именах (например `findByEmail(String email)`)."
        ),
        "syntax": (
            "@Entity\n"
            "@Table(name = \"users\")\n"
            "public class User {\n"
            "    @Id\n"
            "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
            "    private Long id;\n"
            "    private String email;\n"
            "}\n\n"
            "public interface UserRepository extends JpaRepository<User, Long> {\n"
            "    Optional<User> findByEmail(String email);\n"
            "}"
        ),
        "examples": [
            (
                "public interface TaskRepository {\n"
                "    List<Task> findByStatusOrderByPriorityDesc(String status);\n"
                "}"
            )
        ],
        "task": (
            "Смоделируйте сущность и репозиторий в классе `TaskRepositoryModel`:\n"
            "Класс `Task` имеет поля: `Long id`, `String name`, `String category`, `int priority`.\n"
            "Класс `TaskRepositoryModel` должен поддерживать методы:\n"
            "1. `Task save(Task task)`: если id равен null или 0 — присваивает автоинкрементный id и сохраняет задачу; если id уже есть — обновляет задачу. Возвращает сохраненный объект.\n"
            "2. `Task findById(Long id)`: возвращает задачу или null.\n"
            "3. `List<Task> findByCategory(String category)`: возвращает все задачи указанной категории.\n"
            "4. `long count()`: возвращает общее количество сохраненных задач.\n\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\n\n"
            "public class Main {\n"
            "    public static class Task {\n"
            "        public Long id;\n"
            "        public String name;\n"
            "        public String category;\n"
            "        public int priority;\n"
            "        public Task(Long id, String name, String category, int priority) {\n"
            "            this.id = id; this.name = name; this.category = category; this.priority = priority;\n"
            "        }\n"
            "    }\n"
            "    public static class TaskRepositoryModel {\n"
            "        // реализация хранилища\n"
            "    }\n"
            "    public static void main(String[] args) {\n"
            "        TaskRepositoryModel repo = new TaskRepositoryModel();\n"
            "        Task t1 = repo.save(new Task(null, \"Setup PostgreSQL\", \"database\", 10));\n"
            "        Task t2 = repo.save(new Task(null, \"Write Liquibase\", \"database\", 8));\n"
            "        List<Task> dbTasks = repo.findByCategory(\"database\");\n"
            "        System.out.println(repo.count() + \" \" + dbTasks.size() + \" \" + t1.id);\n"
            "    }\n"
            "}\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Автоинкремент первичного ключа и фильтрация по категории",
                "expected": "2 2 1"
            }
        ],
        "hints": [
            "Направление: используйте `Map<Long, Task> store = new LinkedHashMap<>();`",
            "Подход: в save проверяйте `if (task.id == null || task.id == 0) task.id = nextId++;`",
            "Детали: в findByCategory профильтруйте задачи через stream или цикл."
        ],
        "commonMistakes": (
            "Не присваивать сгенерированный id задаче при сохранении новой сущности."
        ),
        "solutionExplanation": (
            "Модель воспроизводит поведение Spring Data JPA с генерацией ключей и запросами по полям."
        ),
        "xp": 40,
        "setupSql": "",
        "concepts": ["Spring Data JPA", "ORM", "Entity", "Repository Pattern"],
        "walkthrough": [
            "Создайте класс Task с атрибутами сущности",
            "Реализуйте метод save с генерацией ID",
            "Реализуйте выборку findByCategory",
            "Реализуйте метод count()"
        ],
        "prerequisites": ["java-spring-boot-controller"],
        "resources": [{"title": "Spring Data JPA Documentation", "url": "https://spring.io/projects/spring-data-jpa", "language": "java"}],
        "lifeExample": "Система учета пациентов в больнице: карточка пациента сохраняется в реляционную таблицу, а поиск по СНИЛС или отделению происходит мгновенно.",
        "guide": make_guide(
            "Spring Data JPA: ORM и репозитории",
            "Моделирование сущностей и CRUD операций",
            (
                "import java.util.*;\n"
                "import java.util.stream.*;\n\n"
                "public class Main {\n"
                "    public static class Task {\n"
                "        public Long id;\n"
                "        public String name;\n"
                "        public String category;\n"
                "        public int priority;\n"
                "        public Task(Long id, String name, String category, int priority) {\n"
                "            this.id = id; this.name = name; this.category = category; this.priority = priority;\n"
                "        }\n"
                "    }\n"
                "    public static class TaskRepositoryModel {\n"
                "        private Map<Long, Task> store = new LinkedHashMap<>();\n"
                "        private long nextId = 1;\n"
                "        public Task save(Task t) {\n"
                "            if (t.id == null || t.id == 0) {\n"
                "                t.id = nextId++;\n"
                "            }\n"
                "            store.put(t.id, t);\n"
                "            return t;\n"
                "        }\n"
                "        public Task findById(Long id) { return store.get(id); }\n"
                "        public List<Task> findByCategory(String cat) {\n"
                "            return store.values().stream()\n"
                "                .filter(x -> Objects.equals(x.category, cat))\n"
                "                .collect(Collectors.toList());\n"
                "        }\n"
                "        public long count() { return store.size(); }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        TaskRepositoryModel repo = new TaskRepositoryModel();\n"
                "        Task t1 = repo.save(new Task(null, \"Setup PostgreSQL\", \"database\", 10));\n"
                "        Task t2 = repo.save(new Task(null, \"Write Liquibase\", \"database\", 8));\n"
                "        List<Task> dbTasks = repo.findByCategory(\"database\");\n"
                "        System.out.println(repo.count() + \" \" + dbTasks.size() + \" \" + t1.id);\n"
                "    }\n"
                "}\n"
            )
        )
    }
]


print(f"Loaded {len(BACKEND_LESSONS)} backend lessons, {len(FRONTEND_LESSONS)} frontend lessons, {len(JAVA_LESSONS)} java lessons.")
