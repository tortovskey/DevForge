import os

FRONTEND_CONTENT = '''
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
            "пользовательский интерфейс не должен зависать. В JavaScript за это отвечает Event Loop и промисы (Promises).\\n\\n"
            "Состояния промиса:\\n"
            "• pending — ожидание результата.\\n"
            "• fulfilled — успешное завершение (вызов resolve).\\n"
            "• rejected — ошибка (вызов reject).\\n\\n"
            "Синтаксис async/await позволяет писать асинхронный код линейно, перехватывая ошибки через привычный try...catch."
        ),
        "syntax": (
            "async function loadData(url) {\\n"
            "  try {\\n"
            "    const res = await fetch(url);\\n"
            "    return await res.json();\\n"
            "  } catch (err) {\\n"
            "    console.error('Network error:', err);\\n"
            "  }\\n"
            "}"
        ),
        "examples": [
            (
                "function wait(ms) {\\n"
                "  return new Promise(resolve => setTimeout(resolve, ms));\\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте асинхронную функцию `retryOperation(operationFn, maxAttempts)`\\n"
            "Она должна выполнять переданную функцию `operationFn()` (которая возвращает промис):\\n"
            "1. Если операция выполнилась успешно — возвращать результат операции.\\n"
            "2. Если операция выбросила ошибку, а количество сделанных попыток меньше `maxAttempts` — пробовать снова.\\n"
            "3. Если попытки исчерпаны — пробрасывать последнюю ошибку наружу через throw."
        ),
        "starterCode": (
            "async function retryOperation(operationFn, maxAttempts) {\\n"
            "  // Ваш код здесь\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Успех с первой попытки",
                "expression": (
                    "let calls = 0;\\n"
                    "const op = async () => { calls++; return 'success'; };\\n"
                    "await retryOperation(op, 3)"
                ),
                "expected": "success"
            },
            {
                "id": "t2",
                "label": "Успех со второй попытки",
                "expression": (
                    "let calls = 0;\\n"
                    "const op = async () => {\\n"
                    "  calls++;\\n"
                    "  if (calls < 2) throw new Error('Network glitch');\\n"
                    "  return 'recovered';\\n"
                    "};\\n"
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
                "async function retryOperation(operationFn, maxAttempts) {\\n"
                "  let lastError;\\n"
                "  for (let attempt = 1; attempt <= maxAttempts; attempt++) {\\n"
                "    try {\\n"
                "      return await operationFn();\\n"
                "    } catch (err) {\\n"
                "      lastError = err;\\n"
                "      if (attempt === maxAttempts) throw lastError;\\n"
                "    }\\n"
                "  }\\n"
                "}\\n"
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
            "container.addEventListener('click', (event) => {\\n"
            "  const btn = event.target.closest('[data-action]');\\n"
            "  if (!btn) return;\\n"
            "  const action = btn.dataset.action;\\n"
            "  const id = btn.dataset.id;\\n"
            "});"
        ),
        "examples": [
            (
                "function parseDataset(element) {\\n"
                "  return element.dataset.action || null;\\n"
                "}"
            )
        ],
        "task": (
            "Реализуйте функцию `dispatchCartAction(eventTargetData, handlers)`:\\n"
            "Она принимает объект кликнутого элемента `eventTargetData = { action: string, id: number, quantity?: number }` "
            "и объект с коллбэками `handlers = { onIncrease(id), onDecrease(id), onRemove(id) }`.\\n"
            "• При action === 'increase' — вызывает `handlers.onIncrease(id)` и возвращает результат.\\n"
            "• При action === 'decrease' — вызывает `handlers.onDecrease(id)` и возвращает результат.\\n"
            "• При action === 'remove' — вызывает `handlers.onRemove(id)` и возвращает результат.\\n"
            "• При неизвестном действии — возвращает null."
        ),
        "starterCode": (
            "function dispatchCartAction(targetData, handlers) {\\n"
            "  // Ваш код здесь\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Увеличение количества товара",
                "expression": (
                    "let incId = null;\\n"
                    "const h = { onIncrease: (id) => { incId = id; return 'inc-done'; } };\\n"
                    "const res = dispatchCartAction({ action: 'increase', id: 42 }, h);\\n"
                    "[res, incId]"
                ),
                "expected": ["inc-done", 42]
            },
            {
                "id": "t2",
                "label": "Удаление товара",
                "expression": (
                    "let remId = null;\\n"
                    "const h = { onRemove: (id) => { remId = id; return 'rem-done'; } };\\n"
                    "const res = dispatchCartAction({ action: 'remove', id: 99 }, h);\\n"
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
                "function dispatchCartAction(targetData, handlers) {\\n"
                "  if (!targetData || !targetData.action) return null;\\n"
                "  switch (targetData.action) {\\n"
                "    case 'increase':\\n"
                "      return handlers.onIncrease ? handlers.onIncrease(targetData.id) : null;\\n"
                "    case 'decrease':\\n"
                "      return handlers.onDecrease ? handlers.onDecrease(targetData.id) : null;\\n"
                "    case 'remove':\\n"
                "      return handlers.onRemove ? handlers.onRemove(targetData.id) : null;\\n"
                "    default:\\n"
                "      return null;\\n"
                "  }\\n"
                "}\\n"
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
            "а обновление происходит в обработчике `onChange`.\\n\\n"
            "Паттерн управления формой включает:\\n"
            "• Объект значений `values`.\\n"
            "• Объект ошибок `errors` (например `{ email: 'Некорректный email' }`).\\n"
            "• Флаг готовности `isValid` (true, когда нет ошибок и все обязательные поля заполнены)."
        ),
        "syntax": (
            "const [values, setValues] = useState({ name: '', email: '' });\\n"
            "const [errors, setErrors] = useState({});"
        ),
        "examples": [
            (
                "function validateEmail(email) {\\n"
                "  return email.includes('@') && email.includes('.');\\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `FormStateManager` для управления состоянием формы заказа:\\n"
            "Конструктор принимает `initialValues: { name: string, email: string, address: string }`.\\n"
            "Методы:\\n"
            "1. `setValue(fieldName, value)`: обновляет значение поля и автоматически валидирует его.\\n"
            "2. `getValues()`: возвращает текущий объект значений.\\n"
            "3. `getErrors()`: возвращает текущий объект ошибок.\\n"
            "4. `isValid()`: возвращает true, если ошибок нет и все три поля не пустые (после trim()).\\n\\n"
            "Правила валидации:\\n"
            "• name: длина от 2 символов (иначе ошибка 'Имя слишком короткое').\\n"
            "• email: содержит '@' и '.' (иначе 'Некорректный email').\\n"
            "• address: длина от 5 символов (иначе 'Укажите полный адрес')."
        ),
        "starterCode": (
            "class FormStateManager {\\n"
            "  constructor(initialValues) {\\n"
            "    // Ваш код здесь\\n"
            "  }\\n"
            "  setValue(fieldName, value) {}\\n"
            "  getValues() {}\\n"
            "  getErrors() {}\\n"
            "  isValid() {}\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Валидация корректной формы",
                "expression": (
                    "const f = new FormStateManager({ name: 'Анна', email: 'anna@mail.ru', address: 'ул. Ленина, 10' });\\n"
                    "[f.isValid(), Object.keys(f.getErrors()).length]"
                ),
                "expected": [true, 0]
            },
            {
                "id": "t2",
                "label": "Обнаружение ошибки в email",
                "expression": (
                    "const f = new FormStateManager({ name: 'Иван', email: 'bad-email', address: 'г. Москва, Арбат' });\\n"
                    "[f.isValid(), f.getErrors().email]"
                ),
                "expected": [false, "Некорректный email"]
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
                "class FormStateManager {\\n"
                "  constructor(initialValues = {}) {\\n"
                "    this.values = { name: '', email: '', address: '', ...initialValues };\\n"
                "    this.errors = {};\\n"
                "    this.validateAll();\\n"
                "  }\\n"
                "  validateField(field, val) {\\n"
                "    const v = (val || '').trim();\\n"
                "    if (field === 'name') {\\n"
                "      if (v.length < 2) return 'Имя слишком короткое';\\n"
                "    } else if (field === 'email') {\\n"
                "      if (!v.includes('@') || !v.includes('.')) return 'Некорректный email';\\n"
                "    } else if (field === 'address') {\\n"
                "      if (v.length < 5) return 'Укажите полный адрес';\\n"
                "    }\\n"
                "    return null;\\n"
                "  }\\n"
                "  validateAll() {\\n"
                "    this.errors = {};\\n"
                "    for (const f of ['name', 'email', 'address']) {\\n"
                "      const err = this.validateField(f, this.values[f]);\\n"
                "      if (err) this.errors[f] = err;\\n"
                "    }\\n"
                "  }\\n"
                "  setValue(field, val) {\\n"
                "    this.values[field] = val;\\n"
                "    const err = this.validateField(field, val);\\n"
                "    if (err) this.errors[field] = err;\\n"
                "    else delete this.errors[field];\\n"
                "  }\\n"
                "  getValues() { return { ...this.values }; }\\n"
                "  getErrors() { return { ...this.errors }; }\\n"
                "  isValid() {\\n"
                "    return Object.keys(this.errors).length === 0 &&\\n"
                "      Boolean(this.values.name?.trim() && this.values.email?.trim() && this.values.address?.trim());\\n"
                "  }\\n"
                "}\\n"
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
            "const totals = useMemo(() => {\\n"
            "  return items.reduce((acc, item) => acc + item.price * item.quantity, 0);\\n"
            "}, [items]);"
        ),
        "examples": [
            (
                "function sumItems(items) {\\n"
                "  return items.reduce((sum, x) => sum + x.price * x.qty, 0);\\n"
                "}"
            )
        ],
        "task": (
            "Создайте класс `CartManager` со следующими методами:\\n"
            "1. `addItem(product: { id: number, name: string, price: number }, qty: number = 1)`:\\n"
            "   • Если товар уже есть в корзине — увеличивает его количество `qty`.\\n"
            "   • Если товара нет — добавляет `{ ...product, quantity: qty }`.\\n"
            "2. `updateQuantity(productId: number, qty: number)`:\\n"
            "   • Если `qty <= 0` — удаляет товар из корзины.\\n"
            "   • Иначе устанавливает количество `quantity = qty`.\\n"
            "3. `removeItem(productId: number)`: удаляет товар.\\n"
            "4. `applyPromo(code: string)`: если code === 'DEVFORGE10' — активирует скидку 10% (0.10).\\n"
            "5. `getSummary() -> { items: array, subtotal: number, discount: number, total: number }`:\\n"
            "   • subtotal — сумма всех товаров (price * quantity).\\n"
            "   • discount — величина скидки (subtotal * discountRate, округленная до целого Math.round).\\n"
            "   • total — subtotal - discount."
        ),
        "starterCode": (
            "class CartManager {\\n"
            "  constructor() {\\n"
            "    // Ваш код здесь\\n"
            "  }\\n"
            "  addItem(product, qty = 1) {}\\n"
            "  updateQuantity(id, qty) {}\\n"
            "  removeItem(id) {}\\n"
            "  applyPromo(code) {}\\n"
            "  getSummary() {}\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Добавление и пересчет корзины",
                "expression": (
                    "const cart = new CartManager();\\n"
                    "cart.addItem({ id: 1, name: 'Клавиатура', price: 3000 }, 1);\\n"
                    "cart.addItem({ id: 1, name: 'Клавиатура', price: 3000 }, 1);\\n"
                    "cart.addItem({ id: 2, name: 'Мышь', price: 1500 }, 1);\\n"
                    "const s = cart.getSummary();\\n"
                    "[s.items.length, s.subtotal, s.total]"
                ),
                "expected": [2, 7500, 7500]
            },
            {
                "id": "t2",
                "label": "Применение промокода на 10%",
                "expression": (
                    "const cart = new CartManager();\\n"
                    "cart.addItem({ id: 1, name: 'Монитор', price: 20000 }, 1);\\n"
                    "cart.applyPromo('DEVFORGE10');\\n"
                    "const s = cart.getSummary();\\n"
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
                "class CartManager {\\n"
                "  constructor() {\\n"
                "    this.items = [];\\n"
                "    this.discountRate = 0;\\n"
                "  }\\n"
                "  addItem(product, qty = 1) {\\n"
                "    const existing = this.items.find(x => x.id === product.id);\\n"
                "    if (existing) {\\n"
                "      existing.quantity += qty;\\n"
                "    } else {\\n"
                "      this.items.push({ ...product, quantity: qty });\\n"
                "    }\\n"
                "  }\\n"
                "  updateQuantity(id, qty) {\\n"
                "    if (qty <= 0) {\\n"
                "      this.removeItem(id);\\n"
                "    } else {\\n"
                "      const it = this.items.find(x => x.id === id);\\n"
                "      if (it) it.quantity = qty;\\n"
                "    }\\n"
                "  }\\n"
                "  removeItem(id) {\\n"
                "    this.items = this.items.filter(x => x.id !== id);\\n"
                "  }\\n"
                "  applyPromo(code) {\\n"
                "    if (code === 'DEVFORGE10') this.discountRate = 0.10;\\n"
                "  }\\n"
                "  getSummary() {\\n"
                "    const subtotal = this.items.reduce((sum, it) => sum + it.price * it.quantity, 0);\\n"
                "    const discount = Math.round(subtotal * this.discountRate);\\n"
                "    return {\\n"
                "      items: this.items.map(it => ({ ...it })),\\n"
                "      subtotal,\\n"
                "      discount,\\n"
                "      total: subtotal - discount\\n"
                "    };\\n"
                "  }\\n"
                "}\\n"
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
            "Итоговый проект объединяет весь стек Frontend-разработки:\\n"
            "• Интерактивный каталог товаров с поиском по названию и фильтрацией по категории.\\n"
            "• Сортировка по цене (по возрастанию / убыванию) и пагинация страниц.\\n"
            "• Полноценная корзина с изменением количества и удалением позиций.\\n"
            "• Оформление заказа с валидацией контактных данных и адреса доставки.\\n"
            "• Формирование готового объекта заказа для отправки на backend."
        ),
        "syntax": (
            "class StoreApp {\\n"
            "  filterCatalog(query, category, sortOrder, page, pageSize) { ... }\\n"
            "  addToCart(productId, qty) { ... }\\n"
            "  checkout(customerData) { ... }\\n"
            "}"
        ),
        "examples": [
            (
                "const app = new StoreApp(mockProducts);\\n"
                "const catalogView = app.filterCatalog('ноутбук', 'all', 'price-asc', 1, 10);\\n"
                "app.addToCart(1, 1);\\n"
                "const order = app.checkout({ name: 'Иван', email: 'ivan@test.ru', address: 'Москва' });"
            )
        ],
        "task": (
            "Реализуйте полноценный класс `StoreApplication`:\\n"
            "Конструктор принимает массив товаров `initialProducts = [{ id, name, category, price, inStock }]`.\\n\\n"
            "Методы:\\n"
            "1. `queryCatalog({ search = '', category = 'all', sort = 'none', page = 1, pageSize = 5 }) -> { items, totalCount, totalPages, currentPage }`:\\n"
            "   • search: нечувствителен к регистру (поиск подстроки в name).\\n"
            "   • category: если не 'all', фильтрует по точному совпадению.\\n"
            "   • sort: 'asc' — по возрастанию цены, 'desc' — по убыванию цены.\\n"
            "   • пагинация: возвращает срез товаров для страницы `page`.\\n"
            "2. `addToCart(productId, qty = 1)`: добавляет товар в корзину (если товар существует и inStock === true).\\n"
            "3. `getCartSummary()`: возвращает `{ items, totalQty, totalCost }`.\\n"
            "4. `submitOrder(customer)`:\\n"
            "   • если корзина пуста — бросает Error('Cart is empty').\\n"
            "   • валидирует customer (name: длина >= 2, email: содержит '@' и '.', address: длина >= 5). При ошибке — бросает Error('Validation failed').\\n"
            "   • очищает корзину и возвращает `{ orderId: number, status: 'confirmed', total: totalCost, customer }`."
        ),
        "starterCode": (
            "class StoreApplication {\\n"
            "  constructor(initialProducts) {\\n"
            "    // Ваш код здесь\\n"
            "  }\\n"
            "  queryCatalog(params) {}\\n"
            "  addToCart(productId, qty = 1) {}\\n"
            "  getCartSummary() {}\\n"
            "  submitOrder(customer) {}\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Поиск и сортировка в каталоге",
                "expression": (
                    "const products = [\\n"
                    "  { id: 1, name: 'Apple iPhone 15', category: 'phones', price: 80000, inStock: true },\\n"
                    "  { id: 2, name: 'Samsung Galaxy S24', category: 'phones', price: 75000, inStock: true },\\n"
                    "  { id: 3, name: 'USB-C Cable', category: 'accessories', price: 1000, inStock: true }\\n"
                    "];\\n"
                    "const store = new StoreApplication(products);\\n"
                    "const res = store.queryCatalog({ category: 'phones', sort: 'asc' });\\n"
                    "[res.items.length, res.items[0].name]"
                ),
                "expected": [2, "Samsung Galaxy S24"]
            },
            {
                "id": "t2",
                "label": "Оформление заказа и очистка корзины",
                "expression": (
                    "const products = [{ id: 1, name: 'Наушники', category: 'audio', price: 5000, inStock: true }];\\n"
                    "const store = new StoreApplication(products);\\n"
                    "store.addToCart(1, 2);\\n"
                    "const order = store.submitOrder({ name: 'Ольга', email: 'olga@test.ru', address: 'г. Казань, ул. Мира' });\\n"
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
                "class StoreApplication {\\n"
                "  constructor(initialProducts = []) {\\n"
                "    this.products = [...initialProducts];\\n"
                "    this.cart = [];\\n"
                "    this.nextOrderId = 1001;\\n"
                "  }\\n"
                "  queryCatalog({ search = '', category = 'all', sort = 'none', page = 1, pageSize = 5 } = {}) {\\n"
                "    let res = this.products.filter(p => {\\n"
                "      const matchSearch = !search || p.name.toLowerCase().includes(search.toLowerCase());\\n"
                "      const matchCat = category === 'all' || p.category === category;\\n"
                "      return matchSearch && matchCat;\\n"
                "    });\\n"
                "    if (sort === 'asc') res.sort((a, b) => a.price - b.price);\\n"
                "    else if (sort === 'desc') res.sort((a, b) => b.price - a.price);\\n"
                "    const totalCount = res.length;\\n"
                "    const totalPages = Math.ceil(totalCount / pageSize) || 1;\\n"
                "    const start = (page - 1) * pageSize;\\n"
                "    const items = res.slice(start, start + pageSize);\\n"
                "    return { items, totalCount, totalPages, currentPage: page };\\n"
                "  }\\n"
                "  addToCart(productId, qty = 1) {\\n"
                "    const prod = this.products.find(p => p.id === productId);\\n"
                "    if (!prod || !prod.inStock) return false;\\n"
                "    const existing = this.cart.find(it => it.id === productId);\\n"
                "    if (existing) existing.quantity += qty;\\n"
                "    else this.cart.push({ ...prod, quantity: qty });\\n"
                "    return true;\\n"
                "  }\\n"
                "  getCartSummary() {\\n"
                "    const totalQty = this.cart.reduce((sum, it) => sum + it.quantity, 0);\\n"
                "    const totalCost = this.cart.reduce((sum, it) => sum + it.price * it.quantity, 0);\\n"
                "    return { items: [...this.cart], totalQty, totalCost };\\n"
                "  }\\n"
                "  submitOrder(customer) {\\n"
                "    if (this.cart.length === 0) throw new Error('Cart is empty');\\n"
                "    if (!customer || !customer.name || customer.name.trim().length < 2) throw new Error('Validation failed');\\n"
                "    if (!customer.email || !customer.email.includes('@') || !customer.email.includes('.')) throw new Error('Validation failed');\\n"
                "    if (!customer.address || customer.address.trim().length < 5) throw new Error('Validation failed');\\n"
                "    const total = this.getCartSummary().totalCost;\\n"
                "    const orderId = this.nextOrderId++;\\n"
                "    this.cart = [];\\n"
                "    return { orderId, status: 'confirmed', total, customer };\\n"
                "  }\\n"
                "}\\n"
            )
        )
    }
]
'''

