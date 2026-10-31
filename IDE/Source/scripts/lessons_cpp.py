# -*- coding: utf-8 -*-
"""
C++ Course Curriculum (18 lessons, order 1..18)
From basics (cout, variables, loops) to functions, references, classes, templates and STL vector.
"""

LESSONS = []

def add(id, title, topic, section, order, level, minutes, theory, syntax, example_code, task, starterCode, solCode, tests, guide_idea, life_ex, terms, ex_snippet, ex_expected):
    LESSONS.append({
        "id": id,
        "language": "cpp",
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
            "Внимательно проверьте точку с запятой в конце каждой инструкции.",
            "Убедитесь, что вывод в точности совпадает с условием задания.",
            "Используйте оператор << для отправки данных в std::cout."
        ],
        "commonMistakes": "Забыли директиву #include <iostream> или точку с запятой.",
        "solutionExplanation": "Код выполняет поставленную задачу в соответствии со стандартами C++.",
        "xp": 50,
        "setupSql": "",
        "concepts": [topic],
        "walkthrough": ["Прочитайте условие", "Напишите решение", "Запустите проверку"],
        "prerequisites": [LESSONS[-1]["id"]] if LESSONS else [],
        "resources": [{"title": f"Справочник: {topic}", "url": f"https://devforge.local/docs/{id}", "language": "RU"}],
        "lifeExample": life_ex,
        "guide": {
            "version": 1,
            "idea": guide_idea,
            "steps": [
                "Изучите синтаксис команды и ее назначение.",
                "Запустите мини-пример и разберите полученный результат.",
                "Выполните самостоятельное задание в редакторе."
            ],
            "experiment": "Попробуйте изменить значение выводимой переменной и проверьте, как изменился вывод.",
            "terms": terms,
            "solution": solCode,
            "taskSteps": ["Объявите нужные переменные", "Выполните вычисления", "Выведите ответ через std::cout"],
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
    "cpp-first-cout", "Первая программа на C++", "Основы", "Введение", 1, "С нуля", 10,
    "Вывод текста в консоль через std::cout и поток вывода.",
    "std::cout << \"Привет, C++!\" << std::endl;",
    "std::cout << \"Hello World!\" << std::endl;",
    "Напишите программу, которая выводит строку 'Привет, C++!' на экран с переводом строки.",
    "#include <iostream>\n\nint main() {\n    // Ваш код здесь\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    std::cout << \"Привет, C++!\" << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Вывод приветствия", "expected": "Привет, C++!"}],
    "C++ — мощный язык программирования, на котором пишут операционные системы, игровые движки и высоконагруженные серверы. Поток std::cout направляет данные прямо в терминал пользователя, а оператор << указывает направление передачи информации.",
    "Представьте громкоговоритель на вокзале: вы передаёте ему текст объявления, и он звучит для всех пассажиров.",
    [{"term": "std::cout", "meaning": "Стандартный поток вывода в C++"}, {"term": "main()", "meaning": "Главная точка входа любой программы"}],
    "#include <iostream>\n\nint main() {\n    std::cout << \"Старт C++\" << std::endl;\n    return 0;\n}",
    "Старт C++\n"
)

# 2. Variables & types
add(
    "cpp-variables", "Переменные и базовые типы", "Переменные", "Основы", 2, "С нуля", 12,
    "Типы данных int, double, char, bool и объявление переменных.",
    "int age = 20; double pi = 3.14;",
    "int x = 10; double y = 2.5; std::cout << x * y << std::endl;",
    "Создайте целочисленную переменную apples со значением 15 и выведите её значение.",
    "#include <iostream>\n\nint main() {\n    // Создайте переменную apples и выведите ее\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int apples = 15;\n    std::cout << apples << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Значение apples", "expected": "15"}],
    "Переменная в C++ — это строго типизированная ячейка оперативной памяти компьютера. Тип int хранит целые числа, double — числа с плавающей точкой, а компилятор гарантирует защиту от сохранения неподходящих типов данных.",
    "Представьте ящик для инструментов с ячейками под гайки определённого размера: ячейка M10 примет только гайку M10.",
    [{"term": "int", "meaning": "Целочисленный тип данных"}, {"term": "double", "meaning": "Вещественное число двойной точности"}],
    "#include <iostream>\n\nint main() {\n    int speed = 90;\n    std::cout << speed << std::endl;\n    return 0;\n}",
    "90\n"
)

