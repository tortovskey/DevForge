MORE_FRONTEND = '''
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
            "между компонентами и гарантирует, что данные, полученные с сервера, строго соответствуют контракту.\\n\\n"
            "Ключевые приёмы:\\n"
            "• Описание контракта интерфейса: interface ButtonProps { label: string; onClick: () => void; disabled?: boolean; }\\n"
            "• Обобщения (Generics): функция или контейнер может работать с любым типом данных, сохраняя проверку типов.\\n"
            "• Сужение типов (Type Narrowing) через дискриминантные объединения (Discriminated Unions)."
        ),
        "syntax": (
            "interface ApiResponse<T> {\\n"
            "  status: 'success' | 'error';\\n"
            "  data?: T;\\n"
            "  error?: string;\\n"
            "}\\n\\n"
            "function handleResponse<T>(res: ApiResponse<T>): T | null {\\n"
            "  if (res.status === 'success' && res.data) return res.data;\\n"
            "  return null;\\n"
            "}"
        ),
        "examples": [
            (
                "interface Item { id: number; name: string; }\\n"
                "function findItem<T extends { id: number }>(items: T[], id: number): T | undefined {\\n"
                "  return items.find(it => it.id === id);\\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте функцию `filterAndSort<T extends { id: number; title: string; price: number }>(items: T[], minPrice: number, ascending: boolean): T[]`\\n"
            "Требования:\\n"
            "1. Отфильтровать элементы, оставив только те, у которых `price >= minPrice`.\\n"
            "2. Отсортировать отфильтрованные элементы по полю `price`:\\n"
            "   • если `ascending === true` — по возрастанию цены;\\n"
            "   • если `ascending === false` — по убыванию цены.\\n"
            "3. Не мутировать исходный массив (возвращать новый массив)."
        ),
        "starterCode": (
            "interface ProductItem {\\n"
            "  id: number;\\n"
            "  title: string;\\n"
            "  price: number;\\n"
            "}\\n\\n"
            "function filterAndSort<T extends ProductItem>(items: T[], minPrice: number, ascending: boolean): T[] {\\n"
            "  // Ваш код здесь\\n"
            "  return [];\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Фильтрация по минимальной цене и сортировка по возрастанию",
                "expression": (
                    "const data = [\\n"
                    "  { id: 1, title: 'Книга', price: 500 },\\n"
                    "  { id: 2, title: 'Блокнот', price: 200 },\\n"
                    "  { id: 3, title: 'Ручка', price: 800 }\\n"
                    "];\\n"
                    "const res = filterAndSort(data, 300, true);\\n"
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
                "function filterAndSort<T extends { id: number; title: string; price: number }>(items: T[], minPrice: number, ascending: boolean): T[] {\\n"
                "  return items\\n"
                "    .filter(it => it.price >= minPrice)\\n"
                "    .sort((a, b) => ascending ? a.price - b.price : b.price - a.price);\\n"
                "}\\n"
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
            "Качественный фронтенд обязан учитывать все состояния запроса:\\n"
            "• `loading: true` — отображение скелетона или спиннера.\\n"
            "• `error: string` — вывод понятного сообщения, если сервер вернул 4xx/5xx статус или пропал интернет.\\n"
            "• `data: T` — отображение готового контента.\\n\\n"
            "При быстром вводе в поле поиска предыдущие запросы нужно отменять с помощью `AbortController`, "
            "чтобы не допустить состояния гонки (race condition)."
        ),
        "syntax": (
            "const controller = new AbortController();\\n"
            "fetch('/api/search?q=phone', { signal: controller.signal })\\n"
            "  .then(res => res.json())\\n"
            "  .catch(err => {\\n"
            "    if (err.name === 'AbortError') console.log('Запрос отменен');\\n"
            "  });\\n"
            "// Для отмены:\\n"
            "controller.abort();"
        ),
        "examples": [
            (
                "async function safeFetch(url) {\\n"
                "  const res = await fetch(url);\\n"
                "  if (!res.ok) throw new Error(`HTTP ${res.status}`);\\n"
                "  return await res.json();\\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `AsyncDataLoader`:\\n"
            "Конструктор принимает функцию `fetcherFn(param: string): Promise<any>`.\\n"
            "Методы:\\n"
            "1. `load(param: string): Promise<any>`:\\n"
            "   • переводит состояние в `{ status: 'loading', data: null, error: null }`;\\n"
            "   • вызывает `fetcherFn(param)`;\\n"
            "   • при успехе: сохраняет `{ status: 'success', data: result, error: null }` и возвращает результат;\\n"
            "   • при ошибке: сохраняет `{ status: 'error', data: null, error: err.message || String(err) }` и пробрасывает ошибку;\\n"
            "2. `getState()`: возвращает текущий объект состояния."
        ),
        "starterCode": (
            "class AsyncDataLoader {\\n"
            "  constructor(fetcherFn) {\\n"
            "    // Ваш код здесь\\n"
            "  }\\n"
            "  async load(param) {}\\n"
            "  getState() {}\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успешная загрузка данных",
                "expression": (
                    "const mock = async (p) => ({ greeting: `Hello, ${p}` });\\n"
                    "const loader = new AsyncDataLoader(mock);\\n"
                    "await loader.load('World');\\n"
                    "loader.getState()"
                ),
                "expected": {"status": "success", "data": {"greeting": "Hello, World"}, "error": None}
            },
            {
                "id": "t2",
                "label": "Обработка сетевой ошибки",
                "expression": (
                    "const mock = async () => { throw new Error('Network timeout'); };\\n"
                    "const loader = new AsyncDataLoader(mock);\\n"
                    "try { await loader.load('test'); } catch (e) {}\\n"
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
                "class AsyncDataLoader {\\n"
                "  constructor(fetcherFn) {\\n"
                "    this.fetcherFn = fetcherFn;\\n"
                "    this.state = { status: 'idle', data: null, error: null };\\n"
                "  }\\n"
                "  async load(param) {\\n"
                "    this.state = { status: 'loading', data: null, error: null };\\n"
                "    try {\\n"
                "      const result = await this.fetcherFn(param);\\n"
                "      this.state = { status: 'success', data: result, error: null };\\n"
                "      return result;\\n"
                "    } catch (err) {\\n"
                "      const msg = err.message || String(err);\\n"
                "      this.state = { status: 'error', data: null, error: msg };\\n"
                "      throw err;\\n"
                "    }\\n"
                "  }\\n"
                "  getState() {\\n"
                "    return { ...this.state };\\n"
                "  }\\n"
                "}\\n"
            )
        )
    }
'''