JAVA_CONTENT = '''
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
            "Фреймворк коллекций Java (Java Collections Framework) предоставляет готовые структуры данных:\\n"
            "• List (ArrayList, LinkedList) — упорядоченные списки с доступом по индексу.\\n"
            "• Set (HashSet, TreeSet) — коллекции уникальных элементов без дубликатов.\\n"
            "• Map (HashMap, TreeMap) — ассоциативные массивы пар 'ключ-значение'. "
            "Поиск по ключу в HashMap выполняется за константное время O(1).\\n\\n"
            "Дженерики (Generics, например List<String>, Map<Long, User>) гарантируют проверку типов на этапе компиляции."
        ),
        "syntax": (
            "import java.util.Map;\\n"
            "import java.util.HashMap;\\n"
            "import java.util.List;\\n"
            "import java.util.ArrayList;\\n\\n"
            "Map<String, Integer> map = new HashMap<>();\\n"
            "map.put(\\"apple\\", 10);\\n"
            "int count = map.getOrDefault(\\"apple\\", 0);"
        ),
        "examples": [
            (
                "Map<String, Integer> counts = new HashMap<>();\\n"
                "for (String word : words) {\\n"
                "    counts.put(word, counts.getOrDefault(word, 0) + 1);\\n"
                "}"
            )
        ],
        "task": (
            "Напишите класс `ProductCatalog` со следующими методами:\\n"
            "1. `void addProduct(String category, String name, int price)` — добавляет товар в каталог.\\n"
            "2. `int getProductCount(String category)` — возвращает количество товаров в указанной категории (или 0, если категория не найдена).\\n"
            "3. `int getTotalPrice(String category)` — возвращает суммарную стоимость всех товаров в указанной категории.\\n\\n"
            "Проверьте работу в методе `main`."
        ),
        "starterCode": (
            "import java.util.*;\\n\\n"
            "public class Main {\\n"
            "    public static class ProductCatalog {\\n"
            "        // Объявите структуры данных\\n"
            "        public void addProduct(String category, String name, int price) {}\\n"
            "        public int getProductCount(String category) { return 0; }\\n"
            "        public int getTotalPrice(String category) { return 0; }\\n"
            "    }\\n"
            "    public static void main(String[] args) {\\n"
            "        ProductCatalog cat = new ProductCatalog();\\n"
            "        cat.addProduct(\\"food\\", \\"bread\\", 50);\\n"
            "        cat.addProduct(\\"food\\", \\"cheese\\", 250);\\n"
            "        System.out.println(cat.getProductCount(\\"food\\"));\\n"
            "        System.out.println(cat.getTotalPrice(\\"food\\"));\\n"
            "    }\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Подсчет количества и суммы в категории",
                "expected": "2\\n300"
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
                "import java.util.*;\\n\\n"
                "public class Main {\\n"
                "    public static class ProductCatalog {\\n"
                "        private Map<String, List<Integer>> items = new HashMap<>();\\n"
                "        public void addProduct(String category, String name, int price) {\\n"
                "            if (!items.containsKey(category)) {\\n"
                "                items.put(category, new ArrayList<>());\\n"
                "            }\\n"
                "            items.get(category).add(price);\\n"
                "        }\\n"
                "        public int getProductCount(String category) {\\n"
                "            return items.containsKey(category) ? items.get(category).size() : 0;\\n"
                "        }\\n"
                "        public int getTotalPrice(String category) {\\n"
                "            if (!items.containsKey(category)) return 0;\\n"
                "            int sum = 0;\\n"
                "            for (int p : items.get(category)) sum += p;\\n"
                "            return sum;\\n"
                "        }\\n"
                "    }\\n"
                "    public static void main(String[] args) {\\n"
                "        ProductCatalog cat = new ProductCatalog();\\n"
                "        cat.addProduct(\\"food\\", \\"bread\\", 50);\\n"
                "        cat.addProduct(\\"food\\", \\"cheese\\", 250);\\n"
                "        System.out.println(cat.getProductCount(\\"food\\"));\\n"
                "        System.out.println(cat.getTotalPrice(\\"food\\"));\\n"
                "    }\\n"
                "}\\n"
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
            "позволив писать декларативный код без громоздких циклов и промежуточных списков.\\n\\n"
            "Поток (Stream) обрабатывает элементы через цепочку операций:\\n"
            "• Промежуточные (Intermediate): `filter()` (отбор), `map()` (преобразование), `sorted()` (сортировка).\\n"
            "• Терминальные (Terminal): `collect()` (сбор в коллекцию), `count()`, `reduce()`, `findFirst()`. "
            "Пока не вызвана терминальная операция, поток не выполняет вычислений (ленивость)."
        ),
        "syntax": (
            "List<String> result = names.stream()\\n"
            "    .filter(name -> name.startsWith(\\"A\\"))\\n"
            "    .map(String::toUpperCase)\\n"
            "    .sorted()\\n"
            "    .collect(Collectors.toList());"
        ),
        "examples": [
            (
                "int sum = numbers.stream()\\n"
                "    .filter(n -> n > 0)\\n"
                "    .mapToInt(Integer::intValue)\\n"
                "    .sum();"
            )
        ],
        "task": (
            "Напишите класс `TaskFilter` со статическим методом:\\n"
            "`List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority)`\\n"
            "Каждый объект `Task` имеет методы `getTitle()` (String) и `getPriority()` (int).\\n\\n"
            "Метод должен с помощью Stream API:\\n"
            "1. Отфильтровать задачи, чей приоритет >= `minPriority`.\\n"
            "2. Преобразовать каждую задачу в верхний регистр названия (`getTitle().toUpperCase()`).\\n"
            "3. Отсортировать названия по алфавиту.\\n"
            "4. Собрать и вернуть в виде `List<String>`.\\n\\n"
            "Выведите результат работы в консоль через разделитель запятая."
        ),
        "starterCode": (
            "import java.util.*;\\n"
            "import java.util.stream.*;\\n\\n"
            "public class Main {\\n"
            "    public static class Task {\\n"
            "        private String title;\\n"
            "        private int priority;\\n"
            "        public Task(String title, int priority) { this.title = title; this.priority = priority; }\\n"
            "        public String getTitle() { return title; }\\n"
            "        public int getPriority() { return priority; }\\n"
            "    }\\n\\n"
            "    public static List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority) {\\n"
            "        // Stream API конвейер здесь\\n"
            "        return null;\\n"
            "    }\\n\\n"
            "    public static void main(String[] args) {\\n"
            "        List<Task> list = Arrays.asList(\\n"
            "            new Task(\\"deploy\\", 10),\\n"
            "            new Task(\\"refactor\\", 3),\\n"
            "            new Task(\\"backup\\", 8)\\n"
            "        );\\n"
            "        List<String> res = getUrgentTaskTitles(list, 5);\\n"
            "        System.out.println(String.join(\\", \\", res));\\n"
            "    }\\n"
            "}\\n"
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
                "import java.util.*;\\n"
                "import java.util.stream.*;\\n\\n"
                "public class Main {\\n"
                "    public static class Task {\\n"
                "        private String title;\\n"
                "        private int priority;\\n"
                "        public Task(String title, int priority) { this.title = title; this.priority = priority; }\\n"
                "        public String getTitle() { return title; }\\n"
                "        public int getPriority() { return priority; }\\n"
                "    }\\n\\n"
                "    public static List<String> getUrgentTaskTitles(List<Task> tasks, int minPriority) {\\n"
                "        return tasks.stream()\\n"
                "            .filter(t -> t.getPriority() >= minPriority)\\n"
                "            .map(t -> t.getTitle().toUpperCase())\\n"
                "            .sorted()\\n"
                "            .collect(Collectors.toList());\\n"
                "    }\\n\\n"
                "    public static void main(String[] args) {\\n"
                "        List<Task> list = Arrays.asList(\\n"
                "            new Task(\\"deploy\\", 10),\\n"
                "            new Task(\\"refactor\\", 3),\\n"
                "            new Task(\\"backup\\", 8)\\n"
                "        );\\n"
                "        List<String> res = getUrgentTaskTitles(list, 5);\\n"
                "        System.out.println(String.join(\\", \\", res));\\n"
                "    }\\n"
                "}\\n"
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
            "Архитектура Spring строится на трёх основных слоях:\\n"
            "1. Controller (@RestController) — принимает HTTP-запросы, валидирует входные данные и возвращает ответы (обычно JSON).\\n"
            "2. Service (@Service) — содержит бизнес-логику приложения.\\n"
            "3. Repository (@Repository) — отвечает за сохранение и загрузку данных из БД.\\n\\n"
            "Внедрение зависимостей (Inversion of Control / DI) связывает компоненты автоматически через конструкторы."
        ),
        "syntax": (
            "@RestController\\n"
            "@RequestMapping(\\"/api/tasks\\")\\n"
            "public class TaskController {\\n"
            "    private final TaskService taskService;\\n"
            "    public TaskController(TaskService service) {\\n"
            "        this.taskService = service;\\n"
            "    }\\n"
            "    @GetMapping\\n"
            "    public List<Task> getAll() {\\n"
            "        return taskService.findAll();\\n"
            "    }\\n"
            "}"
        ),
        "examples": [
            (
                "public class ApiResponse<T> {\\n"
                "    public int status;\\n"
                "    public T data;\\n"
                "    public ApiResponse(int status, T data) {\\n"
                "        this.status = status; this.data = data;\\n"
                "    }\\n"
                "}"
            )
        ],
        "task": (
            "Смоделируйте логику Spring REST-контроллера в классе `TaskApiController`:\\n"
            "Конструктор принимает `TaskService service`.\\n"
            "Методы контроллера:\\n"
            "1. `ApiResponse handleGetById(long id)`: если задача найдена — возвращает `{ status: 200, data: task }`, если нет — `{ status: 404, error: \\"Task not found\\" }`.\\n"
            "2. `ApiResponse handleCreate(String title, int priority)`: если title пустой или priority < 1 — возвращает `{ status: 400, error: \\"Validation failed\\" }`, иначе создает задачу и возвращает `{ status: 201, data: task }`.\\n\\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\\n\\n"
            "public class Main {\\n"
            "    public static class Task {\\n"
            "        public long id;\\n"
            "        public String title;\\n"
            "        public int priority;\\n"
            "        public Task(long id, String title, int priority) {\\n"
            "            this.id = id; this.title = title; this.priority = priority;\\n"
            "        }\\n"
            "    }\\n"
            "    public static class ApiResponse {\\n"
            "        public int status;\\n"
            "        public Object data;\\n"
            "        public String error;\\n"
            "        public ApiResponse(int s, Object d, String e) { status = s; data = d; error = e; }\\n"
            "    }\\n"
            "    public static class TaskService {\\n"
            "        private Map<Long, Task> db = new HashMap<>();\\n"
            "        private long nextId = 1;\\n"
            "        public Task findById(long id) { return db.get(id); }\\n"
            "        public Task create(String title, int priority) {\\n"
            "            Task t = new Task(nextId++, title, priority);\\n"
            "            db.put(t.id, t);\\n"
            "            return t;\\n"
            "        }\\n"
            "    }\\n"
            "    public static class TaskApiController {\\n"
            "        private TaskService service;\\n"
            "        public TaskApiController(TaskService s) { this.service = s; }\\n"
            "        public ApiResponse handleGetById(long id) { return null; }\\n"
            "        public ApiResponse handleCreate(String title, int priority) { return null; }\\n"
            "    }\\n"
            "    public static void main(String[] args) {\\n"
            "        TaskService s = new TaskService();\\n"
            "        TaskApiController c = new TaskApiController(s);\\n"
            "        ApiResponse r1 = c.handleCreate(\\"Init DB\\", 5);\\n"
            "        ApiResponse r2 = c.handleGetById(999);\\n"
            "        System.out.println(r1.status + \\" \\" + ((Task)r1.data).title);\\n"
            "        System.out.println(r2.status + \\" \\" + r2.error);\\n"
            "    }\\n"
            "}\\n"
        ),
        "tests": [
            {
                "id": "t1",
                "label": "Статусы ответов 201 Created и 404 Not Found",
                "expected": "201 Init DB\\n404 Task not found"
            }
        ],
        "hints": [
            "Направление: в handleGetById проверьте `Task t = service.findById(id); if (t == null) return new ApiResponse(404, null, \\"Task not found\\");`",
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
                "import java.util.*;\\n\\n"
                "public class Main {\\n"
                "    public static class Task {\\n"
                "        public long id;\\n"
                "        public String title;\\n"
                "        public int priority;\\n"
                "        public Task(long id, String title, int priority) {\\n"
                "            this.id = id; this.title = title; this.priority = priority;\\n"
                "        }\\n"
                "    }\\n"
                "    public static class ApiResponse {\\n"
                "        public int status;\\n"
                "        public Object data;\\n"
                "        public String error;\\n"
                "        public ApiResponse(int s, Object d, String e) { status = s; data = d; error = e; }\\n"
                "    }\\n"
                "    public static class TaskService {\\n"
                "        private Map<Long, Task> db = new HashMap<>();\\n"
                "        private long nextId = 1;\\n"
                "        public Task findById(long id) { return db.get(id); }\\n"
                "        public Task create(String title, int priority) {\\n"
                "            Task t = new Task(nextId++, title, priority);\\n"
                "            db.put(t.id, t);\\n"
                "            return t;\\n"
                "        }\\n"
                "    }\\n"
                "    public static class TaskApiController {\\n"
                "        private TaskService service;\\n"
                "        public TaskApiController(TaskService s) { this.service = s; }\\n"
                "        public ApiResponse handleGetById(long id) {\\n"
                "            Task t = service.findById(id);\\n"
                "            if (t == null) return new ApiResponse(404, null, \\"Task not found\\");\\n"
                "            return new ApiResponse(200, t, null);\\n"
                "        }\\n"
                "        public ApiResponse handleCreate(String title, int priority) {\\n"
                "            if (title == null || title.trim().isEmpty() || priority < 1) {\\n"
                "                return new ApiResponse(400, null, \\"Validation failed\\");\\n"
                "            }\\n"
                "            Task t = service.create(title, priority);\\n"
                "            return new ApiResponse(201, t, null);\\n"
                "        }\\n"
                "    }\\n"
                "    public static void main(String[] args) {\\n"
                "        TaskService s = new TaskService();\\n"
                "        TaskApiController c = new TaskApiController(s);\\n"
                "        ApiResponse r1 = c.handleCreate(\\"Init DB\\", 5);\\n"
                "        ApiResponse r2 = c.handleGetById(999);\\n"
                "        System.out.println(r1.status + \\" \\" + ((Task)r1.data).title);\\n"
                "        System.out.println(r2.status + \\" \\" + r2.error);\\n"
                "    }\\n"
                "}\\n"
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
            "Итоговый проект направления Java Development моделирует работу промышленного Enterprise API:\\n"
            "• Управление ресурсами и задачами с уникальными идентификаторами.\\n"
            "• Строгая валидация входящих данных (@Valid, минимальная длина, статус).\\n"
            "• Фильтрация по статусу (NEW, IN_PROGRESS, COMPLETED) и поиск по подстроке.\\n"
            "• Пагинация выдачи (page, size) для эффективной работы с большими объёмами данных.\\n"
            "• Единообразная обработка ошибок (400 Bad Request, 404 Not Found)."
        ),
        "syntax": (
            "public class EnterpriseTaskManager {\\n"
            "    public Task create(TaskCreateDto dto) { ... }\\n"
            "    public Task updateStatus(long id, String newStatus) { ... }\\n"
            "    public PageResult<Task> search(String query, String status, int page, int size) { ... }\\n"
            "}"
        ),
        "examples": [
            (
                "EnterpriseTaskManager manager = new EnterpriseTaskManager();\\n"
                "Task task = manager.create(\\"Database Migration\\", \\"Backend\\", 10);\\n"
                "manager.updateStatus(task.id, \\"IN_PROGRESS\\");"
            )
        ],
        "task": (
            "Реализуйте полноценный класс `EnterpriseTaskManager`:\\n"
            "Класс `Task` имеет поля: `long id`, `String title`, `String status` (по умолчанию \\"NEW\\"), `int priority`.\\n\\n"
            "Методы менеджера:\\n"
            "1. `Task createTask(String title, int priority)`:\\n"
            "   • Если title == null или длина < 3, или priority < 1 — бросает `IllegalArgumentException(\\"Invalid task data\\")`.\\n"
            "   • Генерирует автоинкрементный id и сохраняет задачу со статусом \\"NEW\\".\\n"
            "2. `Task updateStatus(long id, String newStatus)`:\\n"
            "   • Если задача не найдена — бросает `NoSuchElementException(\\"Task not found\\")`.\\n"
            "   • Допустимые статусы: \\"NEW\\", \\"IN_PROGRESS\\", \\"COMPLETED\\". При недопустимом статусе — `IllegalArgumentException`.\\n"
            "3. `List<Task> searchTasks(String status, int page, int pageSize)`:\\n"
            "   • Фильтрует по статусу (если status равен null или \\"ALL\\" — возвращает задачи с любым статусом).\\n"
            "   • Применяет пагинацию: пропускает (page - 1) * pageSize и берет pageSize элементов.\\n\\n"
            "Проверьте работу в main."
        ),
        "starterCode": (
            "import java.util.*;\\n\\n"
            "public class Main {\\n"
            "    public static class Task {\\n"
            "        public long id;\\n"
            "        public String title;\\n"
            "        public String status;\\n"
            "        public int priority;\\n"
            "        public Task(long id, String title, int priority) {\\n"
            "            this.id = id; this.title = title; this.priority = priority; this.status = \\"NEW\\";\\n"
            "        }\\n"
            "    }\\n"
            "    public static class EnterpriseTaskManager {\\n"
            "        // Реализация здесь\\n"
            "    }\\n"
            "    public static void main(String[] args) {\\n"
            "        EnterpriseTaskManager m = new EnterpriseTaskManager();\\n"
            "        Task t1 = m.createTask(\\"Setup CI/CD\\", 5);\\n"
            "        Task t2 = m.createTask(\\"Security Audit\\", 10);\\n"
            "        m.updateStatus(t1.id, \\"IN_PROGRESS\\");\\n"
            "        List<Task> res = m.searchTasks(\\"IN_PROGRESS\\", 1, 10);\\n"
            "        System.out.println(res.size() + \\" \\" + res.get(0).title + \\" \\" + res.get(0).status);\\n"
            "    }\\n"
            "}\\n"
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
            "Подход: в searchTasks отфильтруйте задачи через stream: `.filter(t -> status == null || \\"ALL\\".equals(status) || t.status.equals(status))`",
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
                "import java.util.*;\\n"
                "import java.util.stream.*;\\n\\n"
                "public class Main {\\n"
                "    public static class Task {\\n"
                "        public long id;\\n"
                "        public String title;\\n"
                "        public String status;\\n"
                "        public int priority;\\n"
                "        public Task(long id, String title, int priority) {\\n"
                "            this.id = id; this.title = title; this.priority = priority; this.status = \\"NEW\\";\\n"
                "        }\\n"
                "    }\\n"
                "    public static class EnterpriseTaskManager {\\n"
                "        private Map<Long, Task> db = new LinkedHashMap<>();\\n"
                "        private long nextId = 1;\\n"
                "        private Set<String> validStatuses = new HashSet<>(Arrays.asList(\\"NEW\\", \\"IN_PROGRESS\\", \\"COMPLETED\\"));\\n\\n"
                "        public Task createTask(String title, int priority) {\\n"
                "            if (title == null || title.trim().length() < 3 || priority < 1) {\\n"
                "                throw new IllegalArgumentException(\\"Invalid task data\\");\\n"
                "            }\\n"
                "            Task t = new Task(nextId++, title, priority);\\n"
                "            db.put(t.id, t);\\n"
                "            return t;\\n"
                "        }\\n\\n"
                "        public Task updateStatus(long id, String newStatus) {\\n"
                "            if (!db.containsKey(id)) throw new NoSuchElementException(\\"Task not found\\");\\n"
                "            if (!validStatuses.contains(newStatus)) throw new IllegalArgumentException(\\"Invalid status\\");\\n"
                "            Task t = db.get(id);\\n"
                "            t.status = newStatus;\\n"
                "            return t;\\n"
                "        }\\n\\n"
                "        public List<Task> searchTasks(String status, int page, int pageSize) {\\n"
                "            return db.values().stream()\\n"
                "                .filter(t -> status == null || \\"ALL\\".equals(status) || t.status.equals(status))\\n"
                "                .skip((long)(page - 1) * pageSize)\\n"
                "                .limit(pageSize)\\n"
                "                .collect(Collectors.toList());\\n"
                "        }\\n"
                "    }\\n"
                "    public static void main(String[] args) {\\n"
                "        EnterpriseTaskManager m = new EnterpriseTaskManager();\\n"
                "        Task t1 = m.createTask(\\"Setup CI/CD\\", 5);\\n"
                "        Task t2 = m.createTask(\\"Security Audit\\", 10);\\n"
                "        m.updateStatus(t1.id, \\"IN_PROGRESS\\");\\n"
                "        List<Task> res = m.searchTasks(\\"IN_PROGRESS\\", 1, 10);\\n"
                "        System.out.println(res.size() + \\" \\" + res.get(0).title + \\" \\" + res.get(0).status);\\n"
                "    }\\n"
                "}\\n"
            )
        )
    }
]
'''

with open('scripts/curriculum_tracks.py', 'a', encoding='utf-8') as f:
    f.write(FRONTEND_CONTENT)
    f.write(JAVA_CONTENT)

print("Appended frontend and java lessons.")
