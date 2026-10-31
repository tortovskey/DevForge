import type * as Monaco from 'monaco-editor';

/**
 * DevForge Code Intelligence System:
 * - Full Monarch syntax highlighter for 1С (BSL)
 * - Rich autocompletion (keywords, types, methods, snippets, member-access on dot) across all 13 languages
 * - Signature help (parameter hints) on '(' and ','
 * - Interactive hover documentation with signature and examples
 * - Real-time syntax diagnostics
 */

export interface DocEntry {
  signature: string;
  doc: string;
  example?: string;
}

export const HOVER_DOCS: Record<string, Record<string, DocEntry>> = {
  c: {
    printf: { signature: 'int printf(const char *format, ...)', doc: 'Выводит форматированную строку в стандартный поток вывода stdout.', example: 'printf("Ответ: %d\\n", 42);' },
    scanf: { signature: 'int scanf(const char *format, ...)', doc: 'Считывает форматированные данные из стандартного потока stdin.', example: 'scanf("%d", &x);' },
    malloc: { signature: 'void* malloc(size_t size)', doc: 'Выделяет непрерывный блок динамической памяти указанного размера в байтах.', example: 'int *arr = (int*)malloc(10 * sizeof(int));' },
    free: { signature: 'void free(void *ptr)', doc: 'Освобождает ранее выделенный блок динамической памяти.', example: 'free(arr);' },
    sizeof: { signature: 'sizeof(type | expr)', doc: 'Оператор, возвращающий размер типа данных или переменной в байтах.', example: 'size_t s = sizeof(int);' },
    struct: { signature: 'struct Name { ... };', doc: 'Определяет составной пользовательский тип данных.', example: 'struct Point { int x; int y; };' },
    int: { signature: 'int var = 0;', doc: 'Базовый 32-битный целочисленный тип со знаком.', example: 'int count = 10;' },
    char: { signature: 'char ch = \'a\';', doc: 'Однобайтовый символьный тип данных (ASCII).', example: 'char c = \'A\';' },
    void: { signature: 'void func(void)', doc: 'Обозначает отсутствие возвращаемого значения или нетипизированный указатель void*.', example: 'void logMessage(const char *msg);' }
  },
  cpp: {
    'std::cout': { signature: 'std::ostream cout', doc: 'Стандартный выходной поток C++ (консоль).', example: 'std::cout << "DevForge" << std::endl;' },
    cout: { signature: 'std::ostream cout', doc: 'Стандартный выходной поток C++ (консоль).', example: 'std::cout << "DevForge" << std::endl;' },
    'std::cin': { signature: 'std::istream cin', doc: 'Стандартный входной поток C++ для чтения данных.', example: 'std::cin >> x;' },
    cin: { signature: 'std::istream cin', doc: 'Стандартный входной поток C++ для чтения данных.', example: 'std::cin >> x;' },
    'std::endl': { signature: 'std::endl', doc: 'Вставляет символ перевода строки и сбрасывает буфер вывода (flush).', example: 'std::cout << x << std::endl;' },
    endl: { signature: 'std::endl', doc: 'Вставляет символ перевода строки и сбрасывает буфер вывода (flush).', example: 'std::cout << x << std::endl;' },
    'std::vector': { signature: 'template<typename T> class vector', doc: 'Последовательный контейнер динамического массива STL с автоматическим расширением.', example: 'std::vector<int> nums = {1, 2, 3};' },
    vector: { signature: 'template<typename T> class vector', doc: 'Последовательный контейнер динамического массива STL.', example: 'vector<int> nums = {1, 2, 3};' },
    'std::string': { signature: 'class string', doc: 'Стандартный класс динамических строк C++.', example: 'std::string s = "DevForge";' },
    auto: { signature: 'auto var = value;', doc: 'Автоматический вывод типа переменной компилятором из выражения инициализации.', example: 'auto x = 42;' }
  },
  csharp: {
    'Console.WriteLine': { signature: 'void Console.WriteLine(object? value)', doc: 'Записывает строковое представление объекта в консоль с последующим переводом на новую строку.', example: 'Console.WriteLine("Привет, C#!");' },
    'Console.Write': { signature: 'void Console.Write(object? value)', doc: 'Записывает строковое представление объекта в консоль без перевода строки.', example: 'Console.Write("Загрузка: ");' },
    'Console.ReadLine': { signature: 'string? Console.ReadLine()', doc: 'Считывает следующую строку символов из стандартного потока ввода stdin.', example: 'string name = Console.ReadLine();' },
    'int.Parse': { signature: 'int int.Parse(string s)', doc: 'Преобразует строковое представление числа в 32-битное целое число со знаком.', example: 'int n = int.Parse("42");' },
    'double.Parse': { signature: 'double double.Parse(string s)', doc: 'Преобразует строку в число с плавающей точкой двойной точности.', example: 'double d = double.Parse("3.14");' },
    List: { signature: 'class List<T>', doc: 'Строго типизированный список объектов с динамическим размером.', example: 'List<int> numbers = new() { 1, 2, 3 };' },
    var: { signature: 'var x = value;', doc: 'Неявно типизированная локальная переменная. Тип выводится компилятором.', example: 'var items = new List<string>();' },
    static: { signature: 'static member', doc: 'Объявляет статический член класса, принадлежащий самому классу, а не экземпляру.', example: 'public static void Main() { }' },
    class: { signature: 'class Name { ... }', doc: 'Объявляет ссылочный тип данных (класс) в объектно-ориентированном C#.', example: 'class Product { public string Name { get; set; } }' }
  },
  objc: {
    NSLog: { signature: 'void NSLog(NSString *format, ...)', doc: 'Выводит форматированное сообщение в системный журнал Apple Foundation.', example: 'NSLog(@"Привет, %@! Число: %d", @"DevForge", 42);' },
    NSString: { signature: '@interface NSString', doc: 'Неизменяемая строка символов Unicode Foundation.', example: 'NSString *str = @"DevForge";' },
    NSArray: { signature: '@interface NSArray', doc: 'Неизменяемый упорядоченный список объектов Foundation.', example: 'NSArray *items = @[@"A", @"B", @"C"];' },
    NSNumber: { signature: '@interface NSNumber', doc: 'Объектная обертка над примитивными числовыми типами.', example: 'NSNumber *num = @42;' }
  },
  rust: {
    'println!': { signature: 'macro println!($($arg:tt)*)', doc: 'Выводит форматированный текст в stdout с добавлением символа новой строки.', example: 'println!("Ответ: {}", 42);' },
    'print!': { signature: 'macro print!($($arg:tt)*)', doc: 'Выводит форматированный текст в stdout без символа новой строки.', example: 'print!("Значение: ");' },
    'vec!': { signature: 'macro vec![...]', doc: 'Макрос удобного создания вектора Vec<T>.', example: 'let v = vec![1, 2, 3];' },
    let: { signature: 'let [mut] var: Type = val;', doc: 'Объявляет локальную переменную. В Rust переменные по умолчанию неизменяемы (immutable).', example: 'let mut count = 0;' },
    mut: { signature: 'mut', doc: 'Модификатор изменяемости переменной.', example: 'let mut x = 5; x += 1;' },
    fn: { signature: 'fn name(params) -> ReturnType', doc: 'Объявление функции. Последнее выражение без точки с запятой возвращается автоматически.', example: 'fn add(a: i32, b: i32) -> i32 { a + b }' },
    match: { signature: 'match expr { pat => code, ... }', doc: 'Мощная конструкция сопоставления с образцом (Pattern Matching).', example: 'match n { 1 => "один", _ => "другое" }' }
  },
  '1c': {
    Сообщить: { signature: 'Сообщить(Текст, СтатусСообщения)', doc: 'Выводит текстовое сообщение пользователю в панель сообщений 1С.', example: 'Сообщить("Привет, 1С!");' },
    Процедура: { signature: 'Процедура Имя(Параметры) ... КонецПроцедуры', doc: 'Объявляет процедуру (подпрограмму, не возвращающую значение).', example: 'Процедура Печать()\n    Сообщить("Привет");\nКонецПроцедуры' },
    Функция: { signature: 'Функция Имя(Параметры) ... КонецФункции', doc: 'Объявляет функцию, возвращающую значение с помощью оператора Возврат.', example: 'Функция Сложить(А, Б)\n    Возврат А + Б;\nКонецФункции' },
    Если: { signature: 'Если Условие Тогда ... Иначе ... КонецЕсли;', doc: 'Условный оператор ветвления программы.', example: 'Если Сумма > 1000 Тогда\n    Скидка = 10;\nКонецЕсли;' },
    Для: { signature: 'Для Сч = 1 По 10 Цикл ... КонецЦикла;', doc: 'Цикл со счетчиком от начального до конечного значения.', example: 'Для Сч = 1 По 5 Цикл\n    Сообщить(Сч);\nКонецЦикла;' },
    ДляКаждого: { signature: 'Для Каждого Элемент Из Коллекция Цикл ... КонецЦикла;', doc: 'Цикл обхода всех элементов коллекции (Массив, ТаблицаЗначений).', example: 'Для Каждого Эл Из Список Цикл\n    Сообщить(Эл);\nКонецЦикла;' },
    Новый: { signature: 'Новый ИмяТипа(...)', doc: 'Создает новый экземпляр прикладного объекта или универсальной коллекции.', example: 'Массив = Новый Массив;' },
    СтрДлина: { signature: 'СтрДлина(Строка) -> Число', doc: 'Возвращает количество символов в переданной строке.', example: 'Длина = СтрДлина("Текст");' },
    ВРег: { signature: 'ВРег(Строка) -> Строка', doc: 'Преобразует строку в верхний регистр.', example: 'Большие = ВРег("текст");' },
    НРег: { signature: 'НРег(Строка) -> Строка', doc: 'Преобразует строку в нижний регистр.', example: 'Малые = НРег("ТЕКСТ");' }
  },
  python: {
    print: { signature: 'print(*values, sep=" ", end="\\n")', doc: 'Печатает переданные значения в консоль через разделитель sep.', example: 'print("Привет", 42)' },
    input: { signature: 'input(prompt="") -> str', doc: 'Считывает строку пользовательского ввода из stdin.', example: 'name = input("Ваше имя: ")' },
    len: { signature: 'len(s) -> int', doc: 'Возвращает количество элементов в коллекции, списке, строке или словаре.', example: 'count = len([1, 2, 3])' },
    range: { signature: 'range(start, stop[, step])', doc: 'Генерирует неизменяемую арифметическую последовательность целых чисел.', example: 'for i in range(5):' },
    int: { signature: 'int(x=0) -> int', doc: 'Преобразует число или строку в целое число.', example: 'val = int("123")' },
    str: { signature: 'str(object="") -> str', doc: 'Возвращает строковое представление объекта.', example: 's = str(42)' },
    def: { signature: 'def name(parameters):', doc: 'Определяет пользовательскую функцию.', example: 'def greet(name):\n    return f"Привет, {name}!"' }
  },
  javascript: {
    'console.log': { signature: 'console.log(...data: any[])', doc: 'Выводит информационное сообщение в веб-консоль браузера.', example: 'console.log("Ответ:", 42);' },
    'console.error': { signature: 'console.error(...data: any[])', doc: 'Выводит сообщение об ошибке в консоль.', example: 'console.error("Ошибка сети");' },
    map: { signature: 'Array.prototype.map(callback)', doc: 'Создает новый массив с результатом вызова функции для каждого элемента.', example: 'const doubled = arr.map(x => x * 2);' },
    filter: { signature: 'Array.prototype.filter(predicate)', doc: 'Создает новый массив со всеми элементами, прошедшими проверку.', example: 'const evens = arr.filter(x => x % 2 === 0);' },
    reduce: { signature: 'Array.prototype.reduce(fn, initial)', doc: 'Сворачивает массив в единое итоговое значение с аккумулятором.', example: 'const sum = arr.reduce((acc, x) => acc + x, 0);' }
  },
  typescript: {
    interface: { signature: 'interface Name { ... }', doc: 'Определяет контракт структуры объекта в TypeScript.', example: 'interface User {\n    id: number;\n    name: string;\n}' },
    type: { signature: 'type Name = ...', doc: 'Объявляет псевдоним типа (объединения, примитивы, кортежи).', example: 'type Status = "pending" | "ready";' }
  },
  java: {
    'System.out.println': { signature: 'void System.out.println(String s)', doc: 'Выводит строку в консоль и переходит на новую строку.', example: 'System.out.println("Привет из Java!");' },
    'System.out.print': { signature: 'void System.out.print(String s)', doc: 'Выводит строку в консоль без перехода на новую строку.', example: 'System.out.print("Загрузка: ");' },
    Scanner: { signature: 'class Scanner', doc: 'Текстовый сканер для удобного чтения примитивных типов и строк из потока ввода.', example: 'Scanner in = new Scanner(System.in);\nint x = in.nextInt();' }
  },
  sql: {
    SELECT: { signature: 'SELECT columns FROM table', doc: 'Основная команда извлечения строк и столбцов из таблицы БД.', example: 'SELECT id, name FROM users WHERE active = 1;' },
    WHERE: { signature: 'WHERE condition', doc: 'Фильтрует строки по логическому условию.', example: 'WHERE price >= 100' },
    JOIN: { signature: 'JOIN table ON condition', doc: 'Объединяет строки двух и более таблиц по общему ключу.', example: 'JOIN orders ON orders.user_id = users.id' }
  },
  lua: {
    print: { signature: 'print(...)', doc: 'Выводит переданные аргументы в консоль, разделяя их табуляцией.', example: 'print("Привет, Lua!", 42)' },
    'table.insert': { signature: 'table.insert(list, [pos,] value)', doc: 'Вставляет элемент в массив по указанной позиции или в конец.', example: 'table.insert(fruits, "яблоко")' },
    'table.remove': { signature: 'table.remove(list, [pos])', doc: 'Удаляет элемент из массива и возвращает его значение.', example: 'local item = table.remove(fruits, 1)' },
    'table.concat': { signature: 'table.concat(list, [sep])', doc: 'Объединяет элементы массива в одну строку с разделителем.', example: 'local s = table.concat(names, ", ")' },
    setmetatable: { signature: 'setmetatable(table, metatable)', doc: 'Устанавливает метатаблицу для объекта (ключ к ООП и перегрузке операций в Lua).', example: 'setmetatable(obj, { __index = Proto })' },
    getmetatable: { signature: 'getmetatable(table)', doc: 'Возвращает метатаблицу объекта.', example: 'local mt = getmetatable(obj)' },
    'coroutine.create': { signature: 'coroutine.create(f)', doc: 'Создает новую сопрограмму (корутину).', example: 'local co = coroutine.create(function() coroutine.yield(1) end)' },
    'coroutine.resume': { signature: 'coroutine.resume(co, ...)', doc: 'Запускает или возобновляет выполнение корутины.', example: 'local ok, val = coroutine.resume(co)' },
    'coroutine.yield': { signature: 'coroutine.yield(...)', doc: 'Приостанавливает выполнение текущей корутины и передает управление вызывающему коду.', example: 'coroutine.yield("пауза")' },
    pcall: { signature: 'pcall(f, ...)', doc: 'Безопасный вызов функции (защищенный режим). Возвращает true/false и результат.', example: 'local ok, res = pcall(riskyFunction)' }
  },
  assembly: {
    mov: { signature: 'mov dst, src', doc: 'Копирует значение из источника (src) в приемник (dst).', example: 'mov rax, 60' },
    lea: { signature: 'lea dst, [src]', doc: 'Load Effective Address: вычисляет адрес операнда памяти без обращения к самой памяти.', example: 'lea rdi, [rbp - 16]' },
    add: { signature: 'add dst, src', doc: 'Складывает src с dst и сохраняет результат в dst. Обновляет флаги ZF, SF, CF, OF.', example: 'add rax, 10' },
    sub: { signature: 'sub dst, src', doc: 'Вычитает src из dst. Обновляет флаги.', example: 'sub rsp, 32' },
    cmp: { signature: 'cmp op1, op2', doc: 'Сравнивает операнды (выполняет op1 - op2 без сохранения результата) и выставляет флаги.', example: 'cmp rax, 0\nje is_zero' },
    jmp: { signature: 'jmp label', doc: 'Безусловный переход по метке.', example: 'jmp loop_start' },
    je: { signature: 'je label (jz)', doc: 'Переход по метке, если равно (флаг ZF = 1).', example: 'je found' },
    jne: { signature: 'jne label (jnz)', doc: 'Переход по метке, если не равно (флаг ZF = 0).', example: 'jne continue_search' },
    push: { signature: 'push src', doc: 'Уменьшает указатель стека rsp на 8 и записывает значение в стек.', example: 'push rbp' },
    pop: { signature: 'pop dst', doc: 'Считывает значение с вершины стека и увеличивает rsp на 8.', example: 'pop rbp' },
    call: { signature: 'call label', doc: 'Вызов подпрограммы: сохраняет адрес возврата в стек и переходит к метке.', example: 'call my_function' },
    ret: { signature: 'ret', doc: 'Возврат из подпрограммы: извлекает адрес возврата из стека в RIP.', example: 'ret' },
    syscall: { signature: 'syscall', doc: 'Системный вызов ядра Linux x86-64. Номер вызова в RAX: 1=sys_write, 0=sys_read, 60=sys_exit.', example: 'mov rax, 60\nmov rdi, 0\nsyscall' }
  }
};

