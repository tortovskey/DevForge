"""Java curriculum for DevForge (18 lessons from scratch to Junior+ practice)."""

def get_java_lessons():
    lessons = []

    def add(key, order, title, section, level, minutes, xp, theory, syntax, example_code, expected_example, idea, steps, experiment, terms, task, starter, solution, tests, analogy, challenge, task_steps, checklist, common_mistakes, stdin=""):
        lesson_id = f"java-{key}"
        lessons.append({
            "id": lesson_id,
            "language": "java",
            "title": title,
            "topic": title,
            "section": section,
            "order": order,
            "level": level,
            "minutes": minutes,
            "theory": theory,
            "syntax": syntax,
            "examples": [syntax],
            "task": task,
            "starterCode": starter,
            "setupSql": "",
            "concepts": [key],
            "walkthrough": task_steps,
            "hints": [task_steps[0], task_steps[1], "Проверьте закрывающие скобки, точку с запятой ; и запуск через Run."],
            "commonMistakes": common_mistakes,
            "solutionExplanation": f"Решение на Java: {syntax.splitlines()[0] if syntax else ''}. Код компилируется и выполняется в виртуальной машине.",
            "xp": xp,
            "tests": tests,
            "prerequisites": [lessons[-1]["id"]] if lessons else [],
            "resources": [],
            "lifeExample": analogy,
            "challenge": challenge,
            "stdin": stdin,
            "guide": {
                "version": 1,
                "idea": idea,
                "steps": steps,
                "experiment": experiment,
                "example": {
                    "code": example_code,
                    "expected": expected_example,
                    "setupSql": "",
                    "kind": "stdout",
                    "tables": []
                },
                "terms": terms,
                "solution": solution,
                "taskTables": [],
                "taskSteps": task_steps,
                "checklist": checklist
            }
        })

    # 1. First main & System.out.println
    add(
        key="first-main",
        order=1,
        title="Первая программа: класс Main и вызов main",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="В Java любая программа состоит из классов. Точка входа в программу — специальный статический метод:\npublic static void main(String[] args)\n\nДля вывода сообщения на экран используют команду System.out.println(\"текст\");. Каждая команда в Java обязательно завершается точкой с запятой (;).",
        syntax="public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Привет, мир!\");\n    }\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Я изучаю Java!\");\n    }\n}",
        expected_example="Я изучаю Java!\n",
        idea="Java требует строгой структуры: метод main внутри класса Main — это главная дверь, в которую входит исполнитель при запуске программы.",
        steps=[
            "public class Main объявляет основной класс программы.",
            "public static void main(String[] args) — точка входа, откуда начинается выполнение.",
            "System.out.println(...) печатает строку в консоль и переводит курсор на новую строку."
        ],
        experiment="Замените текст внутри кавычек на своё имя и запустите программу кнопкой «Запустить пример».",
        terms=[
            {"term": "public class", "meaning": "Объявление общедоступного класса в Java."},
            {"term": "System.out.println", "meaning": "Стандартный метод вывода строки с последующим переносом строки."}
        ],
        task="Выведите в консоль строку: Привет, DevForge!",
        starter="public class Main {\n    public static void main(String[] args) {\n        // Напишите команду вывода\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Привет, DevForge!\");\n    }\n}",
        tests=[{"id": "t1", "label": "Приветствие", "expected": "Привет, DevForge!"}],
        analogy="Представьте письмо в конверте: конверт — это класс Main, адрес на конверте — метод main, а вложенное послание — строка, которую выводит System.out.println.",
        challenge="Выведите две строки подряд с помощью двух вызовов System.out.println.",
        task_steps=["Внутри метода main напишите System.out.println", "В кавычках укажите \"Привет, DevForge!\"", "Поставьте точку с запятой ; в конце строки"],
        checklist=["Метод main сохранён", "Строка выведена", "Точка с запятой на месте"],
        common_mistakes="Слова System и String пишутся строго с большой буквы, а out и println — с маленькой."
    )

    # 2. Variables & Primitive types
    add(
        key="variables",
        order=2,
        title="Примитивные типы: int, double, boolean, char",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Java — строго типизированный язык. При объявлении переменной сначала указывается её тип, затем имя и значение:\nint count = 10; // целое число\ndouble price = 19.99; // дробное число\nboolean isOpen = true; // логический тип\nchar letter = 'A'; // одиночный символ в одинарных кавычках",
        syntax="int x = 5;\ndouble d = 3.14;\nboolean ok = true;\nchar c = 'J';",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int age = 21;\n        double height = 1.82;\n        System.out.println(age);\n        System.out.println(height);\n    }\n}",
        expected_example="21\n1.82\n",
        idea="Тип данных определяет размер выделяемой памяти и операции, которые разрешено выполнять над переменной.",
        steps=[
            "int age = 21 создаёт целочисленную ячейку памяти с числом 21.",
            "double height = 1.82 создаёт ячейку для чисел с плавающей точкой.",
            "Вывод печатает значения переменных по очереди."
        ],
        experiment="Попробуйте положить дробное число в int: int a = 3.5; и проверьте ошибку компиляции.",
        terms=[
            {"term": "int", "meaning": "Целочисленный тип данных (32 бита)."},
            {"term": "double", "meaning": "Тип данных с плавающей точкой повышенной точности (64 бита)."}
        ],
        task="Объявите переменную int score = 100; и выведите её значение на экран.",
        starter="public class Main {\n    public static void main(String[] args) {\n        // Объявите score и выведите\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int score = 100;\n        System.out.println(score);\n    }\n}",
        tests=[{"id": "t1", "label": "Вывод числа score", "expected": "100"}],
        analogy="Представьте подписанные ячейки на складе: в отсек для обуви нельзя положить телевизор. Так и в ячейку int нельзя записать текст.",
        challenge="Объявите переменную boolean isReady = true; и выведите её.",
        task_steps=["Объявите int score = 100;", "Выведите System.out.println(score);"],
        checklist=["Тип int указан", "Значение 100 выведено"],
        common_mistakes="Не забывайте точку с запятой после объявления переменной."
    )

    # 3. Arithmetic operations
    add(
        key="arithmetic",
        order=3,
        title="Арифметика и целочисленное деление",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="В Java деление двух целых чисел (int / int) всегда даёт целое число: 7 / 2 даст 3, а не 3.5! Дробная часть просто отбрасывается.\nЧтобы получить остаток от деления, используют оператор %: 7 % 2 = 1.\nЧтобы получить дробный результат, хотя бы одно из чисел должно быть double: 7.0 / 2 = 3.5.",
        syntax="int div = 10 / 3; // 3\nint rem = 10 % 3; // 1\ndouble d = 10.0 / 3; // 3.333...",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int a = 14;\n        int b = 4;\n        System.out.println(a / b);\n        System.out.println(a % b);\n    }\n}",
        expected_example="3\n2\n",
        idea="Целочисленное деление полезно, когда нужно узнать количество полных пачек, а остаток % — сколько предметов осталось сверх пачек.",
        steps=[
            "14 / 4 = 3 (целых раза четверка укладывается в 14).",
            "14 % 4 = 2 (остаток после вычитания 3 * 4 = 12).",
            "Результаты выведены построчно."
        ],
        experiment="Замените 14 на 14.0. Как изменится результат деления?",
        terms=[{"term": "целочисленное деление", "meaning": "Деление двух целых чисел с отбрасыванием дробной части."}],
        task="Даны две переменные int total = 25 и int group = 4. Вычислите и выведите остаток от деления total на group (total % group).",
        starter="public class Main {\n    public static void main(String[] args) {\n        int total = 25;\n        int group = 4;\n        // Выведите остаток total % group\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int total = 25;\n        int group = 4;\n        System.out.println(total % group);\n    }\n}",
        tests=[{"id": "t1", "label": "Остаток от деления", "expected": "1"}],
        analogy="Представьте 25 конфет, которые делят поровну между 4 детьми: каждому достанется по 6 конфет (25 / 4 = 6), и 1 конфета останется в коробке (25 % 4 = 1).",
        challenge="Посчитайте частное total / group.",
        task_steps=["Вычислите total % group", "Выведите результат через System.out.println"],
        checklist=["Оператор остатка % использован", "Выведен результат 1"],
        common_mistakes="Не путайте % (остаток) с процентами от числа."
    )

    # 4. Strings
    add(
        key="strings",
        order=4,
        title="Класс String и методы строк",
        section="Строки",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Строки в Java представлены ссылочным типом String (с большой буквы) и заключаются в двойные кавычки.\nОператор + склеивает строки (конкатенация).\nПолезные методы:\n.length() — длина строки;\n.toUpperCase() — перевод в верхний регистр;\n.toLowerCase() — в нижний регистр.",
        syntax="String s = \"Java\";\nint len = s.length();\nString big = s.toUpperCase();",
        example_code="public class Main {\n    public static void main(String[] args) {\n        String name = \"Иван\";\n        System.out.println(\"Привет, \" + name + \"!\");\n        System.out.println(name.length());\n    }\n}",
        expected_example="Привет, Иван!\n4\n",
        idea="Строки в Java неизменяемы (immutable). Метод toUpperCase() возвращает новую строку, не меняя исходную.",
        steps=[
            "\"Привет, \" + name + \"!\" склеивает три части в одну строку.",
            "name.length() возвращает количество символов (4).",
            "Вывод показывает результат конкатенации и число символов."
        ],
        experiment="Выведите name.toUpperCase() — как изменится написание имени?",
        terms=[{"term": "String", "meaning": "Класс для работы с текстовыми строками в Java."}],
        task="Объявите String course = \"Java\"; и выведите строку: Курс: JAVA (используйте course.toUpperCase()).",
        starter="public class Main {\n    public static void main(String[] args) {\n        String course = \"Java\";\n        // Выведите \"Курс: \" + course в верхнем регистре\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        String course = \"Java\";\n        System.out.println(\"Курс: \" + course.toUpperCase());\n    }\n}",
        tests=[{"id": "t1", "label": "Верхний регистр строки", "expected": "Курс: JAVA"}],
        analogy="Представьте печатный станок: вы задаёте текст на ленте, станок делает оттиск заглавными буквами и выдаёт готовый плакат.",
        challenge="Выведите длину строки course.length().",
        task_steps=["Вызовите course.toUpperCase()", "Склейте со строкой \"Курс: \"", "Выведите через System.out.println"],
        checklist=["Использован метод toUpperCase()", "Вывод точно равен 'Курс: JAVA'"],
        common_mistakes="Не забывайте круглые скобки у метода .length() для строк в Java."
    )

    # 5. Math class
    add(
        key="math",
        order=5,
        title="Класс Math: максимум, минимум и корень",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Класс Math содержит встроенные математические методы:\nMath.max(a, b) — наибольшее из двух чисел;\nMath.min(a, b) — наименьшее;\nMath.abs(x) — модуль (абсолютное значение) числа;\nMath.sqrt(x) — квадратный корень (возвращает double).",
        syntax="int m = Math.max(10, 25);\ndouble root = Math.sqrt(16.0); // 4.0",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int x = -15;\n        System.out.println(Math.abs(x));\n        System.out.println(Math.max(10, 20));\n    }\n}",
        expected_example="15\n20\n",
        idea="Все методы Math статические — их вызывают напрямую через Math.имяМетода, без создания объекта через new.",
        steps=[
            "Math.abs(-15) отбрасывает знак минус и возвращает 15.",
            "Math.max(10, 20) сравнивает 10 и 20 и выбирает 20.",
            "Результаты выведены на экран."
        ],
        experiment="Вызовите Math.min(10, 20) и посмотрите, какое число выберет метод.",
        terms=[{"term": "Math", "meaning": "Стандартный утилитный класс Java для математических вычислений."}],
        task="Найдите и выведите максимальное из двух чисел 45 и 90 с помощью Math.max.",
        starter="public class Main {\n    public static void main(String[] args) {\n        int a = 45;\n        int b = 90;\n        // Выведите максимум через Math.max\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int a = 45;\n        int b = 90;\n        System.out.println(Math.max(a, b));\n    }\n}",
        tests=[{"id": "t1", "label": "Максимальное число", "expected": "90"}],
        analogy="Представьте электронные весы с функцией фиксации пикового веса: весы мгновенно показывают наибольшее из двух значений.",
        challenge="Найдите квадратный корень из 100 с помощью Math.sqrt(100).",
        task_steps=["Вызовите Math.max(a, b)", "Выведите результат через System.out.println"],
        checklist=["Использован Math.max", "Выведено число 90"],
        common_mistakes="Слово Math пишется с заглавной буквы."
    )

    # 6. If / Else
    add(
        key="if-else",
        order=6,
        title="Условия: if, else if, else",
        section="Ветвления",
        level="Beginner",
        minutes=20,
        xp=45,
        theory="Конструкция if выполняет блок, если логическое выражение в скобках равно true.\nОператоры сравнения: == (равно), != (не равно), >, <, >=, <=.\nЛогические связки: && (И), || (ИЛИ), ! (НЕ).",
        syntax="if (score >= 60) {\n    System.out.println(\"Сдал\");\n} else {\n    System.out.println(\"Пересдача\");\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int age = 19;\n        if (age >= 18) {\n            System.out.println(\"Совершеннолетний\");\n        } else {\n            System.out.println(\"Несовершеннолетний\");\n        }\n    }\n}",
        expected_example="Совершеннолетний\n",
        idea="Компьютер выполняет только одну подходящую ветку условия, все остальные ветки пропускаются.",
        steps=[
            "age >= 18 проверяет: 19 больше либо равно 18 (true).",
            "Выполняется тело первого блока { ... }.",
            "Ветка else пропускается."
        ],
        experiment="Измените age на 16. Какое сообщение появится в выводе?",
        terms=[{"term": "if / else", "meaning": "Условный оператор для ветвления логики программы."}],
        task="Для переменной int temp = 22 напишите условие: если temp > 20, выведите 'Тепло', иначе 'Холодно'.",
        starter="public class Main {\n    public static void main(String[] args) {\n        int temp = 22;\n        // Напишите проверку if/else\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int temp = 22;\n        if (temp > 20) {\n            System.out.println(\"Тепло\");\n        } else {\n            System.out.println(\"Холодно\");\n        }\n    }\n}",
        tests=[{"id": "t1", "label": "Тепло", "expected": "Тепло"}],
        analogy="Представьте термостат обогревателя: если температура в комнате выше заданной — он отключается, иначе включается на прогрев.",
        challenge="Добавьте ветку else if (temp == 20) с выводом 'Комфортно'.",
        task_steps=["Проверьте if (temp > 20)", "В блоке if выведите 'Тепло'", "В блоке else выведите 'Холодно'"],
        checklist=["Есть ветки if и else", "Выведено 'Тепло'"],
        common_mistakes="Условие обязательно заключается в круглые скобки: if (temp > 20)."
    )

    # 7. Switch
    add(
        key="switch",
        order=7,
        title="Конструкция switch / case",
        section="Ветвления",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Когда нужно проверить одну переменную на равенство нескольким значениям, используют switch.\nПосле каждого case обязательно ставят break, чтобы выполнение не перешло на следующий пункт. default срабатывает, если ни один case не подошёл.",
        syntax="switch (day) {\n    case 1:\n        System.out.println(\"Пн\");\n        break;\n    default:\n        System.out.println(\"Другой\");\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int code = 2;\n        switch (code) {\n            case 1:\n                System.out.println(\"Старт\");\n                break;\n            case 2:\n                System.out.println(\"Пауза\");\n                break;\n            default:\n                System.out.println(\"Стоп\");\n        }\n    }\n}",
        expected_example="Пауза\n",
        idea="switch быстрее и нагляднее длинной цепочки if-else if при сравнении дискретных чисел или строк.",
        steps=[
            "code равен 2.",
            "case 1 не подошёл, управление переходит к case 2.",
            "Печатается 'Пауза', break выходит из switch."
        ],
        experiment="Уберите слово break из case 2. Посмотрите, как выполнится и default тоже.",
        terms=[{"term": "switch", "meaning": "Оператор многовариантного выбора значения."}],
        task="Для int rating = 5 напишите switch: при 5 выведите 'Отлично', при 4 — 'Хорошо', иначе 'Удовлетворительно'.",
        starter="public class Main {\n    public static void main(String[] args) {\n        int rating = 5;\n        // Напишите switch для rating\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int rating = 5;\n        switch (rating) {\n            case 5:\n                System.out.println(\"Отлично\");\n                break;\n            case 4:\n                System.out.println(\"Хорошо\");\n                break;\n            default:\n                System.out.println(\"Удовлетворительно\");\n        }\n    }\n}",
        tests=[{"id": "t1", "label": "Оценка 5", "expected": "Отлично"}],
        analogy="Представьте лифт: вы нажимаете кнопку нужного этажа (case 5), лифт едет прямо туда и открывает двери (break).",
        challenge="Добавьте case 3 со своим сообщением.",
        task_steps=["Напишите switch (rating)", "Добавьте case 5 с выводом 'Отлично' и break", "Добавьте default"],
        checklist=["Использован switch / case", "Выведено 'Отлично'"],
        common_mistakes="Не забывайте ставить break после каждого case."
    )

    # 8. While loop
    add(
        key="while",
        order=8,
        title="Цикл while",
        section="Циклы",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Цикл while повторяет тело до тех пор, пока условие истинно:\nwhile (условие) {\n    // тело цикла\n}\nОбязательно изменяйте переменную в условии, чтобы не получить бесконечный цикл.",
        syntax="int i = 0;\nwhile (i < 5) {\n    System.out.println(i);\n    i++;\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int n = 3;\n        while (n > 0) {\n            System.out.println(n);\n            n--;\n        }\n    }\n}",
        expected_example="3\n2\n1\n",
        idea="Цикл while удобен, когда количество повторений заранее точно не известно, но известно условие остановки.",
        steps=[
            "n = 3 > 0 — печатаем 3, уменьшаем n до 2.",
            "n = 2 > 0 — печатаем 2, уменьшаем n до 1.",
            "n = 1 > 0 — печатаем 1, уменьшаем n до 0.",
            "n = 0 > 0 — условие ложно, цикл завершён."
        ],
        experiment="Что произойдет, если условие цикла изначально ложно (например, n > 10)?",
        terms=[{"term": "while", "meaning": "Цикл с проверкой условия перед каждой итерацией."}],
        task="Используя цикл while, выведите числа от 1 до 3 включительно по одному в строке.",
        starter="public class Main {\n    public static void main(String[] args) {\n        int i = 1;\n        // Напишите цикл while до 3\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int i = 1;\n        while (i <= 3) {\n            System.out.println(i);\n            i++;\n        }\n    }\n}",
        tests=[{"id": "t1", "label": "Счёт 1..3", "expected": "1\n2\n3"}],
        analogy="Представьте обратный отсчёт ракеты: секундомер отсчитывает секунды, пока таймер больше нуля. Как только дошли до 0 — старт.",
        challenge="Сделайте отсчёт от 5 до 1.",
        task_steps=["Задайте int i = 1", "В цикле проверяйте i <= 3", "Увеличивайте i++"],
        checklist=["Использован while", "Выведены числа 1, 2, 3"],
        common_mistakes="Не забывайте увеличивать счётчик i++, иначе программа зависнет."
    )

    # 9. For loop
    add(
        key="for",
        order=9,
        title="Цикл for со счётчиком",
        section="Циклы",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Цикл for компактно объединяет три части:\nfor (инициализация; условие; шаг) {\n    // действия\n}\nНапример: for (int i = 0; i < 5; i++) повторяет блок 5 раз.",
        syntax="for (int i = 0; i < 5; i++) {\n    System.out.println(i);\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 3; i++) {\n            System.out.println(\"Шаг \" + i);\n        }\n    }\n}",
        expected_example="Шаг 1\nШаг 2\nШаг 3\n",
        idea="for — самый частый цикл для обхода чисел от A до B или элементов массива.",
        steps=[
            "int i = 1 объявляет счётчик.",
            "i <= 3 проверяется перед каждым шагом.",
            "i++ прибавляет 1 после каждого шага."
        ],
        experiment="Измените шаг на i += 2. Какие числа напечатаются?",
        terms=[{"term": "цикл for", "meaning": "Цикл со встроенным счётчиком, условием продолжения и шагом изменения."}],
        task="Используя цикл for, посчитайте и выведите сумму чисел от 1 до 4 (1 + 2 + 3 + 4 = 10).",
        starter="public class Main {\n    public static void main(String[] args) {\n        int sum = 0;\n        // Запустите цикл for от 1 до 4 и прибавляйте к sum\n        System.out.println(sum);\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int sum = 0;\n        for (int i = 1; i <= 4; i++) {\n            sum += i;\n        }\n        System.out.println(sum);\n    }\n}",
        tests=[{"id": "t1", "label": "Сумма чисел", "expected": "10"}],
        analogy="Представьте шаги на лестнице: вы поднимаетесь по одной ступеньке от 1-й до 4-й и считаете сумму нарастающим итогом.",
        challenge="Посчитайте сумму чисел от 1 до 10.",
        task_steps=["Объявите int sum = 0", "Запустите for (int i = 1; i <= 4; i++)", "Прибавляйте sum += i", "Выведите sum"],
        checklist=["Цикл от 1 до 4", "Сумма 10 выведена"],
        common_mistakes="Не объявляйте sum внутри тела цикла, иначе она будет сбрасываться каждый круг."
    )

    # 10. Arrays
    add(
        key="arrays",
        order=10,
        title="Одномерные массивы: создание и индексы",
        section="Массивы",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Массив в Java хранит фиксированное количество элементов одного типа.\nСоздание массива:\nint[] numbers = new int[3]; // массив из 3 нулей\nЛибо сразу со значениями:\nint[] primes = {2, 3, 5, 7};\n\nИндексы начинаются с нуля. Длина массива доступна через свойство .length (без скобок!).",
        syntax="int[] arr = new int[5];\narr[0] = 10;\nSystem.out.println(arr.length);",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int[] scores = {90, 85, 78};\n        System.out.println(scores[0]);\n        System.out.println(scores.length);\n    }\n}",
        expected_example="90\n3\n",
        idea="Размер массива в Java фиксируется при создании и больше не может быть изменён.",
        steps=[
            "int[] scores объявляет массив целых чисел.",
            "{90, 85, 78} выделяет память под 3 элемента.",
            "scores[0] возвращает первый элемент (90).",
            "scores.length возвращает количество ячеек (3)."
        ],
        experiment="Измените второй элемент: scores[1] = 100; и выведите его.",
        terms=[
            {"term": "массив (int[])", "meaning": "Структура данных фиксированного размера для хранения однотипных значений."},
            {"term": ".length", "meaning": "Свойство массива, возвращающее его длину."}
        ],
        task="Создайте массив int[] values = {10, 20, 30, 40};. Выведите элемент с индексом 2 (третий по счёту).",
        starter="public class Main {\n    public static void main(String[] args) {\n        // Создайте values и выведите values[2]\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int[] values = {10, 20, 30, 40};\n        System.out.println(values[2]);\n    }\n}",
        tests=[{"id": "t1", "label": "Третий элемент", "expected": "30"}],
        analogy="Представьте лоток для карандашей на 4 отделения: в нулевом отделении лежит 10, в первом 20, во втором 30, в третьем 40.",
        challenge="Выведите длину массива через values.length.",
        task_steps=["Создайте int[] values = {10, 20, 30, 40};", "Выведите values[2]"],
        checklist=["Массив инициализирован", "Выведено число 30"],
        common_mistakes="Помните, что у массивов .length пишется БЕЗ круглых скобок, в отличие от строк."
    )

    # 11. For-each loop
    add(
        key="for-each",
        order=11,
        title="Улучшенный цикл for-each",
        section="Массивы",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Цикл for-each позволяет последовательно перебрать все элементы массива без возни со счётчиками и индексами:\nfor (int item : array) {\n    System.out.println(item);\n}\nДвоеточие читается как «из» («для каждого item из array»).",
        syntax="for (String name : names) {\n    System.out.println(name);\n}",
        example_code="public class Main {\n    public static void main(String[] args) {\n        int[] nums = {5, 10, 15};\n        for (int x : nums) {\n            System.out.println(x);\n        }\n    }\n}",
        expected_example="5\n10\n15\n",
        idea="for-each защищает от частой ошибки выхода за границы массива (ArrayIndexOutOfBoundsException).",
        steps=[
            "nums содержит элементы 5, 10, 15.",
            "На первом шаге переменная x равна 5.",
            "На втором шаге x равна 10, на третьем 15.",
            "Цикл сам останавливается, когда массив пройден."
        ],
        experiment="Посчитайте сумму элементов массива внутри for-each, прибавляя каждый x к внешней переменной sum.",
        terms=[{"term": "for-each", "meaning": "Синтаксис обхода каждого элемента коллекции или массива без явного индекса."}],
        task="Дан массив int[] numbers = {2, 4, 6};. Используя цикл for-each, найдите сумму всех чисел и выведите её.",
        starter="public class Main {\n    public static void main(String[] args) {\n        int[] numbers = {2, 4, 6};\n        int sum = 0;\n        // Пройдите по массиву через for-each и сложите элементы\n        System.out.println(sum);\n    }\n}",
        solution="public class Main {\n    public static void main(String[] args) {\n        int[] numbers = {2, 4, 6};\n        int sum = 0;\n        for (int n : numbers) {\n            sum += n;\n        }\n        System.out.println(sum);\n    }\n}",
        tests=[{"id": "t1", "label": "Сумма массива", "expected": "12"}],
        analogy="Представьте чтение колоды карт: вы берете карты по одной сверху вниз, пока колода не закончится, не думая о порядковом номере каждой карты.",
        challenge="Найдите произведение всех элементов массива через for-each.",
        task_steps=["Напишите for (int n : numbers)", "Прибавляйте sum += n", "Выведите sum (12)"],
        checklist=["Использован синтаксис for (int n : numbers)", "Сумма 12 выведена"],
        common_mistakes="Тип переменной в for-each должен совпадать с типом элементов массива (int для int[])."
    )

    # 12. Methods
    add(
        key="methods",
        order=12,
        title="Методы: объявление и параметры",
        section="Методы",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Метод — это законченный блок команд, выполняющий действие. Статические методы (static) можно вызывать напрямую из main без создания экземпляра класса:\npublic static int add(int a, int b) {\n    return a + b;\n}\nОператор return возвращает результат и выходит из метода.",
        syntax="public static int square(int x) {\n    return x * x;\n}",
        example_code="public class Main {\n    public static int doubleValue(int n) {\n        return n * 2;\n    }\n    public static void main(String[] args) {\n        System.out.println(doubleValue(21));\n    }\n}",
        expected_example="42\n",
        idea="Методы избавляют от дублирования кода: логика пишется один раз, а вызывается сколько угодно раз с разными данными.",
        steps=[
            "doubleValue(int n) принимает число n.",
            "return n * 2 вычисляет удвоенное значение и возвращает его.",
            "В main вызов doubleValue(21) подставляет 42 в вывод."
        ],
        experiment="Добавьте метод public static int triple(int n), утрояющий число.",
        terms=[
            {"term": "метод", "meaning": "Функция, принадлежащая классу в Java."},
            {"term": "static", "meaning": "Модификатор: метод принадлежит самому классу, а не отдельному объекту."}
        ],
        task="Объявите статический метод public static int multiply(int a, int b), возвращающий a * b. В методе main вызовите multiply(7, 8) и выведите результат.",
        starter="public class Main {\n    // Объявите метод multiply здесь\n\n    public static void main(String[] args) {\n        System.out.println(multiply(7, 8));\n    }\n}",
        solution="public class Main {\n    public static int multiply(int a, int b) {\n        return a * b;\n    }\n    public static void main(String[] args) {\n        System.out.println(multiply(7, 8));\n    }\n}",
        tests=[
            {"id": "t1", "label": "Результат multiply", "expected": "56"},
            {"id": "t2", "label": "Проверка метода", "expression": "Main.multiply(4, 5)", "expected": 20}
        ],
        analogy="Представьте кухонный комбайн: у него есть насадка «измельчитель» (метод). Вы засыпаете ингредиенты (параметры), комбайн рубит их и выдает результат.",
        challenge="Напишите метод boolean isPositive(int n).",
        task_steps=["Напишите public static int multiply(int a, int b)", "Внутри верните return a * b;", "Выведите вызов multiply(7, 8)"],
        checklist=["Метод объявлен как public static int", "Вывод равен 56"],
        common_mistakes="Не объявляйте метод ВНУТРИ другого метода (main); методы объявляются на уровне класса."
    )

    # 13. Method overloading
    add(
        key="method-overload",
        order=13,
        title="Перегрузка методов (Overloading)",
        section="Методы",
        level="Junior",
        minutes=25,
        xp=55,
        theory="В Java несколько методов могут иметь ОДНО И ТО ЖЕ имя, если у них различаются списки параметров (по количеству или типам данных).\nЭто называется перегрузкой методов (method overloading).\nКомпилятор сам выбирает нужную версию в зависимости от переданных аргументов.",
        syntax="public static int add(int a, int b) { return a + b; }\npublic static double add(double a, double b) { return a + b; }",
        example_code="public class Main {\n    public static int sum(int a, int b) {\n        return a + b;\n    }\n    public static int sum(int a, int b, int c) {\n        return a + b + c;\n    }\n    public static void main(String[] args) {\n        System.out.println(sum(2, 3));\n        System.out.println(sum(2, 3, 4));\n    }\n}",
        expected_example="5\n9\n",
        idea="Перегрузка позволяет не придумывать искусственные имена вроде sumTwo, sumThree, сохраняя одно интуитивное имя метода sum.",
        steps=[
            "sum(2, 3) вызывает версию с двумя параметрами.",
            "sum(2, 3, 4) вызывает версию с тремя параметрами.",
            "Компилятор выбирает правильный метод ещё до запуска программы."
        ],
        experiment="Добавьте перегрузку sum(double a, double b).",
        terms=[{"term": "перегрузка методов (overloading)", "meaning": "Наличие в одном классе нескольких методов с одинаковым именем, но разными сигнатурами параметров."}],
        task="Объявите два метода printInfo:\n1) public static void printInfo(String name) — выводит \"Имя: \" + name;\n2) public static void printInfo(String name, int age) — выводит name + \" (\" + age + \")\".\nВ main вызовите printInfo(\"Анна\", 20).",
        starter="public class Main {\n    // Объявите две перегрузки printInfo\n\n    public static void main(String[] args) {\n        printInfo(\"Анна\", 20);\n    }\n}",
        solution="public class Main {\n    public static void printInfo(String name) {\n        System.out.println(\"Имя: \" + name);\n    }\n    public static void printInfo(String name, int age) {\n        System.out.println(name + \" (\" + age + \")\");\n    }\n    public static void main(String[] args) {\n        printInfo(\"Анна\", 20);\n    }\n}",
        tests=[{"id": "t1", "label": "Перегрузка с двумя аргументами", "expected": "Анна (20)"}],
        analogy="Представьте кнопку вызова лифта: если нажать один раз — вызывается пассажирский лифт, если нажать и удерживать — грузовой. Кнопка одна, поведение адаптируется.",
        challenge="Вызовите первую перегрузку printInfo(\"Олег\").",
        task_steps=["Объявите printInfo(String name)", "Объявите printInfo(String name, int age)", "Вызовите printInfo(\"Анна\", 20)"],
        checklist=["Оба метода имеют имя printInfo", "Вывод точно равен 'Анна (20)'"],
        common_mistakes="Перегрузка не может различаться ТОЛЬКО типом возвращаемого значения; список параметров обязан отличаться."
    )

    # 14. Classes & Constructors
    add(
        key="classes",
        order=14,
        title="Классы, объекты и конструктор",
        section="ООП",
        level="Junior",
        minutes=30,
        xp=60,
        theory="Класс — это чертёж нового типа данных. Конструктор — специальный метод с тем же именем, что и класс (без возвращаемого типа), который вызывается при создании объекта через new.\nКлючевое слово this указывает на текущий экземпляр класса.",
        syntax="class User {\n    String name;\n    User(String name) {\n        this.name = name;\n    }\n}",
        example_code="class Car {\n    String model;\n    int year;\n    Car(String model, int year) {\n        this.model = model;\n        this.year = year;\n    }\n    void info() {\n        System.out.println(model + \" \" + year);\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Car c = new Car(\"Lada\", 2024);\n        c.info();\n    }\n}",
        expected_example="Lada 2024\n",
        idea="this.model = model разрешает конфликт имён: this.model — это поле объекта, а model — входящий аргумент конструктора.",
        steps=[
            "class Car задаёт структуру машины (модель и год).",
            "new Car(\"Lada\", 2024) выделяет память и вызывает конструктор.",
            "c.info() вызывает метод у созданного объекта."
        ],
        experiment="Создайте второй объект Car c2 = new Car(\"Niva\", 2020); и вызовите c2.info().",
        terms=[
            {"term": "конструктор", "meaning": "Метод без возвращаемого типа, инициализирующий поля нового объекта."},
            {"term": "this", "meaning": "Ссылка на текущий экземпляр класса."}
        ],
        task="Создайте класс Point с полями int x; int y; и конструктором Point(int x, int y). В main создайте Point p = new Point(10, 20); и выведите сумму p.x + p.y.",
        starter="class Point {\n    // Объявите поля x, y и конструктор\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        Point p = new Point(10, 20);\n        System.out.println(p.x + p.y);\n    }\n}",
        solution="class Point {\n    int x;\n    int y;\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Point p = new Point(10, 20);\n        System.out.println(p.x + p.y);\n    }\n}",
        tests=[{"id": "t1", "label": "Сумма координат", "expected": "30"}],
        analogy="Представьте паспортный стол: класс — это пустой бланк паспорта, конструктор — процедура заполнения данных при выдаче, а готовый паспорт — объект.",
        challenge="Добавьте в Point метод void print() { System.out.println(x + \",\" + y); }.",
        task_steps=["Объявите класс Point с полями x и y", "Напишите конструктор Point(int x, int y)", "Сохраните this.x = x; this.y = y;", "Выведите p.x + p.y (30)"],
        checklist=["Класс Point создан", "Конструктор инициализирует поля", "Вывод равен 30"],
        common_mistakes="Имя конструктора должно в точности совпадать с именем класса с большой буквы."
    )

    # 15. Encapsulation & Getters/Setters
    add(
        key="encapsulation",
        order=15,
        title="Инкапсуляция: private, геттеры и сеттеры",
        section="ООП",
        level="Junior",
        minutes=30,
        xp=60,
        theory="Инкапсуляция — сокрытие внутреннего состояния объекта от прямого вмешательства.\nПоля объявляют private, а доступ к ним организуют через публичные методы:\n- геттер: getBalance() (чтение);\n- сеттер: setBalance(int b) (запись с валидацией).",
        syntax="private int balance;\npublic int getBalance() { return balance; }\npublic void setBalance(int b) {\n    if (b >= 0) this.balance = b;\n}",
        example_code="class Account {\n    private int balance;\n    public Account(int initial) {\n        if (initial > 0) this.balance = initial;\n    }\n    public int getBalance() {\n        return balance;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Account acc = new Account(1500);\n        System.out.println(acc.getBalance());\n    }\n}",
        expected_example="1500\n",
        idea="Сеттеры позволяют проверить корректность данных: например, не дать установить отрицательный баланс или пустой пароль.",
        steps=[
            "private int balance защищён: сторонний код не может написать acc.balance = -999.",
            "Конструктор инициализирует баланс.",
            "getBalance() безопасно отдаёт текущее значение."
        ],
        experiment="Попробуйте обратиться к acc.balance напрямую в main. Что скажет компилятор?",
        terms=[
            {"term": "инкапсуляция", "meaning": "Ограничение прямого доступа к данным объекта и объединение данных с методами их обработки."},
            {"term": "private", "meaning": "Модификатор доступа: поле или метод доступны только внутри своего класса."}
        ],
        task="Создайте класс Person с приватным полем private String name;. Добавьте конструктор Person(String name) и публичный метод public String getName() { return name; }. В main создайте Person p = new Person(\"Дмитрий\"); и выведите p.getName().",
        starter="class Person {\n    // Сделайте private поле name, конструктор и геттер getName()\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person(\"Дмитрий\");\n        System.out.println(p.getName());\n    }\n}",
        solution="class Person {\n    private String name;\n    public Person(String name) {\n        this.name = name;\n    }\n    public String getName() {\n        return name;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person(\"Дмитрий\");\n        System.out.println(p.getName());\n    }\n}",
        tests=[{"id": "t1", "label": "Геттер имени", "expected": "Дмитрий"}],
        analogy="Представьте банкомат: хранилище денег надёжно заперто броней (private). Клиент может положить или снять деньги только через интерфейс терминала (методы).",
        challenge="Добавьте сеттер public void setName(String name).",
        task_steps=["Объявите private String name;", "Реализуйте конструктор и метод getName()", "Выведите p.getName()"],
        checklist=["Поле name закрыто модификатором private", "Геттер возвращает значение", "Вывод 'Дмитрий'"],
        common_mistakes="Геттер обязательно должен быть public, иначе его нельзя вызвать извне."
    )

    # 16. Inheritance & Polymorphism
    add(
        key="inheritance",
        order=16,
        title="Наследование: ключевое слово extends",
        section="ООП",
        level="Junior",
        minutes=30,
        xp=65,
        theory="Наследование позволяет создать новый класс на основе существующего, унаследовав его поля и методы:\nclass Dog extends Animal { ... }\nКласс-наследник может переопределять методы родителя (метод с той же сигнатурой).",
        syntax="class Animal {\n    void sound() { System.out.println(\"...\"); }\n}\nclass Cat extends Animal {\n    void sound() { System.out.println(\"Мяу\"); }\n}",
        example_code="class Animal {\n    void speak() {\n        System.out.println(\"Голос\");\n    }\n}\nclass Dog extends Animal {\n    void speak() {\n        System.out.println(\"Гав\");\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Animal d = new Dog();\n        d.speak();\n    }\n}",
        expected_example="Гав\n",
        idea="Полиморфизм: переменная базового типа Animal может хранить объект наследника Dog и вызовет правильный переопределённый метод.",
        steps=[
            "Animal — родительский класс.",
            "Dog extends Animal наследует класс и переопределяет метод speak().",
            "d.speak() вызывает версию из Dog, выводя 'Гав'."
        ],
        experiment="Создайте класс Cat extends Animal с выводом 'Мяу'.",
        terms=[
            {"term": "extends", "meaning": "Ключевое слово для создания класса-наследника."},
            {"term": "переопределение метода (@Override)", "meaning": "Реализация в дочернем классе метода с той же сигнатурой, что и в базовом."}
        ],
        task="Создайте базовый класс Greeting с методом void say() { System.out.println(\"Привет\"); }. Создайте класс EnglishGreeting extends Greeting с переопределённым методом void say() { System.out.println(\"Hello\"); }. В main создайте Greeting g = new EnglishGreeting(); и вызовите g.say().",
        starter="// Объявите Greeting и EnglishGreeting extends Greeting\n\npublic class Main {\n    public static void main(String[] args) {\n        Greeting g = new EnglishGreeting();\n        g.say();\n    }\n}",
        solution="class Greeting {\n    void say() {\n        System.out.println(\"Привет\");\n    }\n}\nclass EnglishGreeting extends Greeting {\n    void say() {\n        System.out.println(\"Hello\");\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Greeting g = new EnglishGreeting();\n        g.say();\n    }\n}",
        tests=[{"id": "t1", "label": "Переопределённый метод", "expected": "Hello"}],
        analogy="Представьте базовый телефон: умеет звонить. Смартфон наследует телефон, но переопределяет интерфейс звонка на сенсорный экран.",
        challenge="Создайте класс SpanishGreeting с выводом 'Hola'.",
        task_steps=["Объявите class Greeting", "Объявите class EnglishGreeting extends Greeting", "Переопределите say()", "Вызовите g.say()"],
        checklist=["Использован extends", "Метод say() переопределён", "Выведено 'Hello'"],
        common_mistakes="Не меняйте имя метода или список параметров при переопределении, иначе получится перегрузка, а не переопределение."
    )

    # 17. Scanner input
    add(
        key="scanner",
        order=17,
        title="Чтение ввода пользователя: Scanner",
        section="Ввод и вывод",
        level="Junior",
        minutes=25,
        xp=65,
        theory="Для чтения ввода с клавиатуры или STDIN в Java используют класс Scanner из пакета java.util:\nScanner sc = new Scanner(System.in);\nint number = sc.nextInt();\nString text = sc.nextLine();\n\nВ DevForge вы можете заранее заполнить поле «Ввод для программы · STDIN», и Scanner последовательно прочитает все строки.",
        syntax="import java.util.Scanner;\nScanner sc = new Scanner(System.in);\nint age = sc.nextInt();",
        example_code="import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int x = sc.nextInt();\n        System.out.println(x * 2);\n    }\n}",
        expected_example="42\n",
        idea="Scanner разбивает поток ввода на слова и числа, автоматически преобразуя текст во внутренние типы Java.",
        steps=[
            "Scanner sc = new Scanner(System.in) подключается к потоку ввода.",
            "sc.nextInt() считывает следующее целое число.",
            "x * 2 удваивает полученное число и выводит в консоль."
        ],
        experiment="Запустите программу с другим числом в STDIN.",
        terms=[{"term": "Scanner", "meaning": "Удобный класс для парсинга примитивных типов и строк из потока System.in."}],
        task="Прочитайте число n через Scanner(System.in) и выведите n + 1 (в STDIN передано число 41, ожидается вывод 42).",
        starter="import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Прочитайте число и прибавьте 1\n    }\n}",
        solution="import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        System.out.println(n + 1);\n    }\n}",
        tests=[
            {"id": "t1", "label": "Ввод 41 -> вывод 42", "expected": "42", "stdin": "41"},
            {"id": "t2", "label": "Ввод 99 -> вывод 100", "expected": "100", "stdin": "99"}
        ],
        analogy="Представьте воронку с ситом: сырые данные поступают в воронку (System.in), а сито (Scanner) отбирает только чистые целые числа (nextInt).",
        challenge="Прочитайте два числа подряд и сложите их.",
        task_steps=["Вызовите int n = sc.nextInt();", "Выведите n + 1", "Убедитесь, что вывод равен 42"],
        checklist=["Scanner использован", "Вычислено n + 1 = 42"],
        common_mistakes="Если в потоке ввода нет чисел, sc.nextInt() выбросит NoSuchElementException.",
        stdin="41"
    )

    # 18. Practical Junior+ Project: Bank Account
    add(
        key="project",
        order=18,
        title="Итоговый проект: банковский счёт с транзакциями",
        section="Практика Junior+",
        level="Junior+",
        minutes=35,
        xp=75,
        theory="В этом проекте вы объедините ООП, инкапсуляцию, условия и массивы.\nМы создаём класс BankAccount:\n- баланс закрыт модификатором private;\n- метод deposit(int amount) пополняет счёт, если сумма > 0;\n- метод withdraw(int amount) снимает средства, если сумма > 0 и на счету достаточно средств;\n- метод getBalance() возвращает текущий остаток.",
        syntax="class BankAccount {\n    private int balance;\n    public void deposit(int a) { if (a > 0) balance += a; }\n}",
        example_code="class SimpleWallet {\n    private int balance = 100;\n    public void spend(int a) {\n        if (a > 0 && a <= balance) balance -= a;\n    }\n    public int getBalance() {\n        return balance;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        SimpleWallet w = new SimpleWallet();\n        w.spend(30);\n        System.out.println(w.getBalance());\n    }\n}",
        expected_example="70\n",
        idea="Приватные поля гарантируют, что баланс не может уйти в минус в обход бизнес-правил метода withdraw.",
        steps=[
            "balance инициализирован начальным значением.",
            "Метод spend(30) проверяет корректность суммы и остатка.",
            "Баланс уменьшается на 30, результат 70."
        ],
        experiment="Попробуйте снять 200 при балансе 100. Сработает ли условие?",
        terms=[{"term": "бизнес-логика", "meaning": "Правила предметной области, инкапсулированные в методах класса."}],
        task="Создайте класс BankAccount с приватным полем private int balance = 0;. Реализуйте методы:\n- public void deposit(int amount) — прибавляет amount к balance, если amount > 0;\n- public boolean withdraw(int amount) — если amount > 0 и balance >= amount, уменьшает balance на amount и возвращает true; иначе false;\n- public int getBalance() — возвращает balance.\n\nВ методе main создайте счёт, внесите 500 (deposit(500)), снимите 200 (withdraw(200)) и выведите итоговый getBalance().",
        starter="class BankAccount {\n    // Реализуйте balance, deposit, withdraw, getBalance\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        BankAccount acc = new BankAccount();\n        acc.deposit(500);\n        acc.withdraw(200);\n        System.out.println(acc.getBalance());\n    }\n}",
        solution="class BankAccount {\n    private int balance = 0;\n    public void deposit(int amount) {\n        if (amount > 0) {\n            balance += amount;\n        }\n    }\n    public boolean withdraw(int amount) {\n        if (amount > 0 && balance >= amount) {\n            balance -= amount;\n            return true;\n        }\n        return false;\n    }\n    public int getBalance() {\n        return balance;\n    }\n}\npublic class Main {\n    public static void main(String[] args) {\n        BankAccount acc = new BankAccount();\n        acc.deposit(500);\n        acc.withdraw(200);\n        System.out.println(acc.getBalance());\n    }\n}",
        tests=[
            {"id": "t1", "label": "Остаток баланса", "expected": "300"},
            {"id": "t2", "label": "Проверка отказа при овердрафте", "expression": "(() => { const b = new BankAccount(); b.deposit(100); const ok = b.withdraw(150); return ok; })()", "expected": False}
        ],
        analogy="Представьте реальный банковский сейф: кассир выполняет операции строго по регламенту проверки платёжеспособности, защищая деньги от ухода в минус.",
        challenge="Добавьте метод для перевода средств transferTo(BankAccount target, int amount).",
        task_steps=["Создайте класс BankAccount с private int balance = 0", "Реализуйте deposit с проверкой amount > 0", "Реализуйте withdraw с проверкой balance >= amount", "Выведите acc.getBalance() (300)"],
        checklist=["Поле balance приватное", "Методы deposit, withdraw, getBalance работают", "Вывод равен 300"],
        common_mistakes="Не разрешайте снимать больше, чем есть на счету (balance >= amount)."
    )

    return lessons

if __name__ == "__main__":
    items = get_java_lessons()
    print(f"Java lessons authored: {len(items)}")