# 3. Arithmetic
add(
    "cpp-arithmetic", "Арифметические операции", "Арифметика", "Основы", 3, "С нуля", 12,
    "Сложение, вычитание, умножение, деление и остаток от деления.",
    "int sum = a + b; int rem = a % b;",
    "int a = 14; int b = 4; std::cout << a / b << \" \" << a % b << std::endl;",
    "Вычислите и выведите сумму чисел 38 и 44.",
    "#include <iostream>\n\nint main() {\n    // Сложите 38 и 44\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int a = 38;\n    int b = 44;\n    std::cout << a + b << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Сумма 38 + 44", "expected": "82"}],
    "Арифметика в C++ выполняется процессором напрямую. Деление двух целых чисел всегда дает целую часть с отбрасыванием остатка, а оператор процента (%) позволяет найти сам остаток.",
    "Представьте деление коробки конфет между детьми: целая часть — сколько достанется каждому поровну, остаток — то, что останется в коробке.",
    [{"term": "Оператор %", "meaning": "Вычисление остатка от целочисленного деления"}, {"term": "Инкремент ++", "meaning": "Увеличение числа на единицу"}],
    "#include <iostream>\n\nint main() {\n    int x = 20;\n    int y = 6;\n    std::cout << x + y << std::endl;\n    return 0;\n}",
    "26\n"
)

# 4. Strings (std::string)
add(
    "cpp-strings", "Строки std::string", "Строки", "Основы", 4, "С нуля", 15,
    "Класс std::string для работы с текстом произвольной длины.",
    "std::string s = \"Hello\"; s += \" World\";",
    "std::string name = \"Ада\"; std::cout << name.length() << std::endl;",
    "Создайте строку std::string lang = \"C++\"; выведите 'Я изучаю ' и значение переменной lang.",
    "#include <iostream>\n#include <string>\n\nint main() {\n    // Создайте строку lang и выведите 'Я изучаю C++'\n    return 0;\n}",
    "#include <iostream>\n#include <string>\n\nint main() {\n    std::string lang = \"C++\";\n    std::cout << \"Я изучаю \" << lang << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Вывод строки", "expected": "Я изучаю C++"}],
    "В отличие от языка Си с его сырыми символьными массивами, C++ предоставляет удобный и безопасный класс std::string, который автоматически управляет выделением и освобождением памяти при изменении длины строки.",
    "Представьте резиновую ленту с надписью: она растягивается по мере добавления букв без риска порваться.",
    [{"term": "std::string", "meaning": "Стандартный класс C++ для безопасной работы со строками"}, {"term": ".length()", "meaning": "Метод получения количества символов в строке"}],
    "#include <iostream>\n#include <string>\n\nint main() {\n    std::string title = \"DevForge\";\n    std::cout << title << std::endl;\n    return 0;\n}",
    "DevForge\n"
)

# 5. if-else
add(
    "cpp-if-else", "Ветвление if-else", "Условия", "Управление", 5, "Базовый", 15,
    "Условный оператор if, else if и else для принятия решений.",
    "if (score >= 60) { std::cout << \"Pass\"; } else { std::cout << \"Fail\"; }",
    "int x = 10; if (x > 0) std::cout << \"Positive\" << std::endl;",
    "Объявите переменную int temp = 22; Если temp > 20, выведите 'Тепло', иначе 'Холодно'.",
    "#include <iostream>\n\nint main() {\n    int temp = 22;\n    // Проверьте условие\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int temp = 22;\n    if (temp > 20) {\n        std::cout << \"Тепло\" << std::endl;\n    } else {\n        std::cout << \"Холодно\" << std::endl;\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Проверка температуры", "expected": "Тепло"}],
    "Конструкция if-else анализирует логическое выражение в скобках. Если условие истинно (true), выполняется первый блок кода в фигурных скобках, а если ложно — альтернативный блок else.",
    "Светофор на перекрёстке: если горит зелёный — автомобиль едет, иначе — останавливается.",
    [{"term": "if", "meaning": "Ключевое слово для проверки истинности условия"}, {"term": "else", "meaning": "Ветка кода, выполняемая при ложном условии"}],
    "#include <iostream>\n\nint main() {\n    int n = 7;\n    if (n % 2 == 0) std::cout << \"Even\" << std::endl; else std::cout << \"Odd\" << std::endl;\n    return 0;\n}",
    "Odd\n"
)

