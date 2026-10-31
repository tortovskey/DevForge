# -*- coding: utf-8 -*-
"""
Objective-C Course Curriculum (15 lessons, order 1..15)
From basics (NSLog, Foundation, scalar types) to message passing, classes (@interface / @implementation), properties, and NSArray.
"""

LESSONS = []

def add(id, title, topic, section, order, level, minutes, theory, syntax, example_code, task, starterCode, solCode, tests, guide_idea, life_ex, terms, ex_snippet, ex_expected):
    LESSONS.append({
        "id": id,
        "language": "objc",
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
            "Строковые литералы Objective-C начинаются со знака собаки: @\"текст\".",
            "Для вывода используйте функцию NSLog(@\"...\");.",
            "Не забывайте ставить точку с запятой в конце каждого выражения."
        ],
        "commonMistakes": "Забыли символ @ перед строковым литералом или квадратные скобки при вызове метода.",
        "solutionExplanation": "Код написан в соответствии со стандартами языка Objective-C и фреймворка Foundation.",
        "xp": 50,
        "setupSql": "",
        "concepts": [topic],
        "walkthrough": ["Изучите структуру функции main", "Напишите инструкции с NSLog", "Запустите проверку"],
        "prerequisites": [LESSONS[-1]["id"]] if LESSONS else [],
        "resources": [{"title": f"Справочник: {topic}", "url": f"https://devforge.local/docs/{id}", "language": "RU"}],
        "lifeExample": life_ex,
        "guide": {
            "version": 1,
            "idea": guide_idea,
            "steps": [
                "Изучите назначение Foundation и функции NSLog.",
                "Обратите внимание на синтаксис строковых литералов с символом @.",
                "Выполните задание в редакторе кода."
            ],
            "experiment": "Попробуйте изменить форматирование строки в NSLog и запустите код.",
            "terms": terms,
            "solution": solCode,
            "taskSteps": ["Откройте блок @autoreleasepool", "Вызовите NSLog с требуемой строкой", "Проверьте корректность синтаксиса"],
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
    "objc-first-nslog", "Первая программа на Objective-C", "Основы", "Введение", 1, "С нуля", 10,
    "Вывод сообщений в консоль с помощью функции NSLog и строковых литералов NSString.",
    "NSLog(@\"Привет, мир!\");",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@\"Hello Cocoa!\");\n    }\n    return 0;\n}",
    "Напишите программу на Objective-C, которая выводит строку 'Привет, Objective-C!' с помощью NSLog.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        // Напишите вывод через NSLog\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@\"Привет, Objective-C!\");\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Вывод в консоль", "expected": "Привет, Objective-C!"}],
    "Objective-C — классический объектно-ориентированный язык экосистемы Apple (macOS, iOS), объединяющий гибкую систему сообщений в стиле Smalltalk и быстродействие языка C. Функция NSLog является стандартным средством протоколирования в Foundation.",
    "Словно бортовой журнал самолета: каждая запись автоматически регистрируется бортовой системой с точной фиксацией сообщения.",
    [{"term": "NSLog", "meaning": "Функция Foundation для вывода сообщений в консоль"}, {"term": "@\"...\"", "meaning": "Префикс @ обозначает константный объект NSString, а не сырой си-массив символов"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@\"Старт Cocoa\");\n    }\n    return 0;\n}",
    "Старт Cocoa\n"
)

# 2. Variables & types
add(
    "objc-variables-types", "Переменные и типы данных", "Переменные", "Основы языка", 2, "С нуля", 12,
    "Базовые типы языка C (int, double, BOOL) и указатели на объекты Foundation (NSString *).",
    "int count = 10;\nBOOL active = YES;\nNSString *name = @\"Apple\";",
    "int x = 42;\nfloat pi = 3.14f;\nBOOL flag = YES;",
    "Объявите целочисленную переменную int version = 2026; и строку NSString *platform = @\"Apple\";. Выведите version, а затем platform с помощью NSLog.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        // Объявите переменные и выведите их\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int version = 2026;\n        NSString *platform = @\"Apple\";\n        NSLog(@\"%d\", version);\n        NSLog(@\"%@\", platform);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Вывод переменных", "expected": "2026\nApple"}],
    "Objective-C строго разделяет скалярные примитивные типы языка C (int, double, char, BOOL со значениями YES/NO) и ссылочные объекты Foundation, на которые всегда объявляются указатели со звездочкой, например NSString *.",
    "Как домашний адрес и сам дом: примитивное число лежит прямо на ладони, а указатель NSString* — это визитка с адресом большого объекта в памяти.",
    [{"term": "NSString *", "meaning": "Указатель на неизменяемую строку фреймворка Foundation"}, {"term": "BOOL", "meaning": "Булев тип данных в Objective-C с константами YES и NO"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int year = 1984;\n        NSLog(@\"%d\", year);\n    }\n    return 0;\n}",
    "1984\n"
)

# 3. String formatting
add(
    "objc-nsstring-format", "Форматирование строк и спецификаторы", "Строки", "Основы языка", 3, "Базовый", 12,
    "Спецификаторы формата %d (целые), %f (вещественные) и %@ (объекты Foundation).",
    "NSLog(@\"Товар: %@, цена: %d руб.\", title, price);",
    "int a = 5;\nint b = 10;\nNSLog(@\"%d + %d = %d\", a, b, a + b);",
    "Даны переменные int width = 10; и int height = 20;. Вычислите площадь int area = width * height; и выведите 'Площадь: 200' с помощью спецификатора %d.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int width = 10;\n        int height = 20;\n        // Посчитайте area и выведите\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int width = 10;\n        int height = 20;\n        int area = width * height;\n        NSLog(@\"Площадь: %d\", area);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Вывод площади", "expected": "Площадь: 200"}],
    "Функция NSLog использует спецификаторы формата наподобие стандартной printf: %d для целых чисел, %f для чисел с плавающей точкой, а для любых объектов Cocoa применяется специальный спецификатор %@, вызывающий метод description объекта.",
    "Шаблон письма с пропущенными полями: система берет бланк и в места %d или %@ аккуратно подставляет значения переданных аргументов.",
    [{"term": "%@", "meaning": "Спецификатор формата для отображения любого объекта Objective-C"}, {"term": "%d", "meaning": "Спецификатор для десятичных целых чисел"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int x = 7;\n        NSLog(@\"x = %d\", x);\n    }\n    return 0;\n}",
    "x = 7\n"
)

# 4. If / Else
add(
    "objc-if-else", "Условные операторы if / else", "Ветвление", "Управление потоком", 4, "Базовый", 12,
    "Логические проверки условий с операторами if, else if и else.",
    "if (batteryLevel < 20) {\n    NSLog(@\"Низкий заряд\");\n} else {\n    NSLog(@\"Заряд в норме\");\n}",
    "int score = 80;\nif (score >= 50) NSLog(@\"Сдал\");",
    "Дана переменная int score = 95;. Если score >= 90 выведите 'Отлично', иначе 'Хорошо'.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int score = 95;\n        // Напишите if / else\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int score = 95;\n        if (score >= 90) {\n            NSLog(@\"Отлично\");\n        } else {\n            NSLog(@\"Хорошо\");\n        }\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Оценка 95", "expected": "Отлично"}],
    "Условная конструкция if проверяет истинность выражения в круглых скобках. В Objective-C любое ненулевое число или ненулевой указатель трактуется как истина (YES), а ноль или nil трактуются как ложь (NO).",
    "Светофор на пешеходном переходе: зеленый свет (YES) разрешает движение, красный (NO) направляет ожидающих.",
    [{"term": "YES / NO", "meaning": "Булевы константы в Objective-C (1 и 0)"}, {"term": "nil", "meaning": "Нулевой указатель на объект"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        int v = 1;\n        if (v == 1) NSLog(@\"OK\");\n    }\n    return 0;\n}",
    "OK\n"
)

# 5. Loops
add(
    "objc-loops", "Циклы for и while", "Циклы", "Управление потоком", 5, "Базовый", 12,
    "Итерация с помощью классических циклов языка C: for и while.",
    "for (int i = 1; i <= 3; i++) {\n    NSLog(@\"%d\", i);\n}",
    "int n = 3;\nwhile (n > 0) { NSLog(@\"%d\", n); n--; }",
    "Используя цикл for, выведите числа от 1 до 3 включительно, каждое на новой строке через NSLog(@\"%d\", i);.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        // Цикл for от 1 до 3\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        for (int i = 1; i <= 3; i++) {\n            NSLog(@\"%d\", i);\n        }\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Числа 1, 2, 3", "expected": "1\n2\n3"}],
    "Циклы for и while в Objective-C полностью соответствуют стандарту ANSI C. Цикл for содержит три секции: инициализация переменной счетчика, проверка условия продолжения перед шагом и инкремент в конце каждого витка.",
    "Секундомер обратного отсчета или метроном: каждый такт строго повторяет действие заданное число раз.",
    [{"term": "Цикл for", "meaning": "Управляющая конструкция повторения блока инструкций по счетчику"}, {"term": "Итерация", "meaning": "Один отдельный проход тела цикла"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        for (int k = 0; k < 2; k++) NSLog(@\"шаг\");\n    }\n    return 0;\n}",
    "шаг\nшаг\n"
)

# 6. Functions
add(
    "objc-functions", "Си-функции в Objective-C", "Функции", "Модульность", 6, "Базовый", 12,
    "Объявление и использование традиционных функций языка C внутри проекта Objective-C.",
    "int multiply(int a, int b) {\n    return a * b;\n}",
    "void printDivider() {\n    NSLog(@\"===\");\n}",
    "Напишите функцию int square(int n), возвращающую квадрат числа (n * n). В main вызовите square(6) и выведите результат через NSLog(@\"%d\", result);.",
    "#import <Foundation/Foundation.h>\n\n// Объявите int square(int n)\n\nint main() {\n    @autoreleasepool {\n        // Вызовите и выведите результат\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint square(int n) {\n    return n * n;\n}\n\nint main() {\n    @autoreleasepool {\n        int res = square(6);\n        NSLog(@\"%d\", res);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Квадрат числа 6", "expected": "36"}],
    "Поскольку Objective-C является строгим надмножеством языка C, вы можете свободно объявлять обычные глобальные функции C для быстрых вычислений и алгоритмов. Они вызываются напрямую по имени без посылки сообщений объектам.",
    "Математическая формула в блокноте: подали аргумент x, быстро вычислили f(x) без необходимости создавать целый механизм.",
    [{"term": "Си-функция", "meaning": "Процедура или подпрограмма без привязки к конкретному объекту"}, {"term": "return", "meaning": "Возврат значения из функции в точку вызова"}],
    "#import <Foundation/Foundation.h>\nint add2(int x) { return x + 2; }\nint main() {\n    @autoreleasepool { NSLog(@\"%d\", add2(5)); }\n    return 0;\n}",
    "7\n"
)

# 7. Interface & Implementation
add(
    "objc-interface-implementation", "Классы: @interface и @implementation", "ООП", "Объектно-ориентированное программирование", 7, "Средний", 15,
    "Разделение объявления класса (@interface) и его реализации (@implementation).",
    "@interface Device : NSObject\n@end\n\n@implementation Device\n@end",
    "@interface Box : NSObject\n@end\n@implementation Box\n@end",
    "Объявите класс Device : NSObject с помощью @interface Device : NSObject @end и @implementation Device @end. В main создайте экземпляр Device *d = [Device new]; и выведите 'Device готов'.",
    "#import <Foundation/Foundation.h>\n\n// Объявите @interface Device : NSObject и @implementation Device\n\nint main() {\n    @autoreleasepool {\n        // Создайте объект Device и выведите 'Device готов'\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface Device : NSObject\n@end\n\n@implementation Device\n@end\n\nint main() {\n    @autoreleasepool {\n        Device *d = [Device new];\n        NSLog(@\"Device готов\");\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Создание Device", "expected": "Device готов"}],
    "В Objective-C объявление интерфейса класса и его реализация четко разнесены по директивам @interface и @implementation. Большинство классов наследуются от корневого класса NSObject, предоставляющего базовую функциональность работы с памятью и рефлексией.",
    "Архитектурный чертеж (interface) и фактическое здание из бетона и стекла (implementation): фасад описывает внешний вид, а стены воплощают его в жизнь.",
    [{"term": "@interface", "meaning": "Директива объявления открытого интерфейса и свойств класса"}, {"term": "@implementation", "meaning": "Директива блока фактической реализации методов класса"}],
    "#import <Foundation/Foundation.h>\n@interface Test : NSObject @end\n@implementation Test @end\nint main() { @autoreleasepool { NSLog(@\"OK\"); } return 0; }",
    "OK\n"
)

# 8. Instance Methods
add(
    "objc-instance-methods", "Методы экземпляра и отправка сообщений", "ООП", "Объектно-ориентированное программирование", 8, "Средний", 15,
    "Объявление методов экземпляра со знаком минус (-) и синтаксис квадратных скобок [receiver message].",
    "- (void)sayHello {\n    NSLog(@\"Привет!\");\n}",
    "- (void)ping {\n    NSLog(@\"pong\");\n}",
    "Добавьте в класс Greeter метод экземпляра - (void)greet, который выводит 'Здравствуйте, Cocoa!'. В main создайте Greeter *g = [Greeter new]; и вызовите [g greet];.",
    "#import <Foundation/Foundation.h>\n\n@interface Greeter : NSObject\n- (void)greet;\n@end\n\n@implementation Greeter\n// Реализуйте метод greet\n@end\n\nint main() {\n    @autoreleasepool {\n        // Создайте экземпляр и вызовите greet\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface Greeter : NSObject\n- (void)greet;\n@end\n\n@implementation Greeter\n- (void)greet {\n    NSLog(@\"Здравствуйте, Cocoa!\");\n}\n@end\n\nint main() {\n    @autoreleasepool {\n        Greeter *g = [Greeter new];\n        [g greet];\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Метод greet", "expected": "Здравствуйте, Cocoa!"}],
    "В Objective-C вызов метода формулируется как отправка сообщения: [получатель сообщение]. Знак минус '-' перед сигнатурой означает метод конкретного экземпляра (объекта). Если получатель равен nil, вызов сообщения безопасно игнорируется без падения программы.",
    "Отправка телеграммы абоненту: вы запечатываете конверт [получатель телеграмма] и отправляете его по адресу.",
    [{"term": "Синтаксис [obj msg]", "meaning": "Отправка сообщения msg объекту obj в runtime Objective-C"}, {"term": "Знак минус (-)", "meaning": "Обозначение метода экземпляра класса"}],
    "#import <Foundation/Foundation.h>\n@interface Echo : NSObject - (void)go; @end\n@implementation Echo - (void)go { NSLog(@\"echo\"); } @end\nint main() { @autoreleasepool { Echo *e = [Echo new]; [e go]; } return 0; }",
    "echo\n"
)

