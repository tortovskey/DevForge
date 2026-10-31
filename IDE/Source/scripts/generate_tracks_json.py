import json

TRACKS = [
    {
        "id": "backend-development",
        "title": "Backend Development",
        "kicker": "Python · FastAPI · PostgreSQL · SQLAlchemy · Docker",
        "description": "Полный путь бэкенд-разработчика: от синтаксиса Python и клиент-серверной архитектуры до проектирования реляционных БД в PostgreSQL, ORM SQLAlchemy, автоматического тестирования в pytest и деплоя в Docker контейнерах.",
        "targetRole": "Junior+ Backend Developer",
        "level": "С нуля до самостоятельного API",
        "icon": "database",
        "badge": "ВЫСОКИЙ СПРОС",
        "stack": ["Python 3.12", "FastAPI", "PostgreSQL", "SQLAlchemy ORM", "pytest", "Docker", "Git", "REST API"],
        "modules": [
            {
                "id": "py-foundations",
                "title": "Модуль 1. Python для Backend: основы и структуры данных",
                "skills": ["Типы данных", "Функции", "Коллекции (dict, set, list)", "ООП и классы", "Генераторы и декораторы"],
                "lessonIds": [
                    "python-first-print", "python-variables", "python-arithmetic", "python-functions",
                    "python-conditions", "python-loops", "python-lists", "python-dictionaries",
                    "python-classes", "python-exceptions", "python-generators", "python-decorators",
                    "python-dataclass", "python-async"
                ]
            },
            {
                "id": "client-server-http",
                "title": "Модуль 2. Клиент-серверная модель, протокол HTTP и REST",
                "skills": ["HTTP методы", "Статус-коды", "Заголовки и тело", "Сериализация JSON", "Архитектура REST"],
                "lessonIds": [
                    "python-json", "backend-http-rest"
                ]
            },
            {
                "id": "fastapi-framework",
                "title": "Модуль 3. Разработка API на FastAPI",
                "skills": ["Маршрутизация", "Схемы Pydantic", "Валидация типов", "Dependency Injection (Depends)", "HTTPException"],
                "lessonIds": [
                    "backend-fastapi-models", "backend-fastapi-routes", "backend-fastapi-depends"
                ]
            },
            {
                "id": "postgres-relational",
                "title": "Модуль 4. Реляционные базы данных и PostgreSQL",
                "skills": ["DDL/DML", "Связи и внешние ключи", "JOIN и агрегаты", "Индексы", "Транзакции и ACID"],
                "lessonIds": [
                    "postgresql-first", "postgresql-returning", "postgresql-left-join",
                    "postgresql-transaction", "postgresql-upsert", "postgresql-normalization"
                ]
            },
            {
                "id": "sqlalchemy-orm",
                "title": "Модуль 5. Слой данных: SQLAlchemy ORM и транзакции",
                "skills": ["Модели данных", "Паттерн Репозиторий", "Сессии и запросы", "Атомарные переводы"],
                "lessonIds": [
                    "backend-sqlalchemy-orm", "backend-sqlalchemy-relations"
                ]
            },
            {
                "id": "testing-docker",
                "title": "Модуль 6. Автоматическое тестирование и Docker",
                "skills": ["pytest фикстуры", "Изоляция тестовых данных", "Dockerfile", "docker-compose.yml"],
                "lessonIds": [
                    "backend-pytest-fixtures", "backend-docker-compose"
                ]
            },
            {
                "id": "backend-capstone",
                "title": "Итоговый проект: Сервис банковских счетов и переводов",
                "skills": ["Аутентификация по токену", "Управление балансом", "Атомарные транзакции", "Пагинация истории"],
                "lessonIds": [
                    "backend-project-bank-api"
                ]
            }
        ],
        "capstone": {
            "id": "backend-project-bank-api",
            "title": "API управления счетами и переводами",
            "description": "Полноценный микросервис: регистрация и авторизация по токену, создание мультивалютных счетов, атомарные переводы средств с транзакционной гарантией, фильтрация истории операций и пагинация.",
            "deliverables": [
                "Класс BankApplication с защищенными эндпоинтами",
                "Атомарные переводы с защитой от двойного списания",
                "Автоматические тесты сценариев валидации и безопасности",
                "Конфигурация Dockerfile и docker-compose для запуска связки FastAPI + PostgreSQL"
            ]
        }
    },
    {
        "id": "frontend-development",
        "title": "Frontend Development",
        "kicker": "HTML · CSS · JavaScript · TypeScript · React",
        "description": "Современная фронтенд-разработка: доступная семантическая вёрстка (a11y), адаптивные сетки Flexbox и Grid, асинхронный JavaScript (Event Loop, Promises), типизация в TypeScript и компонентный подход React с хуками и управлением состоянием.",
        "targetRole": "Junior+ Frontend Developer",
        "level": "С нуля до интерактивных веб-приложений",
        "icon": "code",
        "badge": "ПОПУЛЯРНЫЙ",
        "stack": ["HTML5", "CSS3 / Grid / Flexbox", "JavaScript (ES6+)", "TypeScript", "React", "React Hooks", "Vite", "REST Client"],
        "modules": [
            {
                "id": "html-css-layout",
                "title": "Модуль 1. Семантический HTML5 и современный CSS",
                "skills": ["Семантические теги", "Формы и валидация", "Блочная модель", "Flexbox", "CSS Grid", "Медиа-запросы"],
                "lessonIds": [
                    "html-css-first", "html-css-structure", "html-css-semantics", "html-css-form",
                    "html-css-flex", "html-css-grid", "html-css-responsive", "html-css-focus"
                ]
            },
            {
                "id": "js-core-async",
                "title": "Модуль 2. JavaScript Core и асинхронность",
                "skills": ["Переменные и типы", "Массивы и методы (map, filter, reduce)", "Деструктуризация", "Promises и async/await", "Event Delegation"],
                "lessonIds": [
                    "javascript-first-console", "javascript-functions", "javascript-arrow",
                    "javascript-map", "javascript-filter", "javascript-reduce", "javascript-classes",
                    "frontend-js-async-promises", "frontend-js-dom-events"
                ]
            },
            {
                "id": "ts-typing",
                "title": "Модуль 3. TypeScript для Frontend",
                "skills": ["Аннотации типов", "Интерфейсы", "Generic-типы", "Типизация Props", "Сужение типов"],
                "lessonIds": [
                    "typescript-first-type", "typescript-interfaces", "typescript-generics-interface",
                    "frontend-ts-frontend-props"
                ]
            },
            {
                "id": "react-hooks",
                "title": "Модуль 4. React: компоненты, формы и хуки",
                "skills": ["Компонентный подход", "useState и контролируемые формы", "Валидация полей ввода", "useMemo и useReducer"],
                "lessonIds": [
                    "frontend-react-hooks-state", "frontend-react-hooks-advanced"
                ]
            },
            {
                "id": "network-fetch",
                "title": "Модуль 5. Сетевые запросы и обработка состояний",
                "skills": ["fetch API", "Обработка загрузки и ошибок", "AbortController", "Скелетоны и индикаторы"],
                "lessonIds": [
                    "frontend-network-fetch"
                ]
            },
            {
                "id": "frontend-capstone",
                "title": "Итоговый проект: Каталог товаров и оформление заказа",
                "skills": ["Поиск и фильтры", "Корзина с пересчетом скидок", "Оформление заказа", "Валидация адреса и контактов"],
                "lessonIds": [
                    "frontend-project-catalog-cart"
                ]
            }
        ],
        "capstone": {
            "id": "frontend-project-catalog-cart",
            "title": "Интерактивный каталог товаров с корзиной и оформлением заказа",
            "description": "Полноценный клиент интернет-магазина: каталог с живым поиском и сортировкой по цене, пагинация карточек, хранилище корзины с промокодами и расчетом скидок, валидация формы заказа и подтверждение покупки.",
            "deliverables": [
                "Класс StoreApplication с управлением каталогом и корзиной",
                "Полнофункциональный поиск, фильтрация по категории и сортировка",
                "Интерактивная корзина с динамическим пересчетом скидок",
                "Форма заказа с проверкой валидности данных покупателя"
            ]
        }
    },
    {
        "id": "java-development",
        "title": "Java Development",
        "kicker": "JDK · JVM · OOP · Collections · Streams · Spring Boot · JPA",
        "description": "Промышленная разработка на Java: архитектура виртуальной машины JVM, строгая объектно-ориентированная парадигма, фреймворк коллекций, Stream API, обработка исключений, базы данных JDBC и разработка корпоративных REST API на Spring Boot и Spring Data JPA.",
        "targetRole": "Junior+ Java Software Engineer",
        "level": "С основ языка до корпоративного бэкенда",
        "icon": "terminal",
        "badge": "КОРПОРАТИВНЫЙ СТАНДАРТ",
        "stack": ["Java 17/21", "JVM Internals", "Collections Framework", "Stream API", "JUnit 5", "Spring Boot", "Spring Data JPA", "Maven / Gradle"],
        "modules": [
            {
                "id": "java-core-oop",
                "title": "Модуль 1. Основы языка Java и ООП",
                "skills": ["Типы и память (Stack vs Heap)", "Управляющие конструкции", "Классы и объекты", "Инкапсуляция", "Наследование и полиморфизм"],
                "lessonIds": [
                    "java-first-main", "java-variables", "java-arithmetic", "java-strings",
                    "java-if-else", "java-for-while", "java-arrays", "java-methods",
                    "java-classes", "java-encapsulation", "java-inheritance"
                ]
            },
            {
                "id": "java-collections-generics",
                "title": "Модуль 2. Коллекции и безопасность типов",
                "skills": ["List (ArrayList)", "Map (HashMap)", "Set (HashSet)", "Generics", "Сложность O(1) vs O(N)"],
                "lessonIds": [
                    "java-collections-list-map"
                ]
            },
            {
                "id": "java-robustness-streams",
                "title": "Модуль 3. Исключения и функциональное программирование",
                "skills": ["Checked vs Unchecked", "Кастомные ошибки", "try-with-resources", "Stream API (filter, map, collect)", "Лямбда-выражения"],
                "lessonIds": [
                    "java-exceptions-try-resources", "java-stream-api"
                ]
            },
            {
                "id": "spring-boot-backend",
                "title": "Модуль 4. Разработка REST API на Spring Boot",
                "skills": ["@RestController", "Dependency Injection / IoC", "Обработка HTTP методов", "Валидация входных моделей"],
                "lessonIds": [
                    "java-spring-boot-controller"
                ]
            },
            {
                "id": "spring-data-jpa-module",
                "title": "Модуль 5. Слой данных: Spring Data JPA и ORM",
                "skills": ["@Entity и @Table", "Генерация первичных ключей", "Интерфейс JpaRepository", "CRUD-методы"],
                "lessonIds": [
                    "java-spring-data-jpa"
                ]
            },
            {
                "id": "java-capstone",
                "title": "Итоговый проект: Корпоративный REST API управления задачами",
                "skills": ["CRUD сущностей", "Валидация полей", "Фильтрация и пагинация", "Обработка ошибок 400/404"],
                "lessonIds": [
                    "java-project-enterprise-api"
                ]
            }
        ],
        "capstone": {
            "id": "java-project-enterprise-api",
            "title": "Enterprise REST API сервиса задач и ресурсов",
            "description": "Полноценный микросервис на Spring Boot: моделирование сущностей с валидацией полей, CRUD-операции через репозиторий, фильтрация по статусу, пагинация страниц (page/size), централизованная обработка ошибок с единообразными кодами ответов.",
            "deliverables": [
                "Класс EnterpriseTaskManager с полным циклом управления задачами",
                "Валидация входящих данных и предотвращение недопустимых статусов",
                "Пагинация и фильтрация с помощью Stream API",
                "Обработка ошибок с понятными сообщениями и кодами"
            ]
        }
    }
]

with open('content/tracks.json', 'w', encoding='utf-8') as f:
    json.dump(TRACKS, f, indent=2, ensure_ascii=False)

print(f"Generated content/tracks.json with {len(TRACKS)} tracks!")