# 6. while loop
add(
    "cpp-while", "Цикл while", "Циклы", "Управление", 6, "Базовый", 15,
    "Повторение действий, пока логическое условие остаётся истинным.",
    "while (count > 0) { count--; }",
    "int i = 1; while (i <= 3) { std::cout << i << \" \"; i++; }",
    "С помощью цикла while выведите числа от 1 до 4 через пробел (в конце пробел или перевод строки).",
    "#include <iostream>\n\nint main() {\n    // Выведите 1 2 3 4 через while\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int i = 1;\n    while (i <= 4) {\n        std::cout << i << \" \";\n        i++;\n    }\n    std::cout << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Числа 1 2 3 4", "expected": "1 2 3 4"}],
    "Цикл while проверяет условие перед каждой итерацией. Внутри тела цикла обязательно должно происходить изменение переменной состояния, иначе программа рискует попасть в бесконечный цикл.",
    "Наполнение ведра водой: пока ведро не полное, вы продолжаете подливать воду кружкой.",
    [{"term": "while", "meaning": "Цикл с предусловием"}, {"term": "Итерация", "meaning": "Один полный шаг выполнения тела цикла"}],
    "#include <iostream>\n\nint main() {\n    int c = 3;\n    while (c > 0) { std::cout << c << \" \"; c--; }\n    std::cout << std::endl;\n    return 0;\n}",
    "3 2 1 \n"
)

# 7. for loop
add(
    "cpp-for", "Классический цикл for", "Циклы", "Управление", 7, "Базовый", 15,
    "Цикл со счётчиком: инициализация, условие и шаг в одной строке.",
    "for (int i = 0; i < 5; i++) { ... }",
    "int sum = 0; for (int i = 1; i <= 5; i++) sum += i;",
    "Вычислите сумму чисел от 1 до 5 с помощью цикла for и выведите результат.",
    "#include <iostream>\n\nint main() {\n    // Посчитайте сумму чисел от 1 до 5\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int sum = 0;\n    for (int i = 1; i <= 5; i++) {\n        sum += i;\n    }\n    std::cout << sum << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Сумма 1..5", "expected": "15"}],
    "Цикл for объединяет объявление счётчика, условие завершения и шаг изменения в компактном заголовке. Это самый читаемый и надёжный способ обхода диапазонов чисел.",
    "Счёт кругов на стадионе: спортсмен начинает с круга 1, бежит пока круг <= 5, прибавляя по одному кругу после каждой черты.",
    [{"term": "for", "meaning": "Цикл со счётчиком шагов"}, {"term": "Счётчик", "meaning": "Переменная, отслеживающая текущий номер итерации"}],
    "#include <iostream>\n\nint main() {\n    int prod = 1;\n    for (int i = 1; i <= 4; i++) prod *= i;\n    std::cout << prod << std::endl;\n    return 0;\n}",
    "24\n"
)

# 8. Functions
add(
    "cpp-functions", "Функции в C++", "Функции", "Модульность", 8, "Базовый", 15,
    "Объявление функций, передача параметров и возврат значений.",
    "int multiply(int a, int b) { return a * b; }",
    "int square(int n) { return n * n; }",
    "Напишите функцию int multiply(int a, int b), возвращающую их произведение. В main вызовите multiply(6, 7) и выведите ответ.",
    "#include <iostream>\n\n// Объявите multiply\n\nint main() {\n    // Вызовите multiply(6, 7)\n    return 0;\n}",
    "#include <iostream>\n\nint multiply(int a, int b) {\n    return a * b;\n}\n\nint main() {\n    std::cout << multiply(6, 7) << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Вызов multiply(6, 7)", "expected": "42"}],
    "Функция представляет собой обособленный фрагмент программы, который принимает входные аргументы и возвращает вычисленный ответ через ключевое слово return, избавляя от дублирования кода.",
    "Кухонный миксер: вы загружаете ингредиенты, нажимаете кнопку, и получаете взбитый крем без необходимости повторять движения венчиком вручную.",
    [{"term": "Сигнатура", "meaning": "Имя функции вместе с типами её параметров и возвращаемого значения"}, {"term": "return", "meaning": "Инструкция возврата значения из функции"}],
    "#include <iostream>\n\nint add(int a, int b) { return a + b; }\n\nint main() {\n    std::cout << add(10, 20) << std::endl;\n    return 0;\n}",
    "30\n"
)

