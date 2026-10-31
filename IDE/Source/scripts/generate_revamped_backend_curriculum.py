"""Generate comprehensive, crystal-clear, pedagogical Backend Development curriculum for DevForge 0.5.0."""
import json
from pathlib import Path

BACKEND_LESSONS = [
    # -----------------------------------------------------------------
    # Модуль 1. Архитектура бэкенда и основы HTTP
    # -----------------------------------------------------------------
    {
        "id": "backend-intro-client-server",
        "title": "Что такое Бэкенд и Архитектура Клиент-Сервер",
        "order": 57,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 35,
        "theory": (
            "Веб-приложения работают по модели «Клиент-Сервер» (Client-Server). "
            "Клиент (браузер, мобильное приложение) — это фасад программы, который отображает кнопки, формы и текст. "
            "Бэкенд (Backend, сервер) — это невидимый мозг системы, который работает на удалённом компьютере. "
            "Сервер выполняет три главные задачи:\n"
            "1. Обрабатывает бизнес-логику (проверяет пароли, рассчитывает скидки, списывает деньги).\n"
            "2. Безопасно взаимодействует с базой данных (хранит пользователей, заказы, сообщения).\n"
            "3. Формирует стандартизированный ответ клиенту в формате JSON.\n\n"
            "Общение между клиентом и сервером происходит по сетевому протоколу HTTP через запросы (Request) и ответы (Response). "
            "Любой ответ качественного бэкенда стандартизируется: в нём возвращаются статус выполнения, полезные данные (payload) и информационное сообщение."
        ),
        "lifeExample": (
            "Представьте ресторан. Вы (клиент) сидите за столиком и не заходите на кухню. "
            "Официант принимает ваш заказ и относит его повару (серверу). "
            "Повар готовит блюдо, используя продукты из холодильника (база данных), и официант приносит вам готовый заказ. "
            "Бэкенд — это шеф-повар и кухня, куда клиенту нет прямого доступа ради безопасности."
        ),
        "task": (
            "Реализуйте базовую функцию формирования стандартного ответа API:\n"
            "`format_api_response(status_code: int, data: dict, message: str = 'OK') -> dict`.\n\n"
            "Функция должна возвращать словарь следующего вида:\n"
            "{\n"
            "    'status': status_code,\n"
            "    'success': True если 200 <= status_code < 300 иначе False,\n"
            "    'message': message,\n"
            "    'data': data\n"
            "}"
        ),
        "starterCode": (
            "def format_api_response(status_code: int, data: dict, message: str = 'OK') -> dict:\n"
            "    # Ваше решение здесь\n"
            "    pass\n"
        ),
        "solutionCode": (
            "def format_api_response(status_code: int, data: dict, message: str = 'OK') -> dict:\n"
            "    success = 200 <= status_code < 300\n"
            "    return {\n"
            "        'status': status_code,\n"
            "        'success': success,\n"
            "        'message': message,\n"
            "        'data': data\n"
            "    }\n"
        ),
        "solutionExplanation": (
            "Мы проверяем диапазон кодов успешности (200-299) и упаковываем результат в единый контракт ответа, "
            "который легко разбирать на фронтенде."
        ),
        "hints": [
            "Успешные HTTP-коды лежат в диапазоне от 200 до 299 включительно.",
            "Используйте выражение `200 <= status_code < 300` для булевой переменной success.",
            "Сформируйте и верните итоговый словарь с четырьмя ключами: status, success, message, data."
        ],
        "commonMistakes": [
            "Считать успешными только код 200 (код 201 Created также является успешным).",
            "Забыть вернуть словарь через return."
        ],
        "guide": {
            "walkthrough": [
                "Определяем флаг success: 200 <= status_code < 300.",
                "Собираем словарь со структурой контракта ответа.",
                "Возвращаем сформированный словарь."
            ],
            "terms": [
                {"name": "Client-Server", "desc": "Архитектура разделения интерфейса клиента и логики сервера."},
                {"name": "Backend", "desc": "Серверная часть приложения, отвечающая за данные и безопасность."},
                {"name": "Payload", "desc": "Полезная нагрузка или основные данные ответа."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешный ответ 200 OK",
                "expression": "format_api_response(200, {'id': 1, 'name': 'Alice'})['success']",
                "expected": True
            },
            {
                "id": "t2",
                "label": "Ошибка клиента 404 Not Found",
                "expression": "format_api_response(404, {}, 'Ресурс не найден')['success']",
                "expected": False
            },
            {
                "id": "t3",
                "label": "Проверка структуры словаря",
                "expression": "format_api_response(201, {'created': True})['status']",
                "expected": 201
            }
        ]
    },

    {
        "id": "backend-http-methods-status",
        "title": "Анатомия HTTP: Методы и Коды ответов",
        "order": 58,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 35,
        "theory": (
            "Протокол HTTP — фундамент веба. Каждый запрос клиента содержит HTTP-метод (глагол действия):\n"
            "• GET — получить данные (безопасный метод, не должен изменять состояние на сервере).\n"
            "• POST — создать новую запись (отправляет данные в теле запроса).\n"
            "• PUT / PATCH — обновить существующую запись (PUT перезаписывает целиком, PATCH обновляет часть полей).\n"
            "• DELETE — удалить запись.\n\n"
            "Сервер отвечает трехзначным статус-кодом:\n"
            "• 2xx (Успех): 200 OK (данные получены/изменены), 201 Created (новая запись создана).\n"
            "• 4xx (Ошибка клиента): 400 Bad Request (неверные данные), 401 Unauthorized (нет токена), 403 Forbidden (нет прав), 404 Not Found (не найдено).\n"
            "• 5xx (Ошибка сервера): 500 Internal Server Error (сервер упал из-за ошибки в коде)."
        ),
        "lifeExample": (
            "Представьте почтовое отделение. Метод — это тип бланка: «Получить посылку» (GET), «Отправить новую» (POST), «Забрать на утилизацию» (DELETE). "
            "Статус-код — это штамп почтальона: «Выдано успешно» (200), «Посылка собрана и зарегистрирована» (201), «Неверный адрес получателя» (400), «Посылка не найдена на складе» (404)."
        ),
        "task": (
            "Реализуйте функцию классификации HTTP-статуса:\n"
            "`describe_http_status(status_code: int) -> dict`.\n\n"
            "Функция должна определять категорию статуса и текстовое описание:\n"
            "1. 200..299 -> category: 'success', text: 'OK' (для 200) или 'Created' (для 201) или 'Success' (для остальных 2xx).\n"
            "2. 400..499 -> category: 'client_error', text: 'Bad Request' (для 400), 'Unauthorized' (для 401), 'Forbidden' (для 403), 'Not Found' (для 404) или 'Client Error'.\n"
            "3. 500..599 -> category: 'server_error', text: 'Internal Server Error' (для 500) или 'Server Error'.\n"
            "Возвращайте словарь `{'code': status_code, 'category': category, 'text': text}`."
        ),
        "starterCode": (
            "def describe_http_status(status_code: int) -> dict:\n"
            "    # Ваше решение здесь\n"
            "    pass\n"
        ),
        "solutionCode": (
            "def describe_http_status(status_code: int) -> dict:\n"
            "    known = {\n"
            "        200: ('success', 'OK'),\n"
            "        201: ('success', 'Created'),\n"
            "        400: ('client_error', 'Bad Request'),\n"
            "        401: ('client_error', 'Unauthorized'),\n"
            "        403: ('client_error', 'Forbidden'),\n"
            "        404: ('client_error', 'Not Found'),\n"
            "        500: ('server_error', 'Internal Server Error')\n"
            "    }\n"
            "    if status_code in known:\n"
            "        cat, txt = known[status_code]\n"
            "    elif 200 <= status_code < 300:\n"
            "        cat, txt = 'success', 'Success'\n"
            "    elif 400 <= status_code < 500:\n"
            "        cat, txt = 'client_error', 'Client Error'\n"
            "    else:\n"
            "        cat, txt = 'server_error', 'Server Error'\n"
            "    return {'code': status_code, 'category': cat, 'text': txt}\n"
        ),
        "solutionExplanation": (
            "Мы используем словарь точных соответствий для стандартных кодов и диапазоны для обобщенных статусов."
        ),
        "hints": [
            "Создайте словарь `known` с наиболее частыми статус-кодами (200, 201, 400, 401, 403, 404, 500).",
            "Для остальных кодов проверьте диапазон: 200-299 (success), 400-499 (client_error), 500-599 (server_error).",
            "Верните словарь с ключами 'code', 'category' и 'text'."
        ],
        "commonMistakes": [
            "Путать клиентские ошибки 4xx (виноват клиент, передал плохие данные) с серверными 5xx (баг на сервере)."
        ],
        "guide": {
            "walkthrough": [
                "Проверяем код по словарю известных кодов.",
                "Если кода нет в словаре, определяем диапазон сотен.",
                "Формируем итоговый словарь."
            ],
            "terms": [
                {"name": "HTTP Method", "desc": "Глагол, указывающий требуемое действие над ресурсом (GET, POST и т.д.)."},
                {"name": "Status Code", "desc": "Трехзначный цифровой код результата обработки запроса сервером."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Проверка кода 201 Created",
                "expression": "describe_http_status(201)",
                "expected": {"code": 201, "category": "success", "text": "Created"}
            },
            {
                "id": "t2",
                "label": "Проверка ошибки 404 Not Found",
                "expression": "describe_http_status(404)",
                "expected": {"code": 404, "category": "client_error", "text": "Not Found"}
            },
            {
                "id": "t3",
                "label": "Проверка ошибки 500 Internal Server Error",
                "expression": "describe_http_status(500)['category']",
                "expected": "server_error"
            }
        ]
    },

    {
        "id": "backend-json-rest-api",
        "title": "Формат JSON и принципы RESTful API",
        "order": 59,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 35,
        "theory": (
            "REST (Representational State Transfer) — архитектурный стиль взаимодействия систем через интернет. "
            "Ключевые правила REST API:\n"
            "1. Ресурсы обозначаются существительными во множественном числе: `/users`, `/products`, `/orders`.\n"
            "2. Операции задаются HTTP-методом: `GET /products` (список), `POST /products` (создать), `GET /products/5` (получить товар №5), `DELETE /products/5` (удалить).\n"
            "3. Тело запроса и ответа передается в формате JSON (JavaScript Object Notation).\n\n"
            "В Python модуль `json` преобразует словари в JSON-строку (`json.dumps(obj)`) и обратно распаковывает JSON в словарь (`json.loads(text)`). "
            "В REST API сервер всегда парсит JSON из тела запроса и возвращает чистый структурированный JSON."
        ),
        "lifeExample": (
            "Представьте международный таможенный бланк декларации. Независимо от того, на каком языке говорит таможенник или путешественник, "
            "бланк заполняется по строгим международным полям латиницей. JSON — это такой же международный бланк данных, одинаково понятный любому языку программирования."
        ),
        "task": (
            "Реализуйте функцию сериализации и проверки REST-полезной нагрузки:\n"
            "`process_rest_payload(raw_json: str, required_fields: list[str]) -> tuple[bool, dict | str]`.\n\n"
            "1. Попробуйте распарсить `raw_json` с помощью `json.loads`.\n"
            "   Если строка содержит некорректный синтаксис JSON, верните `(False, 'Invalid JSON')`.\n"
            "2. Проверьте, присутствуют ли все поля из `required_fields` в полученном словаре.\n"
            "   Если какого-то поля не хватает, верните `(False, f'Missing required field: {missing_field}')`.\n"
            "3. Если всё в порядке, верните `(True, parsed_dict)`."
        ),
        "starterCode": (
            "import json\n\n"
            "def process_rest_payload(raw_json: str, required_fields: list[str]) -> tuple[bool, dict | str]:\n"
            "    # Ваше решение здесь\n"
            "    pass\n"
        ),
        "solutionCode": (
            "import json\n\n"
            "def process_rest_payload(raw_json: str, required_fields: list[str]) -> tuple[bool, dict | str]:\n"
            "    try:\n"
            "        data = json.loads(raw_json)\n"
            "    except Exception:\n"
            "        return False, 'Invalid JSON'\n"
            "    if not isinstance(data, dict):\n"
            "        return False, 'Payload must be a JSON object'\n"
            "    for field in required_fields:\n"
            "        if field not in data:\n"
            "            return False, f'Missing required field: {field}'\n"
            "    return True, data\n"
        ),
        "solutionExplanation": (
            "Мы используем блок try-except для перехвата ошибок парсинга JSON и последовательно проверяем обязательные ключи."
        ),
        "hints": [
            "Оберните `json.loads(raw_json)` в блок `try ... except json.JSONDecodeError` или общий `except Exception`.",
            "Проверьте наличие каждого поля циклом `for field in required_fields:`.",
            "При первой же нехватке поля возвращайте `(False, f'Missing required field: {field}')`."
        ],
        "commonMistakes": [
            "Забыть импортировать модуль `json`.",
            "Не обрабатывать ситуацию, когда передан невалидный JSON (например, с незакрытой фигурной скобкой)."
        ],
        "guide": {
            "walkthrough": [
                "Распаковываем строку JSON через json.loads в блоке try.",
                "Проверяем наличие каждого требуемого поля.",
                "Возвращаем кортеж статуса и распарсенных данных."
            ],
            "terms": [
                {"name": "REST", "desc": "Архитектурный стиль веб-сервисов с ориентацией на ресурсы и стандартные методы HTTP."},
                {"name": "JSON", "desc": "Текстовый формат обмена данными, основанный на парах ключ-значение и массивах."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешная валидация валидного JSON",
                "expression": "process_rest_payload('{\"title\": \"Book\", \"price\": 500}', ['title', 'price'])[0]",
                "expected": True
            },
            {
                "id": "t2",
                "label": "Отсутствие обязательного поля",
                "expression": "process_rest_payload('{\"title\": \"Book\"}', ['title', 'price'])",
                "expected": [False, "Missing required field: price"]
            },
            {
                "id": "t3",
                "label": "Битая строка JSON",
                "expression": "process_rest_payload('{bad json}', ['id'])",
                "expected": [False, "Invalid JSON"]
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 2. Основы FastAPI и первый веб-сервис
    # -----------------------------------------------------------------
    {
        "id": "backend-fastapi-first-endpoint",
        "title": "Первый веб-сервер на FastAPI: @app.get",
        "order": 60,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "FastAPI — это самый популярный, высокопроизводительный современный веб-фреймворк для Python. "
            "Он построен на стандартах OpenAPI (Swagger) и автоматической валидации типов.\n\n"
            "Как устроен базовый сервис на FastAPI:\n"
            "```python\n"
            "from fastapi import FastAPI\n\n"
            "app = FastAPI(title='My First API')\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'message': 'Hello, World!'}\n"
            "```\n\n"
            "1. `app = FastAPI()` — создает экземпляр веб-приложения.\n"
            "2. `@app.get('/health')` — декоратор, регистрирующий функцию-обработчик (эндпоинт) для HTTP-метода GET по адресу `/health`.\n"
            "3. Функция возвращает обычный словарь Python — FastAPI автоматически сериализует его в JSON и выставляет заголовок `Content-Type: application/json`."
        ),
        "lifeExample": (
            "Представьте стойку администратора в отеле. Регистрация эндпоинта `@app.get('/wifi')` — это как повесить табличку "
            "«Информация о Wi-Fi на стойке 1». Когда гость подходит и спрашивает Wi-Fi, администратор выдает готовую карточку с паролем."
        ),
        "task": (
            "Создайте приложение FastAPI и зарегистрируйте два эндпоинта:\n"
            "1. `GET /` — возвращает словарь `{'app': 'DevForge API', 'status': 'running'}`.\n"
            "2. `GET /health` — возвращает словарь `{'status': 'ok', 'version': '1.0.0'}`.\n\n"
            "Объект приложения должен называться `app`."
        ),
        "starterCode": (
            "from fastapi import FastAPI\n\n"
            "# 1. Создайте экземпляр приложения app\n"
            "# 2. Зарегистрируйте эндпоинты @app.get('/') и @app.get('/health')\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI\n\n"
            "app = FastAPI(title='DevForge API')\n\n"
            "@app.get('/')\n"
            "def root():\n"
            "    return {'app': 'DevForge API', 'status': 'running'}\n\n"
            "@app.get('/health')\n"
            "def health_check():\n"
            "    return {'status': 'ok', 'version': '1.0.0'}\n"
        ),
        "solutionExplanation": (
            "Мы инициализировали FastAPI и декорировали функции root и health_check декораторами @app.get."
        ),
        "hints": [
            "Инициализируйте приложение строкой `app = FastAPI()`.",
            "Над функцией напишите декоратор `@app.get('/')`.",
            "Над второй функцией напишите декоратор `@app.get('/health')` и верните требуемый словарь."
        ],
        "commonMistakes": [
            "Забыть собачку `@` перед именем декоратора `app.get`.",
            "Забыть круглые скобки при вызове `FastAPI()`."
        ],
        "guide": {
            "walkthrough": [
                "Импортируем класс FastAPI.",
                "Создаем объект приложения: app = FastAPI().",
                "Добавляем обработчик корневого маршрута и маршрута /health."
            ],
            "terms": [
                {"name": "FastAPI", "desc": "Современный быстрый веб-фреймворк для создания REST API на Python."},
                {"name": "Endpoint", "desc": "Конечная точка API (комбинация URL-пути и HTTP-метода)."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Тестирование эндпоинта GET /",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/').json()['status']",
                "expected": "running"
            },
            {
                "id": "t2",
                "label": "Тестирование эндпоинта GET /health",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/health').json()",
                "expected": {"status": "ok", "version": "1.0.0"}
            },
            {
                "id": "t3",
                "label": "Проверка статус-кода 200",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/health').status_code",
                "expected": 200
            }
        ]
    },

    {
        "id": "backend-fastapi-path-params",
        "title": "Параметры путей (Path Parameters) и типизация",
        "order": 61,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "В REST API для обращения к конкретному объекту его идентификатор указывают прямо в URL:\n"
            "• `/users/1`\n"
            "• `/orders/42`\n\n"
            "В FastAPI такие динамические сегменты пути объявляются в фигурных скобках:\n"
            "```python\n"
            "@app.get('/users/{user_id}')\n"
            "def get_user(user_id: int):\n"
            "    return {'user_id': user_id}\n"
            "```\n\n"
            "Обратите внимание на аннотацию типа `user_id: int`!\n"
            "FastAPI автоматически:\n"
            "1. Извлекает строковое значение из URL (например, `'42'`).\n"
            "2. Преобразует его в целое число `42`.\n"
            "3. Если клиент передаст не число (например, `/users/alex`), сервер автоматически вернет ошибку `422 Unprocessable Entity` без падения сервиса."
        ),
        "lifeExample": (
            "Камера хранения на вокзале. Номер на жетоне указывает на конкретную ячейку: ячейка {box_id}. "
            "Если вместо номера вы назовёте слово «арбуз», автомат сразу выдаст ошибку формата номера."
        ),
        "task": (
            "Создайте приложение `app = FastAPI()` с базой пользователей в словаре:\n"
            "```python\n"
            "USERS_DB = {\n"
            "    1: {'name': 'Иван', 'role': 'admin'},\n"
            "    2: {'name': 'Анна', 'role': 'developer'}\n"
            "}\n"
            "```\n"
            "Реализуйте эндпоинт `GET /users/{user_id}`:\n"
            "• Если пользователь с таким `user_id` существует, возвращайте `{'id': user_id, **USERS_DB[user_id]}`.\n"
            "• Если пользователя нет, выбрасывайте `raise HTTPException(status_code=404, detail='User not found')`."
        ),
        "starterCode": (
            "from fastapi import FastAPI, HTTPException\n\n"
            "app = FastAPI()\n\n"
            "USERS_DB = {\n"
            "    1: {'name': 'Иван', 'role': 'admin'},\n"
            "    2: {'name': 'Анна', 'role': 'developer'}\n"
            "}\n\n"
            "# Напишите эндпоинт @app.get('/users/{user_id}')\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI, HTTPException\n\n"
            "app = FastAPI()\n\n"
            "USERS_DB = {\n"
            "    1: {'name': 'Иван', 'role': 'admin'},\n"
            "    2: {'name': 'Анна', 'role': 'developer'}\n"
            "}\n\n"
            "@app.get('/users/{user_id}')\n"
            "def get_user(user_id: int):\n"
            "    if user_id not in USERS_DB:\n"
            "        raise HTTPException(status_code=404, detail='User not found')\n"
            "    return {'id': user_id, **USERS_DB[user_id]}\n"
        ),
        "solutionExplanation": (
            "Мы объявили параметр пути {user_id} с типом int. При отсутствии ключа в словаре выбрасывается HTTPException(404)."
        ),
        "hints": [
            "Укажите фигурные скобки в пути: `@app.get('/users/{user_id}')`.",
            "Аргумент функции должен называться точно так же: `def get_user(user_id: int):`.",
            "Проверьте наличие ключа: `if user_id not in USERS_DB: raise HTTPException(status_code=404, detail='User not found')`."
        ],
        "commonMistakes": [
            "Забыть типизировать `user_id: int` (тогда он останется строкой и поиск в словаре с числовыми ключами не сработает).",
            "Возвращать строку с ошибкой вместо выброса `raise HTTPException`."
        ],
        "guide": {
            "walkthrough": [
                "Объявляем маршрут с шаблонной переменной {user_id}.",
                "Проверяем наличие id в USERS_DB.",
                "Выбрасываем HTTPException(404) или возвращаем данные пользователя."
            ],
            "terms": [
                {"name": "Path Parameter", "desc": "Динамический параметр, встроенный прямо в сегмент URL-пути."},
                {"name": "HTTPException", "desc": "Исключение FastAPI для возврата ошибок с заданным статус-кодом."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Получение существующего пользователя ID 1",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/users/1').json()['name']",
                "expected": "Иван"
            },
            {
                "id": "t2",
                "label": "Ошибка 404 для несуществующего ID 99",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/users/99').status_code",
                "expected": 404
            },
            {
                "id": "t3",
                "label": "Сообщение об ошибке 404",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/users/99').json()['detail']",
                "expected": "User not found"
            }
        ]
    },

    {
        "id": "backend-fastapi-query-params",
        "title": "Параметры запроса (Query Parameters): Фильтрация и Пагинация",
        "order": 62,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Когда параметры не определяют конкретный ресурс, а модифицируют выборку (фильтруют, сортируют, задают страницу), "
            "их передают в строке запроса после знака `?` через `&`:\n"
            "`/items?limit=10&offset=20&search=phone`\n\n"
            "В FastAPI параметры, не упомянутые в фигурных скобках пути `{...}`, автоматически становятся **Query-параметрами**:\n"
            "```python\n"
            "@app.get('/items')\n"
            "def list_items(limit: int = 10, offset: int = 0):\n"
            "    return items[offset : offset + limit]\n"
            "```\n\n"
            "Пагинация (limit/offset) — обязательный стандарт бэкенда: база данных может содержать миллионы строк, "
            "и выдавать их все за один запрос категорически запрещено (сервер исчерпает память и упадёт)."
        ),
        "lifeExample": (
            "Оглавление большой книги или поиск в каталоге: «покажите мне по 10 товаров на странице, начиная с 20-го». "
            "Вы не требуете вывалить на стол весь склад магазина сразу."
        ),
        "task": (
            "Создайте приложение `app = FastAPI()` со списком товаров:\n"
            "```python\n"
            "ITEMS = [\n"
            "    {'id': 1, 'name': 'Ноутбук'},\n"
            "    {'id': 2, 'name': 'Мышь'},\n"
            "    {'id': 3, 'name': 'Клавиатура'},\n"
            "    {'id': 4, 'name': 'Монитор'}\n"
            "]\n"
            "```\n"
            "Реализуйте эндпоинт `GET /items` со следующими параметрами:\n"
            "• `limit: int = 2` (сколько элементов вернуть максимум).\n"
            "• `offset: int = 0` (сколько элементов пропустить с начала).\n"
            "Эндпоинт должен возвращать словарь:\n"
            "```python\n"
            "{'total': len(ITEMS), 'limit': limit, 'offset': offset, 'items': срезанный_список}\n"
            "```"
        ),
        "starterCode": (
            "from fastapi import FastAPI\n\n"
            "app = FastAPI()\n\n"
            "ITEMS = [\n"
            "    {'id': 1, 'name': 'Ноутбук'},\n"
            "    {'id': 2, 'name': 'Мышь'},\n"
            "    {'id': 3, 'name': 'Клавиатура'},\n"
            "    {'id': 4, 'name': 'Монитор'}\n"
            "]\n\n"
            "# Реализуйте @app.get('/items') с пагинацией\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI\n\n"
            "app = FastAPI()\n\n"
            "ITEMS = [\n"
            "    {'id': 1, 'name': 'Ноутбук'},\n"
            "    {'id': 2, 'name': 'Мышь'},\n"
            "    {'id': 3, 'name': 'Клавиатура'},\n"
            "    {'id': 4, 'name': 'Монитор'}\n"
            "]\n\n"
            "@app.get('/items')\n"
            "def list_items(limit: int = 2, offset: int = 0):\n"
            "    sliced = ITEMS[offset : offset + limit]\n"
            "    return {\n"
            "        'total': len(ITEMS),\n"
            "        'limit': limit,\n"
            "        'offset': offset,\n"
            "        'items': sliced\n"
            "    }\n"
        ),
        "solutionExplanation": (
            "Используем срез списка ITEMS[offset : offset + limit] и возвращаем метаданные пагинации вместе с элементами."
        ),
        "hints": [
            "Объявите функцию с аргументами по умолчанию: `def list_items(limit: int = 2, offset: int = 0):`.",
            "Срез списка в Python делается так: `ITEMS[offset : offset + limit]`.",
            "Сформируйте словарь с ключами total, limit, offset, items."
        ],
        "commonMistakes": [
            "Писать `ITEMS[offset:limit]` вместо `ITEMS[offset : offset + limit]` (второе число среза — это конечный индекс, а не количество)."
        ],
        "guide": {
            "walkthrough": [
                "Объявляем GET эндпоинт без фигурных скобок в пути.",
                "Принимаем limit и offset со значениями по умолчанию.",
                "Делаем срез элементов и возвращаем словарь ответа."
            ],
            "terms": [
                {"name": "Query Parameter", "desc": "Параметр в URL после символа '?', используемый для фильтрации и пагинации."},
                {"name": "Pagination", "desc": "Разбиение большого набора данных на отдельные страницы."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Пагинация по умолчанию (первые 2 элемента)",
                "expression": "from fastapi.testclient import TestClient; len(TestClient(app).get('/items').json()['items'])",
                "expected": 2
            },
            {
                "id": "t2",
                "label": "Пагинация со сдвигом offset=2",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/items?offset=2&limit=2').json()['items'][0]['name']",
                "expected": "Клавиатура"
            },
            {
                "id": "t3",
                "label": "Общее количество total",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/items').json()['total']",
                "expected": 4
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 3. Валидация данных с Pydantic
    # -----------------------------------------------------------------
    {
        "id": "backend-pydantic-schemas",
        "title": "Pydantic: Модели данных и валидация входящих запросов",
        "order": 63,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Когда клиент отправляет POST-запрос на создание ресурса, данные передаются в теле запроса (Request Body) в формате JSON. "
            "Бэкенд никогда не должен слепо доверять входящим данным!\n\n"
            "Библиотека Pydantic — ядро валидации данных в FastAPI. "
            "Вы описываете схему данных как класс, унаследованный от `BaseModel`:\n"
            "```python\n"
            "from pydantic import BaseModel\n\n"
            "class ProductCreate(BaseModel):\n"
            "    name: str\n"
            "    price: float\n"
            "    is_active: bool = True\n"
            "```\n\n"
            "Когда вы указываете этот класс в параметрах эндпоинта:\n"
            "```python\n"
            "@app.post('/products')\n"
            "def create_product(product: ProductCreate):\n"
            "    # product — это уже проверенный и типизированный объект!\n"
            "    return {'saved': product.name, 'price': product.price}\n"
            "```\n"
            "FastAPI автоматически парсит тело запроса, проверяет типы и возвращает 422, если переданы неверные данные."
        ),
        "lifeExample": (
            "Служба доставки грузов. Вы не можете отправить посылку без указания адреса и веса. "
            "Оператор вводит данные в форму: если поле «вес» пустое или вместо граммов написаны буквы, система просто не даст оформить квитанцию."
        ),
        "task": (
            "1. Создайте модель `UserCreate(BaseModel)` с полями:\n"
            "   • `username: str`\n"
            "   • `email: str`\n"
            "   • `age: int` (со значением по умолчанию `18`)\n"
            "2. Создайте приложение `app = FastAPI()`.\n"
            "3. Зарегистрируйте эндпоинт `POST /users` со статус-кодом `status.HTTP_201_CREATED`.\n"
            "   Эндпоинт должен принимать объект `user: UserCreate` и возвращать словарь:\n"
            "   `{'id': 1, 'username': user.username, 'email': user.email, 'age': user.age}`."
        ),
        "starterCode": (
            "from fastapi import FastAPI, status\n"
            "from pydantic import BaseModel\n\n"
            "# 1. Объявите UserCreate(BaseModel)\n"
            "# 2. Создайте app = FastAPI()\n"
            "# 3. Напишите @app.post('/users', status_code=status.HTTP_201_CREATED)\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI, status\n"
            "from pydantic import BaseModel\n\n"
            "class UserCreate(BaseModel):\n"
            "    username: str\n"
            "    email: str\n"
            "    age: int = 18\n\n"
            "app = FastAPI()\n\n"
            "@app.post('/users', status_code=status.HTTP_201_CREATED)\n"
            "def create_user(user: UserCreate):\n"
            "    return {\n"
            "        'id': 1,\n"
            "        'username': user.username,\n"
            "        'email': user.email,\n"
            "        'age': user.age\n"
            "    }\n"
        ),
        "solutionExplanation": (
            "Мы объявили схему Pydantic с типами и значением по умолчанию для возраста. В эндпоинте указали статус-код 201."
        ),
        "hints": [
            "Унаследуйте класс от `BaseModel`: `class UserCreate(BaseModel):`.",
            "Для значения по умолчанию используйте знак равенства: `age: int = 18`.",
            "В декораторе укажите: `@app.post('/users', status_code=status.HTTP_201_CREATED)`."
        ],
        "commonMistakes": [
            "Забыть статус-код 201 (по умолчанию FastAPI вернет 200, но для создания ресурса стандартом является 201 Created)."
        ],
        "guide": {
            "walkthrough": [
                "Объявляем Pydantic модель с аннотациями типов.",
                "Регистрируем POST эндпоинт со статусом 201.",
                "Принимаем объект схемы в аргументах и возвращаем сформированный словарь."
            ],
            "terms": [
                {"name": "Pydantic", "desc": "Библиотека для валидации данных и управления настройками с помощью аннотаций типов."},
                {"name": "Request Body", "desc": "Тело HTTP-запроса, содержащее отправляемые клиентом данные."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешное создание пользователя через POST",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/users', json_data={'username': 'alex', 'email': 'alex@dev.io'}).status_code",
                "expected": 201
            },
            {
                "id": "t2",
                "label": "Проверка значения по умолчанию age=18",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/users', json_data={'username': 'alex', 'email': 'alex@dev.io'}).json()['age']",
                "expected": 18
            },
            {
                "id": "t3",
                "label": "Ошибка 422 при отсутствии обязательного поля email",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/users', json_data={'username': 'alex'}).status_code",
                "expected": 422
            }
        ]
    },

    {
        "id": "backend-pydantic-validation",
        "title": "Валидация полей с Field и Response Models",
        "order": 64,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Одной проверки типа недостаточно: имя пользователя не может быть пустым, пароль должен быть не короче 8 символов, "
            "а цена не может быть отрицательной. В Pydantic для этого используется функция `Field(...)`:\n"
            "```python\n"
            "from pydantic import BaseModel, Field\n\n"
            "class RegisterRequest(BaseModel):\n"
            "    username: str = Field(min_length=3, max_length=20)\n"
            "    password: str = Field(min_length=8)\n"
            "    coins: int = Field(default=0, ge=0)  # ge = greater or equal (>= 0)\n"
            "```\n\n"
            "Вторая важнейшая задача — **безопасность ответа**. Сервер никогда не должен возвращать наружу хеши паролей или секретные токены. "
            "Для этого используют отдельную модель ответа (Response Model):\n"
            "```python\n"
            "class UserResponse(BaseModel):\n"
            "    id: int\n"
            "    username: str\n"
            "    coins: int\n"
            "    # Поля password здесь нет — оно никогда не утечет клиенту!\n"
            "```"
        ),
        "lifeExample": (
            "Медицинская карта пациента. Врач видит полные результаты анализов и диагнозы, "
            "но когда выдается больничный лист работодателю, на нем отображаются только номер, ФИО и даты освобождения от работы."
        ),
        "task": (
            "1. Создайте модель `AccountCreate(BaseModel)` с полями:\n"
            "   • `username: str` с ограничением `min_length=3`.\n"
            "   • `password: str` с ограничением `min_length=8`.\n"
            "   • `balance: float = Field(default=0.0, ge=0.0)`.\n"
            "2. Создайте модель `AccountResponse(BaseModel)` с полями `id: int`, `username: str`, `balance: float` (без пароля!).\n"
            "3. Создайте функцию `register_account(payload: dict) -> dict`:\n"
            "   Она валидирует входящий словарь через `AccountCreate(**payload)`, имитирует сохранение (назначая `id = 1`) "
            "   и возвращает безопасный словарь через `AccountResponse(id=1, username=acc.username, balance=acc.balance).model_dump()`."
        ),
        "starterCode": (
            "from pydantic import BaseModel, Field, ValidationError\n\n"
            "# 1. Создайте AccountCreate и AccountResponse\n"
            "# 2. Реализуйте register_account(payload: dict) -> dict\n"
        ),
        "solutionCode": (
            "from pydantic import BaseModel, Field, ValidationError\n\n"
            "class AccountCreate(BaseModel):\n"
            "    username: str = Field(min_length=3)\n"
            "    password: str = Field(min_length=8)\n"
            "    balance: float = Field(default=0.0, ge=0.0)\n\n"
            "class AccountResponse(BaseModel):\n"
            "    id: int\n"
            "    username: str\n"
            "    balance: float\n\n"
            "def register_account(payload: dict) -> dict:\n"
            "    acc = AccountCreate(**payload)\n"
            "    safe = AccountResponse(id=1, username=acc.username, balance=acc.balance)\n"
            "    return safe.model_dump()\n"
        ),
        "solutionExplanation": (
            "AccountCreate отсекает короткие логины/пароли и отрицательные балансы. AccountResponse гарантирует, что пароль не вернется в ответе."
        ),
        "hints": [
            "Используйте `Field(min_length=3)` для username и `Field(min_length=8)` для пароля.",
            "Для баланса используйте `Field(default=0.0, ge=0.0)`.",
            "В функции `register_account` создайте `AccountCreate(**payload)`, затем `AccountResponse(...)` и вызовите `.model_dump()`."
        ],
        "commonMistakes": [
            "Оставить поле password в модели ответа AccountResponse.",
            "Забыть распаковать словарь через `**payload`."
        ],
        "guide": {
            "walkthrough": [
                "Создаем схему валидации входящих данных AccountCreate с ограничениями Field.",
                "Создаем безопасную схему ответа AccountResponse без конфиденциальных данных.",
                "Пишем функцию регистрации с конвертацией схемы в словарь."
            ],
            "terms": [
                {"name": "Field", "desc": "Функция Pydantic для задания расширенной валидации и ограничений полей."},
                {"name": "DTO", "desc": "Data Transfer Object — объект для безопасной передачи данных между слоями приложения."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешная регистрация и отсечение пароля",
                "expression": "register_account({'username': 'ivan', 'password': 'super_secret_123', 'balance': 150.0})",
                "expected": {"id": 1, "username": "ivan", "balance": 150.0}
            },
            {
                "id": "t2",
                "label": "Ошибка валидации при коротком логине (<3)",
                "expression": "try:\n    register_account({'username': 'yo', 'password': '12345678'})\n    res = 'ok'\nexcept ValidationError:\n    res = 'error'\nres",
                "expected": "error"
            },
            {
                "id": "t3",
                "label": "Ошибка валидации при коротком пароле (<8)",
                "expression": "try:\n    register_account({'username': 'alex', 'password': '123'})\n    res = 'ok'\nexcept ValidationError:\n    res = 'error'\nres",
                "expected": "error"
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 4. Обработка ошибок и Dependency Injection
    # -----------------------------------------------------------------
    {
        "id": "backend-fastapi-http-exceptions",
        "title": "Обработка ошибок и HTTPException",
        "order": 65,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "В профессиональном бэкенде ошибки — это нормальная часть работы (пользователь ввёл не тот пароль, "
            "запросил удалённую статью или у него кончились деньги на счёте). "
            "Главное правило бэкенда: **сервер никогда не должен падать с 500 Internal Server Error при предсказуемой ошибке клиента**.\n\n"
            "В FastAPI для контролируемого прерывания запроса выбрасывается `HTTPException`:\n"
            "```python\n"
            "from fastapi import HTTPException, status\n\n"
            "if balance < amount:\n"
            "    raise HTTPException(\n"
            "        status_code=status.HTTP_400_BAD_REQUEST,\n"
            "        detail='Недостаточно средств на счете'\n"
            "    )\n"
            "```\n"
            "FastAPI перехватывает это исключение, останавливает выполнение функции и отправляет клиенту красивый JSON:\n"
            "`{'detail': 'Недостаточно средств на счете'}` с HTTP-статусом 400."
        ),
        "lifeExample": (
            "Банкомат. Если вы пытаетесь снять 10 000 рублей, имея на карте 1 000, банкомат не искрит и не ломается. "
            "Он вежливо выводит на экран: «Недостаточно средств» и возвращает карту. HTTPException делает ровно то же самое."
        ),
        "task": (
            "Создайте приложение `app = FastAPI()` со счетами:\n"
            "```python\n"
            "ACCOUNTS = {1: {'owner': 'Мария', 'balance': 500.0}}\n"
            "```\n"
            "Реализуйте эндпоинт `POST /accounts/{account_id}/withdraw` с параметром запроса `amount: float`:\n"
            "1. Если `account_id not in ACCOUNTS` -> выбросить `HTTPException(404, detail='Счет не найден')`.\n"
            "2. Если `amount <= 0` -> выбросить `HTTPException(400, detail='Сумма должна быть положительной')`.\n"
            "3. Если `ACCOUNTS[account_id]['balance'] < amount` -> выбросить `HTTPException(400, detail='Недостаточно средств')`.\n"
            "4. Иначе списать сумму с баланса и вернуть `{'account_id': account_id, 'new_balance': ACCOUNTS[account_id]['balance']}`."
        ),
        "starterCode": (
            "from fastapi import FastAPI, HTTPException, status\n\n"
            "app = FastAPI()\n"
            "ACCOUNTS = {1: {'owner': 'Мария', 'balance': 500.0}}\n\n"
            "# Реализуйте эндпоинт списания @app.post('/accounts/{account_id}/withdraw')\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI, HTTPException, status\n\n"
            "app = FastAPI()\n"
            "ACCOUNTS = {1: {'owner': 'Мария', 'balance': 500.0}}\n\n"
            "@app.post('/accounts/{account_id}/withdraw')\n"
            "def withdraw(account_id: int, amount: float):\n"
            "    if account_id not in ACCOUNTS:\n"
            "        raise HTTPException(status_code=404, detail='Счет не найден')\n"
            "    if amount <= 0:\n"
            "        raise HTTPException(status_code=400, detail='Сумма должна быть положительной')\n"
            "    if ACCOUNTS[account_id]['balance'] < amount:\n"
            "        raise HTTPException(status_code=400, detail='Недостаточно средств')\n"
            "    ACCOUNTS[account_id]['balance'] -= amount\n"
            "    return {'account_id': account_id, 'new_balance': ACCOUNTS[account_id]['balance']}\n"
        ),
        "solutionExplanation": (
            "Мы последовательно проверили валидность счета, сумму списания и остаток баланса, выбрасывая HTTPException при любых нарушениях."
        ),
        "hints": [
            "Используйте `raise HTTPException(status_code=404, detail='Счет не найден')` если счет отсутствует.",
            "Проверьте `amount <= 0` и выбросите статус 400.",
            "Спишите баланс `ACCOUNTS[account_id]['balance'] -= amount` и верните словарь с результатом."
        ],
        "commonMistakes": [
            "Сначала списать баланс, а потом проверить, хватило ли денег.",
            "Использовать return вместо raise для HTTPException."
        ],
        "guide": {
            "walkthrough": [
                "Объявляем POST эндпоинт со списанием средств.",
                "Проверяем существование счета (404).",
                "Проверяем корректность суммы и баланс (400).",
                "Обновляем баланс и возвращаем результат."
            ],
            "terms": [
                {"name": "HTTPException", "desc": "Класс исключения FastAPI, транслирующийся в HTTP-ответ с ошибкой."},
                {"name": "Guard Clause", "desc": "Паттерн раннего возврата ошибки для предотвращения глубокой вложенности кода."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешное списание 200 со счета 500",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/accounts/1/withdraw?amount=200').json()['new_balance']",
                "expected": 300.0
            },
            {
                "id": "t2",
                "label": "Ошибка 400 при попытке списать больше остатка",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/accounts/1/withdraw?amount=999').status_code",
                "expected": 400
            },
            {
                "id": "t3",
                "label": "Ошибка 404 для несуществующего счета",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).post('/accounts/999/withdraw?amount=10').status_code",
                "expected": 404
            }
        ]
    },

    {
        "id": "backend-fastapi-dependency-injection",
        "title": "Dependency Injection: Архитектура Depends",
        "order": 66,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Dependency Injection (DI, внедрение зависимостей) — главная архитектурная фишка FastAPI. "
            "Вместо того чтобы внутри каждого эндпоинта вручную проверять авторизацию или открывать базу данных, "
            "вы выносите эту логику в отдельную независимую функцию и подключаете её через `Depends`:\n"
            "```python\n"
            "from fastapi import Depends, FastAPI, HTTPException\n\n"
            "def get_current_user():\n"
            "    # проверка токена...\n"
            "    return {'user_id': 10, 'name': 'Ольга'}\n\n"
            "@app.get('/profile')\n"
            "def read_profile(user: dict = Depends(get_current_user)):\n"
            "    return {'welcome': user['name']}\n"
            "```\n\n"
            "Преимущества Depends:\n"
            "1. DRY (Don't Repeat Yourself) — одна и та же функция аутентификации подключается ко всем защищённым маршрутам.\n"
            "2. Тестируемость — в тестах зависимость можно подменить (mock) одной строчкой без изменения кода эндпоинта."
        ),
        "lifeExample": (
            "Турникет метро. Вам не нужно каждый раз доказывать машинисту поезда, что вы оплатили проезд. "
            "Турникет на входе (Depends) проверяет билет и пропускает вас на перрон. Поезд просто везет всех, кто уже прошел турникет."
        ),
        "task": (
            "Создайте систему аутентификации через Depends:\n"
            "1. Реализуйте функцию-зависимость `get_api_key(api_key: str = 'secret-key-123') -> str`:\n"
            "   • Если `api_key == 'secret-key-123'`, вернуть этот ключ.\n"
            "   • Иначе выбросить `HTTPException(status_code=401, detail='Invalid API Key')`.\n"
            "2. Создайте приложение `app = FastAPI()`.\n"
            "3. Зарегистрируйте защищённый эндпоинт `GET /admin/dashboard`:\n"
            "   `def admin_dashboard(key: str = Depends(get_api_key)):`\n"
            "   Эндпоинт должен возвращать `{'access': 'granted', 'section': 'analytics'}`."
        ),
        "starterCode": (
            "from fastapi import Depends, FastAPI, HTTPException, status\n\n"
            "# 1. Реализуйте get_api_key\n"
            "# 2. Создайте app = FastAPI()\n"
            "# 3. Зарегистрируйте @app.get('/admin/dashboard')\n"
        ),
        "solutionCode": (
            "from fastapi import Depends, FastAPI, HTTPException, status\n\n"
            "def get_api_key(api_key: str = 'secret-key-123') -> str:\n"
            "    if api_key != 'secret-key-123':\n"
            "        raise HTTPException(status_code=401, detail='Invalid API Key')\n"
            "    return api_key\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/admin/dashboard')\n"
            "def admin_dashboard(key: str = Depends(get_api_key)):\n"
            "    return {'access': 'granted', 'section': 'analytics'}\n"
        ),
        "solutionExplanation": (
            "Мы объявили функцию get_api_key и подключили ее через Depends к эндпоинту. При неверном ключе автоматически возвращается 401."
        ),
        "hints": [
            "В `get_api_key` проверьте: `if api_key != 'secret-key-123': raise HTTPException(401, 'Invalid API Key')`.",
            "В эндпоинте используйте параметр `key: str = Depends(get_api_key)`.",
            "Верните требуемый словарь `{'access': 'granted', 'section': 'analytics'}`."
        ],
        "commonMistakes": [
            "Вызывать зависимость со скобками `Depends(get_api_key())` вместо передачи ссылки `Depends(get_api_key)`."
        ],
        "guide": {
            "walkthrough": [
                "Создаем функцию проверки ключа API.",
                "Инициализируем FastAPI.",
                "Регистрируем маршрут с параметром Depends."
            ],
            "terms": [
                {"name": "Dependency Injection", "desc": "Паттерн проектирования, передающий сервису готовые зависимости извне."},
                {"name": "Depends", "desc": "Специальный маркер FastAPI для объявления зависимостей эндпоинта."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешный доступ с правильным API-ключом",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/admin/dashboard?api_key=secret-key-123').json()['access']",
                "expected": "granted"
            },
            {
                "id": "t2",
                "label": "Ошибка 401 при неверном ключе",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/admin/dashboard?api_key=wrong-key').status_code",
                "expected": 401
            },
            {
                "id": "t3",
                "label": "Текст ошибки 401",
                "expression": "from fastapi.testclient import TestClient; TestClient(app).get('/admin/dashboard?api_key=wrong-key').json()['detail']",
                "expected": "Invalid API Key"
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 5. Базы данных и SQLAlchemy 2.0 ORM
    # -----------------------------------------------------------------
    {
        "id": "backend-db-relational-design",
        "title": "Реляционные базы данных: Моделирование сущностей и связи",
        "order": 67,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Реляционные базы данных (PostgreSQL, SQLite, MySQL) организуют данные в строгие двумерные таблицы.\n"
            "Главные концепции:\n"
            "1. **Первичный ключ (Primary Key, PK)** — уникальный идентификатор строки (обычно целое число `id`), гарантирующий, что каждая запись уникальна.\n"
            "2. **Внешний ключ (Foreign Key, FK)** — колонка, которая ссылается на Primary Key другой таблицы. Это связывает данные между собой.\n\n"
            "Самая частая связь в бэкенде — **Один-ко-многим (One-to-Many, 1:N)**:\n"
            "У одного пользователя может быть много заказов или банковских счетов. "
            "В таблице `accounts` колонка `user_id` является Foreign Key, указывающим на `users.id`.\n"
            "Это предотвращает появление счетов без владельца (сиротские записи) и обеспечивает ссылочную целостность (Referential Integrity)."
        ),
        "lifeExample": (
            "Паспорт и визы. Ваш паспорт имеет уникальный номер (Primary Key). "
            "Каждая виза в паспорте привязана к номеру вашего паспорта (Foreign Key). "
            "Виза не может существовать сама по себе в воздухе — она всегда принадлежит конкретному паспорту."
        ),
        "task": (
            "Смоделируйте отношение «Один-ко-многим» для пользователей и их банковских счетов:\n"
            "Реализуйте класс `InMemoryRelationalStore` со следующими методами:\n"
            "1. `add_user(user_id: int, name: str)` — сохраняет пользователя.\n"
            "2. `add_account(account_id: int, user_id: int, currency: str = 'RUB')`:\n"
            "   • Если `user_id` отсутствует среди пользователей, выбрасывать `ValueError(f'User {user_id} does not exist')` (проверка внешнего ключа!).\n"
            "   • Иначе сохранить счет.\n"
            "3. `get_user_accounts(user_id: int) -> list[dict]` — возвращает список всех счетов указанного пользователя."
        ),
        "starterCode": (
            "class InMemoryRelationalStore:\n"
            "    def __init__(self):\n"
            "        self.users = {}\n"
            "        self.accounts = {}\n\n"
            "    def add_user(self, user_id: int, name: str):\n"
            "        pass\n\n"
            "    def add_account(self, account_id: int, user_id: int, currency: str = 'RUB'):\n"
            "        pass\n\n"
            "    def get_user_accounts(self, user_id: int) -> list[dict]:\n"
            "        pass\n"
        ),
        "solutionCode": (
            "class InMemoryRelationalStore:\n"
            "    def __init__(self):\n"
            "        self.users = {}\n"
            "        self.accounts = {}\n\n"
            "    def add_user(self, user_id: int, name: str):\n"
            "        self.users[user_id] = {'id': user_id, 'name': name}\n\n"
            "    def add_account(self, account_id: int, user_id: int, currency: str = 'RUB'):\n"
            "        if user_id not in self.users:\n"
            "            raise ValueError(f'User {user_id} does not exist')\n"
            "        self.accounts[account_id] = {'id': account_id, 'user_id': user_id, 'currency': currency}\n\n"
            "    def get_user_accounts(self, user_id: int) -> list[dict]:\n"
            "        return [acc for acc in self.accounts.values() if acc['user_id'] == user_id]\n"
        ),
        "solutionExplanation": (
            "Мы реализовали эмуляцию реляционной связи 1:N с проверкой ссылочной целостности Foreign Key."
        ),
        "hints": [
            "В `add_account` сначала проверьте: `if user_id not in self.users: raise ValueError(...)`.",
            "В `get_user_accounts` отфильтруйте список счетов по `acc['user_id'] == user_id`."
        ],
        "commonMistakes": [
            "Разрешить создание счета без проверки существования пользователя в self.users."
        ],
        "guide": {
            "walkthrough": [
                "Инициализируем словари пользователей и счетов.",
                "Проверяем наличие родительского user_id перед добавлением счета.",
                "Выполняем выборку счетов по user_id."
            ],
            "terms": [
                {"name": "Primary Key", "desc": "Уникальный идентификатор строки в реляционной таблице."},
                {"name": "Foreign Key", "desc": "Внешний ключ, связывающий строку одной таблицы со строкой другой."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешное добавление пользователя и двух счетов",
                "expression": (
                    "store = InMemoryRelationalStore()\n"
                    "store.add_user(1, 'Анна')\n"
                    "store.add_account(101, 1, 'RUB')\n"
                    "store.add_account(102, 1, 'USD')\n"
                    "len(store.get_user_accounts(1))"
                ),
                "expected": 2
            },
            {
                "id": "t2",
                "label": "Ошибка Foreign Key при привязке к несуществующему пользователю",
                "expression": (
                    "store = InMemoryRelationalStore()\n"
                    "try:\n"
                    "    store.add_account(999, 42)\n"
                    "    res = 'ok'\n"
                    "except ValueError:\n"
                    "    res = 'error'\n"
                    "res"
                ),
                "expected": "error"
            }
        ]
    },

    {
        "id": "backend-sqlalchemy-models",
        "title": "SQLAlchemy 2.0: Декларативные модели (Declarative Base)",
        "order": 68,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Писать сырые SQL-запросы в виде строк (`cursor.execute('INSERT INTO ...')`) неудобно и чревато ошибками SQL Injection. "
            "Поэтому в современном бэкенде используют **ORM (Object-Relational Mapping)** — библиотеку, которая отображает классы Python на таблицы базы данных.\n\n"
            "Золотой стандарт Python — **SQLAlchemy 2.0**:\n"
            "```python\n"
            "from sqlalchemy import declarative_base, Column, Integer, String, Float\n\n"
            "Base = declarative_base()\n\n"
            "class Product(Base):\n"
            "    __tablename__ = 'products'\n\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    name = Column(String)\n"
            "    price = Column(Float)\n"
            "```\n\n"
            "Что здесь происходит:\n"
            "1. `Base = declarative_base()` — базовый класс для всех моделей.\n"
            "2. `__tablename__ = 'products'` — имя таблицы в базе данных.\n"
            "3. Экземпляр `p = Product(name='Клавиатура', price=2500.0)` — это обычный объект Python, поля которого соответствуют колонкам в таблице."
        ),
        "lifeExample": (
            "Опалубка для фундамента. Класс модели — это чертёж и форма, куда заливается бетон. "
            "Каждая отлитая плита (экземпляр класса) в точности повторяет форму чертежа и имеет заданные размеры."
        ),
        "task": (
            "Объявите декларативную модель `BankAccount` с помощью SQLAlchemy:\n"
            "1. Создайте `Base = declarative_base()`.\n"
            "2. Создайте класс `BankAccount(Base)`:\n"
            "   • `__tablename__ = 'bank_accounts'`\n"
            "   • `id`: колонка типа `Integer` с `primary_key=True`.\n"
            "   • `owner`: колонка типа `String`.\n"
            "   • `balance`: колонка типа `Float`.\n"
            "3. Создайте объект счета `acc = BankAccount(owner='Алексей', balance=10000.0)`."
        ),
        "starterCode": (
            "from sqlalchemy import declarative_base, Column, Integer, String, Float\n\n"
            "# 1. Создайте Base\n"
            "# 2. Объявите BankAccount\n"
            "# 3. Создайте acc = BankAccount(owner='Алексей', balance=10000.0)\n"
        ),
        "solutionCode": (
            "from sqlalchemy import declarative_base, Column, Integer, String, Float\n\n"
            "Base = declarative_base()\n\n"
            "class BankAccount(Base):\n"
            "    __tablename__ = 'bank_accounts'\n\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    owner = Column(String)\n"
            "    balance = Column(Float)\n\n"
            "acc = BankAccount(owner='Алексей', balance=10000.0)\n"
        ),
        "solutionExplanation": (
            "Мы объявили класс BankAccount, унаследованный от Base, определили имя таблицы и типы колонок."
        ),
        "hints": [
            "Не забудьте атрибут `__tablename__ = 'bank_accounts'`.",
            "Для первичного ключа передайте `primary_key=True`: `id = Column(Integer, primary_key=True)`.",
            "Создайте экземпляр `acc = BankAccount(owner='Алексей', balance=10000.0)`."
        ],
        "commonMistakes": [
            "Опечатка в `__tablename__` (нужно два подчеркивания с каждой стороны).",
            "Забыть унаследовать модель от `Base`."
        ],
        "guide": {
            "walkthrough": [
                "Создаем базовый декларативный класс через declarative_base().",
                "Определяем модель BankAccount с колонками id, owner, balance.",
                "Создаем тестовый экземпляр acc."
            ],
            "terms": [
                {"name": "ORM", "desc": "Object-Relational Mapping — технология связывания баз данных с концепциями ООП."},
                {"name": "Declarative Base", "desc": "Базовый класс SQLAlchemy, от которого наследуются модели таблиц."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Проверка имени таблицы",
                "expression": "BankAccount.__tablename__",
                "expected": "bank_accounts"
            },
            {
                "id": "t2",
                "label": "Проверка владельца счета",
                "expression": "acc.owner",
                "expected": "Алексей"
            },
            {
                "id": "t3",
                "label": "Проверка баланса счета",
                "expression": "acc.balance",
                "expected": 10000.0
            }
        ]
    },

    {
        "id": "backend-sqlalchemy-crud",
        "title": "CRUD-операции в SQLAlchemy 2.0 (Create, Read, Update, Delete)",
        "order": 69,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "CRUD (Create, Read, Update, Delete) — четыре базовые операции с базой данных.\n"
            "В SQLAlchemy 2.0 все операции выполняются через объект сессии (`Session`):\n\n"
            "1. **Create (Создать)**:\n"
            "```python\n"
            "item = Product(name='Мышь', price=500.0)\n"
            "session.add(item)\n"
            "session.commit()  # Записывает данные в БД и генерирует id\n"
            "```\n\n"
            "2. **Read (Прочитать)**:\n"
            "В SQLAlchemy 2.0 используется чистый синтаксис функции `select()`:\n"
            "```python\n"
            "# Получить все товары дороже 100 рублей:\n"
            "query = select(Product).where(Product.price > 100)\n"
            "items = session.scalars(query).all()\n\n"
            "# Получить конкретный товар по имени:\n"
            "item = session.scalars(select(Product).where(Product.name == 'Мышь')).first()\n"
            "```"
        ),
        "lifeExample": (
            "Офисная папка с документами. Чтобы внести договор в архив, секретарь кладёт его в папку (`session.add`) "
            "и ставит штамп с печатью (`session.commit`). Чтобы найти нужный договор, секретарь открывает опись (`select`) "
            "и выбирает нужный лист."
        ),
        "task": (
            "Напишите репозиторий товаров на SQLAlchemy:\n"
            "Даны инициализированный движок `engine` с таблицей `items` и модель `Item(Base)`:\n"
            "```python\n"
            "class Item(Base):\n"
            "    __tablename__ = 'items'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    title = Column(String)\n"
            "    price = Column(Float)\n"
            "```\n"
            "Реализуйте две функции:\n"
            "1. `create_item(session, title: str, price: float) -> Item`:\n"
            "   Создает объект `Item`, добавляет в сессию через `session.add`, фиксирует `session.commit()` и возвращает созданный объект.\n"
            "2. `find_item_by_title(session, title: str) -> Item | None`:\n"
            "   Выполняет `session.scalars(select(Item).where(Item.title == title)).first()` и возвращает найденный элемент."
        ),
        "starterCode": (
            "from sqlalchemy import declarative_base, Column, Integer, String, Float, select, create_engine, sessionmaker\n\n"
            "Base = declarative_base()\n"
            "class Item(Base):\n"
            "    __tablename__ = 'items'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    title = Column(String)\n"
            "    price = Column(Float)\n\n"
            "# Реализуйте функции create_item и find_item_by_title\n"
        ),
        "solutionCode": (
            "from sqlalchemy import declarative_base, Column, Integer, String, Float, select, create_engine, sessionmaker\n\n"
            "Base = declarative_base()\n"
            "class Item(Base):\n"
            "    __tablename__ = 'items'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    title = Column(String)\n"
            "    price = Column(Float)\n\n"
            "def create_item(session, title: str, price: float) -> Item:\n"
            "    item = Item(title=title, price=price)\n"
            "    session.add(item)\n"
            "    session.commit()\n"
            "    return item\n\n"
            "def find_item_by_title(session, title: str) -> Item | None:\n"
            "    return session.scalars(select(Item).where(Item.title == title)).first()\n"
        ),
        "solutionExplanation": (
            "Мы создали запись с помощью session.add + session.commit и выполнили поиск через select(Item).where().first()."
        ),
        "hints": [
            "В `create_item` создайте экземпляр `Item(title=title, price=price)`, вызовите `session.add(item)`, затем `session.commit()`.",
            "В `find_item_by_title` используйте конструкцию `session.scalars(select(Item).where(Item.title == title)).first()`."
        ],
        "commonMistakes": [
            "Забыть вызвать `session.commit()` после `session.add()` (без commit данные не сохранятся в базе)."
        ],
        "guide": {
            "walkthrough": [
                "Определяем функцию добавления сущности с commit.",
                "Определяем функцию чтения с запросом select.",
                "Возвращаем первый найденный объект или None."
            ],
            "terms": [
                {"name": "CRUD", "desc": "Create, Read, Update, Delete — четыре базовые операции управления записями данных."},
                {"name": "Session", "desc": "Рабочая сессия ORM, аккумулирующая изменения для отправки в базу."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Создание товара и сохранение в БД",
                "expression": (
                    "engine = create_engine('sqlite:///:memory:')\n"
                    "engine.conn.execute('CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price REAL)')\n"
                    "session = sessionmaker(bind=engine)()\n"
                    "it = create_item(session, 'Монитор', 15000.0)\n"
                    "it.id"
                ),
                "expected": 1
            },
            {
                "id": "t2",
                "label": "Поиск созданного товара по названию",
                "expression": (
                    "engine = create_engine('sqlite:///:memory:')\n"
                    "engine.conn.execute('CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price REAL)')\n"
                    "session = sessionmaker(bind=engine)()\n"
                    "create_item(session, 'Мышь', 800.0)\n"
                    "found = find_item_by_title(session, 'Мышь')\n"
                    "found.price if found else None"
                ),
                "expected": 800.0
            }
        ]
    },

    {
        "id": "backend-fastapi-db-integration",
        "title": "Связка FastAPI + SQLAlchemy: Паттерн get_db",
        "order": 70,
        "language": "python",
        "level": "Junior",
        "minutes": 15,
        "xp": 40,
        "theory": (
            "Как правильно открывать соединение с базой данных в веб-приложении?\n"
            "Нельзя использовать одну глобальную сессию на всё приложение (это вызовет гонки данных и сбои при параллельных запросах). "
            "Правильный паттерн индустрии — **сессия на каждый запрос (Session-per-request)**:\n\n"
            "1. Создается генератор `get_db()`:\n"
            "```python\n"
            "def get_db():\n"
            "    db = SessionLocal()\n"
            "    try:\n"
            "        yield db  # Передает сессию в эндпоинт\n"
            "    finally:\n"
            "        db.close()  # Гарантированно закрывает сессию после ответа!\n"
            "```\n\n"
            "2. В эндпоинте сессия подключается через `Depends`:\n"
            "```python\n"
            "@app.post('/items')\n"
            "def create_item(item: ItemCreate, db: Session = Depends(get_db)):\n"
            "    db_item = Item(name=item.name, price=item.price)\n"
            "    db.add(db_item)\n"
            "    db.commit()\n"
            "    return {'id': db_item.id, 'name': db_item.name}\n"
            "```\n"
            "Благодаря конструкции `try ... finally` сессия гарантированно вернётся в пул соединений, даже если в эндпоинте произойдет ошибка."
        ),
        "lifeExample": (
            "Прокат велосипедов. Вы приходите, берете велосипед на одну поездку, катаетесь по городу и обязательно "
            "возвращаете его на станцию проката. Велосипед не остается у вас дома навсегда — им могут пользоваться другие люди."
        ),
        "task": (
            "Объедините FastAPI и SQLAlchemy:\n"
            "1. Создайте приложение `app = FastAPI()`.\n"
            "2. Реализуйте генератор `get_db()` с сессией из `SessionLocal = sessionmaker(bind=engine)`.\n"
            "3. Зарегистрируйте эндпоинт `POST /notes` со схемой `NoteCreate(title: str)`:\n"
            "   Эндпоинт принимает `note: NoteCreate` и `db: Session = Depends(get_db)`.\n"
            "   Сохраняет в базу запись `Note(title=note.title)` и возвращает `{'id': db_note.id, 'title': db_note.title}` со статусом 201."
        ),
        "starterCode": (
            "from fastapi import FastAPI, Depends, status\n"
            "from pydantic import BaseModel\n"
            "from sqlalchemy import declarative_base, Column, Integer, String, create_engine, sessionmaker\n\n"
            "Base = declarative_base()\n"
            "class Note(Base):\n"
            "    __tablename__ = 'notes'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    title = Column(String)\n\n"
            "engine = create_engine('sqlite:///:memory:')\n"
            "engine.conn.execute('CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)')\n"
            "SessionLocal = sessionmaker(bind=engine)\n\n"
            "# Реализуйте NoteCreate, get_db и эндпоинт @app.post('/notes')\n"
        ),
        "solutionCode": (
            "from fastapi import FastAPI, Depends, status\n"
            "from pydantic import BaseModel\n"
            "from sqlalchemy import declarative_base, Column, Integer, String, create_engine, sessionmaker\n\n"
            "Base = declarative_base()\n"
            "class Note(Base):\n"
            "    __tablename__ = 'notes'\n"
            "    id = Column(Integer, primary_key=True)\n"
            "    title = Column(String)\n\n"
            "engine = create_engine('sqlite:///:memory:')\n"
            "engine.conn.execute('CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)')\n"
            "SessionLocal = sessionmaker(bind=engine)\n\n"
            "class NoteCreate(BaseModel):\n"
            "    title: str\n\n"
            "def get_db():\n"
            "    db = SessionLocal()\n"
            "    try:\n"
            "        yield db\n"
            "    finally:\n"
            "        db.close()\n\n"
            "app = FastAPI()\n\n"
            "@app.post('/notes', status_code=status.HTTP_201_CREATED)\n"
            "def create_note(note: NoteCreate, db = Depends(get_db)):\n"
            "    db_note = Note(title=note.title)\n"
            "    db.add(db_note)\n"
            "    db.commit()\n"
            "    return {'id': db_note.id, 'title': db_note.title}\n"
        ),
        "solutionExplanation": (
            "Мы связали модель Pydantic для валидации входа и модель SQLAlchemy для сохранения в SQLite через Depends(get_db)."
        ),
        "hints": [
            "Генератор get_db пишется с конструкцией `try: yield db finally: db.close()`.",
            "В аргументах эндпоинта укажите `note: NoteCreate, db = Depends(get_db)`.",
            "Не забудьте вызвать `db.commit()` после `db.add(db_note)`."
        ],
        "commonMistakes": [
            "Забыть yield в генераторе get_db.",
            "Смешивать модель Pydantic и модель SQLAlchemy в одну переменную."
        ],
        "guide": {
            "walkthrough": [
                "Определяем Pydantic модель NoteCreate.",
                "Создаем генератор зависимостей сессий get_db.",
                "Реализуем эндпоинт создания заметки с инъекцией БД."
            ],
            "terms": [
                {"name": "Session-per-request", "desc": "Архитектурный паттерн открытия отдельной сессии БД на каждый входящий запрос."},
                {"name": "get_db", "desc": "Каноническое имя функции-зависимости FastAPI для предоставления сессии базы данных."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Создание заметки через REST эндпоинт с сохранением в БД",
                "expression": (
                    "from fastapi.testclient import TestClient\n"
                    "client = TestClient(app)\n"
                    "resp = client.post('/notes', json_data={'title': 'Купить хлеб'})\n"
                    "resp.status_code"
                ),
                "expected": 201
            },
            {
                "id": "t2",
                "label": "Проверка сохраненных данных в теле ответа",
                "expression": (
                    "from fastapi.testclient import TestClient\n"
                    "client = TestClient(app)\n"
                    "resp = client.post('/notes', json_data={'title': 'Изучить FastAPI'})\n"
                    "resp.json()['title']"
                ),
                "expected": "Изучить FastAPI"
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 6. Транзакции, Тестирование и Docker
    # -----------------------------------------------------------------
    {
        "id": "backend-transactions-acid",
        "title": "Транзакции и ACID: Атомарные финансовые операции",
        "order": 71,
        "language": "python",
        "level": "Junior+",
        "minutes": 15,
        "xp": 45,
        "theory": (
            "Классическая задача любого финтех-сервиса — перевод денег со счета А на счет Б.\n"
            "Перевод состоит из двух шагов:\n"
            "1. Списать 1000 рублей со счета А.\n"
            "2. Зачислить 1000 рублей на счет Б.\n\n"
            "Что произойдет, если между шагом 1 и шагом 2 сервер отключится или упадет с ошибкой? "
            "Деньги со счета А спишутся, но до счета Б не дойдут — они растворятся в воздухе!\n\n"
            "Для решения этой проблемы существуют **транзакции базы данных (Transactions)** и принцип **атомарности (Atomicity в ACID)**:\n"
            "«Либо все операции выполняются успешно вместе, либо не выполняется ни одна».\n"
            "• `session.commit()` — навсегда фиксирует все изменения транзакции.\n"
            "• `session.rollback()` — отменяет все действия текущей транзакции при возникновении любой ошибки."
        ),
        "lifeExample": (
            "Обмен товарами из рук в руки: один человек протягивает деньги, второй — товар. "
            "Сделка считается состоявшейся только в тот момент, когда оба предмета переданы. "
            "Если покупатель уронил купюру — продавец не отдает товар, сделка отменяется (rollback)."
        ),
        "task": (
            "Реализуйте функцию атомарного денежного перевода:\n"
            "`transfer_money(accounts: dict, from_id: int, to_id: int, amount: float) -> tuple[bool, str]`.\n\n"
            "Словарь счетов: `{id: {'owner': str, 'balance': float}}`.\n"
            "Правила перевода:\n"
            "1. Сумма `amount` должна быть строго > 0. Если нет, вернуть `(False, 'Invalid transfer amount')`.\n"
            "2. Оба счета должны существовать в словаре. Если нет, вернуть `(False, 'Account not found')`.\n"
            "3. На счете `from_id` должно быть достаточно средств (`balance >= amount`). Если нет, вернуть `(False, 'Insufficient funds')`.\n"
            "4. Выполнить списание и зачисление атомарно и вернуть `(True, 'Transfer successful')`."
        ),
        "starterCode": (
            "def transfer_money(accounts: dict, from_id: int, to_id: int, amount: float) -> tuple[bool, str]:\n"
            "    # Ваше решение здесь\n"
            "    pass\n"
        ),
        "solutionCode": (
            "def transfer_money(accounts: dict, from_id: int, to_id: int, amount: float) -> tuple[bool, str]:\n"
            "    if amount <= 0:\n"
            "        return False, 'Invalid transfer amount'\n"
            "    if from_id not in accounts or to_id not in accounts:\n"
            "        return False, 'Account not found'\n"
            "    if accounts[from_id]['balance'] < amount:\n"
            "        return False, 'Insufficient funds'\n"
            "    # Атомарное обновление\n"
            "    accounts[from_id]['balance'] -= amount\n"
            "    accounts[to_id]['balance'] += amount\n"
            "    return True, 'Transfer successful'\n"
        ),
        "solutionExplanation": (
            "Мы предварительно валидируем все предусловия и только после этого атомарно изменяем балансы обоих счетов."
        ),
        "hints": [
            "Сначала проверьте валидность суммы `amount <= 0`.",
            "Затем проверьте наличие обоих счетов: `if from_id not in accounts or to_id not in accounts:`.",
            "Проверьте достаточность баланса: `if accounts[from_id]['balance'] < amount:`.",
            "Только после всех проверок измените оба баланса."
        ],
        "commonMistakes": [
            "Списать деньги до проверки существования счета получателя."
        ],
        "guide": {
            "walkthrough": [
                "Проверяем положительность суммы.",
                "Проверяем существование отправителя и получателя.",
                "Проверяем остаток на балансе.",
                "Списываем с отправителя и начисляем получателю."
            ],
            "terms": [
                {"name": "Transaction", "desc": "Неделимая группа операций с базой данных, выполняемая по принципу 'всё или ничего'."},
                {"name": "ACID", "desc": "Набор требований к надежности транзакций: Atomicity, Consistency, Isolation, Durability."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Успешный перевод 300 рублей между счетами",
                "expression": (
                    "accs = {1: {'owner': 'Алиса', 'balance': 1000.0}, 2: {'owner': 'Боб', 'balance': 200.0}}\n"
                    "ok, msg = transfer_money(accs, 1, 2, 300.0)\n"
                    "(ok, accs[1]['balance'], accs[2]['balance'])"
                ),
                "expected": [True, 700.0, 500.0]
            },
            {
                "id": "t2",
                "label": "Отказ при нехватке средств на счете",
                "expression": (
                    "accs = {1: {'owner': 'Алиса', 'balance': 100.0}, 2: {'owner': 'Боб', 'balance': 0.0}}\n"
                    "transfer_money(accs, 1, 2, 500.0)[1]"
                ),
                "expected": "Insufficient funds"
            },
            {
                "id": "t3",
                "label": "Отказ при неверной сумме",
                "expression": (
                    "accs = {1: {'balance': 100.0}, 2: {'balance': 0.0}}\n"
                    "transfer_money(accs, 1, 2, -50.0)[0]"
                ),
                "expected": False
            }
        ]
    },

    {
        "id": "backend-testing-pytest-api",
        "title": "Тестирование API с помощью pytest и TestClient",
        "order": 72,
        "language": "python",
        "level": "Junior+",
        "minutes": 15,
        "xp": 45,
        "theory": (
            "Без автоматических тестов бэкенд обречен на баги при любом изменении кода. "
            "В Python стандартом тестирования является библиотека **pytest** в связке с **TestClient** от FastAPI.\n\n"
            "`TestClient` позволяет отправлять HTTP-запросы в память вашего приложения без запуска реального сетевого сервера!\n"
            "```python\n"
            "from fastapi import FastAPI\n"
            "from fastapi.testclient import TestClient\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/items/{item_id}')\n"
            "def get_item(item_id: int):\n"
            "    return {'id': item_id, 'status': 'available'}\n\n"
            "def test_get_item():\n"
            "    client = TestClient(app)\n"
            "    response = client.get('/items/42')\n"
            "    assert response.status_code == 200\n"
            "    assert response.json() == {'id': 42, 'status': 'available'}\n"
            "```\n"
            "Инструкция `assert` проверяет утверждение: если оно ложно, тест падает и сообщает строку с ошибкой."
        ),
        "lifeExample": (
            "Автомобильный полигон. Перед тем как выпустить новую модель машины на дороги общего пользования, "
            "инженеры проводят краш-тесты, проверяют тормоза на льду и электронику. Тесты в коде — это ваш защитный полигон."
        ),
        "task": (
            "Напишите тестовую функцию `verify_calculator_api(app) -> bool`:\n"
            "Дано приложение `app`, у которого есть эндпоинт `GET /calc/add?a=10&b=20` (возвращает `{'result': 30}`).\n"
            "Ваша тестовая функция должна:\n"
            "1. Создать `client = TestClient(app)`.\n"
            "2. Отправить GET-запрос `client.get('/calc/add?a=15&b=25')`.\n"
            "3. Проверить через `assert response.status_code == 200`.\n"
            "4. Проверить через `assert response.json()['result'] == 40`.\n"
            "5. Вернуть `True`, если все проверки пройдены."
        ),
        "starterCode": (
            "from fastapi.testclient import TestClient\n\n"
            "def verify_calculator_api(app) -> bool:\n"
            "    # Напишите тесты с TestClient и assert\n"
            "    pass\n"
        ),
        "solutionCode": (
            "from fastapi.testclient import TestClient\n\n"
            "def verify_calculator_api(app) -> bool:\n"
            "    client = TestClient(app)\n"
            "    resp = client.get('/calc/add?a=15&b=25')\n"
            "    assert resp.status_code == 200, f'Expected 200, got {resp.status_code}'\n"
            "    data = resp.json()\n"
            "    assert data['result'] == 40, f'Expected 40, got {data.get(\"result\")}'\n"
            "    return True\n"
        ),
        "solutionExplanation": (
            "Мы инициализировали TestClient, выполнили запрос к API и проверили код статуса и тело ответа через assert."
        ),
        "hints": [
            "Инициализируйте клиента: `client = TestClient(app)`.",
            "Вызовите `resp = client.get('/calc/add?a=15&b=25')`.",
            "Проверьте код: `assert resp.status_code == 200`.",
            "Проверьте данные: `assert resp.json()['result'] == 40` и верните True."
        ],
        "commonMistakes": [
            "Забыть вызвать `.json()` у объекта response для чтения распарсенного словаря."
        ],
        "guide": {
            "walkthrough": [
                "Создаем TestClient для приложения.",
                "Отправляем тестовый запрос с параметрами.",
                "Проверяем статус-код и результат через assert.",
                "Возвращаем True при успехе."
            ],
            "terms": [
                {"name": "TestClient", "desc": "Инструмент тестирования FastAPI для отправки HTTP-запросов в память приложения."},
                {"name": "Assertion", "desc": "Утверждение в тесте, проверяющее истинность условия."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Тестирование корректного API калькулятора",
                "expression": (
                    "from fastapi import FastAPI\n"
                    "calc_app = FastAPI()\n"
                    "@calc_app.get('/calc/add')\n"
                    "def add(a: int, b: int): return {'result': a + b}\n"
                    "verify_calculator_api(calc_app)"
                ),
                "expected": True
            }
        ]
    },

    {
        "id": "backend-dockerfile-container",
        "title": "Контейнеризация: Создание Dockerfile для веб-сервиса",
        "order": 73,
        "language": "python",
        "level": "Junior+",
        "minutes": 15,
        "xp": 45,
        "theory": (
            "Классическая проблема разработки: «На моем компьютере всё работало, а на сервере упало!». "
            "Причины: другая версия Python, отсутствующие библиотеки или другие настройки системы.\n\n"
            "**Docker** решает эту проблему раз и навсегда. "
            "Он упаковывает ваше приложение, интерпретатор Python и все зависимости в единый изолированный образ (Image), "
            "который гарантированно запускается одинаково на любой машине (Windows, macOS, Linux, облако).\n\n"
            "Файл `Dockerfile` — это пошаговый рецепт сборки образа:\n"
            "1. `FROM python:3.12-slim` — базовый образ операционной системы с уже установленным Python 3.12.\n"
            "2. `WORKDIR /app` — создание и переход в рабочую папку внутри контейнера.\n"
            "3. `COPY requirements.txt .` — копирование списка зависимостей.\n"
            "4. `RUN pip install --no-cache-dir -r requirements.txt` — установка библиотек.\n"
            "5. `COPY . .` — копирование исходного кода проекта.\n"
            "6. `CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]` — команда запуска сервера."
        ),
        "lifeExample": (
            "Морской грузовой контейнер. Раньше грузы перевозили в бочках, мешках и ящиках разной формы, "
            "и при перегрузке они разбивались. Стандартизированный контейнер подходит к любому кораблю, поезду или крану в любой точке мира."
        ),
        "task": (
            "Напишите валидатор и генератор Dockerfile для Python микросервиса:\n"
            "`generate_fastapi_dockerfile(app_file: str, port: int = 8000) -> str`.\n\n"
            "Функция должна возвращать многострочный текст Dockerfile следующего вида:\n"
            "```dockerfile\n"
            "FROM python:3.12-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            "EXPOSE {port}\n"
            "CMD [\"uvicorn\", \"{app_file}:app\", \"--host\", \"0.0.0.0\", \"--port\", \"{port}\"]\n"
            "```"
        ),
        "starterCode": (
            "def generate_fastapi_dockerfile(app_file: str, port: int = 8000) -> str:\n"
            "    # Сформируйте текст Dockerfile\n"
            "    pass\n"
        ),
        "solutionCode": (
            "def generate_fastapi_dockerfile(app_file: str, port: int = 8000) -> str:\n"
            "    lines = [\n"
            "        'FROM python:3.12-slim',\n"
            "        'WORKDIR /app',\n"
            "        'COPY requirements.txt .',\n"
            "        'RUN pip install --no-cache-dir -r requirements.txt',\n"
            "        'COPY . .',\n"
            "        f'EXPOSE {port}',\n"
            "        f'CMD [\"uvicorn\", \"{app_file}:app\", \"--host\", \"0.0.0.0\", \"--port\", \"{port}\"]'\n"
            "    ]\n"
            "    return '\\n'.join(lines)\n"
        ),
        "solutionExplanation": (
            "Мы объединяем стандартные директивы Dockerfile в правильном порядке, учитывающем кэширование слоев сборщика."
        ),
        "hints": [
            "Сначала копируется `requirements.txt` и выполняется `RUN pip install`, чтобы использовать кэш Docker при изменении кода.",
            "В директиве CMD укажите команду Uvicorn с проброшенным портом и именем файла приложения.",
            "Объедините строки через `\\n`."
        ],
        "commonMistakes": [
            "Копировать весь проект до `pip install` (это ломает кэш сборки Docker, и библиотеки будут переустанавливаться при каждом изменении файла)."
        ],
        "guide": {
            "walkthrough": [
                "Задаем базовый образ и рабочую директорию.",
                "Копируем зависимости и запускаем установку.",
                "Копируем исходники, открываем порт и задаем CMD."
            ],
            "terms": [
                {"name": "Dockerfile", "desc": "Текстовый документ с набором команд для автоматической сборки образа контейнера."},
                {"name": "Image", "desc": "Неизменяемый снимок файловой системы и параметров, готовый для запуска в контейнере."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Проверка наличия директивы FROM",
                "expression": "'FROM python:3.12-slim' in generate_fastapi_dockerfile('main')",
                "expected": True
            },
            {
                "id": "t2",
                "label": "Проверка команды запуска CMD с портом 8080",
                "expression": "'--port\", \"8080\"' in generate_fastapi_dockerfile('api', 8080)",
                "expected": True
            },
            {
                "id": "t3",
                "label": "Проверка директивы EXPOSE",
                "expression": "'EXPOSE 8080' in generate_fastapi_dockerfile('api', 8080)",
                "expected": True
            }
        ]
    },

    {
        "id": "backend-docker-compose-infra",
        "title": "Оркестрация микросервисов с docker-compose",
        "order": 74,
        "language": "python",
        "level": "Junior+",
        "minutes": 15,
        "xp": 45,
        "theory": (
            "В реальных проектах бэкенд не работает в одиночку: ему нужна база данных (PostgreSQL), кэш (Redis) и очереди задач. "
            "Запускать каждый контейнер руками через `docker run` неудобно и долго.\n\n"
            "Инструмент **docker-compose** позволяет описать всю архитектуру проекта в одном файле `docker-compose.yml` "
            "и запустить все сервисы одной командой:\n"
            "`docker compose up -d`\n\n"
            "В файле задаются:\n"
            "• `services` — список микросервисов (например, `web` и `db`).\n"
            "• `ports` — маппинг портов с машины разработчика внутрь контейнера (`8000:8000`).\n"
            "• `environment` — переменные окружения (логин/пароль к базе, секретные ключи).\n"
            "• `volumes` — именованные тома для сохранения данных БД на жестком диске (чтобы данные не пропали при остановке контейнера)."
        ),
        "lifeExample": (
            "Симфонический оркестр. Отдельно скрипка и отдельно барабан звучат хорошо, но дирижёр объединяет всех музыкантов "
            "в единое согласованное произведение. docker-compose — это дирижер для группы контейнеров."
        ),
        "task": (
            "Реализуйте функцию генерации конфигурации docker-compose для связки FastAPI + PostgreSQL:\n"
            "`build_compose_manifest(app_port: int, db_port: int, db_name: str) -> dict`.\n\n"
            "Функция должна возвращать словарь со следующей структурой:\n"
            "```python\n"
            "{\n"
            "    'version': '3.8',\n"
            "    'services': {\n"
            "        'web': {\n"
            "            'build': '.',\n"
            "            'ports': [f'{app_port}:{app_port}'],\n"
            "            'depends_on': ['db'],\n"
            "            'environment': {\n"
            "                'DATABASE_URL': f'postgresql://postgres:secret@db:{db_port}/{db_name}'\n"
            "            }\n"
            "        },\n"
            "        'db': {\n"
            "            'image': 'postgres:16-alpine',\n"
            "            'ports': [f'{db_port}:5432'],\n"
            "            'environment': {\n"
            "                'POSTGRES_DB': db_name,\n"
            "                'POSTGRES_PASSWORD': 'secret'\n"
            "            },\n"
            "            'volumes': ['postgres_data:/var/lib/postgresql/data']\n"
            "        }\n"
            "    },\n"
            "    'volumes': {\n"
            "        'postgres_data': None\n"
            "    }\n"
            "}\n"
            "```"
        ),
        "starterCode": (
            "def build_compose_manifest(app_port: int, db_port: int, db_name: str) -> dict:\n"
            "    # Сформируйте конфигурационный словарь\n"
            "    pass\n"
        ),
        "solutionCode": (
            "def build_compose_manifest(app_port: int, db_port: int, db_name: str) -> dict:\n"
            "    return {\n"
            "        'version': '3.8',\n"
            "        'services': {\n"
            "            'web': {\n"
            "                'build': '.',\n"
            "                'ports': [f'{app_port}:{app_port}'],\n"
            "                'depends_on': ['db'],\n"
            "                'environment': {\n"
            "                    'DATABASE_URL': f'postgresql://postgres:secret@db:{db_port}/{db_name}'\n"
            "                }\n"
            "            },\n"
            "            'db': {\n"
            "                'image': 'postgres:16-alpine',\n"
            "                'ports': [f'{db_port}:5432'],\n"
            "                'environment': {\n"
            "                    'POSTGRES_DB': db_name,\n"
            "                    'POSTGRES_PASSWORD': 'secret'\n"
            "                },\n"
            "                'volumes': ['postgres_data:/var/lib/postgresql/data']\n"
            "            }\n"
            "        },\n"
            "        'volumes': {\n"
            "            'postgres_data': None\n"
            "        }\n"
            "    }\n"
        ),
        "solutionExplanation": (
            "Мы связали сервис приложения web и базу данных db через внутреннюю сеть Docker и настроили переменные окружения."
        ),
        "hints": [
            "Укажите `depends_on: ['db']` в сервисе `web`, чтобы сервер запускался после базы данных.",
            "В строке подключения DATABASE_URL хостом базы является имя сервиса `db`.",
            "Не забудьте секцию `volumes: {'postgres_data': None}`."
        ],
        "commonMistakes": [
            "Указывать `localhost` вместо `db` в DATABASE_URL (внутри сети Docker каждый сервис доступен по своему имени сервиса, а не по localhost)."
        ],
        "guide": {
            "walkthrough": [
                "Определяем версию спецификации compose 3.8.",
                "Конфигурируем сервис веб-приложения web с зависимостью от db.",
                "Конфигурируем сервис базы данных postgres с volume."
            ],
            "terms": [
                {"name": "docker-compose", "desc": "Инструмент для определения и запуска многоконтейнерных приложений Docker."},
                {"name": "Volume", "desc": "Механизм постоянного хранения данных контейнера вне его жизненного цикла."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Проверка зависимости web от db",
                "expression": "build_compose_manifest(8000, 5432, 'devforge')['services']['web']['depends_on']",
                "expected": ["db"]
            },
            {
                "id": "t2",
                "label": "Проверка URL базы данных",
                "expression": "build_compose_manifest(8000, 5432, 'production_db')['services']['web']['environment']['DATABASE_URL']",
                "expected": "postgresql://postgres:secret@db:5432/production_db"
            },
            {
                "id": "t3",
                "label": "Проверка тома для сохранения данных",
                "expression": "'postgres_data' in build_compose_manifest(8000, 5432, 'test')['volumes']",
                "expected": True
            }
        ]
    },

    # -----------------------------------------------------------------
    # Модуль 7. Итоговый проект (Capstone)
    # -----------------------------------------------------------------
    {
        "id": "backend-project-bank-api",
        "title": "Итоговый проект: API банковских счетов, балансов и переводов",
        "order": 75,
        "language": "python",
        "level": "Junior+",
        "minutes": 45,
        "xp": 100,
        "theory": (
            "Поздравляем с выходом на финишную прямую направления Backend Development!\n\n"
            "В этом курсовом проекте вы объедините все полученные навыки в полноценное законченное веб-приложение:\n"
            "1. **Моделирование данных**: Управление клиентами и счетами.\n"
            "2. **Авторизация**: Защита эндпоинтов через Bearer токен.\n"
            "3. **Транзакционность**: Атомарный перевод средств без возможности потери денег или ухода баланса в минус.\n"
            "4. **Обработка ошибок**: Возврат строгих HTTP-статусов (400, 401, 404).\n"
            "5. **Аудит и история**: Запись каждой выполненной транзакции с отметкой времени."
        ),
        "lifeExample": (
            "Реальный бэкенд необанка (Тинькофф, Точка, Revolut). "
            "Клиенты регистрируются, открывают счета в рублях и долларах, пополняют баланс и переводят деньги друзьям. "
            "Система работает безупречно, транзакции не теряются при любых сбоях."
        ),
        "task": (
            "Реализуйте класс банковского сервиса `BankApplication` со следующими методами:\n\n"
            "1. `register_user(username: str, password: str) -> str`:\n"
            "   • Если длина пароля < 6, выбросить `ValueError('Password too short')`.\n"
            "   • Генерирует и возвращает токен авторизации: `f'token_{username}'`.\n\n"
            "2. `open_account(token: str, currency: str = 'RUB', initial_deposit: float = 0.0) -> int`:\n"
            "   • Проверяет токен (должен начинаться на `'token_'`). Если невалиден, выбросить `PermissionError('Invalid token')`.\n"
            "   • Создает новый счет с уникальным числовым `account_id` (начиная с 1) и балансом `initial_deposit`.\n"
            "   • Возвращает `account_id`.\n\n"
            "3. `get_balance(token: str, account_id: int) -> float`:\n"
            "   • Проверяет токен (иначе `PermissionError`).\n"
            "   • Если счет не найден, выбросить `KeyError('Account not found')`.\n"
            "   • Возвращает текущий баланс счета.\n\n"
            "4. `transfer(token: str, from_id: int, to_id: int, amount: float) -> dict`:\n"
            "   • Проверяет токен (иначе `PermissionError`).\n"
            "   • `amount` должна быть > 0 (иначе `ValueError('Invalid amount')`).\n"
            "   • Оба счета должны существовать (иначе `KeyError('Account not found')`).\n"
            "   • Баланс `from_id` должен быть >= `amount` (иначе `ValueError('Insufficient funds')`).\n"
            "   • Списывает сумму с `from_id` и начисляет на `to_id`.\n"
            "   • Возвращает `{'status': 'success', 'from_id': from_id, 'to_id': to_id, 'amount': amount}`."
        ),
        "starterCode": (
            "class BankApplication:\n"
            "    def __init__(self):\n"
            "        self.tokens = set()\n"
            "        self.accounts = {}\n"
            "        self._next_id = 1\n\n"
            "    def register_user(self, username: str, password: str) -> str:\n"
            "        pass\n\n"
            "    def open_account(self, token: str, currency: str = 'RUB', initial_deposit: float = 0.0) -> int:\n"
            "        pass\n\n"
            "    def get_balance(self, token: str, account_id: int) -> float:\n"
            "        pass\n\n"
            "    def transfer(self, token: str, from_id: int, to_id: int, amount: float) -> dict:\n"
            "        pass\n"
        ),
        "solutionCode": (
            "class BankApplication:\n"
            "    def __init__(self):\n"
            "        self.tokens = set()\n"
            "        self.accounts = {}\n"
            "        self._next_id = 1\n\n"
            "    def register_user(self, username: str, password: str) -> str:\n"
            "        if len(password) < 6:\n"
            "            raise ValueError('Password too short')\n"
            "        token = f'token_{username}'\n"
            "        self.tokens.add(token)\n"
            "        return token\n\n"
            "    def _check_token(self, token: str):\n"
            "        if not token or token not in self.tokens:\n"
            "            raise PermissionError('Invalid token')\n\n"
            "    def open_account(self, token: str, currency: str = 'RUB', initial_deposit: float = 0.0) -> int:\n"
            "        self._check_token(token)\n"
            "        acc_id = self._next_id\n"
            "        self._next_id += 1\n"
            "        self.accounts[acc_id] = {'currency': currency, 'balance': float(initial_deposit)}\n"
            "        return acc_id\n\n"
            "    def get_balance(self, token: str, account_id: int) -> float:\n"
            "        self._check_token(token)\n"
            "        if account_id not in self.accounts:\n"
            "            raise KeyError('Account not found')\n"
            "        return self.accounts[account_id]['balance']\n\n"
            "    def transfer(self, token: str, from_id: int, to_id: int, amount: float) -> dict:\n"
            "        self._check_token(token)\n"
            "        if amount <= 0:\n"
            "            raise ValueError('Invalid amount')\n"
            "        if from_id not in self.accounts or to_id not in self.accounts:\n"
            "            raise KeyError('Account not found')\n"
            "        if self.accounts[from_id]['balance'] < amount:\n"
            "            raise ValueError('Insufficient funds')\n"
            "        self.accounts[from_id]['balance'] -= amount\n"
            "        self.accounts[to_id]['balance'] += amount\n"
            "        return {'status': 'success', 'from_id': from_id, 'to_id': to_id, 'amount': amount}\n"
        ),
        "solutionExplanation": (
            "Мы создали комплексный сервис с авторизацией по токенам, проверкой прав, открытием счетов и атомарными переводами."
        ),
        "hints": [
            "Сделайте вспомогательный метод `_check_token(token)`, проверяющий наличие токена в `self.tokens`.",
            "В `register_user` проверьте `len(password) < 6` и сохраните токен в `self.tokens`.",
            "В `transfer` проверьте положительность суммы, существование счетов и достаточность баланса перед списанием."
        ],
        "commonMistakes": [
            "Позволить выполнить операцию с невалидным токеном.",
            "Списать баланс со счета отправителя при ошибке на счете получателя."
        ],
        "guide": {
            "walkthrough": [
                "Инициализируем хранилище токенов и счетов.",
                "Реализуем регистрацию с валидацией пароля.",
                "Реализуем открытие счетов и проверку баланса.",
                "Реализуем атомарный перевод со всеми проверками безопасности."
            ],
            "terms": [
                {"name": "Capstone Project", "desc": "Итоговая выпускная практическая работа, подтверждающая квалификацию разработчика."},
                {"name": "Atomic Transfer", "desc": "Перевод денег, гарантирующий одновременное изменение балансов обоих участников без потери средств."}
            ]
        },
        "tests": [
            {
                "id": "t1",
                "label": "Регистрация, открытие счетов и проверка баланса",
                "expression": (
                    "app = BankApplication()\n"
                    "tok = app.register_user('alex', 'password123')\n"
                    "acc1 = app.open_account(tok, 'RUB', 1000.0)\n"
                    "app.get_balance(tok, acc1)"
                ),
                "expected": 1000.0
            },
            {
                "id": "t2",
                "label": "Атомарный перевод средств между счетами",
                "expression": (
                    "app = BankApplication()\n"
                    "tok = app.register_user('alex', 'password123')\n"
                    "acc1 = app.open_account(tok, 'RUB', 1000.0)\n"
                    "acc2 = app.open_account(tok, 'RUB', 0.0)\n"
                    "app.transfer(tok, acc1, acc2, 400.0)\n"
                    "(app.get_balance(tok, acc1), app.get_balance(tok, acc2))"
                ),
                "expected": [600.0, 400.0]
            },
            {
                "id": "t3",
                "label": "Отказ при попытке перевода без токена или с нехваткой средств",
                "expression": (
                    "app = BankApplication()\n"
                    "tok = app.register_user('alex', 'password123')\n"
                    "acc1 = app.open_account(tok, 'RUB', 100.0)\n"
                    "acc2 = app.open_account(tok, 'RUB', 0.0)\n"
                    "try:\n"
                    "    app.transfer(tok, acc1, acc2, 500.0)\n"
                    "    res = 'ok'\n"
                    "except ValueError:\n"
                    "    res = 'error'\n"
                    "res"
                ),
                "expected": "error"
            }
        ]
    }
]

def main():
    root = Path(__file__).resolve().parent.parent
    lessons_path = root / "content" / "lessons.json"
    tracks_path = root / "content" / "tracks.json"

    # 1. Update lessons.json: remove old confusing backend-* lessons and insert new ones
    lessons = json.loads(lessons_path.read_text(encoding="utf-8"))
    old_count = len(lessons)
    
    # Filter out old backend-* lessons
    filtered_lessons = [l for l in lessons if not l["id"].startswith("backend-")]
    
    # Append the new 19 crystal-clear backend lessons
    filtered_lessons.extend(BACKEND_LESSONS)
    
    # Verify uniqueness of IDs
    ids = [l["id"] for l in filtered_lessons]
    assert len(ids) == len(set(ids)), "Duplicate lesson IDs found!"

    lessons_path.write_text(json.dumps(filtered_lessons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated content/lessons.json: {old_count} -> {len(filtered_lessons)} lessons.")

    # 2. Update tracks.json for backend-development
    tracks = json.loads(tracks_path.read_text(encoding="utf-8"))
    for t in tracks:
        if t["id"] == "backend-development":
            t["modules"] = [
                {
                    "id": "backend-mod-http",
                    "title": "Модуль 1. Архитектура бэкенда и протокол HTTP",
                    "skills": ["Клиент-Серверная модель", "Анатомия HTTP", "Методы GET/POST/PUT/DELETE", "Статус-коды", "JSON и REST"],
                    "lessonIds": [
                        "backend-intro-client-server",
                        "backend-http-methods-status",
                        "backend-json-rest-api"
                    ]
                },
                {
                    "id": "backend-mod-fastapi",
                    "title": "Модуль 2. Основы веб-сервисов на FastAPI",
                    "skills": ["Создание FastAPI приложения", "Маршруты @app.get", "Параметры путей {id}", "Типизация и валидация", "Пагинация и Query"],
                    "lessonIds": [
                        "backend-fastapi-first-endpoint",
                        "backend-fastapi-path-params",
                        "backend-fastapi-query-params"
                    ]
                },
                {
                    "id": "backend-mod-pydantic",
                    "title": "Модуль 3. Валидация данных со схемами Pydantic",
                    "skills": ["Модели BaseModel", "Request Body", "Ограничения Field", "DTO и Response Models", "Защита от утечки паролей"],
                    "lessonIds": [
                        "backend-pydantic-schemas",
                        "backend-pydantic-validation"
                    ]
                },
                {
                    "id": "backend-mod-exceptions-di",
                    "title": "Модуль 4. Обработка ошибок и Dependency Injection",
                    "skills": ["HTTPException", "Guard Clauses", "Принцип Inversion of Control", "Depends", "Авторизация по токену"],
                    "lessonIds": [
                        "backend-fastapi-http-exceptions",
                        "backend-fastapi-dependency-injection"
                    ]
                },
                {
                    "id": "backend-mod-databases-orm",
                    "title": "Модуль 5. Базы данных и SQLAlchemy 2.0 ORM",
                    "skills": ["Реляционные БД", "Связи 1:N и Foreign Key", "Декларативные модели", "CRUD операции", "Паттерн get_db"],
                    "lessonIds": [
                        "backend-db-relational-design",
                        "backend-sqlalchemy-models",
                        "backend-sqlalchemy-crud",
                        "backend-fastapi-db-integration"
                    ]
                },
                {
                    "id": "backend-mod-transactions-docker",
                    "title": "Модуль 6. Транзакции, Тестирование и Docker",
                    "skills": ["Атомарность (ACID)", "Автотесты с pytest", "FastAPI TestClient", "Dockerfile", "Оркестрация docker-compose"],
                    "lessonIds": [
                        "backend-transactions-acid",
                        "backend-testing-pytest-api",
                        "backend-dockerfile-container",
                        "backend-docker-compose-infra"
                    ]
                },
                {
                    "id": "backend-mod-capstone",
                    "title": "Итоговый проект: Сервис банковских счетов и переводов",
                    "skills": ["Аутентификация по токену", "Управление счетами", "Атомарные переводы", "Защита от двойного списания", "Тестирование безопасности"],
                    "lessonIds": [
                        "backend-project-bank-api"
                    ]
                }
            ]

    tracks_path.write_text(json.dumps(tracks, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Updated content/tracks.json with new 7 modules and 19 lessons.")

if __name__ == "__main__":
    main()