export const SIGNATURES: Record<string, { label: string; doc: string; params: string[] }> = {
  'printf': { label: 'int printf(const char *format, ...)', doc: 'Форматированный вывод в stdout', params: ['const char *format', '...args'] },
  'scanf': { label: 'int scanf(const char *format, ...)', doc: 'Считывание данных из stdin', params: ['const char *format', '...pointers'] },
  'Console.WriteLine': { label: 'void Console.WriteLine(object? value)', doc: 'Вывод в консоль C# с переводом строки', params: ['object? value'] },
  'Console.Write': { label: 'void Console.Write(object? value)', doc: 'Вывод в консоль C# без перевода строки', params: ['object? value'] },
  'int.Parse': { label: 'int int.Parse(string s)', doc: 'Парсинг целого числа в C#', params: ['string s'] },
  'System.out.println': { label: 'void System.out.println(Object x)', doc: 'Вывод строки в консоль Java', params: ['Object x'] },
  'System.out.print': { label: 'void System.out.print(Object x)', doc: 'Вывод в консоль Java без перевода строки', params: ['Object x'] },
  'print': { label: 'print(*values, sep=" ", end="\\n")', doc: 'Вывод данных в консоль Python', params: ['*values', 'sep=" "', 'end="\\n"'] },
  'input': { label: 'input(prompt="") -> str', doc: 'Чтение строки из stdin в Python', params: ['prompt=""'] },
  'range': { label: 'range(start, stop[, step])', doc: 'Генератор последовательности чисел', params: ['start', 'stop', 'step'] },
  'console.log': { label: 'console.log(...data: any[])', doc: 'Вывод в консоль браузера', params: ['...data'] },
  'Сообщить': { label: 'Сообщить(Текст, СтатусСообщения)', doc: 'Вывод сообщения пользователю 1С', params: ['Текст', 'СтатусСообщения'] }
};