# 9. Methods with Arguments
add(
    "objc-methods-args", "Методы с параметрами", "ООП", "Объектно-ориентированное программирование", 9, "Средний", 15,
    "Именованные метки аргументов в селекторах методов Objective-C.",
    "- (int)add:(int)a to:(int)b {\n    return a + b;\n}",
    "- (void)printName:(NSString *)name times:(int)count;",
    "Создайте класс Calculator с методом - (int)doubleValue:(int)val;, возвращающим val * 2. В main создайте объект calc, вызовите [calc doubleValue:21] и выведите результат через NSLog.",
    "#import <Foundation/Foundation.h>\n\n@interface Calculator : NSObject\n- (int)doubleValue:(int)val;\n@end\n\n@implementation Calculator\n// Реализуйте doubleValue\n@end\n\nint main() {\n    @autoreleasepool {\n        // Вызовите метод и выведите результат\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface Calculator : NSObject\n- (int)doubleValue:(int)val;\n@end\n\n@implementation Calculator\n- (int)doubleValue:(int)val {\n    return val * 2;\n}\n@end\n\nint main() {\n    @autoreleasepool {\n        Calculator *calc = [Calculator new];\n        int res = [calc doubleValue:21];\n        NSLog(@\"%d\", res);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Вызов doubleValue:21", "expected": "42"}],
    "Особенность Objective-C — высокая читаемость методов благодаря именованным меткам параметров: вместо безликих скобок сигнатура читается как естественное предложение на английском языке. Двоеточие является неотъемлемой частью селектора метода.",
    "Как диалог: 'Пожалуйста, Calculator, удвойЗначение: 21' — предельно понятно и не оставляет сомнений в назначении аргумента.",
    [{"term": "Селектор (Selector)", "meaning": "Уникальное внутреннее имя метода в рантайме, включающее имена меток и двоеточия"}, {"term": "Именованные метки", "meaning": "Слова перед двоеточиями, поясняющие смысл каждого параметра"}],
    "#import <Foundation/Foundation.h>\n@interface Math : NSObject - (int)neg:(int)x; @end\n@implementation Math - (int)neg:(int)x { return -x; } @end\nint main() { @autoreleasepool { Math *m = [Math new]; NSLog(@\"%d\", [m neg:5]); } return 0; }",
    "-5\n"
)