# 9. References (Ссылки)
add(
    "cpp-references", "Ссылки и передача по ссылке", "Память", "Продвинутый", 9, "Средний", 18,
    "Ссылки (Type&) как псевдонимы существующих переменных.",
    "void increment(int& x) { x++; }",
    "int a = 5; int& ref = a; ref = 10; // a теперь 10",
    "Напишите функцию void doubleVal(int& n), которая удваивает переданную по ссылке переменную. В main вызовите её для x = 12 и выведите x.",
    "#include <iostream>\n\n// Объявите doubleVal\n\nint main() {\n    int x = 12;\n    // удвойте x и выведите\n    return 0;\n}",
    "#include <iostream>\n\nvoid doubleVal(int& n) {\n    n *= 2;\n}\n\nint main() {\n    int x = 12;\n    doubleVal(x);\n    std::cout << x << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Удвоение через ссылку", "expected": "24"}],
    "Ссылка в C++ создаёт альтернативное имя для уже существующего объекта в памяти. Изменение значения через ссылку напрямую меняет исходную переменную без затрат на копирование данных.",
    "Второй ключ от той же самой квартиры: открывая замок вторым ключом, вы входите в то же самое помещение.",
    [{"term": "Ссылка (&)", "meaning": "Псевдоним (alias) для существующей ячейки памяти"}, {"term": "Передача по значению", "meaning": "Создание отдельной независимой копии объекта"}],
    "#include <iostream>\n\nvoid addTen(int& val) { val += 10; }\n\nint main() {\n    int num = 5;\n    addTen(num);\n    std::cout << num << std::endl;\n    return 0;\n}",
    "15\n"
)

# 10. std::vector
add(
    "cpp-vector", "Динамический массив std::vector", "Контейнеры", "STL", 10, "Средний", 18,
    "Контейнер std::vector, методы push_back, size и доступ по индексу [].",
    "std::vector<int> v; v.push_back(10); v.push_back(20);",
    "std::vector<int> nums = {1, 2, 3}; std::cout << nums.size() << std::endl;",
    "Создайте вектор std::vector<int> nums; добавьте числа 10, 20, 30 и выведите сумму первого и последнего элементов.",
    "#include <iostream>\n#include <vector>\n\nint main() {\n    // Вектор с 10, 20, 30 и вывод суммы первого и последнего\n    return 0;\n}",
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> nums;\n    nums.push_back(10);\n    nums.push_back(20);\n    nums.push_back(30);\n    std::cout << nums[0] + nums[2] << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Сумма первого и последнего", "expected": "40"}],
    "Вектор std::vector — краеугольный камень стандартной библиотеки шаблонов C++ (STL). Он автоматически выделяет дополнительную память при добавлении элементов через метод push_back().",
    "Блокнот с отрывными листами, в который можно доклеивать новые чистые страницы по мере заполнения записями.",
    [{"term": "std::vector", "meaning": "Динамический последовательный контейнер"}, {"term": "push_back()", "meaning": "Метод добавления элемента в конец вектора"}],
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> v = {5, 10};\n    std::cout << v.size() << std::endl;\n    return 0;\n}",
    "2\n"
)

# 11. Range-based for loop
add(
    "cpp-range-for", "Диапазонный цикл for-each", "Циклы", "C++11", 11, "Средний", 15,
    "Элегантный обход элементов контейнера через for (auto x : container).",
    "for (int x : vec) { std::cout << x << \" \"; }",
    "std::vector<int> v = {2, 4, 6}; for (auto x : v) std::cout << x << \" \";",
    "Создайте вектор std::vector<int> nums = {3, 5, 7}; Вычислите сумму всех элементов с помощью range-for и выведите её.",
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> nums = {3, 5, 7};\n    // Посчитайте сумму через for (auto x : nums)\n    return 0;\n}",
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> nums = {3, 5, 7};\n    int sum = 0;\n    for (auto x : nums) {\n        sum += x;\n    }\n    std::cout << sum << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Сумма вектора", "expected": "15"}],
    "Синтаксис range-based for из стандарта C++11 позволяет перебирать коллекции без возни с индексами и итераторами, делая код устойчивым к ошибкам выхода за границы диапазона.",
    "Конвейерная лента с деталями: контролёр берёт каждую деталь по очереди, не считая их порядковые номера вслух.",
    [{"term": "auto", "meaning": "Автоматическое определение типа переменной"}, {"term": "Range-for", "meaning": "Цикл по элементам диапазона"}],
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> items = {1, 2, 3};\n    for (auto n : items) std::cout << n * 2 << \" \";\n    std::cout << std::endl;\n    return 0;\n}",
    "2 4 6 \n"
)