interface CompletionDef {
  label: string;
  kind: Monaco.languages.CompletionItemKind;
  snippet?: string;
  detail: string;
  doc: string;
}

const COMMON_COMPLETIONS: Record<string, CompletionDef[]> = {
  c: [
    { label: 'main', kind: 15 /* Snippet */, snippet: 'int main(void) {\n    ${1}\n    return 0;\n}', detail: 'Шаблон main', doc: 'Точка входа программы на C' },
    { label: 'printf', kind: 1 /* Function */, snippet: 'printf("${1:%s}\\n", ${2});', detail: 'Функция вывода', doc: 'Форматированный вывод в консоль' },
    { label: 'scanf', kind: 1 /* Function */, snippet: 'scanf("${1:%d}", &${2});', detail: 'Функция ввода', doc: 'Форматированный ввод из stdin' },
    { label: 'for', kind: 15, snippet: 'for (int ${1:i} = 0; ${1:i} < ${2:n}; ${1:i}++) {\n    ${3}\n}', detail: 'Цикл for', doc: 'Цикл со счетчиком' },
    { label: 'while', kind: 15, snippet: 'while (${1:condition}) {\n    ${2}\n}', detail: 'Цикл while', doc: 'Цикл с предусловием' },
    { label: 'if', kind: 15, snippet: 'if (${1:condition}) {\n    ${2}\n}', detail: 'Условие if', doc: 'Ветвление' },
    { label: 'struct', kind: 15, snippet: 'typedef struct {\n    ${2}\n} ${1:Name};', detail: 'Структура typedef', doc: 'Определение структуры' },
    { label: 'malloc', kind: 1, snippet: '(${1:int}*)malloc(${2:size} * sizeof(${1:int}));', detail: 'Выделение памяти', doc: 'Динамическая память' },
    { label: 'free', kind: 1, snippet: 'free(${1});', detail: 'Освобождение памяти', doc: 'Очистка памяти' },
    { label: 'sizeof', kind: 14 /* Keyword */, snippet: 'sizeof(${1})', detail: 'Оператор sizeof', doc: 'Размер в байтах' },
    { label: '#include <stdio.h>', kind: 15, snippet: '#include <stdio.h>\n', detail: 'Заголовок stdio', doc: 'Ввод/вывод' },
    { label: '#include <stdlib.h>', kind: 15, snippet: '#include <stdlib.h>\n', detail: 'Заголовок stdlib', doc: 'Память и утилиты' }
  ],
  cpp: [
    { label: 'main', kind: 15, snippet: '#include <iostream>\n\nint main() {\n    ${1}\n    return 0;\n}', detail: 'Точка входа C++', doc: 'Шаблон C++ программы' },
    { label: 'cout', kind: 15, snippet: 'std::cout << ${1} << std::endl;', detail: 'std::cout', doc: 'Вывод в консоль' },
    { label: 'cin', kind: 15, snippet: 'std::cin >> ${1};', detail: 'std::cin', doc: 'Ввод из консоли' },
    { label: 'vector', kind: 15, snippet: 'std::vector<${1:int}> ${2:vec} = {${3}};', detail: 'std::vector', doc: 'Динамический массив' },
    { label: 'for-range', kind: 15, snippet: 'for (const auto& ${1:item} : ${2:container}) {\n    ${3}\n}', detail: 'Range-for', doc: 'Обход контейнера' },
    { label: 'class', kind: 15, snippet: 'class ${1:ClassName} {\npublic:\n    ${1:ClassName}() {}\n};', detail: 'Класс C++', doc: 'Определение класса' }
  ],
  csharp: [
    { label: 'Console.WriteLine', kind: 1, snippet: 'Console.WriteLine(${1});', detail: 'Метод Console.WriteLine', doc: 'Вывод в консоль с новой строки' },
    { label: 'Console.Write', kind: 1, snippet: 'Console.Write(${1});', detail: 'Метод Console.Write', doc: 'Вывод без новой строки' },
    { label: 'Console.ReadLine', kind: 1, snippet: 'Console.ReadLine()', detail: 'Метод Console.ReadLine', doc: 'Чтение строки из консоли' },
    { label: 'cw', kind: 15, snippet: 'Console.WriteLine(${1});', detail: 'Console.WriteLine (сниппет)', doc: 'Быстрый ввод вывода' },
    { label: 'class', kind: 15, snippet: 'class ${1:Program}\n{\n    static void Main()\n    {\n        ${2}\n    }\n}', detail: 'Класс Program', doc: 'Шаблон класса C#' },
    { label: 'prop', kind: 15, snippet: 'public ${1:int} ${2:MyProperty} { get; set; }', detail: 'Автосвойство { get; set; }', doc: 'Свойство с автоаксессорами' },
    { label: 'foreach', kind: 15, snippet: 'foreach (var ${1:item} in ${2:collection})\n{\n    ${3}\n}', detail: 'Цикл foreach', doc: 'Обход элементов' },
    { label: 'for', kind: 15, snippet: 'for (int ${1:i} = 0; ${1:i} < ${2:10}; ${1:i}++)\n{\n    ${3}\n}', detail: 'Цикл for', doc: 'Цикл со счетчиком' },
    { label: 'List', kind: 7 /* Class */, snippet: 'List<${1:int}> ${2:list} = new List<${1:int}>();', detail: 'Коллекция List<T>', doc: 'Динамический список' },
    { label: 'int.Parse', kind: 1, snippet: 'int.Parse(${1})', detail: 'Парсинг int', doc: 'Преобразование строки в число' },
    { label: 'double.Parse', kind: 1, snippet: 'double.Parse(${1})', detail: 'Парсинг double', doc: 'Преобразование строки в double' },
    { label: 'static void Main', kind: 15, snippet: 'static void Main()\n{\n    ${1}\n}', detail: 'Метод Main', doc: 'Точка входа C#' }
  ],
  objc: [
    { label: 'NSLog', kind: 1, snippet: 'NSLog(@"${1:%@}", ${2});', detail: 'Функция NSLog', doc: 'Вывод в консоль Apple' },
    { label: 'main', kind: 15, snippet: 'int main(int argc, const char * argv[]) {\n    @autoreleasepool {\n        ${1}\n    }\n    return 0;\n}', detail: 'Точка входа Objective-C', doc: 'Шаблон программы' },
    { label: 'NSString', kind: 7, snippet: 'NSString *${1:str} = @"${2}";', detail: 'Строка NSString', doc: 'Строковый объект' },
    { label: 'NSArray', kind: 7, snippet: 'NSArray *${1:arr} = @[${2}];', detail: 'Массив NSArray', doc: 'Список объектов' }
  ],
  rust: [
    { label: 'main', kind: 15, snippet: 'fn main() {\n    ${1}\n}', detail: 'Точка входа fn main', doc: 'Главная функция Rust' },
    { label: 'println!', kind: 1, snippet: 'println!("${1}", ${2});', detail: 'Макрос println!', doc: 'Вывод с переводом строки' },
    { label: 'print!', kind: 1, snippet: 'print!("${1}", ${2});', detail: 'Макрос print!', doc: 'Вывод без перевода строки' },
    { label: 'fn', kind: 15, snippet: 'fn ${1:name}(${2}) -> ${3:i32} {\n    ${4}\n}', detail: 'Функция fn', doc: 'Объявление функции' },
    { label: 'let mut', kind: 15, snippet: 'let mut ${1:var} = ${2};', detail: 'Изменяемая переменная', doc: 'let mut' },
    { label: 'struct', kind: 15, snippet: 'struct ${1:Name} {\n    ${2:field}: ${3:i32},\n}', detail: 'Структура struct', doc: 'Пользовательский тип' },
    { label: 'match', kind: 15, snippet: 'match ${1:expr} {\n    ${2:pattern} => ${3},\n    _ => ${4},\n}', detail: 'Сопоставление match', doc: 'Pattern matching' }
  ],
  '1c': [
    { label: 'Сообщить', kind: 1, snippet: 'Сообщить("${1:Текст}");', detail: 'Функция Сообщить', doc: 'Вывод сообщения в 1С' },
    { label: 'Если', kind: 15, snippet: 'Если ${1:Условие} Тогда\n    ${2}\nИначе\n    ${3}\nКонецЕсли;', detail: 'Если-Тогда-КонецЕсли', doc: 'Условный оператор' },
    { label: 'Для', kind: 15, snippet: 'Для ${1:Сч} = 1 По ${2:10} Цикл\n    ${3}\nКонецЦикла;', detail: 'Для ... По ... Цикл', doc: 'Цикл со счетчиком' },
    { label: 'ДляКаждого', kind: 15, snippet: 'Для Каждого ${1:Элемент} Из ${2:Коллекция} Цикл\n    ${3}\nКонецЦикла;', detail: 'Для Каждого Из', doc: 'Обход элементов' },
    { label: 'Процедура', kind: 15, snippet: 'Процедура ${1:Имя}(${2})\n    ${3}\nКонецПроцедуры', detail: 'Процедура', doc: 'Подпрограмма без возврата' },
    { label: 'Функция', kind: 15, snippet: 'Функция ${1:Имя}(${2})\n    ${3}\n    Возврат ${4};\nКонецФункции', detail: 'Функция с возвратом', doc: 'Подпрограмма с возвратом' },
    { label: 'Массив', kind: 15, snippet: '${1:Массив} = Новый Массив;\n${1:Массив}.Добавить(${2});', detail: 'Новый Массив', doc: 'Создание и наполнение массива' },
    { label: 'Структура', kind: 15, snippet: '${1:Стр} = Новый Структура("${2:Ключ}", ${3:Значение});', detail: 'Новый Структура', doc: 'Коллекция ключ-значение' },
    { label: 'ТаблицаЗначений', kind: 15, snippet: '${1:ТЗ} = Новый ТаблицаЗначений;\n${1:ТЗ}.Колонки.Добавить("${2:Колонка}");', detail: 'ТаблицаЗначений', doc: 'Двумерная таблица в памяти' }
  ],
  python: [
    { label: 'print', kind: 1, snippet: 'print(${1})', detail: 'Функция print', doc: 'Вывод в консоль' },
    { label: 'input', kind: 1, snippet: 'input("${1}")', detail: 'Функция input', doc: 'Ввод строки' },
    { label: 'len', kind: 1, snippet: 'len(${1})', detail: 'Функция len', doc: 'Длина коллекции' },
    { label: 'range', kind: 1, snippet: 'range(${1:10})', detail: 'Функция range', doc: 'Диапазон чисел' },
    { label: 'def', kind: 15, snippet: 'def ${1:name}(${2}):\n    ${3:pass}', detail: 'Определение функции', doc: 'def func():' },
    { label: 'for-range', kind: 15, snippet: 'for ${1:i} in range(${2:10}):\n    ${3}', detail: 'Цикл for in range', doc: 'Итерация по числам' },
    { label: 'if-main', kind: 15, snippet: 'if __name__ == "__main__":\n    ${1:main()}', detail: 'Блок запуска скрипта', doc: 'Точка входа' },
    { label: 'class', kind: 15, snippet: 'class ${1:ClassName}:\n    def __init__(self${2}):\n        ${3:pass}', detail: 'Класс Python', doc: 'Определение класса' }
  ],
  javascript: [
    { label: 'console.log', kind: 1, snippet: 'console.log(${1});', detail: 'console.log', doc: 'Вывод в веб-консоль' },
    { label: 'clg', kind: 15, snippet: 'console.log(${1});', detail: 'Сниппет console.log', doc: 'Быстрый вывод' },
    { label: 'function', kind: 15, snippet: 'function ${1:name}(${2}) {\n    ${3}\n}', detail: 'Объявление функции', doc: 'function keyword' },
    { label: 'arrow', kind: 15, snippet: 'const ${1:name} = (${2}) => {\n    ${3}\n};', detail: 'Стрелочная функция', doc: 'const fn = () =>' },
    { label: 'for-of', kind: 15, snippet: 'for (const ${1:item} of ${2:array}) {\n    ${3}\n}', detail: 'Цикл for..of', doc: 'Обход элементов' }
  ],
  typescript: [
    { label: 'interface', kind: 15, snippet: 'interface ${1:Name} {\n    ${2:id}: ${3:number};\n}', detail: 'Интерфейс', doc: 'Контракт объекта' },
    { label: 'type', kind: 15, snippet: 'type ${1:Name} = ${2:string};', detail: 'Псевдоним типа', doc: 'type alias' }
  ],
  java: [
    { label: 'System.out.println', kind: 1, snippet: 'System.out.println(${1});', detail: 'Вывод в консоль', doc: 'Печать с переносом строки' },
    { label: 'sout', kind: 15, snippet: 'System.out.println(${1});', detail: 'Сниппет sout', doc: 'Быстрый println' },
    { label: 'psvm', kind: 15, snippet: 'public static void main(String[] args) {\n    ${1}\n}', detail: 'Метод main', doc: 'Точка входа программы' },
    { label: 'Scanner', kind: 7, snippet: 'Scanner in = new Scanner(System.in);\nint ${1:n} = in.nextInt();', detail: 'Чтение stdin', doc: 'Ввод Scanner' }
  ],
  sql: [
    { label: 'SELECT', kind: 14, snippet: 'SELECT ${1:*} FROM ${2:table};', detail: 'Запрос выборки', doc: 'SELECT * FROM' },
    { label: 'WHERE', kind: 14, snippet: 'WHERE ${1:condition}', detail: 'Фильтр строк', doc: 'WHERE' },
    { label: 'INSERT INTO', kind: 15, snippet: 'INSERT INTO ${1:table} (${2:columns}) VALUES (${3:values});', detail: 'Вставка строк', doc: 'INSERT INTO' },
    { label: 'CREATE TABLE', kind: 15, snippet: 'CREATE TABLE ${1:name} (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    ${2:title} TEXT NOT NULL\n);', detail: 'Создание таблицы', doc: 'DDL' }
  ],
  html: [
    { label: 'html5', kind: 15, snippet: '<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <title>${1:Title}</title>\n</head>\n<body>\n    ${2}\n</body>\n</html>', detail: 'Шаблон HTML5', doc: 'Базовая разметка' },
    { label: 'div', kind: 15, snippet: '<div class="${1:card}">\n    ${2}\n</div>', detail: 'Контейнер div', doc: 'Блочный элемент' },
    { label: 'button', kind: 15, snippet: '<button class="${1:btn}">${2:Нажми меня}</button>', detail: 'Кнопка button', doc: 'Интерактивная кнопка' }
  ],
  css: [
    { label: 'display: flex', kind: 15, snippet: 'display: flex;\njustify-content: center;\nalign-items: center;', detail: 'Flexbox контейнер', doc: 'Центрирование flex' },
    { label: 'display: grid', kind: 15, snippet: 'display: grid;\ngrid-template-columns: repeat(${1:3}, 1fr);\ngap: ${2:16px};', detail: 'CSS Grid сетка', doc: 'Сетка' }
  ],
  lua: [
    { label: 'print', kind: 1, snippet: 'print(${1})', detail: 'Вывод в консоль', doc: 'Функция print' },
    { label: 'function', kind: 15, snippet: 'function ${1:name}(${2})\n    ${3}\nend', detail: 'Функция Lua', doc: 'Определение функции' },
    { label: 'local-func', kind: 15, snippet: 'local function ${1:name}(${2})\n    ${3}\nend', detail: 'Локальная функция', doc: 'Локальная область видимости' },
    { label: 'for-i', kind: 15, snippet: 'for ${1:i} = ${2:1}, ${3:10} do\n    ${4}\nend', detail: 'Числовой цикл for', doc: 'Итерация по диапазону' },
    { label: 'for-ipairs', kind: 15, snippet: 'for ${1:i}, ${2:v} in ipairs(${3:list}) do\n    ${4}\nend', detail: 'Цикл ipairs', doc: 'Итерация по массиву' },
    { label: 'for-pairs', kind: 15, snippet: 'for ${1:k}, ${2:v} in pairs(${3:table}) do\n    ${4}\nend', detail: 'Цикл pairs', doc: 'Итерация по таблице/словарю' },
    { label: 'table.insert', kind: 1, snippet: 'table.insert(${1:tbl}, ${2:val})', detail: 'Вставка в таблицу', doc: 'table.insert' },
    { label: 'setmetatable', kind: 1, snippet: 'setmetatable(${1:tbl}, ${2:mt})', detail: 'Метатаблица', doc: 'ООП в Lua' }
  ],
  assembly: [
    { label: 'template_start', kind: 15, snippet: 'section .data\n    ${1:msg} db "${2:Hello, World!}", 10\n    ${1:msg}_len equ $ - ${1:msg}\n\nsection .text\n    global _start\n\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, ${1:msg}\n    mov rdx, ${1:msg}_len\n    syscall\n\n    mov rax, 60\n    mov rdi, 0\n    syscall', detail: 'Шаблон x86-64 NASM', doc: 'Полный каркас программы' },
    { label: 'sys_write', kind: 15, snippet: 'mov rax, 1          ; sys_write\nmov rdi, 1          ; stdout\nmov rsi, ${1:msg}    ; buffer\nmov rdx, ${2:len}    ; length\nsyscall', detail: 'Вызов sys_write', doc: 'Вывод строки через syscall' },
    { label: 'sys_exit', kind: 15, snippet: 'mov rax, 60         ; sys_exit\nmov rdi, ${1:0}      ; exit code\nsyscall', detail: 'Вызов sys_exit', doc: 'Завершение программы' },
    { label: 'sys_read', kind: 15, snippet: 'mov rax, 0          ; sys_read\nmov rdi, 0          ; stdin\nmov rsi, ${1:buf}    ; buffer\nmov rdx, ${2:64}     ; max bytes\nsyscall', detail: 'Вызов sys_read', doc: 'Чтение stdin' },
    { label: 'section .text', kind: 14, snippet: 'section .text\n    global _start\n_start:\n    ${1}', detail: 'Секция кода', doc: 'section .text' },
    { label: 'section .data', kind: 14, snippet: 'section .data\n    ${1:msg} db "${2:text}", 10', detail: 'Секция данных', doc: 'section .data' },
    { label: 'mov', kind: 14, snippet: 'mov ${1:rax}, ${2:0}', detail: 'Инструкция mov', doc: 'Перемещение данных' },
    { label: 'add', kind: 14, snippet: 'add ${1:rax}, ${2:1}', detail: 'Инструкция add', doc: 'Сложение' },
    { label: 'sub', kind: 14, snippet: 'sub ${1:rax}, ${2:1}', detail: 'Инструкция sub', doc: 'Вычитание' },
    { label: 'cmp', kind: 14, snippet: 'cmp ${1:rax}, ${2:0}\nje ${3:label}', detail: 'Сравнение и переход', doc: 'cmp + je' }
  ]
};