# 10. Class Methods
add(
    "objc-class-methods", "Методы класса (+)", "ООП", "Объектно-ориентированное программирование", 10, "Средний", 15,
    "Методы, вызываемые напрямую на самом классе (статические / фабричные методы) со знаком плюс (+).",
    "+ (NSString *)appVersion {\n    return @\"1.0\";\n}",
    "+ (void)printAppName {\n    NSLog(@\"DevForge\");\n}",
    "Создайте класс AppInfo с методом класса + (NSString *)appName;, который возвращает @'DevForge Studio'. В main вызовите [AppInfo appName] и выведите результат через NSLog(@\"%@\", ...);.",
    "#import <Foundation/Foundation.h>\n\n@interface AppInfo : NSObject\n+ (NSString *)appName;\n@end\n\n@implementation AppInfo\n// Реализуйте метод класса appName\n@end\n\nint main() {\n    @autoreleasepool {\n        // Вызовите [AppInfo appName] и выведите\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface AppInfo : NSObject\n+ (NSString *)appName;\n@end\n\n@implementation AppInfo\n+ (NSString *)appName {\n    return @\"DevForge Studio\";\n}\n@end\n\nint main() {\n    @autoreleasepool {\n        NSString *name = [AppInfo appName];\n        NSLog(@\"%@\", name);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Метод класса appName", "expected": "DevForge Studio"}],
    "Методы со знаком плюс (+) принадлежат объекту-классу, а не отдельному экземпляру. Они часто используются в качестве фабричных методов для быстрого создания настроенных объектов (например, [NSString stringWithFormat:...]) или для глобальных утилит.",
    "Табличка на проходной фабрики: чтобы узнать название завода, вам не нужно покупать один из выпущенных им телевизоров.",
    [{"term": "Знак плюс (+)", "meaning": "Обозначение метода класса в синтаксисе Objective-C"}, {"term": "Фабричный метод", "meaning": "Метод класса, инкапсулирующий создание и настройку объектов"}],
    "#import <Foundation/Foundation.h>\n@interface Ping : NSObject + (void)go; @end\n@implementation Ping + (void)go { NSLog(@\"pong\"); } @end\nint main() { @autoreleasepool { [Ping go]; } return 0; }",
    "pong\n"
)