# 12. Classes and objects
add(
    "cpp-classes", "Классы и объекты", "ООП", "Архитектура", 12, "Средний", 20,
    "Объявление класса, секции public и private, методы класса.",
    "class Rectangle { public: int width, height; int area() { return width * height; } };",
    "class Point { public: int x, y; }; Point p; p.x = 10;",
    "Создайте класс Rectangle с полями int width, height и методом int area(). В main создайте объект с размерами 4 и 5 и выведите площадь.",
    "#include <iostream>\n\n// Объявите класс Rectangle\n\nint main() {\n    // Создайте прямоугольник 4x5 и выведите площадь\n    return 0;\n}",
    "#include <iostream>\n\nclass Rectangle {\npublic:\n    int width;\n    int height;\n    int area() {\n        return width * height;\n    }\n};\n\nint main() {\n    Rectangle r;\n    r.width = 4;\n    r.height = 5;\n    std::cout << r.area() << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Площадь 4x5", "expected": "20"}],
    "Класс объединяет переменные состояния (поля) и функции (методы) в целостный тип данных. Секция public открывает доступ к членам класса для внешней программы.",
    "Чертёж дома: класс — это сам архитектурный чертёж, а объект — реально построенный по этому чертежу дом на улице.",
    [{"term": "Класс", "meaning": "Пользовательский тип данных, объединяющий поля и методы"}, {"term": "Объект", "meaning": "Конкретный экземпляр класса в памяти программы"}],
    "#include <iostream>\n\nclass Box {\npublic:\n    int size = 5;\n};\n\nint main() {\n    Box b;\n    std::cout << b.size << std::endl;\n    return 0;\n}",
    "5\n"
)

# 13. Constructors
add(
    "cpp-constructors", "Конструкторы классов", "ООП", "Архитектура", 13, "Средний", 20,
    "Инициализация объектов через конструкторы с параметрами.",
    "class Person { public: std::string name; Person(std::string n) : name(n) {} };",
    "class Item { public: int id; Item(int i) { id = i; } }; Item it(42);",
    "Создайте класс User с полем std::string name и конструктором User(std::string n). В main создайте объект User u(\"Иван\"); и выведите u.name.",
    "#include <iostream>\n#include <string>\n\n// Объявите класс User с конструктором\n\nint main() {\n    // Создайте пользователя и выведите имя\n    return 0;\n}",
    "#include <iostream>\n#include <string>\n\nclass User {\npublic:\n    std::string name;\n    User(std::string n) {\n        name = n;\n    }\n};\n\nint main() {\n    User u(\"Иван\");\n    std::cout << u.name << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Имя пользователя", "expected": "Иван"}],
    "Конструктор — специальная функция-член класса, которая автоматически вызывается при рождении нового объекта. Он гарантирует, что объект сразу начнёт жизнь в корректном инициализированном состоянии.",
    "Заводская сборка автомобиля: перед тем как выехать с конвейера, в автомобиль обязательно заливают масло и бензин.",
    [{"term": "Конструктор", "meaning": "Метод инициализации, имя которого совпадает с именем класса"}, {"term": "Инициализация", "meaning": "Присвоение стартовых корректных значений полям"}],
    "#include <iostream>\n\nclass Counter {\npublic:\n    int val;\n    Counter(int start) { val = start; }\n};\n\nint main() {\n    Counter c(100);\n    std::cout << c.val << std::endl;\n    return 0;\n}",
    "100\n"
)

