"""JavaScript curriculum for DevForge (20 lessons from scratch to Junior+ practice)."""

def get_js_lessons():
    lessons = []
    
    def add(key, order, title, section, level, minutes, xp, theory, syntax, example_code, expected_example, idea, steps, experiment, terms, task, starter, solution, tests, analogy, challenge, task_steps, checklist, common_mistakes):
        lesson_id = f"javascript-{key}"
        lessons.append({
            "id": lesson_id,
            "language": "javascript",
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
            "hints": [task_steps[0], task_steps[1], "Проверьте кавычки, имена переменных и запуск кода через Run."],
            "commonMistakes": common_mistakes,
            "solutionExplanation": f"Решение использует {syntax.splitlines()[0] if syntax else 'базовый синтаксис JS'}. При вызове возвращаются требуемые данные.",
            "xp": xp,
            "tests": tests,
            "prerequisites": [lessons[-1]["id"]] if lessons else [],
            "resources": [],
            "lifeExample": analogy,
            "challenge": challenge,
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

    # 1. First console.log
    add(
        key="first-console",
        order=1,
        title="Первая программа: console.log",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="JavaScript — язык интерактивности и веб-приложений. Команда console.log() выводит текст или данные на экран (в консоль).\n\nТекст заключается в кавычки — одинарные ('...'), двойные (\"...\") или косые (`...`). Инструкции обычно завершаются точкой с запятой (;).",
        syntax="console.log('Привет, мир!');",
        example_code="console.log('Я учусь JavaScript!');",
        expected_example="Я учусь JavaScript!\n",
        idea="console.log — универсальная команда вывода в JavaScript. Браузер выводит всё, что передано в круглых скобках.",
        steps=[
            "console — встроенный объект для вывода отладочной информации.",
            ".log(...) — метод, выводящий строку на экран.",
            "Кавычки указывают, что внутри находится обычный текст, а не команда."
        ],
        experiment="Замените текст внутри кавычек на своё имя и запустите пример. Что вывелось?",
        terms=[{"term": "console.log", "meaning": "Команда вывода строки или значения в консоль."}],
        task="Выведите в консоль строку: Привет, DevForge!",
        starter="// Напишите ваш код здесь\n",
        solution="console.log('Привет, DevForge!');",
        tests=[{"id": "t1", "label": "Вывод строки", "expected": "Привет, DevForge!"}],
        analogy="Представьте громкоговоритель на вокзале: диспетчер берёт микрофон (console) и объявляет сообщение (.log). Пассажиры слышат именно слова сообщения, а не марку микрофона.",
        challenge="Выведите две строки подряд с помощью двух console.log. В каком порядке они появились?",
        task_steps=["Напишите console.log", "В скобках в кавычках укажите Привет, DevForge!", "Нажмите Run для проверки вывода."],
        checklist=["Есть вызов console.log", "Строка взята в кавычки", "Текст точно совпадает с заданием"],
        common_mistakes="Не забывайте круглые скобки и закрывающие кавычки."
    )

    # 2. Variables let & const
    add(
        key="variables",
        order=2,
        title="Переменные: let и const",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Переменная — это именованное хранилище для данных.\n\nВ современном JS используют два ключевых слова:\n- let — для переменных, значение которых может меняться;\n- const — для констант, которые задаются один раз и не перезаписываются.",
        syntax="let score = 10;\nconst maxScore = 100;\nscore = 15;",
        example_code="let count = 5;\ncount = count + 1;\nconsole.log(count);",
        expected_example="6\n",
        idea="Переменная создаётся один раз с помощью let или const. Затем к ней обращаются просто по имени.",
        steps=[
            "let count = 5 создаёт ячейку с именем count и числом 5.",
            "count = count + 1 берет старое значение (5), прибавляет 1 и сохраняет 6.",
            "console.log(count) выводит текущее значение."
        ],
        experiment="Замените let на const в первой строке и нажмите Run. Посмотрите на ошибку попытки перезаписи константы.",
        terms=[
            {"term": "let", "meaning": "Объявление изменяемой переменной."},
            {"term": "const", "meaning": "Объявление неизменяемой константы."}
        ],
        task="Объявите переменную let points = 10, прибавьте к ней 5 (points = points + 5) и выведите points.",
        starter="let points = 10;\n// Прибавьте 5 и выведите результат\n",
        solution="let points = 10;\npoints = points + 5;\nconsole.log(points);",
        tests=[{"id": "t1", "label": "Значение points", "expected": "15"}],
        analogy="Представьте коробку с надписью «points»: сначала вы кладете туда 10 монет, затем досыпаете ещё 5. В коробке становится 15 монет.",
        challenge="Попробуйте умножить points на 2 вместо сложения.",
        task_steps=["Объявите let points = 10;", "Увеличьте points на 5;", "Выведите результат через console.log(points);"],
        checklist=["Использован let", "Значение обновлено до 15", "Результат выведен в консоль"],
        common_mistakes="Не пишите повторно let points = points + 5; повторное объявление вызовет ошибку."
    )

    # 3. Numbers & Math
    add(
        key="numbers",
        order=3,
        title="Числа и арифметика",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="JavaScript выполняет стандартные арифметические операции:\n+ сложение, - вычитание, * умножение, / деление, % остаток от деления.\n\nКруглые скобки задают приоритет вычислений, как в обычной математике.",
        syntax="const total = (2 + 3) * 4;\nconst remainder = 10 % 3;",
        example_code="const a = 10;\nconst b = 3;\nconsole.log(a % b);",
        expected_example="1\n",
        idea="Оператор % (остаток от деления) очень удобен для проверки чётности: четные числа при делении на 2 дают остаток 0.",
        steps=[
            "10 делится на 3: берём 3 раза по 3 (это 9).",
            "Остаток равен 10 - 9 = 1.",
            "console.log печатает 1."
        ],
        experiment="Замените 10 на 12. Какой остаток от деления на 3 получится?",
        terms=[{"term": "остаток от деления (%)", "meaning": "Возвращает целое число, оставшееся после деления одного числа на другое."}],
        task="Создайте две переменные const price = 50 и const count = 4. Вычислите и выведите их произведение.",
        starter="const price = 50;\nconst count = 4;\n// Выведите общую стоимость\n",
        solution="const price = 50;\nconst count = 4;\nconsole.log(price * count);",
        tests=[{"id": "t1", "label": "Произведение", "expected": "200"}],
        analogy="Представьте покупку 4 порций мороженого по 50 рублей: общая стоимость вычисляется умножением 50 на 4.",
        challenge="Посчитайте остаток от деления 25 на 7.",
        task_steps=["Умножьте price на count", "Выведите результат через console.log"],
        checklist=["Операция умножения (*)", "Вывод равен 200"],
        common_mistakes="Не путайте знак умножения (*) и деления (/)."
    )

    # 4. Strings & Template Literals
    add(
        key="strings",
        order=4,
        title="Строки и шаблонные строки",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Строки в JavaScript можно объединять знаком плюс ('Привет, ' + name) или с помощью шаблонных строк в обратных кавычках: `Привет, ${name}!`. Внутри ${} можно вычислять любые выражения.",
        syntax="const name = 'Анна';\nconsole.log(`Привет, ${name}!`);",
        example_code="const user = 'Иван';\nconst age = 20;\nconsole.log(`${user} (${age} лет)`);",
        expected_example="Иван (20 лет)\n",
        idea="Шаблонные строки в обратных кавычках (тильда на клавиатуре) избавляют от бесконечных плюсов и пробелов при сборке предложений.",
        steps=[
            "Обратные кавычки ` ` открывают шаблонную строку.",
            "${user} подставляет значение переменной user прямо в текст.",
            "Пробелы и символы внутри шаблона сохраняются в точности."
        ],
        experiment="Попробуйте внутри ${} написать арифметику: `${2 + 2}`. Что выведет консоль?",
        terms=[{"term": "шаблонная строка", "meaning": "Строка в обратных кавычках с поддержкой вставок вида ${выражение}."}],
        task="Объявите const lang = 'JavaScript' и выведите строку: Я изучаю JavaScript!",
        starter="const lang = 'JavaScript';\n// Выведите строку через шаблон или конкатенацию\n",
        solution="const lang = 'JavaScript';\nconsole.log(`Я изучаю ${lang}!`);",
        tests=[{"id": "t1", "label": "Шаблонная строка", "expected": "Я изучаю JavaScript!"}],
        analogy="Представьте бланк с пропущенной строчкой: имя вписывается точно на место прочерка, а весь остальной текст бланка остаётся неизменным.",
        challenge="Сделайте шаблон, объединяющий имя и фамилию через пробел.",
        task_steps=["Используйте обратные кавычки и ${lang}", "Выведите полученную строку"],
        checklist=["Точное совпадение текста", "Восклицательный знак в конце"],
        common_mistakes="Не путайте обычные кавычки ' с обратными `."
    )

    # 5. Booleans & Typeof
    add(
        key="booleans",
        order=5,
        title="Логический тип и оператор typeof",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Тип boolean имеет всего два значения: true (истина) и false (ложь).\nОператор typeof сообщает тип любого значения: 'number', 'string', 'boolean', 'object', 'undefined'.",
        syntax="const isReady = true;\nconsole.log(typeof isReady); // 'boolean'",
        example_code="const isOnline = true;\nconsole.log(typeof isOnline);",
        expected_example="boolean\n",
        idea="Оператор typeof позволяет программе проверить, с чем она работает: с числом, текстом или ответом да/нет.",
        steps=[
            "isOnline хранит значение true.",
            "typeof isOnline вычисляет строку с названием типа данных.",
            "Результат 'boolean' выводится в консоль."
        ],
        experiment="Проверьте typeof от числа 42 и от строки 'тест'.",
        terms=[{"term": "boolean", "meaning": "Логический тип данных: только true или false."}],
        task="Создайте переменную const isActive = false и выведите её значение.",
        starter="// Объявите isActive и выведите в консоль\n",
        solution="const isActive = false;\nconsole.log(isActive);",
        tests=[{"id": "t1", "label": "Вывод boolean", "expected": "false"}],
        analogy="Представьте переключатель света: он может быть либо включён (true), либо выключен (false). Третьего состояния у него нет.",
        challenge="Выведите typeof isActive в следующей строке.",
        task_steps=["Объявите const isActive = false;", "Выведите isActive через console.log."],
        checklist=["Переменная isActive создана", "Значение false выведено"],
        common_mistakes="Не пишите true и false в кавычках: 'false' — это уже текст, а не boolean."
    )

    # 6. If / Else
    add(
        key="if-else",
        order=6,
        title="Условия: if, else if, else",
        section="Условия и ветвления",
        level="Beginner",
        minutes=20,
        xp=45,
        theory="Конструкция if выполняет блок кода, если условие в круглых скобках истинно (true). Если ложно — управление переходит к ветке else if или else.",
        syntax="if (age >= 18) {\n  console.log('Доступ разрешён');\n} else {\n  console.log('Рано');\n}",
        example_code="const temp = 25;\nif (temp > 20) {\n  console.log('Тепло');\n} else {\n  console.log('Прохладно');\n}",
        expected_example="Тепло\n",
        idea="Условие if задаёт развилку в программе: компьютер выбирает одну из веток в зависимости от данных.",
        steps=[
            "temp > 20 проверяется: 25 больше 20, условие true.",
            "Выполняется тело первого блока { ... }.",
            "Блок else пропускается."
        ],
        experiment="Поменяйте temp на 15. Какая ветка сработает теперь?",
        terms=[
            {"term": "if", "meaning": "Оператор проверки условия."},
            {"term": "else", "meaning": "Запасная ветка, если условие оказалось ложным."}
        ],
        task="Напишите условие для переменной const score = 75: если score >= 60, выведите 'Сдал', иначе 'Не сдал'.",
        starter="const score = 75;\n// Напишите проверку if / else\n",
        solution="const score = 75;\nif (score >= 60) {\n  console.log('Сдал');\n} else {\n  console.log('Не сдал');\n}",
        tests=[{"id": "t1", "label": "Сдал", "expected": "Сдал"}],
        analogy="Представьте турникет в метро: если баланс на билете достаточен — створки открываются, иначе загорается красный индикатор.",
        challenge="Добавьте ветку else if (score >= 90) с выводом 'Отлично'.",
        task_steps=["Проверьте score >= 60", "В блоке if выведите 'Сдал'", "В блоке else выведите 'Не сдал'"],
        checklist=["Есть if и else", "Скобки фигурные { } расставлены правильно", "Вывод 'Сдал'"],
        common_mistakes="Условие обязательно оборачивается в круглые скобки (score >= 60)."
    )

    # 7. Strict equality === & Logic operators
    add(
        key="comparison",
        order=7,
        title="Строгое сравнение === и логика",
        section="Условия и ветвления",
        level="Beginner",
        minutes=20,
        xp=45,
        theory="В JavaScript всегда рекомендуется использовать строгое равенство === (и строгое неравенство !==), чтобы избежать неожиданного приведения типов.\nЛогические операторы:\n&& — логическое И (оба условия должны быть true);\n|| — логическое ИЛИ (хотя бы одно true);\n! — логическое НЕ (инверсия).",
        syntax="const ok = (age >= 18) && hasPassport;\nif (role === 'admin' || role === 'moderator') { ... }",
        example_code="const a = 5;\nconst b = '5';\nconsole.log(a === b);\nconsole.log(a == b);",
        expected_example="false\ntrue\n",
        idea="=== проверяет и значение, и тип данных. Число 5 не равно строке '5'.",
        steps=[
            "5 === '5' проверяет типы: number !== string, результат false.",
            "5 == '5' пытается привести строку к числу, поэтому даёт true (именно поэтому == опасен).",
            "Всегда пишите === для надёжности."
        ],
        experiment="Проверьте результат сравнения 0 === false.",
        terms=[{"term": "===", "meaning": "Строгое равенство без неявного приведения типов."}],
        task="Даны const age = 22 и const hasTicket = true. Если age >= 18 И hasTicket равен true, выведите 'Проходите', иначе 'Отказ'.",
        starter="const age = 22;\nconst hasTicket = true;\n// Проверьте оба условия через &&\n",
        solution="const age = 22;\nconst hasTicket = true;\nif (age >= 18 && hasTicket) {\n  console.log('Проходите');\n} else {\n  console.log('Отказ');\n}",
        tests=[{"id": "t1", "label": "Логическое И", "expected": "Проходите"}],
        analogy="Представьте посадку на рейс: вам обязательно нужны И паспорт подходящего возраста, И посадочный талон. Если нет чего-то одного — проход закрыт.",
        challenge="Проверьте, что выведется, если hasTicket изменить на false.",
        task_steps=["Объедините условия через &&", "Выведите 'Проходите' при успехе"],
        checklist=["Использован оператор &&", "Вывод 'Проходите'"],
        common_mistakes="Не используйте один знак равенства = в условии: = это присваивание."
    )

    # 8. Switch
    add(
        key="switch",
        order=8,
        title="Конструкция switch / case",
        section="Условия и ветвления",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Когда одно значение нужно сравнить с несколькими вариантами, switch читается легче, чем цепочка if / else if.\nПосле каждого case ставят break, иначе выполнение провалится в следующий пункт. default срабатывает, если совпадений нет.",
        syntax="switch (day) {\n  case 1: console.log('Пн'); break;\n  default: console.log('Другой');\n}",
        example_code="const role = 'admin';\nswitch (role) {\n  case 'admin':\n    console.log('Полный доступ');\n    break;\n  default:\n    console.log('Гость');\n}",
        expected_example="Полный доступ\n",
        idea="switch сравнивает переменную с каждым case с помощью строгого равенства ===.",
        steps=[
            "role сравнивается со строкой 'admin'.",
            "Совпадение найдено — выполняется console.log('Полный доступ').",
            "break завершает работу switch."
        ],
        experiment="Замените 'admin' на 'user'. Что выведет default?",
        terms=[
            {"term": "switch", "meaning": "Многовариантный выбор значения."},
            {"term": "break", "meaning": "Выход из конструкции switch."}
        ],
        task="Для переменной const code = 'RU' выведите 'Россия', для 'KZ' — 'Казахстан', иначе 'Неизвестно'.",
        starter="const code = 'RU';\n// Напишите switch для code\n",
        solution="const code = 'RU';\nswitch (code) {\n  case 'RU':\n    console.log('Россия');\n    break;\n  case 'KZ':\n    console.log('Казахстан');\n    break;\n  default:\n    console.log('Неизвестно');\n}",
        tests=[{"id": "t1", "label": "Выбор кода", "expected": "Россия"}],
        analogy="Представьте пульт телевизора: вы нажимаете кнопку '1' — включается первый канал, '2' — второй. Любая другая кнопка выдает сообщение «канал не настроен».",
        challenge="Добавьте кейс для 'BY' с выводом 'Беларусь'.",
        task_steps=["Напишите switch (code)", "Добавьте case 'RU' с break", "Добавьте default"],
        checklist=["Есть break после каждого case", "Вывод 'Россия'"],
        common_mistakes="Не забывайте ключевое слово break, иначе выполнится следующий блок."
    )

    # 9. While loop
    add(
        key="while",
        order=9,
        title="Цикл while",
        section="Циклы",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Цикл while повторяет блок инструкций до тех пор, пока условие остаётся истинным.\nВнутри цикла обязательно нужно изменять переменную условия, иначе цикл станет бесконечным.",
        syntax="let i = 0;\nwhile (i < 3) {\n  console.log(i);\n  i++;\n}",
        example_code="let count = 3;\nwhile (count > 0) {\n  console.log(count);\n  count--;\n}",
        expected_example="3\n2\n1\n",
        idea="Перед каждым шагом while проверяет условие: если true — тело цикла выполняется ещё раз.",
        steps=[
            "count = 3 > 0 — true, печатаем 3, count становится 2.",
            "count = 2 > 0 — true, печатаем 2, count становится 1.",
            "count = 1 > 0 — true, печатаем 1, count становится 0.",
            "count = 0 > 0 — false, цикл завершается."
        ],
        experiment="Что произойдет, если убрать count--? (Программа зависнет в бесконечном цикле).",
        terms=[
            {"term": "while", "meaning": "Цикл с предусловием."},
            {"term": "инкремент (++) / декремент (--)", "meaning": "Увеличение или уменьшение числа на 1."}
        ],
        task="Используя while, выведите числа от 1 до 3 включительно по одному на строке.",
        starter="let n = 1;\n// Напишите цикл while до 3\n",
        solution="let n = 1;\nwhile (n <= 3) {\n  console.log(n);\n  n++;\n}",
        tests=[{"id": "t1", "label": "Счёт от 1 до 3", "expected": "1\n2\n3"}],
        analogy="Представьте отжимания на тренировке: тренер говорит «отжимайся, пока счётчик меньше 4». Сделали раз — прибавили к счёту единицу.",
        challenge="Перепишите условие так, чтобы цикл считал только до 2.",
        task_steps=["Задайте начальное let n = 1", "В условии укажите n <= 3", "Внутри увеличивайте n++"],
        checklist=["Использован while", "Выведены числа 1, 2, 3"],
        common_mistakes="Всегда увеличивайте счётчик n++, чтобы цикл не стал бесконечным."
    )

    # 10. For loop
    add(
        key="for",
        order=10,
        title="Цикл for со счётчиком",
        section="Циклы",
        level="Elementary",
        minutes=20,
        xp=45,
        theory="Цикл for объединяет инициализацию, условие и шаг в одной строке:\nfor (let i = 0; i < N; i++) { ... }\nЭто самый популярный цикл при работе с известным числом повторений.",
        syntax="for (let i = 0; i < 5; i++) {\n  console.log(i);\n}",
        example_code="for (let i = 0; i < 3; i++) {\n  console.log(`Шаг ${i}`);\n}",
        expected_example="Шаг 0\nШаг 1\nШаг 2\n",
        idea="В заголовке for собраны все три детали: откуда начать (let i = 0), когда остановиться (i < 3) и как шагать (i++).",
        steps=[
            "let i = 0: создаём счётчик.",
            "i < 3 проверяется перед каждым кругом.",
            "После каждого круга выполняется i++."
        ],
        experiment="Измените i++ на i += 2. Как изменятся шаги?",
        terms=[{"term": "цикл for", "meaning": "Цикл со счётчиком и фиксированным шагом."}],
        task="Используя цикл for, посчитайте и выведите сумму чисел от 1 до 5 (1 + 2 + 3 + 4 + 5 = 15).",
        starter="let sum = 0;\n// Запустите цикл for от 1 до 5 и прибавляйте к sum\nconsole.log(sum);",
        solution="let sum = 0;\nfor (let i = 1; i <= 5; i++) {\n  sum += i;\n}\nconsole.log(sum);",
        tests=[{"id": "t1", "label": "Сумма 1..5", "expected": "15"}],
        analogy="Представьте копилку: каждый день с понедельника по пятницу (дни 1..5) вы опускаете столько монет, какой сегодня день.",
        challenge="Посчитайте сумму чисел от 1 до 10.",
        task_steps=["Задайте let sum = 0;", "Запустите for (let i = 1; i <= 5; i++)", "Прибавляйте sum += i;"],
        checklist=["Цикл от 1 до 5 включительно", "Выведена сумма 15"],
        common_mistakes="Не объявляйте let sum внутри цикла, иначе она будет сбрасываться на каждом круге."
    )

    # 11. Functions
    add(
        key="functions",
        order=11,
        title="Функции: объявление и return",
        section="Функции",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Функция — это изолированный фрагмент кода, решающий конкретную задачу. Она может принимать аргументы и возвращать результат с помощью return.",
        syntax="function add(a, b) {\n  return a + b;\n}\nconst res = add(2, 3);",
        example_code="function double(x) {\n  return x * 2;\n}\nconsole.log(double(7));",
        expected_example="14\n",
        idea="return не просто отдаёт результат наружу — он немедленно завершает работу функции.",
        steps=[
            "double(7) передаёт число 7 в параметр x.",
            "return x * 2 вычисляет 14 и возвращает его в точку вызова.",
            "console.log выводит полученные 14."
        ],
        experiment="Что вернет функция, если забыть ключевое слово return? (undefined).",
        terms=[
            {"term": "function", "meaning": "Ключевое слово объявления функции."},
            {"term": "return", "meaning": "Возврат значения из функции и завершение её работы."}
        ],
        task="Напишите функцию multiply(a, b), которая возвращает произведение двух чисел. Вызовите multiply(6, 7) и выведите результат.",
        starter="// Объявите функцию multiply(a, b)\n\nconsole.log(multiply(6, 7));",
        solution="function multiply(a, b) {\n  return a * b;\n}\nconsole.log(multiply(6, 7));",
        tests=[
            {"id": "t1", "label": "Вызов 6 * 7", "expected": "42"},
            {"id": "t2", "label": "Проверка функции", "expression": "multiply(3, 4)", "expected": 12}
        ],
        analogy="Представьте блендер: вы загружаете фрукты (параметры a и b), нажимаете кнопку, блендер готовит смузи и выдаёт готовый стакан (return).",
        challenge="Напишите функцию square(x), возвращающую x * x.",
        task_steps=["Напишите function multiply(a, b)", "Внутри напишите return a * b;", "Вызовите функцию и выведите результат"],
        checklist=["Функция возвращает произведение через return", "Вывод равен 42"],
        common_mistakes="Не путайте console.log внутри функции с return: без return функция возвращает undefined."
    )

    # 12. Arrow functions
    add(
        key="arrow",
        order=12,
        title="Стрелочные функции",
        section="Функции",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Стрелочные функции — компактный синтаксис для записи функций: (a, b) => a + b.\nЕсли выражение занимает одну строку, фигурные скобки и слово return можно опустить (неявный возврат).",
        syntax="const add = (a, b) => a + b;\nconst square = x => x * x;",
        example_code="const greet = name => `Привет, ${name}!`;\nconsole.log(greet('Анна'));",
        expected_example="Привет, Анна!\n",
        idea="Стрелочные функции чаще всего используют для коротких вычислений и передачи в методы массивов.",
        steps=[
            "name => `Привет, ${name}!` — функция с одним аргументом.",
            "Стрелка => заменяет слово function.",
            "Выражение справа автоматически возвращается."
        ],
        experiment="Добавьте фигурные скобки: name => { `Привет, ${name}!` }. Что теперь вернётся без явного return?",
        terms=[{"term": "стрелочная функция", "meaning": "Краткая форма записи функций с помощью оператора =>."}],
        task="Создайте стрелочную функцию const cube = x => x * x * x. Выведите результат cube(3).",
        starter="// Объявите стрелочную функцию cube\n\nconsole.log(cube(3));",
        solution="const cube = x => x * x * x;\nconsole.log(cube(3));",
        tests=[
            {"id": "t1", "label": "Куб числа 3", "expected": "27"},
            {"id": "t2", "label": "Проверка cube(2)", "expression": "cube(2)", "expected": 8}
        ],
        analogy="Стрелочная функция похожа на быстрый ярлык или математическую формулу: входные данные слева от стрелки, результат справа.",
        challenge="Создайте стрелочную функцию sub = (a, b) => a - b.",
        task_steps=["Объявите const cube = x => x * x * x;", "Выведите cube(3) в консоль."],
        checklist=["Использована стрелка =>", "Вычислен куб 27"],
        common_mistakes="Если вы ставите фигурные скобки { }, не забудьте явно написать return."
    )

    # 13. Arrays
    add(
        key="arrays",
        order=13,
        title="Массивы: создание и индексы",
        section="Коллекции",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Массив — это упорядоченный список элементов в квадратных скобках: [1, 2, 3].\nНумерация элементов начинается с нуля: arr[0] — первый элемент.\nСвойство .length возвращает количество элементов.\nМетод .push() добавляет элемент в конец.",
        syntax="const items = ['яблоко', 'банан'];\nitems.push('груша');\nconsole.log(items.length); // 3",
        example_code="const fruits = ['яблоко', 'банан'];\nfruits.push('апельсин');\nconsole.log(fruits[0]);\nconsole.log(fruits.length);",
        expected_example="яблоко\n3\n",
        idea="Массивы позволяют хранить группу однородных или разнородных данных под одним именем переменной.",
        steps=[
            "fruits содержит 2 элемента.",
            ".push('апельсин') добавляет третий элемент в конец.",
            "fruits[0] читает самый первый элемент ('яблоко').",
            ".length возвращает 3."
        ],
        experiment="Какой индекс у последнего элемента в массиве из 3 элементов? (2, потому что 0, 1, 2).",
        terms=[
            {"term": "массив", "meaning": "Упорядоченная структура данных с доступом по числовым индексам."},
            {"term": "индекс", "meaning": "Порядковый номер элемента в массиве, начиная с 0."}
        ],
        task="Создайте массив const numbers = [10, 20, 30]. Добавьте в конец число 40 через push и выведите numbers[3].",
        starter="const numbers = [10, 20, 30];\n// Добавьте 40 и выведите четвертый элемент\n",
        solution="const numbers = [10, 20, 30];\nnumbers.push(40);\nconsole.log(numbers[3]);",
        tests=[{"id": "t1", "label": "Элемент с индексом 3", "expected": "40"}],
        analogy="Представьте платяной шкаф с пронумерованными полками: верхняя полка нулевая, следующая первая и так далее.",
        challenge="Выведите длину получившегося массива через numbers.length.",
        task_steps=["Вызовите numbers.push(40)", "Выведите numbers[3]"],
        checklist=["Число 40 добавлено", "Выведен элемент с индексом 3"],
        common_mistakes="Помните, что первый элемент находится под индексом 0, а не 1."
    )

    # 14. Array.map
    add(
        key="map",
        order=14,
        title="Метод массивов: map",
        section="Коллекции",
        level="Elementary",
        minutes=25,
        xp=55,
        theory="Метод .map(fn) создаёт новый массив той же длины, применив функцию-преобразователь к каждому элементу исходного массива. Исходный массив не изменяется.",
        syntax="const doubled = numbers.map(x => x * 2);",
        example_code="const nums = [1, 2, 3];\nconst squares = nums.map(x => x * x);\nconsole.log(squares);",
        expected_example="[1,4,9]\n",
        idea="map — это конвейер: каждый элемент поступает на обработку, а на выходе получается новый элемент.",
        steps=[
            "nums.map берёт 1, вычисляет 1 * 1 = 1.",
            "Берёт 2, вычисляет 2 * 2 = 4.",
            "Берёт 3, вычисляет 3 * 3 = 9.",
            "Возвращает новый массив [1, 4, 9]."
        ],
        experiment="Попробуйте прибавить 10 к каждому элементу через .map(x => x + 10).",
        terms=[{"term": "map", "meaning": "Метод массива для создания нового массива путём преобразования каждого элемента."}],
        task="Дан массив const prices = [100, 200, 300]. С помощью .map() увеличьте каждую цену на 10% (умножить на 1.1) и выведите новый массив.",
        starter="const prices = [100, 200, 300];\n// Создайте массив newPrices через .map()\n",
        solution="const prices = [100, 200, 300];\nconst newPrices = prices.map(p => p * 1.1);\nconsole.log(newPrices);",
        tests=[{"id": "t1", "label": "Новые цены", "expected": "[110,220,330]"}],
        analogy="Представьте заводской конвейер окраски деталей: каждая деталь заходит одного цвета, а на выходе получается покрашенная деталь.",
        challenge="Преобразуйте массив строк в верхний регистр через .map(s => s.toUpperCase()).",
        task_steps=["Примените .map(p => p * 1.1)", "Выведите результат через console.log"],
        checklist=["Использован .map", "Цены увеличены на 10%"],
        common_mistakes="Не забывайте возвращать значение из стрелочной функции."
    )

    # 15. Array.filter
    add(
        key="filter",
        order=15,
        title="Метод массивов: filter",
        section="Коллекции",
        level="Elementary",
        minutes=25,
        xp=55,
        theory="Метод .filter(fn) отбирает только те элементы, для которых функция возвращает true. Получается новый массив с отобранными элементами.",
        syntax="const evens = numbers.filter(x => x % 2 === 0);",
        example_code="const scores = [45, 80, 92, 30];\nconst passed = scores.filter(s => s >= 60);\nconsole.log(passed);",
        expected_example="[80,92]\n",
        idea="filter действует как сито: элементы, не подошедшие под критерий, отсеиваются.",
        steps=[
            "filter проверяет 45 >= 60 (false) — отброшено.",
            "80 >= 60 (true) — добавлено в результат.",
            "92 >= 60 (true) — добавлено в результат.",
            "30 >= 60 (false) — отброшено. Результат: [80, 92]."
        ],
        experiment="Измените условие на s < 60, чтобы найти не сдавших.",
        terms=[{"term": "filter", "meaning": "Метод массива для фильтрации элементов по предикату."}],
        task="Дан массив const nums = [5, 12, 8, 130, 44]. Отфильтруйте числа больше 10 и выведите результат.",
        starter="const nums = [5, 12, 8, 130, 44];\n// Отфильтруйте числа > 10\n",
        solution="const nums = [5, 12, 8, 130, 44];\nconst big = nums.filter(x => x > 10);\nconsole.log(big);",
        tests=[{"id": "t1", "label": "Числа больше 10", "expected": "[12,130,44]"}],
        analogy="Представьте фейсконтроль в клубе: охранник пропускает только тех гостей, у кого возраст строго от 18 лет.",
        challenge="Отфильтруйте только чётные числа из массива nums.",
        task_steps=["Вызовите nums.filter(x => x > 10)", "Выведите результат"],
        checklist=["Отобраны числа [12, 130, 44]", "Использован .filter"],
        common_mistakes="Функция в filter должна возвращать boolean (true или false)."
    )

    # 16. Array.reduce
    add(
        key="reduce",
        order=16,
        title="Метод массивов: reduce",
        section="Коллекции",
        level="Junior",
        minutes=25,
        xp=55,
        theory="Метод .reduce((acc, curr) => ..., initialValue) сворачивает массив в одно единое значение (сумму, объект, строку).\nacc — это аккумулятор (накопитель), curr — текущий элемент.",
        syntax="const sum = numbers.reduce((acc, curr) => acc + curr, 0);",
        example_code="const nums = [1, 2, 3, 4];\nconst sum = nums.reduce((acc, x) => acc + x, 0);\nconsole.log(sum);",
        expected_example="10\n",
        idea="reduce помнит результат предыдущего шага в аккумуляторе и добавляет к нему следующий элемент.",
        steps=[
            "Начальное значение acc = 0.",
            "acc = 0 + 1 = 1; затем 1 + 2 = 3; затем 3 + 3 = 6; затем 6 + 4 = 10.",
            "Возвращается итоговое число 10."
        ],
        experiment="Попробуйте перемножить все числа массива, задав начальное значение 1 и операцию acc * x.",
        terms=[{"term": "reduce", "meaning": "Сворачивание массива к одному итоговому значению."}],
        task="Дан массив const cart = [150, 300, 50]. С помощью reduce найдите общую сумму покупок и выведите её.",
        starter="const cart = [150, 300, 50];\n// Найдите сумму элементов через reduce\n",
        solution="const cart = [150, 300, 50];\nconst total = cart.reduce((acc, item) => acc + item, 0);\nconsole.log(total);",
        tests=[{"id": "t1", "label": "Сумма корзины", "expected": "500"}],
        analogy="Представьте кассира в супермаркете: он берёт чек, начальная сумма 0. Сканирует каждый товар и прибавляет его цену к текущей сумме.",
        challenge="Найдите максимальное число в массиве с помощью reduce и Math.max.",
        task_steps=["Используйте .reduce((acc, x) => acc + x, 0)", "Выведите total"],
        checklist=["Итоговая сумма 500", "Использован reduce с начальным 0"],
        common_mistakes="Всегда передавайте начальное значение вторым аргументом (например, 0)."
    )

    # 17. Objects
    add(
        key="objects",
        order=17,
        title="Объекты: свойства и значения",
        section="Объекты",
        level="Junior",
        minutes=25,
        xp=55,
        theory="Объект — это коллекция пар «ключ: значение» в фигурных скобках {}.\nКлючи обычно строки, а значениями может быть что угодно.\nДоступ к полям: через точку (user.name) или квадратные скобки (user['name']).",
        syntax="const user = {\n  name: 'Анна',\n  age: 25\n};\nconsole.log(user.name);",
        example_code="const book = {\n  title: 'Мастер и Маргарита',\n  pages: 450\n};\nconsole.log(book.title);\nconsole.log(book.pages);",
        expected_example="Мастер и Маргарита\n450\n",
        idea="Если массив хранит элементы по порядку номеров, то объект хранит свойства по их именам.",
        steps=[
            "Создаётся объект book с двумя ключами: title и pages.",
            "book.title обращается к значению по ключу 'title'.",
            "book.pages возвращает число 450."
        ],
        experiment="Добавьте новое свойство на лету: book.author = 'Булгаков'; и выведите его.",
        terms=[{"term": "объект", "meaning": "Структура данных для хранения именованных свойств (ключ-значение)."}],
        task="Создайте объект const product = { title: 'Клавиатура', price: 2500 }. Выведите строку: Клавиатура стоит 2500 руб.",
        starter="// Создайте объект product и выведите строку\n",
        solution="const product = {\n  title: 'Клавиатура',\n  price: 2500\n};\nconsole.log(`${product.title} стоит ${product.price} руб.`);",
        tests=[{"id": "t1", "label": "Свойства объекта", "expected": "Клавиатура стоит 2500 руб."}],
        analogy="Представьте паспорт гражданина: у каждого поля есть название (Фамилия, Имя, Дата рождения) и соответствующее значение.",
        challenge="Измените цену продукта через product.price = 3000.",
        task_steps=["Создайте объект product", "Используйте шаблонную строку с product.title и product.price"],
        checklist=["Создан объект", "Точное совпадение вывода"],
        common_mistakes="Не забывайте двоеточие между ключом и значением и запятые между свойствами."
    )

    # 18. Destructuring & Spread
    add(
        key="destructuring",
        order=18,
        title="Деструктуризация и spread (...)",
        section="Объекты",
        level="Junior",
        minutes=25,
        xp=55,
        theory="Деструктуризация позволяет удобно извлекать поля объекта или элементы массива в отдельные переменные:\nconst { name, age } = user;\nОператор spread (...) копирует свойства одного объекта в другой.",
        syntax="const { x, y } = point;\nconst copy = { ...user, active: true };",
        example_code="const coords = { x: 10, y: 20 };\nconst { x, y } = coords;\nconsole.log(x + y);",
        expected_example="30\n",
        idea="Деструктуризация избавляет от повторения coords.x и coords.y, сразу создавая локальные переменные x и y.",
        steps=[
            "const { x, y } = coords находит ключи x и y в объекте.",
            "Создаются две отдельные переменные x = 10 и y = 20.",
            "x + y складывает 10 и 20."
        ],
        experiment="Попробуйте объединить два массива с помощью spread: [...[1, 2], ...[3, 4]].",
        terms=[
            {"term": "деструктуризация", "meaning": "Синтаксис распаковки значений из объектов или массивов."},
            {"term": "spread (...)", "meaning": "Оператор разворачивания элементов массива или свойств объекта."}
        ],
        task="Дан объект const person = { name: 'Ольга', city: 'Москва' }. Извлеките name и city через деструктуризацию и выведите `${name} из города ${city}`.",
        starter="const person = { name: 'Ольга', city: 'Москва' };\n// Деструктурируйте name и city\n",
        solution="const person = { name: 'Ольга', city: 'Москва' };\nconst { name, city } = person;\nconsole.log(`${name} из города ${city}`);",
        tests=[{"id": "t1", "label": "Деструктуризация", "expected": "Ольга из города Москва"}],
        analogy="Представьте вскрытие посылки: вы распаковываете коробку и сразу раскладываете нужные вещи по своим местам.",
        challenge="Создайте копию person с добавлением поля age: 30 с помощью spread.",
        task_steps=["Распакуйте const { name, city } = person;", "Выведите итоговую строку."],
        checklist=["Использована деструктуризация { name, city }", "Вывод верен"],
        common_mistakes="Имена переменных при деструктуризации объекта должны совпадать с именами ключей."
    )

    # 19. Classes
    add(
        key="classes",
        order=19,
        title="Классы и ООП в JavaScript",
        section="ООП",
        level="Junior",
        minutes=30,
        xp=60,
        theory="Класс — это шаблон для создания однотипных объектов. Метод constructor(...) вызывается автоматически при создании объекта через new.\nВнутри методов ключевое слово this указывает на текущий созданный объект.",
        syntax="class User {\n  constructor(name) {\n    this.name = name;\n  }\n  greet() {\n    return `Привет, ${this.name}!`;\n  }\n}",
        example_code="class Car {\n  constructor(brand) {\n    this.brand = brand;\n  }\n  info() {\n    return `Авто: ${this.brand}`;\n  }\n}\nconst c = new Car('Toyota');\nconsole.log(c.info());",
        expected_example="Авто: Toyota\n",
        idea="Класс описывает чертёж, а оператор new Car(...) собирает по этому чертежу конкретную машину.",
        steps=[
            "class Car объявляет структуру машины.",
            "constructor(brand) сохраняет переданную марку в this.brand.",
            "new Car('Toyota') создаёт новый экземпляр.",
            "c.info() вызывает метод у конкретного экземпляра."
        ],
        experiment="Создайте второй автомобиль new Car('BMW') и вызовите info().",
        terms=[
            {"term": "class", "meaning": "Шаблон для создания объектов с данными и методами."},
            {"term": "constructor", "meaning": "Специальный метод инициализации нового объекта."},
            {"term": "this", "meaning": "Ссылка на текущий экземпляр объекта."}
        ],
        task="Создайте класс Rectangle с конструктором (w, h) и методом getArea(), возвращающим w * h. Создайте new Rectangle(5, 4) и выведите площадь.",
        starter="// Объявите класс Rectangle\n\nconst r = new Rectangle(5, 4);\nconsole.log(r.getArea());",
        solution="class Rectangle {\n  constructor(w, h) {\n    this.w = w;\n    this.h = h;\n  }\n  getArea() {\n    return this.w * this.h;\n  }\n}\nconst r = new Rectangle(5, 4);\nconsole.log(r.getArea());",
        tests=[
            {"id": "t1", "label": "Площадь прямоугольника", "expected": "20"},
            {"id": "t2", "label": "Проверка другого экземпляра", "expression": "new Rectangle(3, 7).getArea()", "expected": 21}
        ],
        analogy="Представьте форму для выпечки печенья: форма (класс) одна, а испечённых печений (объектов) можно создать сотни.",
        challenge="Добавьте метод getPerimeter(), возвращающий 2 * (w + h).",
        task_steps=["Объявите class Rectangle", "В constructor сохраните this.w и this.h", "Добавьте метод getArea()"],
        checklist=["Класс создан", "Метод getArea возвращает 20"],
        common_mistakes="Не забывайте обращаться к полям через this.w, а не просто w."
    )

    # 20. JSON & Practical project
    add(
        key="json-project",
        order=20,
        title="Итоговый проект: обработка JSON и аналитика",
        section="Практика Junior+",
        level="Junior+",
        minutes=35,
        xp=70,
        theory="JSON (JavaScript Object Notation) — главный формат обмена данными в вебе.\nJSON.stringify(obj) превращает объект в строку для отправки по сети.\nJSON.parse(str) парсит строку обратно в объект JavaScript.\n\nВ этом проекте вы объедините работу с массивами, объектами и методами filter/reduce.",
        syntax="const json = JSON.stringify({ a: 1 });\nconst data = JSON.parse(json);",
        example_code="const raw = '[{\"id\":1,\"val\":10},{\"id\":2,\"val\":20}]';\nconst list = JSON.parse(raw);\nconst total = list.reduce((acc, x) => acc + x.val, 0);\nconsole.log(`Итого: ${total}`);",
        expected_example="Итого: 30\n",
        idea="Любые данные с сервера приходят в виде текста JSON. Первым делом мы парсим их в объекты, а затем анализируем.",
        steps=[
            "JSON.parse(raw) превращает строку в массив объектов.",
            "list.reduce суммирует поле val каждого объекта.",
            "console.log выводит итоговую сумму."
        ],
        experiment="Добавьте в JSON строку третий элемент {\"id\":3,\"val\":30} и посмотрите на результат.",
        terms=[
            {"term": "JSON.parse", "meaning": "Преобразование строки формата JSON в структуру объектов/массивов JavaScript."},
            {"term": "JSON.stringify", "meaning": "Сериализация структуры данных в текст JSON."}
        ],
        task="Напишите функцию calculateDeliveredTotal(ordersJson), которая принимает строку JSON с заказами вида '[{\"id\":1,\"amount\":100,\"delivered\":true},{\"id\":2,\"amount\":50,\"delivered\":false}]', отбирает только доставленные (delivered === true) и возвращает сумму их amount. Вызовите функцию на тестовых данных и выведите сумму.",
        starter="function calculateDeliveredTotal(ordersJson) {\n  // Распарсите JSON, отфильтруйте доставленные и просуммируйте amount\n}\n\nconst testOrders = '[{\"id\":1,\"amount\":150,\"delivered\":true},{\"id\":2,\"amount\":200,\"delivered\":false},{\"id\":3,\"amount\":250,\"delivered\":true}]';\nconsole.log(calculateDeliveredTotal(testOrders));",
        solution="function calculateDeliveredTotal(ordersJson) {\n  const orders = JSON.parse(ordersJson);\n  return orders\n    .filter(o => o.delivered)\n    .reduce((sum, o) => sum + o.amount, 0);\n}\n\nconst testOrders = '[{\"id\":1,\"amount\":150,\"delivered\":true},{\"id\":2,\"amount\":200,\"delivered\":false},{\"id\":3,\"amount\":250,\"delivered\":true}]';\nconsole.log(calculateDeliveredTotal(testOrders));",
        tests=[
            {"id": "t1", "label": "Сумма доставленных заказов", "expected": "400"},
            {"id": "t2", "label": "Проверка без доставленных", "expression": "calculateDeliveredTotal('[{\"id\":1,\"amount\":100,\"delivered\":false}]')", "expected": 0}
        ],
        analogy="Представьте бухгалтера интернет-магазина: он выгружает список заказов из базы (JSON), отфильтровывает только успешно вручённые посылки и подсчитывает фактическую выручку.",
        challenge="Модифицируйте функцию, чтобы она также возвращала количество доставленных заказов.",
        task_steps=["Распарсите ordersJson через JSON.parse", "Примените .filter(o => o.delivered)", "Посчитайте сумму через .reduce", "Выведите результат (400)"],
        checklist=["Парсинг JSON выполнен", "Фильтрация по delivered", "Суммирование amount", "Вывод 400"],
        common_mistakes="Не забудьте вернуть результат из функции calculateDeliveredTotal через return."
    )

    return lessons

if __name__ == "__main__":
    items = get_js_lessons()
    print(f"JavaScript lessons authored: {len(items)}")