# 11. Properties
add(
    "objc-properties", "Свойства класса @property", "ООП", "Объектно-ориентированное программирование", 11, "Средний", 15,
    "Инкапсуляция данных объекта с помощью директивы @property и доступ через точечный синтаксис.",
    "@property (nonatomic, strong) NSString *name;",
    "@property (nonatomic) int count;",
    "Создайте класс User с целочисленным свойством @property (nonatomic) int age;. В main создайте объект u, установите u.age = 25; и выведите возраст через NSLog(@\"Возраст: %d\", u.age);.",
    "#import <Foundation/Foundation.h>\n\n@interface User : NSObject\n@property (nonatomic) int age;\n@end\n\n@implementation User\n@end\n\nint main() {\n    @autoreleasepool {\n        User *u = [User new];\n        // Задайте age и выведите\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface User : NSObject\n@property (nonatomic) int age;\n@end\n\n@implementation User\n@end\n\nint main() {\n    @autoreleasepool {\n        User *u = [User new];\n        u.age = 25;\n        NSLog(@\"Возраст: %d\", u.age);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Свойство age", "expected": "Возраст: 25"}],
    "Директива @property автоматически генерирует методы-геттеры и сеттеры для полей объекта, а также обеспечивает правильное управление памятью (strong, weak, assign). К свойствам можно обращаться как через сообщения, так и через привычный точечный синтаксис object.property.",
    "Дверная ручка с замком: поворачивая ручку снаружи, вы приводите в движение скрытые внутри механизмы ригеля.",
    [{"term": "@property", "meaning": "Директива автоматического создания геттера, сеттера и поля хранения"}, {"term": "Точечный синтаксис", "meaning": "Удобная запись u.age вместо вызова методов [u age] и [u setAge:25]"}],
    "#import <Foundation/Foundation.h>\n@interface Car : NSObject @property int speed; @end\n@implementation Car @end\nint main() { @autoreleasepool { Car *c = [Car new]; c.speed = 100; NSLog(@\"%d\", c.speed); } return 0; }",
    "100\n"
)