// Member dot-completions
const MEMBER_COMPLETIONS: Record<string, Record<string, { label: string; kind: Monaco.languages.CompletionItemKind; detail: string; insertText: string }[]>> = {
  csharp: {
    'Console.': [
      { label: 'WriteLine', kind: 1, detail: 'void WriteLine(object value)', insertText: 'WriteLine(${1});' },
      { label: 'Write', kind: 1, detail: 'void Write(object value)', insertText: 'Write(${1});' },
      { label: 'ReadLine', kind: 1, detail: 'string? ReadLine()', insertText: 'ReadLine()' },
      { label: 'Clear', kind: 1, detail: 'void Clear()', insertText: 'Clear();' }
    ],
    'int.': [
      { label: 'Parse', kind: 1, detail: 'int Parse(string s)', insertText: 'Parse(${1})' },
      { label: 'TryParse', kind: 1, detail: 'bool TryParse(string s, out int result)', insertText: 'TryParse(${1}, out int res)' }
    ],
    'double.': [
      { label: 'Parse', kind: 1, detail: 'double Parse(string s)', insertText: 'Parse(${1})' }
    ]
  },
  java: {
    'System.': [
      { label: 'out', kind: 9 /* Field */, detail: 'PrintStream out', insertText: 'out' },
      { label: 'in', kind: 9, detail: 'InputStream in', insertText: 'in' },
      { label: 'err', kind: 9, detail: 'PrintStream err', insertText: 'err' }
    ],
    'System.out.': [
      { label: 'println', kind: 1, detail: 'void println(Object x)', insertText: 'println(${1});' },
      { label: 'print', kind: 1, detail: 'void print(Object x)', insertText: 'print(${1});' },
      { label: 'printf', kind: 1, detail: 'PrintStream printf(String fmt, Object... args)', insertText: 'printf("${1:%s}\\n", ${2});' }
    ]
  },
  '1c': {
    '.': [
      { label: 'Добавить', kind: 1, detail: 'Добавить(Значение)', insertText: 'Добавить(${1});' },
      { label: 'Количество', kind: 1, detail: 'Количество() -> Число', insertText: 'Количество()' },
      { label: 'Очистить', kind: 1, detail: 'Очистить()', insertText: 'Очистить();' },
      { label: 'Найти', kind: 1, detail: 'Найти(Значение)', insertText: 'Найти(${1})' },
      { label: 'Вставить', kind: 1, detail: 'Вставить(Ключ, Значение)', insertText: 'Вставить(${1});' }
    ]
  }
};