# 14. Encapsulation
add(
    "cpp-encapsulation", "Инкапсуляция и геттеры/сеттеры", "ООП", "Архитектура", 14, "Продвинутый", 20,
    "Скрытие внутреннего состояния в private и доступ через публичные методы.",
    "class Bank { private: int balance; public: int getBalance() { return balance; } };",
    "class Wallet { private: int money = 0; public: void add(int m) { money += m; } int get() { return money; } };",
    "Создайте класс Score с приватным полем int points и публичными методами addPoints(int p) и getPoints(). Добавьте 50 очков и выведите их.",
    "#include <iostream>\n\n// Объявите класс Score с приватным points\n\nint main() {\n    // Создайте Score, добавьте 50 и выведите результат\n    return 0;\n}",
    "#include <iostream>\n\nclass Score {\nprivate:\n    int points = 0;\npublic:\n    void addPoints(int p) {\n        if (p > 0) points += p;\n    }\n    int getPoints() {\n        return points;\n    }\n};\n\nint main() {\n    Score s;\n    s.addPoints(50);\n    std::cout << s.getPoints() << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Баллы Score", "expected": "50"}],
    "Инкапсуляция защищает критически важные поля от некорректного прямого вмешательства. Метод-сеттер может проверить данные на корректность перед тем, как изменить приватную переменную.",
    "Банкомат: клиенты не имеют прямого доступа к хранилищу наличных купюр, а взаимодействуют с деньгами только через безопасный интерфейс кнопок и экрана.",
    [{"term": "private", "meaning": "Секция, доступная только методам внутри самого класса"}, {"term": "Геттер", "meaning": "Метод для безопасного чтения значения приватного поля"}],
    "#include <iostream>\n\nclass Temp {\nprivate: int t = 20;\npublic: int get() { return t; }\n};\n\nint main() {\n    Temp temp;\n    std::cout << temp.get() << std::endl;\n    return 0;\n}",
    "20\n"
)

# 15. Templates
add(
    "cpp-templates", "Шаблоны функций (Templates)", "Обобщения", "Метапрограммирование", 15, "Продвинутый", 22,
    "Обобщённое программирование с помощью template <typename T>.",
    "template <typename T> T getMax(T a, T b) { return a > b ? a : b; }",
    "template <typename T> void printVal(T val) { std::cout << val << std::endl; }",
    "Напишите шаблон функции template <typename T> T getMin(T a, T b), возвращающий меньшее из двух чисел. В main вызовите getMin(15, 8) и выведите ответ.",
    "#include <iostream>\n\n// Объявите шаблон getMin\n\nint main() {\n    // Вызовите getMin(15, 8)\n    return 0;\n}",
    "#include <iostream>\n\ntemplate <typename T>\nT getMin(T a, T b) {\n    return a < b ? a : b;\n}\n\nint main() {\n    std::cout << getMin(15, 8) << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Результат getMin(15, 8)", "expected": "8"}],
    "Шаблоны C++ позволяют написать единственный алгоритм, который компилятор автоматически адаптирует для целых чисел, вещественных дробей или пользовательских типов данных.",
    "Универсальная форма для выпечки: в неё можно залить шоколадное тесто, а можно фруктовое — форма кекса останется одинаковой.",
    [{"term": "template", "meaning": "Ключевое слово для создания обобщённого шаблона кода"}, {"term": "Инстанцирование", "meaning": "Генерация компилятором конкретной функции под указанный тип"}],
    "#include <iostream>\n\ntemplate <typename T>\nT id(T x) { return x; }\n\nint main() {\n    std::cout << id(42) << std::endl;\n    return 0;\n}",
    "42\n"
)

# 16. Operator overloading
add(
    "cpp-operators", "Перегрузка операторов", "ООП", "Синтаксис", 16, "Продвинутый", 22,
    "Переопределение оператора + для пользовательских классов.",
    "Point operator+(const Point& other) { return Point{x + other.x, y + other.y}; }",
    "struct Vec2 { int x, y; Vec2 operator+(Vec2 o) { return {x+o.x, y+o.y}; } };",
    "Создайте структуру Point { int x, y; }; реализуйте оператор + для сложения двух точек. Сложите p1{2, 3} и p2{4, 5} и выведите p3.x и p3.y через пробел.",
    "#include <iostream>\n\n// Объявите структуру Point с оператором +\n\nint main() {\n    // Сложите точки и выведите x и y\n    return 0;\n}",
    "#include <iostream>\n\nstruct Point {\n    int x, y;\n    Point operator+(const Point& other) const {\n        return Point{x + other.x, y + other.y};\n    }\n};\n\nint main() {\n    Point p1{2, 3};\n    Point p2{4, 5};\n    Point p3 = p1 + p2;\n    std::cout << p3.x << \" \" << p3.y << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Сложение точек", "expected": "6 8"}],
    "Перегрузка операторов позволяет пользовательским типам вести себя так же естественно, как встроенным числам, позволяя писать интуитивные математические выражения p1 + p2.",
    "Знак плюс в разных контекстах: сложение денег даёт сумму рублей, а сложение векторов смещает точку в пространстве.",
    [{"term": "operator+", "meaning": "Специальная функция перегрузки операции сложения"}, {"term": "const", "meaning": "Обещание не изменять исходный объект при вычислениях"}],
    "#include <iostream>\n\nstruct Number {\n    int val;\n    Number operator+(Number o) { return {val + o.val}; }\n};\n\nint main() {\n    Number a{10}, b{20};\n    std::cout << (a + b).val << std::endl;\n    return 0;\n}",
    "30\n"
)