# 12. Custom Initializer
add(
    "objc-init-custom", "Инициализаторы объекта", "ООП", "Объектно-ориентированное программирование", 12, "Средний", 15,
    "Двухфазная инициализация объектов alloc и init, создание собственных инициализаторов.",
    "- (instancetype)initWithName:(NSString *)name {\n    self = [super init];\n    if (self) {\n        _name = name;\n    }\n    return self;\n}",
    "- (id)initWithTitle:(NSString *)title;",
    "Создайте класс Book со свойством @property (nonatomic) int pages;. Добавьте метод - (id)initWithPages:(int)p, который сохраняет p в свойство pages и возвращает self. В main создайте книгу через [[Book alloc] initWithPages:350] и выведите 'Страниц: 350'.",
    "#import <Foundation/Foundation.h>\n\n@interface Book : NSObject\n@property (nonatomic) int pages;\n- (id)initWithPages:(int)p;\n@end\n\n@implementation Book\n// Реализуйте initWithPages\n@end\n\nint main() {\n    @autoreleasepool {\n        // Создайте объект и выведите\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface Book : NSObject\n@property (nonatomic) int pages;\n- (id)initWithPages:(int)p;\n@end\n\n@implementation Book\n- (id)initWithPages:(int)p {\n    self.pages = p;\n    return self;\n}\n@end\n\nint main() {\n    @autoreleasepool {\n        Book *b = [[Book alloc] initWithPages:350];\n        NSLog(@\"Страниц: %d\", b.pages);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Инициализатор страниц", "expected": "Страниц: 350"}],
    "В Objective-C создание объекта строго разделено на две фазы: выделение памяти методом [+alloc] и первичная настройка полей методом [-init]. Кастомные инициализаторы традиционно начинаются с префикса initWith... и возвращают настроенный указатель self.",
    "Покупка земельного участка (alloc — выделение территории) и последующее строительство дома на нем (init — отделка и заселение).",
    [{"term": "alloc", "meaning": "Метод класса NSObject, выделяющий блок памяти под новый объект"}, {"term": "init", "meaning": "Метод экземпляра для начальной инициализации полей объекта"}],
    "#import <Foundation/Foundation.h>\n@interface Box : NSObject @property int size; - (id)initWithSize:(int)s; @end\n@implementation Box - (id)initWithSize:(int)s { self.size = s; return self; } @end\nint main() { @autoreleasepool { Box *b = [[Box alloc] initWithSize:5]; NSLog(@\"%d\", b.size); } return 0; }",
    "5\n"
)

