# -*- coding: utf-8 -*-
"""
C# Course Curriculum (18 lessons, order 1..18)
From basics (Console.WriteLine, variables, control flow) to arrays, methods, List<T>, and OOP classes.
"""

LESSONS = []

def add(id, title, topic, section, order, level, minutes, theory, syntax, example_code, task, starterCode, solCode, tests, guide_idea, life_ex, terms, ex_snippet, ex_expected):
    LESSONS.append({
        "id": id,
        "language": "csharp",
        "title": title,
        "topic": topic,
        "section": section,
        "order": order,
        "level": level,
        "minutes": minutes,
        "theory": theory,
        "syntax": syntax,
        "examples": [example_code],
        "task": task,
        "starterCode": starterCode,
        "tests": tests,
        "hints": [
            "Внимательно следите за регистром букв в Console.WriteLine и именах типов.",
            "Каждая инструкция в C# должна завершаться точкой с запятой (;).",
            "Код программы должен находиться внутри метода Main класса Program."
        ],
        "commonMistakes": "Опечатка в названии Console.WriteLine или пропущенная точка с запятой.",
        "solutionExplanation": "Решение написано с соблюдением стандартов платформы .NET и языка C#.",
        "xp": 50,
        "setupSql": "",
        "concepts": [topic],
        "walkthrough": ["Изучите структуру класса Program", "Напишите инструкции в методе Main", "Запустите тесты"],
        "prerequisites": [LESSONS[-1]["id"]] if LESSONS else [],
        "resources": [{"title": f"Справочник: {topic}", "url": f"https://devforge.local/docs/{id}", "language": "RU"}],
        "lifeExample": life_ex,
        "guide": {
            "version": 1,
            "idea": guide_idea,
            "steps": [
                "Разберите назначение класса и метода Main.",
                "Изучите синтаксис команды и ее влияние на консоль.",
                "Выполните задание в окне редактора."
            ],
            "experiment": "Попробуйте изменить выводимый текст или параметры и посмотрите на результат в терминале.",
            "terms": terms,
            "solution": solCode,
            "taskSteps": ["Откройте метод Main", "Напишите команду Console.WriteLine", "Проверьте отсутствие синтаксических ошибок"],
            "checklist": ["Синтаксис корректен", "Тесты пройдены успешно"],
            "taskTables": [],
            "example": {
                "kind": "stdout",
                "code": ex_snippet,
                "expected": ex_expected,
                "setupSql": "",
                "tables": []
            }
        }
    })