MORE_JAVA = '''
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
            "Обработка ошибок в Java строится на классах исключений (Exceptions):\\n"
            "• Checked (проверяемые, наследники Exception) — компилятор требует явно обработать через try-catch "
            "или объявить в сигнатуре метода через throws (например IOException, SQLException).\\n"
            "• Unchecked (непроверяемые, наследники RuntimeException) — ошибки логики программы (NullPointerException, IllegalArgumentException).\\n\\n"
            "Конструкция `try-with-resources` гарантирует автоматическое закрытие ресурсов (файлы, сетевые сокеты, соединения с БД), "
            "реализующих интерфейс `AutoCloseable`, даже если внутри блока возникла критическая ошибка."
        ),
        "syntax": (
            "public class InsufficientFundsException extends Exception {\\n"
            "    public InsufficientFundsException(String msg) { super(msg); }\\n"
            "}\\n\\n"
            "try (Connection conn = dataSource.getConnection()) {\\n"
            "    // ресурс conn закроется автоматически при выходе из блока\\n"
            "}"
        ),
        "examples": [
            (
                "public void validateAge(int age) {\\n"
                "    if (age < 18) throw new IllegalArgumentException(\\"Too young\\");\\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `SafeBankVault` со следующими возможностями:\\n"
            "1. Создайте проверяемое исключение `public static class OverdraftException extends Exception`.\\n"
            "2. В классе `SafeBankVault` реализуйте приватное поле `int balanceCents`. Конструктор принимает начальный баланс.\\n"
            "3. Метод `void withdraw(int amount) throws OverdraftException`:\\n"
            "   • если `amount <= 0` — бросает `IllegalArgumentException(\\"Amount must be positive\\")`;\\n"
            "   • если `balanceCents < amount` — бросает `OverdraftException(\\"Not enough balance\\")`;\\n"
            "   • иначе уменьшает баланс на `amount`.\\n"
            "4. Метод `int getBalance()`: возвращает текущий баланс.\\n\\n"
            "Проверьте работу в `main`, перехватив `OverdraftException` и выведя сообщение ошибки."
        ),
        "starterCode": (
            "public class Main {\\n"
            "    public static class OverdraftException extends Exception {\\n"
            "        public OverdraftException(String msg) { super(msg); }\\n"
            "    }\\n"
            "    public static class SafeBankVault {\\n"
            "        private int balanceCents;\\n"
            "        public SafeBankVault(int initial) { this.balanceCents = initial; }\\n"
            "        public void withdraw(int amount) throws OverdraftException {\\n"
            "            // реализация\\n"
            "        }\\n"
            "        public int getBalance() { return balanceCents; }\\n"
            "    }\\n"
            "    public static void main(String[] args) {\\n"
            "        SafeBankVault vault = new SafeBankVault(500);\\n"
            "        try {\\n"
            "            vault.withdraw(300);\\n"
            "            vault.withdraw(400); // вызовет OverdraftException\\n"
            "        } catch (OverdraftException e) {\\n"
            "            System.out.println(e.getMessage());\\n"
            "        }\\n"
            "        System.out.println(vault.getBalance());\\n"
            "    }\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Перехват OverdraftException и сохранение баланса",
                "expected": "Not enough balance\\n200"
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
                "public class Main {\\n"
                "    public static class OverdraftException extends Exception {\\n"
                "        public OverdraftException(String msg) { super(msg); }\\n"
                "    }\\n"
                "    public static class SafeBankVault {\\n"
                "        private int balanceCents;\\n"
                "        public SafeBankVault(int initial) { this.balanceCents = initial; }\\n"
                "        public void withdraw(int amount) throws OverdraftException {\\n"
                "            if (amount <= 0) throw new IllegalArgumentException(\\"Amount must be positive\\");\\n"
                "            if (balanceCents < amount) throw new OverdraftException(\\"Not enough balance\\");\\n"
                "            balanceCents -= amount;\\n"
                "        }\\n"
                "        public int getBalance() { return balanceCents; }\\n"
                "    }\\n"
                "    public static void main(String[] args) {\\n"
                "        SafeBankVault vault = new SafeBankVault(500);\\n"
                "        try {\\n"
                "            vault.withdraw(300);\\n"
                "            vault.withdraw(400);\\n"
                "        } catch (OverdraftException e) {\\n"
                "            System.out.println(e.getMessage());\\n"
                "        }\\n"
                "        System.out.println(vault.getBalance());\\n"
                "    }\\n"
                "}\\n"
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
            "@Entity\\n"
            "@Table(name = \\"users\\")\\n"
            "public class User {\\n"
            "    @Id\\n"
            "    @GeneratedValue(strategy = GenerationType.IDENTITY)\\n"
            "    private Long id;\\n"
            "    private String email;\\n"
            "}\\n\\n"
            "public interface UserRepository extends JpaRepository<User, Long> {\\n"
            "    Optional<User> findByEmail(String email);\\n"
            "}"
        ),
        "examples": [
            (
                "public interface TaskRepository {\\n"
                "    List<Task> findByStatusOrderByPriorityDesc(String status);\\n"
                "}"
            )
        ],
        "task": (
            "Смоделируйте сущность и репозиторий в классе `TaskRepositoryModel`:\\n"
            "Класс `Task` имеет поля: `Long id`, `String name`, `String category`, `int priority`.\\n"
            "Класс `TaskRepositoryModel` должен поддерживать методы:\\n"
            "1. `Task save(Task task)`: если id равен null или 0 — присваивает автоинкрементный id и сохраняет задачу; если id уже есть — обновляет задачу. Возвращает сохраненный объект.\\n"
            "2. `Task findById(Long id)`: возвращает задачу или null.\\n"
            "3. `List<Task> findByCategory(String category)`: возвращает все задачи указанной категории.\\n"
            "4. `long count()`: возвращает общее количество сохраненных задач.\\n\\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\\n\\n"
            "public class Main {\\n"
            "    public static class Task {\\n"
            "        public Long id;\\n"
            "        public String name;\\n"
            "        public String category;\\n"
            "        public int priority;\\n"
            "        public Task(Long id, String name, String category, int priority) {\\n"
            "            this.id = id; this.name = name; this.category = category; this.priority = priority;\\n"
            "        }\\n"
            "    }\\n"
            "    public static class TaskRepositoryModel {\\n"
            "        // реализация хранилища\\n"
            "    }\\n"
            "    public static void main(String[] args) {\\n"
            "        TaskRepositoryModel repo = new TaskRepositoryModel();\\n"
            "        Task t1 = repo.save(new Task(null, \\"Setup PostgreSQL\\", \\"database\\", 10));\\n"
            "        Task t2 = repo.save(new Task(null, \\"Write Liquibase\\", \\"database\\", 8));\\n"
            "        List<Task> dbTasks = repo.findByCategory(\\"database\\");\\n"
            "        System.out.println(repo.count() + \\" \\" + dbTasks.size() + \\" \\" + t1.id);\\n"
            "    }\\n"
            "}\\n"
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
                "import java.util.*;\\n"
                "import java.util.stream.*;\\n\\n"
                "public class Main {\\n"
                "    public static class Task {\\n"
                "        public Long id;\\n"
                "        public String name;\\n"
                "        public String category;\\n"
                "        public int priority;\\n"
                "        public Task(Long id, String name, String category, int priority) {\\n"
                "            this.id = id; this.name = name; this.category = category; this.priority = priority;\\n"
                "        }\\n"
                "    }\\n"
                "    public static class TaskRepositoryModel {\\n"
                "        private Map<Long, Task> store = new LinkedHashMap<>();\\n"
                "        private long nextId = 1;\\n"
                "        public Task save(Task t) {\\n"
                "            if (t.id == null || t.id == 0) {\\n"
                "                t.id = nextId++;\\n"
                "            }\\n"
                "            store.put(t.id, t);\\n"
                "            return t;\\n"
                "        }\\n"
                "        public Task findById(Long id) { return store.get(id); }\\n"
                "        public List<Task> findByCategory(String cat) {\\n"
                "            return store.values().stream()\\n"
                "                .filter(x -> Objects.equals(x.category, cat))\\n"
                "                .collect(Collectors.toList());\\n"
                "        }\\n"
                "        public long count() { return store.size(); }\\n"
                "    }\\n"
                "    public static void main(String[] args) {\\n"
                "        TaskRepositoryModel repo = new TaskRepositoryModel();\\n"
                "        Task t1 = repo.save(new Task(null, \\"Setup PostgreSQL\\", \\"database\\", 10));\\n"
                "        Task t2 = repo.save(new Task(null, \\"Write Liquibase\\", \\"database\\", 8));\\n"
                "        List<Task> dbTasks = repo.findByCategory(\\"database\\");\\n"
                "        System.out.println(repo.count() + \\" \\" + dbTasks.size() + \\" \\" + t1.id);\\n"
                "    }\\n"
                "}\\n"
            )
        )
    }
'''

# Read curriculum_tracks.py and insert into the lists
with open('scripts/curriculum_tracks.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Insert MORE_FRONTEND before the closing bracket of FRONTEND_LESSONS
# Insert MORE_JAVA before the closing bracket of JAVA_LESSONS
idx_fe = code.find('FRONTEND_LESSONS = [')
idx_fe_end = code.find(']', idx_fe)
code = code[:idx_fe_end] + ',' + MORE_FRONTEND + '\n' + code[idx_fe_end:]

idx_java = code.find('JAVA_LESSONS = [')
idx_java_end = code.rfind(']')
code = code[:idx_java_end] + ',' + MORE_JAVA + '\n' + code[idx_java_end:]

with open('scripts/curriculum_tracks.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully injected all remaining track lessons!")