# 13. NSArray
add(
    "objc-nsarray", "Коллекция NSArray", "Коллекции", "Фреймворк Foundation", 13, "Базовый", 15,
    "Хранение упорядоченного списка объектов с помощью литерала @[...] и метода count.",
    "NSArray *items = @[@\"iPhone\", @\"iPad\", @\"Mac\"];\nNSLog(@\"Количество: %lu\", (unsigned long)[items count]);",
    "NSArray *nums = @[@1, @2, @3];",
    "Создайте массив NSArray *devices = @[@\"iPhone\", @\"iPad\", @\"Mac\"];. Выведите количество элементов с помощью [devices count] и первый элемент devices[0].",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        // Создайте NSArray и выведите count и [0]\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSArray *devices = @[@\"iPhone\", @\"iPad\", @\"Mac\"];\n        NSLog(@\"%lu\", (unsigned long)[devices count]);\n        NSLog(@\"%@\", devices[0]);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Размер и первый элемент", "expected": "3\niPhone"}],
    "Класс NSArray представляет собой неизменяемый упорядоченный список объектов в Cocoa. Литеральный синтаксис @[...] создает массив прямо на месте. Доступ к элементам осуществляется через квадратные скобки arr[0] или метод [arr objectAtIndex:0].",
    "Фирменная коробка с набором аксессуаров: все предметы аккуратно разложены по ячейкам в строгом неизменном порядке.",
    [{"term": "NSArray", "meaning": "Базовый неизменяемый массив объектов в Foundation"}, {"term": "@[...]", "meaning": "Удобный литерал создания массива объектов в Objective-C"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSArray *a = @[@\"A\", @\"B\"];\n        NSLog(@\"%lu\", (unsigned long)[a count]);\n    }\n    return 0;\n}",
    "2\n"
)

# 14. Fast Enumeration
add(
    "objc-fast-enumeration", "Быстрое перечисление for...in", "Коллекции", "Фреймворк Foundation", 14, "Базовый", 12,
    "Перебор элементов массива NSArray с помощью цикла быстрого перечисления for (... in ...).",
    "for (NSString *item in list) {\n    NSLog(@\"%@\", item);\n}",
    "for (id element in collection) { ... }",
    "Дан массив NSArray *names = @[@\"iOS\", @\"macOS\", @\"watchOS\"];. Используя цикл for (NSString *name in names), выведите каждую систему в консоль.",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSArray *names = @[@\"iOS\", @\"macOS\", @\"watchOS\"];\n        // Переберите массив через for...in\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSArray *names = @[@\"iOS\", @\"macOS\", @\"watchOS\"];\n        for (NSString *name in names) {\n            NSLog(@\"%@\", name);\n        }\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Перебор ОС", "expected": "iOS\nmacOS\nwatchOS"}],
    "Синтаксис быстрого перечисления (Fast Enumeration) for (Type *item in collection) обеспечивает лаконичный и высокопроизводительный обход любых коллекций Foundation благодаря протоколу NSFastEnumeration.",
    "Конвейерная разгрузка чемоданов: каждый предмет автоматически извлекается из контейнера и отдается на обработку.",
    [{"term": "Fast Enumeration", "meaning": "Механизм быстрого обхода элементов коллекции с помощью for...in"}, {"term": "NSFastEnumeration", "meaning": "Внутренний протокол быстрого постраничного перебора объектов"}],
    "#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSArray *arr = @[@\"Раз\", @\"Два\"];\n        for (NSString *s in arr) NSLog(@\"%@\", s);\n    }\n    return 0;\n}",
    "Раз\nДва\n"
)

# 15. Final Project
add(
    "objc-summary-project", "Итоговый проект: Картотека задач", "Практика", "Комплексные проекты", 15, "Продвинутый", 20,
    "Создание законченного приложения на Objective-C: класс задачи TodoItem, инициализатор, массив NSArray и вывод списка.",
    "NSArray *tasks = @[t1, t2];",
    "@interface Item : NSObject @property NSString *title; @end",
    "Создайте класс Task со свойством @property (nonatomic) int priority;. Добавьте метод - (id)initWithPriority:(int)p { self.priority = p; return self; }. В main создайте две задачи с приоритетами 1 и 2, сложите их сумму приоритетов и выведите 'Сумма приоритетов: 3'.",
    "#import <Foundation/Foundation.h>\n\n@interface Task : NSObject\n@property (nonatomic) int priority;\n- (id)initWithPriority:(int)p;\n@end\n\n@implementation Task\n// Реализуйте initWithPriority\n@end\n\nint main() {\n    @autoreleasepool {\n        // Создайте объекты, вычислите сумму и выведите\n    }\n    return 0;\n}",
    "#import <Foundation/Foundation.h>\n\n@interface Task : NSObject\n@property (nonatomic) int priority;\n- (id)initWithPriority:(int)p;\n@end\n\n@implementation Task\n- (id)initWithPriority:(int)p {\n    self.priority = p;\n    return self;\n}\n@end\n\nint main() {\n    @autoreleasepool {\n        Task *t1 = [[Task alloc] initWithPriority:1];\n        Task *t2 = [[Task alloc] initWithPriority:2];\n        int total = t1.priority + t2.priority;\n        NSLog(@\"Сумма приоритетов: %d\", total);\n    }\n    return 0;\n}",
    [{"id": "t1", "label": "Сумма приоритетов", "expected": "Сумма приоритетов: 3"}],
    "В итоговом проекте соединяются все ключевые кирпичики Objective-C: объектно-ориентированная модель с интерфейсом и реализацией, автоматические свойства @property, настраиваемые инициалисты, отправка сообщений и форматированный вывод.",
    "Словно сборка фирменного приложения для App Store: классы описывают логику предметной области, а рантайм связывает их в надежную систему.",
    [{"term": "Архитектура Cocoa", "meaning": "Объектная экосистема Apple, построенная на концепциях Smalltalk и фреймворке Foundation"}, {"term": "Интеграция компонентов", "meaning": "Объединение моделей, методов и коллекций в цельную прикладную программу"}],
    "#import <Foundation/Foundation.h>\n@interface N : NSObject @property int v; @end\n@implementation N @end\nint main() { @autoreleasepool { N *a = [N new]; a.v = 10; NSLog(@\"%d\", a.v); } return 0; }",
    "10\n"
)

if __name__ == "__main__":
    print(f"Loaded {len(LESSONS)} Objective-C lessons.")