# 17. Input via std::cin
add(
    "cpp-cin", "Пользовательский ввод std::cin", "Ввод-вывод", "Потоки", 17, "Базовый", 15,
    "Считывание данных из входного потока с помощью оператора >>.",
    "int age; std::cin >> age;",
    "int x; std::cin >> x; std::cout << x * 2 << std::endl;",
    "Считайте целое число из входного потока и выведите число, увеличенное на 1.",
    "#include <iostream>\n\nint main() {\n    // Считайте число через cin и выведите + 1\n    return 0;\n}",
    "#include <iostream>\n\nint main() {\n    int n;\n    std::cin >> n;\n    std::cout << n + 1 << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Ввод 41 -> вывод 42", "expected": "42", "stdin": "41"}],
    "Поток std::cin считывает символы из стандартного потока ввода программы, автоматически парсит их в целевой тип переменной и пропускает пробелы и символы перевода строк.",
    "Приёмная труба почтового ящика: опущенное внутрь письмо направляется прямо в руки адресата.",
    [{"term": "std::cin", "meaning": "Стандартный входной поток данных C++"}, {"term": "Оператор >>", "meaning": "Оператор извлечения данных из входного потока"}],
    "#include <iostream>\n\nint main() {\n    int val = 25;\n    std::cout << val + 5 << std::endl;\n    return 0;\n}",
    "30\n"
)

# 18. Capstone Project
add(
    "cpp-project", "Итоговый проект: Складской учёт", "Проект", "Практика", 18, "Junior+", 30,
    "Объединение классов, вектора, методов и вывода для симуляции склада товаров.",
    "class Inventory { std::vector<Item> items; };",
    "class Store { public: int count = 0; void add() { count++; } };",
    "Создайте класс Item с полями std::string name и int count. Создайте класс Warehouse с вектором items, методом addItem(name, count) и методом getTotalItems(). Добавьте товары 'Книги' (15 шт) и 'Тетради' (25 шт) и выведите общее число единиц.",
    "#include <iostream>\n#include <string>\n#include <vector>\n\n// Создайте классы Item и Warehouse\n\nint main() {\n    // Добавьте товары и выведите общий остаток\n    return 0;\n}",
    "#include <iostream>\n#include <string>\n#include <vector>\n\nstruct Item {\n    std::string name;\n    int count;\n};\n\nclass Warehouse {\nprivate:\n    std::vector<Item> items;\npublic:\n    void addItem(std::string name, int count) {\n        items.push_back(Item{name, count});\n    }\n    int getTotalItems() {\n        int total = 0;\n        for (const auto& item : items) {\n            total += item.count;\n        }\n        return total;\n    }\n};\n\nint main() {\n    Warehouse wh;\n    wh.addItem(\"Книги\", 15);\n    wh.addItem(\"Тетради\", 25);\n    std::cout << wh.getTotalItems() << std::endl;\n    return 0;\n}",
    [{"id": "t1", "label": "Итоговый остаток склада", "expected": "40"}],
    "Финальный проект на C++ объединяет структуры данных, динамические векторы STL, методы инкапсуляции и циклы обхода коллекций в законченную архитектуру реального микроприложения.",
    "Автоматизированный логистический центр: посылки регистрируются на входе, заносятся в базу данных и суммируются для генерации отчёта руководству.",
    [{"term": "Архитектура", "meaning": "Принцип взаимосвязи структур данных и методов приложения"}, {"term": "STL", "meaning": "Standard Template Library — стандартная библиотека шаблонов C++"}],
    "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> qty = {10, 20};\n    int s = 0; for (int q : qty) s += q;\n    std::cout << s << std::endl;\n    return 0;\n}",
    "30\n"
)