let registeredOnce = false;

export function registerIntelligence(monaco: typeof Monaco) {
  if (registeredOnce) return;
  registeredOnce = true;

  // 1. Register 1C Language Definition
  try {
    monaco.languages.register({ id: '1c' });
    monaco.languages.setLanguageConfiguration('1c', {
      comments: { lineComment: '//' },
      brackets: [['(', ')'], ['[', ']']],
      autoClosingPairs: [
        { open: '(', close: ')' },
        { open: '[', close: ']' },
        { open: '"', close: '"' }
      ]
    });
    monaco.languages.setMonarchTokensProvider('1c', {
      defaultToken: '',
      tokenPostfix: '.1c',
      keywords: [
        'Процедура', 'КонецПроцедуры', 'Функция', 'КонецФункции',
        'Если', 'Тогда', 'Иначе', 'ИначеЕсли', 'КонецЕсли',
        'Для', 'Каждого', 'Из', 'По', 'Цикл', 'КонецЦикла',
        'Попытка', 'Исключение', 'КонецПопытки',
        'Возврат', 'Новый', 'И', 'ИЛИ', 'НЕ', 'Истина', 'Ложь', 'Неопределено', 'Экспорт'
      ],
      tokenizer: {
        root: [
          [/\/\/.*$/, 'comment'],
          [/"([^"\\]|\\.)*"/, 'string'],
          [/\b(Процедура|КонецПроцедуры|Функция|КонецФункции|Если|Тогда|Иначе|ИначеЕсли|КонецЕсли|Для|Каждого|Из|По|Цикл|КонецЦикла|Попытка|Исключение|КонецПопытки|Возврат|Новый|И|ИЛИ|НЕ|Истина|Ложь|Неопределено|Экспорт)\b/, 'keyword'],
          [/\b(Число|Строка|Дата|Булево|Массив|Структура|Соответствие|СписокЗначений|ТаблицаЗначений)\b/, 'type'],
          [/\b(Сообщить|СтрДлина|ВРег|НРег|СокрЛП|СокрЛ|СокрП|Формат|Окр|Цел|ТекущаяДата)\b/, 'keyword.flow'],
          [/\d+/, 'number'],
          [/[{}()\[\]]/, '@brackets'],
          [/[;,.]/, 'delimiter']
        ]
      }
    });
  } catch {
    // Already defined or registered
  }

  // 1b. Register x86-64 NASM Assembly Language Definition
  try {
    monaco.languages.register({ id: 'assembly', extensions: ['.asm', '.s', '.inc'] });
    monaco.languages.setLanguageConfiguration('assembly', {
      comments: { lineComment: ';' },
      brackets: [['[', ']']],
      autoClosingPairs: [
        { open: '[', close: ']' },
        { open: '"', close: '"' },
        { open: "'", close: "'" }
      ]
    });
    monaco.languages.setMonarchTokensProvider('assembly', {
      defaultToken: '',
      tokenPostfix: '.asm',
      tokenizer: {
        root: [
          [/;.*$/, 'comment'],
          [/"([^"\\]|\\.)*"/, 'string'],
          [/'([^'\\]|\\.)*'/, 'string'],
          [/^[a-zA-Z_][a-zA-Z0-9_]*:/, 'type.identifier'],
          [/\b(section|global|extern|equ|db|dw|dd|dq|resb|resw|resd|resq|byte|word|dword|qword)\b/i, 'keyword.directive'],
          [/\b(mov|lea|xchg|add|sub|inc|dec|imul|idiv|mul|div|neg|and|or|xor|not|shl|shr|sal|sar|cmp|test|jmp|je|jz|jne|jnz|jl|jle|jg|jge|js|jns|call|ret|loop|push|pop|syscall|nop)\b/i, 'keyword'],
          [/\b(rax|rbx|rcx|rdx|rsi|rdi|rbp|rsp|r8|r9|r10|r11|r12|r13|r14|r15|eax|ebx|ecx|edx|esi|edi|ebp|esp|r8d|r9d|r10d|r11d|r12d|r13d|r14d|r15d|ax|bx|cx|dx|si|di|bp|sp|al|bl|cl|dl|ah|bh|ch|dh)\b/i, 'variable.predefined'],
          [/0x[0-9a-fA-F]+|-?\d+/, 'number'],
          [/[\[\]]/, '@brackets'],
          [/[,:]/, 'delimiter']
        ]
      }
    });
  } catch {
    // Already defined
  }

  // 2. Hover Providers for all languages
  for (const [lang, docs] of Object.entries(HOVER_DOCS)) {
    const monacoLang = lang === 'objc' ? 'objective-c' : lang;
    monaco.languages.registerHoverProvider(monacoLang, {
      provideHover: (model, position) => {
        const lineContent = model.getLineContent(position.lineNumber);
        const word = model.getWordAtPosition(position);
        if (!word) return null;

        // Try to match multi-word symbols like Console.WriteLine, System.out.println
        let matchedKey = word.word;
        let matchedDoc: DocEntry | undefined = docs[word.word];

        // Search if full expression is part of the line at this position
        for (const [key, entry] of Object.entries(docs)) {
          if (key.includes('.')) {
            const idx = lineContent.indexOf(key);
            if (idx !== -1 && position.column >= idx + 1 && position.column <= idx + key.length + 1) {
              matchedKey = key;
              matchedDoc = entry;
              break;
            }
          }
        }

        if (!matchedDoc) return null;

        const contents: Monaco.IMarkdownString[] = [
          { value: `\`\`\`${monacoLang}\n${matchedDoc.signature}\n\`\`\`` },
          { value: matchedDoc.doc }
        ];
        if (matchedDoc.example) {
          contents.push({ value: `**Пример:**\n\`\`\`${monacoLang}\n${matchedDoc.example}\n\`\`\`` });
        }
        return { contents };
      }
    });
  }

  // 3. Signature Help Provider for all languages
  const triggerLangs = ['c', 'cpp', 'csharp', 'objective-c', 'rust', '1c', 'python', 'javascript', 'typescript', 'java', 'lua', 'assembly'];
  for (const lang of triggerLangs) {
    monaco.languages.registerSignatureHelpProvider(lang, {
      signatureHelpTriggerCharacters: ['(', ','],
      signatureHelpRetriggerCharacters: [','],
      provideSignatureHelp: (model, position) => {
        const lineContent = model.getLineContent(position.lineNumber).slice(0, position.column - 1);
        const lastParen = lineContent.lastIndexOf('(');
        if (lastParen === -1) return null;

        const beforeParen = lineContent.slice(0, lastParen).trim();
        const commaCount = (lineContent.slice(lastParen).match(/,/g) || []).length;

        // Find symbol before paren
        let foundSig: { label: string; doc: string; params: string[] } | undefined;
        for (const [name, sig] of Object.entries(SIGNATURES)) {
          if (beforeParen.endsWith(name)) {
            foundSig = sig;
            break;
          }
        }

        if (!foundSig) return null;

        return {
          value: {
            signatures: [{
              label: foundSig.label,
              documentation: foundSig.doc,
              parameters: foundSig.params.map(p => ({ label: p }))
            }],
            activeSignature: 0,
            activeParameter: Math.min(commaCount, foundSig.params.length - 1)
          },
          dispose: () => {}
        };
      }
    });
  }

  // 4. Completion Item Providers for all languages
  const ALL_LANGUAGES = ['c', 'cpp', 'csharp', 'objective-c', 'rust', '1c', 'python', 'javascript', 'typescript', 'java', 'sql', 'html', 'css', 'lua', 'assembly'];

  for (const lang of ALL_LANGUAGES) {
    const list = COMMON_COMPLETIONS[lang === 'objective-c' ? 'objc' : lang] || [];
    const memberMap = MEMBER_COMPLETIONS[lang === 'objective-c' ? 'objc' : lang] || {};

    monaco.languages.registerCompletionItemProvider(lang, {
      triggerCharacters: ['.', ':', '<', '(', '"', ' '],
      provideCompletionItems: (model, position) => {
        const word = model.getWordUntilPosition(position);
        const range = {
          startLineNumber: position.lineNumber,
          endLineNumber: position.lineNumber,
          startColumn: word.startColumn,
          endColumn: word.endColumn
        };

        const lineBefore = model.getLineContent(position.lineNumber).slice(0, position.column - 1);

        // Check member access after dot
        for (const [prefix, members] of Object.entries(memberMap)) {
          if (lineBefore.endsWith(prefix) || (prefix === '.' && lineBefore.endsWith('.'))) {
            const memberSuggestions: Monaco.languages.CompletionItem[] = members.map(m => ({
              label: m.label,
              kind: m.kind,
              detail: m.detail,
              insertText: m.insertText,
              insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              range
            }));
            return { suggestions: memberSuggestions };
          }
        }

        // General suggestions
        const suggestions: Monaco.languages.CompletionItem[] = list.map(item => ({
          label: item.label,
          kind: item.kind,
          detail: item.detail,
          documentation: { value: item.doc },
          insertText: item.snippet || item.label,
          insertTextRules: item.snippet ? monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet : undefined,
          range
        }));

        return { suggestions };
      }
    });
  }

  // 5. Lightweight bracket and syntax balance diagnostic linter
  monaco.editor.onDidCreateModel(model => {
    const updateMarkers = () => {
      const text = model.getValue();
      const markers: Monaco.editor.IMarkerData[] = [];
      const lines = text.split('\n');
      const stack: { char: string; line: number; col: number }[] = [];
      const pairs: Record<string, string> = { ')': '(', '}': '{', ']': '[' };

      for (let l = 0; l < lines.length; l++) {
        const line = lines[l];
        const trimmed = line.trim();
        if (trimmed.startsWith('//') || trimmed.startsWith('#')) continue;

        let inQuote = false, qChar = '';
        for (let c = 0; c < line.length; c++) {
          const ch = line[c];
          if ((ch === '"' || ch === "'") && (c === 0 || line[c - 1] !== '\\')) {
            if (!inQuote) { inQuote = true; qChar = ch; }
            else if (qChar === ch) { inQuote = false; }
          }
          if (inQuote) continue;

          if (ch === '(' || ch === '{' || ch === '[') {
            stack.push({ char: ch, line: l + 1, col: c + 1 });
          } else if (ch === ')' || ch === '}' || ch === ']') {
            const expected = pairs[ch];
            if (!stack.length || stack[stack.length - 1].char !== expected) {
              markers.push({
                severity: monaco.MarkerSeverity.Error,
                message: `Лишняя или несогласованная закрывающая скобка '${ch}'`,
                startLineNumber: l + 1,
                startColumn: c + 1,
                endLineNumber: l + 1,
                endColumn: c + 2
              });
            } else {
              stack.pop();
            }
          }
        }
      }

      for (const unclosed of stack) {
        markers.push({
          severity: monaco.MarkerSeverity.Warning,
          message: `Не закрыта скобка '${unclosed.char}'`,
          startLineNumber: unclosed.line,
          startColumn: unclosed.col,
          endLineNumber: unclosed.line,
          endColumn: unclosed.col + 1
        });
      }

      monaco.editor.setModelMarkers(model, 'devforge-linter', markers);
    };

    let timeout: any;
    model.onDidChangeContent(() => {
      clearTimeout(timeout);
      timeout = setTimeout(updateMarkers, 400);
    });
    setTimeout(updateMarkers, 400);
  });
}