# 1. First program
add(
    "cs-first-console", "Первая программа на C#", "Основы", "Введение", 1, "С нуля", 10,
    "Вывод информации в консоль с помощью Console.WriteLine платформы .NET.",
    "Console.WriteLine(\"Привет, мир!\");",
    "using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Hello .NET!\");\n    }\n}",
    "Напишите программу на C#, которая выводит строку 'Привет, C#!' в консоль.",
    "using System;\n\nclass Program {\n    static void Main() {\n        // Напишите вывод здесь\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Привет, C#!\");\n    }\n}",
    [{"id": "t1", "label": "Вывод в консоль", "expected": "Привет, C#!"}],
    "C# — один из самых популярных и удобных строго типизированных языков, созданный компанией Microsoft для платформы .NET. Метод Console.WriteLine выводит переданный текст на экран и автоматически переносит курсор на следующую строчку.",
    "Представьте принтер: вы отправляете строку на печать, он печатает её на листе и подаёт бумагу дальше на одну строку.",
    [{"term": "Console.WriteLine", "meaning": "Метод вывода строки в консоль с переносом строки"}, {"term": "Main()", "meaning": "Точка входа в программу на C#"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Старт .NET\");\n    }\n}",
    "Старт .NET\n"
)

# 2. Variables & types
add(
    "cs-variables-types", "Переменные и базовые типы", "Переменные", "Основы языка", 2, "С нуля", 12,
    "Типы данных int, double, string, bool для хранения чисел, строк и логических значений.",
    "int age = 25;\nstring name = \"Алиса\";",
    "int x = 10;\ndouble pi = 3.14;\nstring text = \"Данные\";\nbool flag = true;",
    "Объявите строковую переменную language со значением 'C#' и целочисленную переменную year со значением 2000. Выведите language, а на следующей строке year.",
    "using System;\n\nclass Program {\n    static void Main() {\n        // Объявите переменные и выведите их\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        string language = \"C#\";\n        int year = 2000;\n        Console.WriteLine(language);\n        Console.WriteLine(year);\n    }\n}",
    [{"id": "t1", "label": "Вывод языка и года", "expected": "C#\n2000"}],
    "Переменные в C# имеют строгую типизацию: компилятор точно знает, сколько памяти занимает переменная и какие операции с ней разрешены. Тип int хранит целые числа, double — вещественные, string — текст в двойных кавычках, а bool — логические флаги true/false.",
    "Каждая переменная — это подписанный ящик на складе строго определенной формы: в круглый кладут мячи, в плоский — документы.",
    [{"term": "int", "meaning": "32-битное целое число со знаком"}, {"term": "string", "meaning": "Последовательность символов в кодировке UTF-16"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        string city = \"Москва\";\n        Console.WriteLine(city);\n    }\n}",
    "Москва\n"
)

# 3. Arithmetic & interpolation
add(
    "cs-arithmetic", "Арифметика и интерполяция строк", "Операции", "Основы языка", 3, "Базовый", 12,
    "Арифметические операции +, -, *, / и строковая интерполяция с префиксом $.",
    "int sum = a + b;\nConsole.WriteLine($\"Сумма: {sum}\");",
    "int a = 15;\nint b = 4;\nConsole.WriteLine($\"{a} + {b} = {a + b}\");",
    "Даны две переменные: price = 250 и count = 3. Вычислите общую стоимость и выведите строку в формате 'Итого: 750 руб.' с помощью интерполяции строк.",
    "using System;\n\nclass Program {\n    static void Main() {\n        int price = 250;\n        int count = 3;\n        // Посчитайте total и выведите через $\"Итого: ...\"\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int price = 250;\n        int count = 3;\n        int total = price * count;\n        Console.WriteLine($\"Итого: {total} руб.\");\n    }\n}",
    [{"id": "t1", "label": "Итоговая стоимость", "expected": "Итого: 750 руб."}],
    "Интерполяция строк $\"... {выражение} ...\" в C# позволяет гармонично вставлять переменные и вычисления прямо внутрь текста без громоздкой конкатенации. Арифметические операторы работают привычным образом: сложение, вычитание, умножение и целочисленное деление.",
    "Словно заполнение бланка или чека: шаблон текста уже готов, а в фигурные скобки подставляются итоговые расчетные значения.",
    [{"term": "Интерполяция строк", "meaning": "Синтаксис $\"...{переменная}...\" для вставки значений в строку"}, {"term": "Оператор *", "meaning": "Умножение чисел в C#"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int a = 4;\n        int b = 5;\n        Console.WriteLine($\"Площадь: {a * b}\");\n    }\n}",
    "Площадь: 20\n"
)

# 4. If / Else
add(
    "cs-if-else", "Условные конструкции if / else", "Ветвление", "Управление потоком", 4, "Базовый", 15,
    "Ветвление алгоритма с помощью операторов if, else if и else.",
    "if (score >= 60) {\n    Console.WriteLine(\"Сдал\");\n} else {\n    Console.WriteLine(\"Пересдача\");\n}",
    "int n = 10;\nif (n > 0) Console.WriteLine(\"Положительное\");",
    "Переменная score равна 85. Если score >= 90, выведите 'Отлично', если score >= 75 — 'Хорошо', иначе 'Удовлетворительно'.",
    "using System;\n\nclass Program {\n    static void Main() {\n        int score = 85;\n        // Добавьте проверку if / else if / else\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int score = 85;\n        if (score >= 90) {\n            Console.WriteLine(\"Отлично\");\n        } else if (score >= 75) {\n            Console.WriteLine(\"Хорошо\");\n        } else {\n            Console.WriteLine(\"Удовлетворительно\");\n        }\n    }\n}",
    [{"id": "t1", "label": "Проверка оценки", "expected": "Хорошо"}],
    "Ветвление позволяет программе принимать решения на основе данных. Блок if выполняется только при истинности логического выражения. Конструкции else if дают возможность проверить цепочку взаимоисключающих условий, а блок else служит запасным вариантом.",
    "Как стрелочник на железной дороге: поезд направляется на первый путь, если он свободен, иначе на второй, а если оба заняты — на запасной путь.",
    [{"term": "if", "meaning": "Оператор ветвления, выполняющий блок при истинности условия"}, {"term": "else if", "meaning": "Дополнительная проверка условия в случае ложности предыдущих"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int temp = 22;\n        if (temp > 20) Console.WriteLine(\"Тепло\");\n    }\n}",
    "Тепло\n"
)

# 5. Switch
add(
    "cs-switch", "Оператор switch / case", "Ветвление", "Управление потоком", 5, "Базовый", 12,
    "Множественный выбор значения переменной через оператор switch с ключевыми словами case и break.",
    "switch (code) {\n    case 1: Console.WriteLine(\"Один\"); break;\n    default: Console.WriteLine(\"Другое\"); break;\n}",
    "int day = 3;\nswitch (day) {\n    case 1: Console.WriteLine(\"Пн\"); break;\n    case 2: Console.WriteLine(\"Вт\"); break;\n    default: Console.WriteLine(\"День\"); break;\n}",
    "Дана переменная int level = 2;. Используя switch, выведите 'Начальный' для 1, 'Средний' для 2, 'Продвинутый' для 3, и 'Неизвестно' по умолчанию.",
    "using System;\n\nclass Program {\n    static void Main() {\n        int level = 2;\n        // Напишите switch (level)\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int level = 2;\n        switch (level) {\n            case 1:\n                Console.WriteLine(\"Начальный\");\n                break;\n            case 2:\n                Console.WriteLine(\"Средний\");\n                break;\n            case 3:\n                Console.WriteLine(\"Продвинутый\");\n                break;\n            default:\n                Console.WriteLine(\"Неизвестно\");\n                break;\n        }\n    }\n}",
    [{"id": "t1", "label": "Выбор уровня", "expected": "Средний"}],
    "Оператор switch удобен, когда нужно сопоставить одну переменную со множеством дискретных константных значений. Каждая ветка case завершается оператором break, чтобы предотвратить случайное проваливание в следующий блок, а ветка default отрабатывает, если ни одно значение не подошло.",
    "Как кнопки выбора напитка в кофейном аппарате: нажал кнопку 1 — получил эспрессо, кнопку 2 — капучино.",
    [{"term": "switch", "meaning": "Оператор множественного выбора значения"}, {"term": "break", "meaning": "Прерывание выполнения текущей ветки или цикла"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int code = 1;\n        switch(code) {\n            case 1: Console.WriteLine(\"Успех\"); break;\n        }\n    }\n}",
    "Успех\n"
)

# 6. While Loop
add(
    "cs-while-loop", "Цикл while", "Циклы", "Управление потоком", 6, "Базовый", 12,
    "Повторение действий с помощью цикла с предусловием while.",
    "int i = 0;\nwhile (i < 5) {\n    Console.WriteLine(i);\n    i++;\n}",
    "int count = 3;\nwhile (count > 0) {\n    Console.WriteLine(count);\n    count--;\n}",
    "Используя цикл while, выведите числа от 1 до 4 включительно, каждое на новой строке.",
    "using System;\n\nclass Program {\n    static void Main() {\n        int i = 1;\n        // Напишите цикл while\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int i = 1;\n        while (i <= 4) {\n            Console.WriteLine(i);\n            i++;\n        }\n    }\n}",
    [{"id": "t1", "label": "Числа от 1 до 4", "expected": "1\n2\n3\n4"}],
    "Цикл while проверяет условие перед каждой итерацией. Если условие истинно, тело цикла выполняется, после чего условие проверяется повторно. Обязательно нужно менять переменную условия внутри цикла, иначе возникнет бесконечный цикл.",
    "Словно бегун на стадионе: пока не прозвучал свисток судьи о завершении кругов, он продолжает бежать следующий круг.",
    [{"term": "while", "meaning": "Цикл, выполняющийся до тех пор, пока условие истинно"}, {"term": "Инкремент (i++)", "meaning": "Увеличение значения переменной на единицу"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int k = 1;\n        while (k <= 2) { Console.WriteLine(k); k++; }\n    }\n}",
    "1\n2\n"
)

# 7. For Loop
add(
    "cs-for-loop", "Цикл for", "Циклы", "Управление потоком", 7, "Базовый", 12,
    "Классический цикл for с инициализацией, условием продолжения и шагом.",
    "for (int i = 0; i < 5; i++) {\n    Console.WriteLine(i);\n}",
    "for (int i = 2; i <= 6; i += 2) {\n    Console.WriteLine(i);\n}",
    "Используя цикл for, вычислите сумму чисел от 1 до 5 включительно (1+2+3+4+5) и выведите строку 'Сумма: 15'.",
    "using System;\n\nclass Program {\n    static void Main() {\n        int sum = 0;\n        // Цикл for от 1 до 5\n        // Выведите $\"Сумма: {sum}\"\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int sum = 0;\n        for (int i = 1; i <= 5; i++) {\n            sum += i;\n        }\n        Console.WriteLine($\"Сумма: {sum}\");\n    }\n}",
    [{"id": "t1", "label": "Сумма 1..5", "expected": "Сумма: 15"}],
    "Цикл for объединяет инициализацию счетчика, условие выхода и шаг приращения в одном компактном заголовке. Это самый распространенный цикл, когда количество повторений известно заранее. Переменная счетчика локализована внутри заголовка цикла.",
    "Как шаги по ступенькам лестницы: вы начинаете с первой ступени, шагаете на одну вверх и останавливаетесь на верхней площадке.",
    [{"term": "for", "meaning": "Цикл со счетчиком, объединяющий старт, условие и шаг"}, {"term": "sum += i", "meaning": "Сокращенная форма прибавления: sum = sum + i"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        for (int i = 1; i <= 3; i++) Console.WriteLine(i * 10);\n    }\n}",
    "10\n20\n30\n"
)

# 8. Arrays
add(
    "cs-arrays", "Одномерные массивы", "Массивы", "Структуры данных", 8, "Базовый", 15,
    "Создание массивов фиксированного размера, индексация с нуля и свойство Length.",
    "int[] numbers = new int[] { 10, 20, 30 };\nConsole.WriteLine(numbers[0]);",
    "string[] colors = { \"Красный\", \"Зеленый\", \"Синий\" };\nConsole.WriteLine(colors.Length);",
    "Создайте массив целых чисел с элементами 10, 20, 30, 40. Выведите первый элемент, последний элемент (по индексу 3) и длину массива каждый на новой строке.",
    "using System;\n\nclass Program {\n    static void Main() {\n        // Создайте массив и выведите [0], [3], Length\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        int[] items = new int[] { 10, 20, 30, 40 };\n        Console.WriteLine(items[0]);\n        Console.WriteLine(items[3]);\n        Console.WriteLine(items.Length);\n    }\n}",
    [{"id": "t1", "label": "Элементы и длина массива", "expected": "10\n40\n4"}],
    "Массив в C# представляет собой непрерывную последовательность однотипных элементов в памяти фиксированной длины. Доступ к элементам осуществляется по индексу в квадратных скобках [index], причем нумерация строго начинается с нуля. Свойство Length возвращает количество элементов.",
    "Органайзер для лекарств с пронумерованными ячейками: в каждой лежит таблетка одного типа, а ячейки пронумерованы от 0 до N-1.",
    [{"term": "Массив", "meaning": "Структура данных фиксированного размера, хранящая однотипные элементы"}, {"term": "Length", "meaning": "Свойство массива, возвращающее общее количество элементов"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int[] a = { 5, 8 };\n        Console.WriteLine(a[0] + a[1]);\n    }\n}",
    "13\n"
)

# 9. Foreach Loop
add(
    "cs-foreach", "Цикл foreach", "Массивы", "Структуры данных", 9, "Базовый", 12,
    "Удобный перебор элементов массива или коллекции без явного использования индексов.",
    "foreach (int item in numbers) {\n    Console.WriteLine(item);\n}",
    "string[] names = { \"Анна\", \"Борис\" };\nforeach (string name in names) {\n    Console.WriteLine(name);\n}",
    "Дан массив string[] words = { \"Code\", \"Build\", \"Run\" };. Используя цикл foreach, выведите каждое слово с восклицательным знаком (например, Code!).",
    "using System;\n\nclass Program {\n    static void Main() {\n        string[] words = { \"Code\", \"Build\", \"Run\" };\n        // Переберите массив через foreach\n    }\n}",
    "using System;\n\nclass Program {\n    static void Main() {\n        string[] words = { \"Code\", \"Build\", \"Run\" };\n        foreach (string w in words) {\n            Console.WriteLine($\"{w}!\");\n        }\n    }\n}",
    [{"id": "t1", "label": "Слова с восклицанием", "expected": "Code!\nBuild!\nRun!"}],
    "Цикл foreach последовательно извлекает каждый элемент коллекции, помещает его во временную переменную и передает в тело цикла. Это защищает от выхода за границы массива (IndexOutOfRangeException) и делает код чистым и читаемым.",
    "Конвейерная лента: каждый предмет по очереди подъезжает к вам, вы берете его, осматриваете и переходите к следующему.",
    [{"term": "foreach", "meaning": "Специальный цикл для безопасного перебора всех элементов коллекции"}, {"term": "in", "meaning": "Ключевое слово, указывающее источник данных для foreach"}],
    "using System;\n\nclass Program {\n    static void Main() {\n        int[] digits = { 1, 2 };\n        foreach (int d in digits) Console.WriteLine(d);\n    }\n}",
    "1\n2\n"
)

# 10. Methods Void
add(
    "cs-methods-void", "Статические методы (void)", "Методы", "Модульность", 10, "Базовый", 15,
    "Определение и вызов вспомогательных методов без возвращаемого значения (void).",
    "static void Greet(string name) {\n    Console.WriteLine($\"Привет, {name}!\");\n}",
    "static void PrintLine() {\n    Console.WriteLine(\"----------\");\n}",
    "Создайте статический метод PrintWelcome(string user), который выводит 'Добро пожаловать, {user}!'. В методе Main вызовите его для пользователя 'Алексей'.",
    "using System;\n\nclass Program {\n    // Объявите static void PrintWelcome...\n\n    static void Main() {\n        // Вызовите метод\n    }\n}",
    "using System;\n\nclass Program {\n    static void PrintWelcome(string user) {\n        Console.WriteLine($\"Добро пожаловать, {user}!\");\n    }\n\n    static void Main() {\n        PrintWelcome(\"Алексей\");\n    }\n}",
    [{"id": "t1", "label": "Вызов метода приветствия", "expected": "Добро пожаловать, Алексей!"}],
    "Методы позволяют разбить сложную программу на небольшие независимые подпрограммы. Ключевое слово void означает, что метод не возвращает никаких данных обратно вызывающему коду, а лишь производит действие (например, вывод на экран).",
    "Как кнопка на пульте: вы нажимаете ее, устройство совершает действие, но не выдает вам бумажный чек в ответ.",
    [{"term": "void", "meaning": "Тип возвращаемого значения для методов, которые ничего не возвращают"}, {"term": "Параметр метода", "meaning": "Переменная в объявлении метода, принимающая переданное значение"}],
    "using System;\n\nclass Program {\n    static void Ping() { Console.WriteLine(\"Понг\"); }\n    static void Main() { Ping(); }\n}",
    "Понг\n"
)

# 11. Methods Return
add(
    "cs-methods-return", "Методы с возвращаемым значением", "Методы", "Модульность", 11, "Базовый", 15,
    "Возврат результата работы метода с помощью ключевого слова return.",
    "static int Square(int x) {\n    return x * x;\n}",
    "static double Max(double a, double b) {\n    return a > b ? a : b;\n}",
    "Напишите метод Multiply(int a, int b), который возвращает их произведение. В Main вызовите его для чисел 6 и 7 и выведите результат.",
    "using System;\n\nclass Program {\n    // Напишите static int Multiply...\n\n    static void Main() {\n        // Вызовите Multiply(6, 7) и выведите\n    }\n}",
    "using System;\n\nclass Program {\n    static int Multiply(int a, int b) {\n        return a * b;\n    }\n\n    static void Main() {\n        int res = Multiply(6, 7);\n        Console.WriteLine(res);\n    }\n}",
    [{"id": "t1", "label": "Произведение 6 * 7", "expected": "42"}],
    "Если метод должен вычислить и вернуть значение в вызывающий код, вместо void указывается тип возвращаемых данных (например int, double, string). Для возврата значения используется инструкция return, которая немедленно завершает работу метода.",
    "Словно калькулятор: вы вводите два числа, нажимаете кнопку умножения и забираете вычисленный результат на экране.",
    [{"term": "return", "meaning": "Инструкция возврата значения из метода и выхода из него"}, {"term": "Сигнатура метода", "meaning": "Имя метода и типы его принимаемых параметров"}],
    "using System;\n\nclass Program {\n    static int DoubleIt(int n) { return n * 2; }\n    static void Main() { Console.WriteLine(DoubleIt(21)); }\n}",
    "42\n"
)

# 12. Method Overloading
add(
    "cs-methods-params", "Перегрузка методов", "Методы", "Модульность", 12, "Средний", 15,
    "Определение нескольких методов с одинаковым именем, но разным набором или типами параметров.",
    "static int Add(int a, int b) => a + b;\nstatic double Add(double a, double b) => a + b;",
    "static void Print(int x) { Console.WriteLine($\"Число: {x}\"); }\nstatic void Print(string s) { Console.WriteLine($\"Текст: {s}\"); }",
    "Создайте две перегрузки метода PrintInfo: одна принимает string text и выводит 'Строка: {text}', вторая принимает int number и выводит 'Число: {number}'. Вызовите обе в Main: сначала со строкой 'DevForge', затем с числом 2026.",
    "using System;\n\nclass Program {\n    // Перегрузки PrintInfo\n\n    static void Main() {\n        // Вызовы PrintInfo\n    }\n}",
    "using System;\n\nclass Program {\n    static void PrintInfo(string text) {\n        Console.WriteLine($\"Строка: {text}\");\n    }\n    static void PrintInfo(int number) {\n        Console.WriteLine($\"Число: {number}\");\n    }\n\n    static void Main() {\n        PrintInfo(\"DevForge\");\n        PrintInfo(2026);\n    }\n}",
    [{"id": "t1", "label": "Перегрузка методов", "expected": "Строка: DevForge\nЧисло: 2026"}],
    "Перегрузка методов (Overloading) позволяет использовать одно понятное имя для схожих операций над разными типами аргументов. Компилятор сам во время сборки определяет, какую версию вызвать, исходя из переданных типов и количества аргументов.",
    "Универсальный инструмент: одно название 'зарядить', но можно зарядить телефон шнуром Type-C, а можно зарядить часы магнитной таблеткой.",
    [{"term": "Перегрузка методов", "meaning": "Создание методов с одинаковым именем и разными сигнатурами"}, {"term": "Статическое связывание", "meaning": "Выбор нужного метода на этапе компиляции"}],
    "using System;\n\nclass Program {\n    static void Show(int x) { Console.WriteLine(x); }\n    static void Show(string s) { Console.WriteLine(s); }\n    static void Main() { Show(100); Show(\"OK\"); }\n}",
    "100\nOK\n"
)

# 13. List<T>
add(
    "cs-lists", "Динамические списки List<T>", "Коллекции", "Коллекции .NET", 13, "Средний", 15,
    "Работа с обобщенным списком List<T> из пространства имен System.Collections.Generic.",
    "List<int> numbers = new List<int>();\nnumbers.Add(10);\nConsole.WriteLine(numbers.Count);",
    "List<string> fruits = new List<string> { \"Яблоко\", \"Банан\" };\nfruits.Add(\"Груша\");",
    "Создайте List<string> cities = new List<string>();. Добавьте в список города 'Москва', 'Казань', 'Самара'. Выведите количество элементов через cities.Count и первый элемент cities[0] каждый на новой строке.",
    "using System;\nusing System.Collections.Generic;\n\nclass Program {\n    static void Main() {\n        // Создайте список List<string>, добавьте города и выведите Count и [0]\n    }\n}",
    "using System;\nusing System.Collections.Generic;\n\nclass Program {\n    static void Main() {\n        List<string> cities = new List<string>();\n        cities.Add(\"Москва\");\n        cities.Add(\"Казань\");\n        cities.Add(\"Самара\");\n        Console.WriteLine(cities.Count);\n        Console.WriteLine(cities[0]);\n    }\n}",
    [{"id": "t1", "label": "Размер и первый город", "expected": "3\nМосква"}],
    "В отличие от массивов с неизменным размером, List<T> — это динамический массив, размер которого автоматически увеличивается при добавлении новых элементов методом Add(). Он обеспечивает быстрый доступ по индексу и обладает множеством встроенных методов поиска и сортировки.",
    "Блокнот со съемными листами: вы можете в любой момент добавить новый чистый лист в конец, не меняя весь блокнот целиком.",
    [{"term": "List<T>", "meaning": "Обобщенный динамический массив в пространстве System.Collections.Generic"}, {"term": "Count", "meaning": "Свойство списка, возвращающее текущее число элементов"}],
    "using System;\nusing System.Collections.Generic;\n\nclass Program {\n    static void Main() {\n        List<int> lst = new List<int> { 1, 2, 3 };\n        Console.WriteLine(lst.Count);\n    }\n}",
    "3\n"
)

# 14. Classes & Fields
add(
    "cs-classes-fields", "Классы и объекты", "ООП", "Объектно-ориентированное программирование", 14, "Средний", 15,
    "Определение собственного класса с полями и создание экземпляров через new.",
    "class User {\n    public string Name;\n    public int Age;\n}",
    "User u = new User();\nu.Name = \"Иван\";\nu.Age = 30;",
    "Определите класс Car с открытыми полями public string Brand; и public int Year;. В методе Main создайте объект Car c = new Car();, установите Brand = 'Lada', Year = 2024 и выведите 'Lada: 2024'.",
    "using System;\n\nclass Car {\n    // Поля класса Car\n}\n\nclass Program {\n    static void Main() {\n        // Создайте объект и выведите данные\n    }\n}",
    "using System;\n\nclass Car {\n    public string Brand;\n    public int Year;\n}\n\nclass Program {\n    static void Main() {\n        Car c = new Car();\n        c.Brand = \"Lada\";\n        c.Year = 2024;\n        Console.WriteLine($\"{c.Brand}: {c.Year}\");\n    }\n}",
    [{"id": "t1", "label": "Поля объекта Car", "expected": "Lada: 2024"}],
    "Класс — это чертеж или шаблон, описывающий состояние (поля) и поведение будущих объектов. Экземпляр класса (объект) создается оператором new, выделяющим память под объект в управляемой куче (managed heap). Модификатор public делает поля доступными извне.",
    "Чертеж автомобиля: по одному чертежу можно выпустить тысячи реальных автомобилей на конвейере завода.",
    [{"term": "Класс", "meaning": "Пользовательский тип данных, шаблон для создания объектов"}, {"term": "Экземпляр (объект)", "meaning": "Конкретная реализация класса в оперативной памяти"}],
    "using System;\n\nclass Point { public int X; public int Y; }\nclass Program {\n    static void Main() {\n        Point p = new Point { X = 10, Y = 20 };\n        Console.WriteLine(p.X);\n    }\n}",
    "10\n"
)

# 15. Properties
add(
    "cs-properties", "Свойства с автоаксессорами", "ООП", "Объектно-ориентированное программирование", 15, "Средний", 15,
    "Инкапсуляция данных с помощью свойств { get; set; }.",
    "class Account {\n    public string Title { get; set; }\n    public decimal Balance { get; set; }\n}",
    "class Item {\n    public string Name { get; set; }\n}",
    "Создайте класс Book со свойствами public string Title { get; set; } и public int Pages { get; set; }. В Main создайте книгу 'Clean Code' на 464 страницы и выведите 'Книга: Clean Code, 464 стр.'.",
    "using System;\n\nclass Book {\n    // Свойства Title и Pages\n}\n\nclass Program {\n    static void Main() {\n        // Создайте объект и выведите результат\n    }\n}",
    "using System;\n\nclass Book {\n    public string Title { get; set; }\n    public int Pages { get; set; }\n}\n\nclass Program {\n    static void Main() {\n        Book b = new Book();\n        b.Title = \"Clean Code\";\n        b.Pages = 464;\n        Console.WriteLine($\"Книга: {b.Title}, {b.Pages} стр.\");\n    }\n}",
    [{"id": "t1", "label": "Свойства объекта Book", "expected": "Книга: Clean Code, 464 стр."}],
    "Свойства в C# объединяют синтаксическую простоту полей с мощью методов-геттеров и сеттеров. Автоматические свойства { get; set; } позволяют компилятору автоматически сгенерировать скрытое закрытое поле, гарантируя правильную инкапсуляцию данных.",
    "Умный термостат: вы просто считываете или задаете температуру на дисплее, а внутри прибор производит необходимые проверки и регулировки.",
    [{"term": "Свойство (Property)", "meaning": "Член класса, предоставляющий гибкий механизм для чтения и записи поля"}, {"term": "Инкапсуляция", "meaning": "Сокрытие внутреннего состояния объекта от прямого несанкционированного доступа"}],
    "using System;\n\nclass Box { public int Size { get; set; } }\nclass Program {\n    static void Main() {\n        Box b = new Box { Size = 50 };\n        Console.WriteLine(b.Size);\n    }\n}",
    "50\n"
)

# 16. Constructors
add(
    "cs-constructors", "Конструкторы класса", "ООП", "Объектно-ориентированное программирование", 16, "Средний", 15,
    "Инициализация полей и свойств объекта в момент его создания с помощью конструктора.",
    "public class Player {\n    public string Name;\n    public Player(string name) {\n        Name = name;\n    }\n}",
    "class User {\n    public string Email;\n    public User(string email) { Email = email; }\n}",
    "Создайте класс Person с открытым полем public string Name;. Добавьте конструктор public Person(string name), который инициализирует Name. В Main создайте объект Person p = new Person('Мария'); и выведите p.Name.",
    "using System;\n\nclass Person {\n    public string Name;\n    // Конструктор\n}\n\nclass Program {\n    static void Main() {\n        // Создайте Person и выведите Name\n    }\n}",
    "using System;\n\nclass Person {\n    public string Name;\n    public Person(string name) {\n        Name = name;\n    }\n}\n\nclass Program {\n    static void Main() {\n        Person p = new Person(\"Мария\");\n        Console.WriteLine(p.Name);\n    }\n}",
    [{"id": "t1", "label": "Конструктор Person", "expected": "Мария"}],
    "Конструктор — это специальный метод класса, который автоматически вызывается при создании каждого нового объекта через new. Имя конструктора всегда в точности совпадает с именем класса, и у него нет типа возвращаемого значения. Конструкторы обеспечивают корректную начальную настройку состояния объекта.",
    "Заводская сборка и заправка нового смартфона перед упаковкой в коробку: сразу записывается серийный номер и заряжается аккумулятор.",
    [{"term": "Конструктор", "meaning": "Специальный метод класса для первичной инициализации объекта при создании"}, {"term": "Ключевое слово new", "meaning": "Оператор выделения памяти и вызова конструктора"}],
    "using System;\n\nclass Cat {\n    public string Nick;\n    public Cat(string n) { Nick = n; }\n}\nclass Program {\n    static void Main() {\n        Cat c = new Cat(\"Барсик\");\n        Console.WriteLine(c.Nick);\n    }\n}",
    "Барсик\n"
)

# 17. Instance Methods
add(
    "cs-methods-oop", "Методы экземпляра класса", "ООП", "Объектно-ориентированное программирование", 17, "Продвинутый", 15,
    "Объявление методов внутри класса для работы с его состоянием.",
    "class Counter {\n    private int count = 0;\n    public void Increment() { count++; }\n    public int GetValue() { return count; }\n}",
    "class Greeter {\n    public void SayHi(string who) { Console.WriteLine($\"Привет, {who}!\"); }\n}",
    "Создайте класс Calculator с методом public int Add(int a, int b), возвращающим их сумму. В Main создайте экземпляр Calculator calc = new Calculator();, вычислите calc.Add(15, 25) и выведите результат.",
    "using System;\n\nclass Calculator {\n    // Метод Add\n}\n\nclass Program {\n    static void Main() {\n        // Экземпляр и вызов Add\n    }\n}",
    "using System;\n\nclass Calculator {\n    public int Add(int a, int b) {\n        return a + b;\n    }\n}\n\nclass Program {\n    static void Main() {\n        Calculator calc = new Calculator();\n        int sum = calc.Add(15, 25);\n        Console.WriteLine(sum);\n    }\n}",
    [{"id": "t1", "label": "Метод экземпляра", "expected": "40"}],
    "Методы экземпляра (в отличие от статических методов static) вызываются на конкретном объекте и имеют доступ к его полям и свойствам через скрытую ссылку this. Это основа объектно-ориентированного подхода: объединение данных и операций над ними в одной сущности.",
    "Действие конкретного робота: у робота есть руки и мотор, и его метод 'ПоднятьГруз()' использует именно его собственные механизмы.",
    [{"term": "Метод экземпляра", "meaning": "Метод класса, оперирующий данными конкретного объекта"}, {"term": "this", "meaning": "Указатель на текущий экземпляр класса внутри его методов"}],
    "using System;\n\nclass Greeter {\n    public string Hello() { return \"Привет!\"; }\n}\nclass Program {\n    static void Main() {\n        Greeter g = new Greeter();\n        Console.WriteLine(g.Hello());\n    }\n}",
    "Привет!\n"
)

# 18. Final Project
add(
    "cs-summary-project", "Итоговый проект: Картотека товаров", "Практика", "Комплексные проекты", 18, "Продвинутый", 20,
    "Комплексный проект на C#: класс товара, список List<Product>, фильтрация и подсчет суммы.",
    "List<Product> catalog = new List<Product>();",
    "class Item { public string Name; public int Cost; }",
    "Создайте класс Product с полями public string Name; и public int Price;. Создайте конструктор Product(string name, int price). В Main создайте List<Product> c двумя товарами: ('Ноутбук', 50000) и ('Мышь', 1500). Посчитайте их общую стоимость в цикле foreach и выведите 'Итого товаров: 2, сумма: 51500 руб.'.",
    "using System;\nusing System.Collections.Generic;\n\nclass Product {\n    // Поля Name, Price и конструктор\n}\n\nclass Program {\n    static void Main() {\n        // Создайте список, добавьте товары, посчитайте сумму и выведите\n    }\n}",
    "using System;\nusing System.Collections.Generic;\n\nclass Product {\n    public string Name;\n    public int Price;\n    public Product(string name, int price) {\n        Name = name;\n        Price = price;\n    }\n}\n\nclass Program {\n    static void Main() {\n        List<Product> items = new List<Product>();\n        items.Add(new Product(\"Ноутбук\", 50000));\n        items.Add(new Product(\"Мышь\", 1500));\n\n        int total = 0;\n        foreach (Product p in items) {\n            total += p.Price;\n        }\n        Console.WriteLine($\"Итого товаров: {items.Count}, сумма: {total} руб.\");\n    }\n}",
    [{"id": "t1", "label": "Итог каталога товаров", "expected": "Итого товаров: 2, сумма: 51500 руб."}],
    "В итоговом проекте объединяются все ключевые концепции C#: описание предметной области через классы с конструкторами, управление коллекцией с помощью обобщенного динамического списка List<T>, итерация foreach и интерполированный вывод.",
    "Словно кассовая система магазина: каждый товар добавляется в чек, после чего кассовая лента суммирует позиции и выдает готовый расчет покупателю.",
    [{"term": "Комплексная архитектура", "meaning": "Построение программы из взаимодействующих классов и коллекций"}, {"term": "Агрегация данных", "meaning": "Вычисление суммарных и статистических показателей по набору объектов"}],
    "using System;\nusing System.Collections.Generic;\n\nclass Item {\n    public int Val;\n    public Item(int v) { Val = v; }\n}\nclass Program {\n    static void Main() {\n        List<Item> l = new List<Item> { new Item(10), new Item(20) };\n        Console.WriteLine(l[0].Val + l[1].Val);\n    }\n}",
    "30\n"
)

if __name__ == "__main__":
    print(f"Loaded {len(LESSONS)} C# lessons.")
