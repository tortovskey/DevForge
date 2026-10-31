"""TypeScript curriculum for DevForge (18 lessons from scratch to Junior+ practice)."""

def get_ts_lessons():
    lessons = []

    def add(key, order, title, section, level, minutes, xp, theory, syntax, example_code, expected_example, idea, steps, experiment, terms, task, starter, solution, tests, analogy, challenge, task_steps, checklist, common_mistakes):
        lesson_id = f"typescript-{key}"
        lessons.append({
            "id": lesson_id,
            "language": "typescript",
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
            "hints": [task_steps[0], task_steps[1], "Проверьте типы, синтаксис двоеточия : и запуск через Run."],
            "commonMistakes": common_mistakes,
            "solutionExplanation": f"Решение использует возможности типизации TypeScript: {syntax.splitlines()[0] if syntax else ''}.",
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

    # 1. First type annotation
    add(
        key="first-type",
        order=1,
        title="Первый шаг в TypeScript: аннотации типов",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="TypeScript — это надстройка над JavaScript, добавляющая статическую типизацию. Вы указываете тип данных через двоеточие после имени переменной:\nlet name: string = 'Иван';\nlet age: number = 25;\nlet active: boolean = true;\n\nКомпилятор защищает вас от передачи текста вместо числа ещё до запуска кода.",
        syntax="let username: string = 'DevForge';\nlet score: number = 100;",
        example_code="const appName: string = 'DevForge IDE';\nconst version: number = 4;\nconsole.log(`${appName} v${version}`);",
        expected_example="DevForge IDE v4\n",
        idea="Двоеточие после переменной указывает компилятору контракт: в этой ячейке может лежать только значение этого типа.",
        steps=[
            "appName: string гарантирует, что значение всегда будет строкой.",
            "version: number фиксирует числовой тип.",
            "При попытке записать строку в version TypeScript укажет на ошибку."
        ],
        experiment="Попробуйте присвоить числу строку: const x: number = 'текст'; и посмотрите на поведение компилятора.",
        terms=[{"term": "аннотация типа", "meaning": "Синтаксис вида : type, указывающий тип переменной или выражения."}],
        task="Объявите две переменные с явными типами: const language: string = 'TypeScript' и const lessonsCount: number = 18. Выведите их через пробел.",
        starter="// Объявите типизированные переменные language и lessonsCount\n",
        solution="const language: string = 'TypeScript';\nconst lessonsCount: number = 18;\nconsole.log(`${language} ${lessonsCount}`);",
        tests=[{"id": "t1", "label": "Вывод переменных", "expected": "TypeScript 18"}],
        analogy="Представьте медицинский шприц или мерную мензурку с чёткой маркировкой: вы не перепутаете раствор, потому что на ёмкости явно написан её тип.",
        challenge="Объявите переменную const isStrict: boolean = true.",
        task_steps=["Объявите language с типом string", "Объявите lessonsCount с типом number", "Выведите `${language} ${lessonsCount}`"],
        checklist=["Указаны аннотации : string и : number", "Вывод точно равен TypeScript 18"],
        common_mistakes="Не пишите тип с большой буквы: в TypeScript типы пишутся с маленькой (string, number, boolean)."
    )

    # 2. Arrays & Tuples
    add(
        key="arrays",
        order=2,
        title="Типизация массивов и кортежей",
        section="С нуля",
        level="Beginner",
        minutes=15,
        xp=40,
        theory="Массив однородных элементов типизируется как type[] или Array<type>:\nconst numbers: number[] = [1, 2, 3];\n\nКортеж (tuple) задаёт фиксированную длину и типы для каждого индекса:\nconst user: [string, number] = ['Анна', 25];",
        syntax="const tags: string[] = ['ts', 'js'];\nconst point: [number, number] = [10, 20];",
        example_code="const scores: number[] = [85, 90, 78];\nscores.push(95);\nconsole.log(scores.length);",
        expected_example="4\n",
        idea="Тип number[] защищает массив от случайного добавления строки или объекта.",
        steps=[
            "scores: number[] разрешает хранить только числа.",
            "scores.push(95) успешно добавляет число.",
            "scores.push('сто') вызвало бы ошибку компиляции."
        ],
        experiment="Попробуйте создать кортеж координат: const p: [number, number] = [5, 10]; и вывести сумму p[0] + p[1].",
        terms=[
            {"term": "number[]", "meaning": "Массив, содержащий только элементы типа number."},
            {"term": "кортеж (tuple)", "meaning": "Массив фиксированной структуры, где каждый индекс имеет свой тип."}
        ],
        task="Создайте массив строк const colors: string[] = ['красный', 'зелёный']. Добавьте 'синий' через .push() и выведите длину colors.length.",
        starter="const colors: string[] = ['красный', 'зелёный'];\n// Добавьте 'синий' и выведите длину\n",
        solution="const colors: string[] = ['красный', 'зелёный'];\ncolors.push('синий');\nconsole.log(colors.length);",
        tests=[{"id": "t1", "label": "Длина массива", "expected": "3"}],
        analogy="Представьте патронташ или лоток для яиц: туда помещаются предметы только одной строго заданной формы.",
        challenge="Создайте кортеж let user: [number, string] = [1, 'Admin'];",
        task_steps=["Используйте colors.push('синий')", "Выведите colors.length"],
        checklist=["Массив типизирован как string[]", "Длина равна 3"],
        common_mistakes="Не забывайте квадратные скобки [] в объявлении типа массива string[]."
    )

    # 3. Functions typing
    add(
        key="functions",
        order=3,
        title="Типизация функций: параметры и return",
        section="Функции",
        level="Beginner",
        minutes=20,
        xp=45,
        theory="В функциях TypeScript мы указываем типы всех параметров и тип возвращаемого значения:\nfunction add(a: number, b: number): number {\n  return a + b;\n}\nЕсли функция ничего не возвращает, её тип — void.",
        syntax="function log(msg: string): void {\n  console.log(msg);\n}",
        example_code="function multiply(x: number, y: number): number {\n  return x * y;\n}\nconsole.log(multiply(5, 6));",
        expected_example="30\n",
        idea="Типизация функции служит живой документацией: сразу видно, что функция ждёт на вход и что отдаёт взамен.",
        steps=[
            "(x: number, y: number) требует ровно два числа.",
            ": number после скобок гарантирует, что return вернёт число.",
            "Любая попытка вызвать multiply('пять', 6) будет отсечена компилятором."
        ],
        experiment="Попробуйте вернуть из multiply строку: return 'результат'; компилятор укажет на несовпадение с типом : number.",
        terms=[
            {"term": "сигнатура функции", "meaning": "Описание типов входящих параметров и возвращаемого типа функции."},
            {"term": "void", "meaning": "Специальный тип, означающий отсутствие возвращаемого значения."}
        ],
        task="Напишите функцию getGreeting(name: string): string, возвращающую 'Привет, ' + name. Вызовите её для 'TypeScript' и выведите результат.",
        starter="// Объявите типизированную функцию getGreeting\n\nconsole.log(getGreeting('TypeScript'));",
        solution="function getGreeting(name: string): string {\n  return 'Привет, ' + name;\n}\nconsole.log(getGreeting('TypeScript'));",
        tests=[
            {"id": "t1", "label": "Приветствие", "expected": "Привет, TypeScript"},
            {"id": "t2", "label": "Проверка типа функции", "expression": "getGreeting('Мир')", "expected": "Привет, Мир"}
        ],
        analogy="Представьте электрическую розетку: её форма и напряжение строго стандартизированы. Вилка другого типа просто не вставится.",
        challenge="Напишите функцию isEven(n: number): boolean.",
        task_steps=["Объявите getGreeting с параметром (name: string): string", "Верните строку приветствия", "Выведите результат вызова"],
        checklist=["Указан тип возврата : string", "Вывод 'Привет, TypeScript'"],
        common_mistakes="Не забывайте тип возвращаемого значения после круглых скобок : string."
    )

    # 4. Optional parameters
    add(
        key="optional-params",
        order=4,
        title="Опциональные параметры и дефолты",
        section="Функции",
        level="Beginner",
        minutes=20,
        xp=45,
        theory="Знак вопроса ? после имени параметра делает его опциональным (необязательным):\nfunction greet(name: string, title?: string): string\nВнутри функции title будет иметь тип string | undefined.\nТакже можно задавать значения по умолчанию: name: string = 'Гость'.",
        syntax="function buildName(first: string, last?: string): string {\n  return last ? `${first} ${last}` : first;\n}",
        example_code="function welcome(user: string, role: string = 'гость'): string {\n  return `${user} (${role})`;\n}\nconsole.log(welcome('Иван'));\nconsole.log(welcome('Ольга', 'админ'));",
        expected_example="Иван (гость)\nОльга (админ)\n",
        idea="Опциональные параметры позволяют вызывать функцию с разным числом аргументов без ошибок типизации.",
        steps=[
            "welcome('Иван') использует значение по умолчанию 'гость'.",
            "welcome('Ольга', 'админ') явно передаёт второй аргумент.",
            "TypeScript проверяет типы обоих вызовов."
        ],
        experiment="Уберите = 'гость' и сделайте role?: string с тернарным оператором role ? role : 'гость'.",
        terms=[{"term": "опциональный параметр (?)", "meaning": "Параметр, передавать который при вызове не обязательно."}],
        task="Напишите функцию formatPrice(amount: number, currency: string = 'руб.'): string, возвращающую `${amount} ${currency}`. Вызовите formatPrice(500) и выведите результат.",
        starter="// Объявите функцию formatPrice с параметром по умолчанию currency\n\nconsole.log(formatPrice(500));",
        solution="function formatPrice(amount: number, currency: string = 'руб.'): string {\n  return `${amount} ${currency}`;\n}\nconsole.log(formatPrice(500));",
        tests=[
            {"id": "t1", "label": "Формат с дефолтом", "expected": "500 руб."},
            {"id": "t2", "label": "Формат с явной валютой", "expression": "formatPrice(10, 'USD')", "expected": "10 USD"}
        ],
        analogy="Представьте доставку пиццы: адрес обязателен, а код домофона опционален (можно передать, а можно пропустить).",
        challenge="Вызовите formatPrice(100, '$').",
        task_steps=["Задайте currency: string = 'руб.'", "Верните строку с суммой и валютой"],
        checklist=["Параметр по умолчанию настроен", "Вывод равен '500 руб.'"],
        common_mistakes="Опциональные параметры всегда должны идти ПОСЛЕ обязательных."
    )

    # 5. Union types & Narrowing
    add(
        key="union-types",
        order=5,
        title="Объединения типов (Union) и сужение",
        section="Типы данных",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Оператор | (вертикальная черта) позволяет объединять типы:\nlet id: string | number;\nЗначение может быть либо строкой, либо числом.\nЧтобы безопасно работать с конкретным типом, используют проверку typeof (сужение типов / type narrowing).",
        syntax="function printId(id: string | number) {\n  if (typeof id === 'string') {\n    console.log(id.toUpperCase());\n  } else {\n    console.log(id * 2);\n  }\n}",
        example_code="function formatId(val: string | number): string {\n  if (typeof val === 'number') {\n    return `ID#${val}`;\n  }\n  return val.trim();\n}\nconsole.log(formatId(101));\nconsole.log(formatId('  test  '));",
        expected_example="ID#101\ntest\n",
        idea="TypeScript понимает проверку typeof: внутри ветки if тип переменной сужается до number, а в else — до string.",
        steps=[
            "val: string | number принимает оба типа.",
            "typeof val === 'number' гарантирует, что внутри if переменная является числом.",
            "Ниже if переменная гарантированно строка, поэтому доступен метод .trim()."
        ],
        experiment="Попробуйте вызвать метод toUpperCase() до проверки typeof. TypeScript выдаст ошибку, так как у числа нет такого метода.",
        terms=[
            {"term": "Union тип (|)", "meaning": "Тип-объединение, допускающий значения любого из указанных типов."},
            {"term": "сужение типов (narrowing)", "meaning": "Уточнение типа переменной внутри блока кода с помощью проверок."}
        ],
        task="Напишите функцию padLeft(value: string | number): string: если value число — верните '0' + value, если строка — верните value. Вызовите padLeft(7) и выведите результат.",
        starter="// Напишите функцию padLeft со сужением типов\n\nconsole.log(padLeft(7));",
        solution="function padLeft(value: string | number): string {\n  if (typeof value === 'number') {\n    return '0' + value;\n  }\n  return value;\n}\nconsole.log(padLeft(7));",
        tests=[
            {"id": "t1", "label": "Число с нулем", "expected": "07"},
            {"id": "t2", "label": "Строка без изменений", "expression": "padLeft('42')", "expected": "42"}
        ],
        analogy="Представьте сортировочный центр: посылка может быть письмом или коробкой (Union). Сортировщик проверяет форму: письма отправляет в конверты, коробки — на поддоны (сужение).",
        challenge="Проверьте работу padLeft с текстовым аргументом '15'.",
        task_steps=["Объявите параметр value: string | number", "Проверьте if (typeof value === 'number')", "Верните результат"],
        checklist=["Использован union тип |", "Выполнено сужение через typeof", "Результат равен '07'"],
        common_mistakes="Не забывайте возвращать строку из обеих веток условия."
    )

    # 6. Type Aliases
    add(
        key="type-aliases",
        order=6,
        title="Псевдонимы типов: ключевое слово type",
        section="Типы данных",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Ключевое слово type позволяет дать собственное имя любому типу данных:\ntype ID = string | number;\ntype Point = { x: number; y: number };\nЭто делает код чище и позволяет переиспользовать описание структуры данных.",
        syntax="type Coordinate = number;\ntype User = {\n  id: number;\n  name: string;\n};",
        example_code="type Point = { x: number; y: number };\nconst p: Point = { x: 10, y: 25 };\nconsole.log(`Точка: ${p.x}, ${p.y}`);",
        expected_example="Точка: 10, 25\n",
        idea="Вместо того чтобы копировать { x: number; y: number } в десятке функций, мы объявляем удобный псевдоним type Point.",
        steps=[
            "type Point описывает форму объекта с полями x и y.",
            "const p: Point обязывает объект иметь именно эти поля и типы.",
            "Любое пропущенное поле вызовет подсказку от компилятора."
        ],
        experiment="Добавьте в Point поле z?: number и создайте 3D точку.",
        terms=[{"term": "type alias", "meaning": "Пользовательское имя для типа данных, объявляемое через ключевое слово type."}],
        task="Создайте тип type Item = { title: string; price: number };. Создайте переменную const phone: Item = { title: 'Смартфон', price: 30000 }; и выведите phone.title.",
        starter="// Объявите type Item и переменную phone\n",
        solution="type Item = {\n  title: string;\n  price: number;\n};\nconst phone: Item = {\n  title: 'Смартфон',\n  price: 30000\n};\nconsole.log(phone.title);",
        tests=[{"id": "t1", "label": "Название товара", "expected": "Смартфон"}],
        analogy="Представьте ГОСТ или чертёж детали с названием «Болт М8»: вместо перечисления всех размеров каждый раз говорят просто «Болт М8».",
        challenge="Добавьте функцию printItem(item: Item): void, выводящую товар.",
        task_steps=["Объявите type Item", "Создайте объект phone: Item", "Выведите phone.title"],
        checklist=["Псевдоним type Item объявлен", "Поле title выведено"],
        common_mistakes="Имена типов принято писать с заглавной буквы (например, Item, Point, User)."
    )

    # 7. Interfaces
    add(
        key="interfaces",
        order=7,
        title="Интерфейсы (interface)",
        section="Интерфейсы",
        level="Elementary",
        minutes=20,
        xp=50,
        theory="Интерфейс — основной способ описания формы объектов в TypeScript:\ninterface User {\n  id: number;\n  name: string;\n  email?: string;\n}\nИнтерфейсы очень похожи на type для объектов, но ориентированы на расширение и контракт классов.",
        syntax="interface Person {\n  name: string;\n  age: number;\n}",
        example_code="interface Car {\n  brand: string;\n  speed: number;\n}\nconst auto: Car = { brand: 'Lada', speed: 180 };\nconsole.log(`${auto.brand}: ${auto.speed} км/ч`);",
        expected_example="Lada: 180 км/ч\n",
        idea="Интерфейс задаёт обязательный договор для объекта: какие свойства обязаны существовать и какие у них типы.",
        steps=[
            "interface Car описывает два обязательных поля.",
            "Объект auto точно соответствует интерфейсу Car.",
            "Любое лишнее или пропущенное свойство будет подсвечено как ошибка."
        ],
        experiment="Попробуйте пропустить свойство speed в объекте auto. Какую ошибку покажет компилятор?",
        terms=[{"term": "interface", "meaning": "Синтаксическая конструкция для описания контракта формы объекта."}],
        task="Объявите interface Student с полями name: string и grade: number. Создайте объект const s: Student = { name: 'Илья', grade: 5 }; и выведите s.grade.",
        starter="// Объявите interface Student и создайте объект s\n",
        solution="interface Student {\n  name: string;\n  grade: number;\n}\nconst s: Student = {\n  name: 'Илья',\n  grade: 5\n};\nconsole.log(s.grade);",
        tests=[{"id": "t1", "label": "Оценка студента", "expected": "5"}],
        analogy="Представьте анкету соискателя: в ней есть строго обозначенные графы «ФИО» и «Возраст», которые обязательно нужно заполнить.",
        challenge="Сделайте поле email?: string опциональным.",
        task_steps=["Объявите interface Student", "Создайте объект s: Student", "Выведите s.grade"],
        checklist=["Интерфейс объявлен через ключевое слово interface", "Вывод равен 5"],
        common_mistakes="После закрывающей фигурной скобки интерфейса точка с запятой обычно не ставится."
    )

    # 8. Interface extends
    add(
        key="interface-extends",
        order=8,
        title="Расширение интерфейсов (extends)",
        section="Интерфейсы",
        level="Junior",
        minutes=25,
        xp=55,
        theory="Интерфейсы могут наследовать свойства других интерфейсов с помощью ключевого слова extends:\ninterface Animal { name: string; }\ninterface Dog extends Animal { breed: string; }\nОбъект типа Dog обязан иметь и name, и breed.",
        syntax="interface BaseUser { id: number; }\ninterface AdminUser extends BaseUser { role: string; }",
        example_code="interface Shape {\n  color: string;\n}\ninterface Circle extends Shape {\n  radius: number;\n}\nconst c: Circle = { color: 'red', radius: 10 };\nconsole.log(`${c.color} круг радиусом ${c.radius}`);",
        expected_example="red круг радиусом 10\n",
        idea="extends избавляет от дублирования базовых полей в десятках специализированных интерфейсов.",
        steps=[
            "Shape содержит базовое свойство color.",
            "Circle extends Shape наследует color и добавляет своё свойство radius.",
            "Экземпляр c: Circle содержит оба поля."
        ],
        experiment="Создайте interface Square extends Shape со свойством side: number.",
        terms=[{"term": "extends", "meaning": "Наследование интерфейсом свойств другого интерфейса."}],
        task="Объявите interface Vehicle { brand: string; } и interface ElectricCar extends Vehicle { battery: number; }. Создайте объект car: ElectricCar = { brand: 'Tesla', battery: 100 }; и выведите car.brand.",
        starter="// Объявите Vehicle и ElectricCar через extends\n",
        solution="interface Vehicle {\n  brand: string;\n}\ninterface ElectricCar extends Vehicle {\n  battery: number;\n}\nconst car: ElectricCar = {\n  brand: 'Tesla',\n  battery: 100\n};\nconsole.log(car.brand);",
        tests=[{"id": "t1", "label": "Марка электрокара", "expected": "Tesla"}],
        analogy="Представьте категорию прав «Транспортное средство»: «Электромобиль» является транспортным средством, но дополнительно обладает ёмкостью аккумулятора.",
        challenge="Добавьте вывод ёмкости батареи car.battery.",
        task_steps=["Объявите Vehicle", "Объявите ElectricCar extends Vehicle", "Создайте объект и выведите brand"],
        checklist=["Использован extends", "Поле brand унаследовано и выведено"],
        common_mistakes="Интерфейс-наследник должен реализовать и свои свойства, и все свойства предков."
    )

    # 9. Enums
    add(
        key="enums",
        order=9,
        title="Перечисления (enum)",
        section="Типы данных",
        level="Junior",
        minutes=20,
        xp=50,
        theory="Перечисление (enum) связывает понятные человеческие имена с набором констант:\nenum Direction { Up, Down, Left, Right }\nПо умолчанию элементы нумеруются с нуля (Up = 0, Down = 1 и т.д.). Также enum могут быть строковыми.",
        syntax="enum Status {\n  Draft,\n  Published,\n  Archived\n}",
        example_code="enum Status {\n  Pending,\n  Success,\n  Failed\n}\nconst current: Status = Status.Success;\nconsole.log(current);",
        expected_example="1\n",
        idea="enum избавляет от «магических чисел» и опечаток в строках статусов.",
        steps=[
            "Status.Pending получает индекс 0.",
            "Status.Success получает индекс 1.",
            "Status.Failed получает индекс 2.",
            "console.log(Status.Success) выводит 1."
        ],
        experiment="Задайте строковые значения: enum Role { Admin = 'ADMIN', User = 'USER' }.",
        terms=[{"term": "enum", "meaning": "Перечисление именованных числовых или строковых констант."}],
        task="Объявите enum OrderStatus { Created, Paid, Shipped }. Создайте переменную const state: OrderStatus = OrderStatus.Paid; и выведите её значение.",
        starter="// Объявите OrderStatus и выведите state\n",
        solution="enum OrderStatus {\n  Created,\n  Paid,\n  Shipped\n}\nconst state: OrderStatus = OrderStatus.Paid;\nconsole.log(state);",
        tests=[{"id": "t1", "label": "Значение Paid", "expected": "1"}],
        analogy="Представьте цвета светофора: Красный (0), Жёлтый (1), Зелёный (2). Вместо номера сигнала мы используем понятное слово.",
        challenge="Выведите OrderStatus.Shipped — чему равен его индекс?",
        task_steps=["Объявите enum OrderStatus", "Задайте state = OrderStatus.Paid", "Выведите state"],
        checklist=["Использовано ключевое слово enum", "Выведено число 1"],
        common_mistakes="Элементы enum разделяются запятыми, а не точками с запятой."
    )

    # 10. Literal types
    add(
        key="literal-types",
        order=10,
        title="Литеральные типы",
        section="Типы данных",
        level="Junior",
        minutes=20,
        xp=50,
        theory="Литеральный тип ограничивает значение точной строкой или числом, а не просто абстрактной строкой:\ntype Direction = 'north' | 'south' | 'east' | 'west';\nЛюбая попытка передать 'up' вызовет ошибку на этапе компиляции.",
        syntax="type Theme = 'light' | 'dark';\nlet currentTheme: Theme = 'dark';",
        example_code="type Status = 'open' | 'closed';\nfunction printStatus(s: Status) {\n  console.log(`Статус: ${s}`);\n}\nprintStatus('open');",
        expected_example="Статус: open\n",
        idea="Литеральные типы в сочетании с объединениями (Union) — это лёгкая и идиоматичная замена enum во многих TypeScript проектах.",
        steps=[
            "type Status разрешает ровно два конкретных слова: 'open' или 'closed'.",
            "printStatus('open') проходит проверку.",
            "Опечатка вроде printStatus('opened') будет мгновенно обнаружена."
        ],
        experiment="Попробуйте передать в printStatus произвольную строку 'unknown'.",
        terms=[{"term": "литеральный тип", "meaning": "Тип, представляющий ровно одно конкретное литеральное значение (строку или число)."}],
        task="Объявите type Method = 'GET' | 'POST';. Создайте переменную const reqMethod: Method = 'GET'; и выведите её.",
        starter="// Объявите type Method и переменную reqMethod\n",
        solution="type Method = 'GET' | 'POST';\nconst reqMethod: Method = 'GET';\nconsole.log(reqMethod);",
        tests=[{"id": "t1", "label": "Метод запроса", "expected": "GET"}],
        analogy="Представьте переключатель КПП в автомобиле: рычаг может встать только в P, R, N или D. Поставить его в несуществующее положение физически невозможно.",
        challenge="Создайте литеральный тип для размеров одежды: type Size = 'S' | 'M' | 'L'.",
        task_steps=["Объявите type Method = 'GET' | 'POST'", "Инициализируйте reqMethod = 'GET'", "Выведите в консоль"],
        checklist=["Тип объявлен через объединение строк", "Вывод равен GET"],
        common_mistakes="Не забывайте кавычки вокруг значений литерального типа."
    )

    # 11. Any vs Unknown
    add(
        key="any-unknown",
        order=11,
        title="any и unknown: безопасная динамика",
        section="Продвинутые типы",
        level="Junior",
        minutes=25,
        xp=55,
        theory="Тип any отключает проверку типов TypeScript полностью — это аварийный люк.\nТип unknown означает «значение любого типа, но перед использованием проверь его тип».\nunknown во много раз безопаснее any, так как требует проверки (narrowing) перед вызовом методов.",
        syntax="let a: any = 5; a.toUpperCase(); // Скомпилируется, но упадёт в рантайме!\nlet u: unknown = 'тест';\nif (typeof u === 'string') console.log(u.toUpperCase());",
        example_code="function printSafe(data: unknown) {\n  if (typeof data === 'string') {\n    console.log(data.trim());\n  } else {\n    console.log('Не строка');\n  }\n}\nprintSafe('  Привет  ');",
        expected_example="Привет\n",
        idea="unknown заставляет разработчика явно проверить тип значения перед его использованием, предотвращая падения программы.",
        steps=[
            "data: unknown говорит: мы пока не знаем, что пришло.",
            "data.trim() напрямую вызовет ошибку TypeScript.",
            "После if (typeof data === 'string') компилятор разрешает вызов .trim()."
        ],
        experiment="Вызовите printSafe(123) и посмотрите на ветку else.",
        terms=[
            {"term": "any", "meaning": "Отключение статической типизации для переменной (не рекомендуется)."},
            {"term": "unknown", "meaning": "Безопасный аналог any, требующий предварительной проверки типа перед операциями."}
        ],
        task="Напишите функцию getLength(val: unknown): number: если val строка — верните val.length, иначе верните 0. Вызовите getLength('DevForge') и выведите результат.",
        starter="// Объявите функцию getLength с параметром val: unknown\n\nconsole.log(getLength('DevForge'));",
        solution="function getLength(val: unknown): number {\n  if (typeof val === 'string') {\n    return val.length;\n  }\n  return 0;\n}\nconsole.log(getLength('DevForge'));",
        tests=[
            {"id": "t1", "label": "Длина строки", "expected": "8"},
            {"id": "t2", "label": "Проверка не-строки", "expression": "getLength(12345)", "expected": 0}
        ],
        analogy="Представьте подозрительный пакет на ленте багажа: any — это открыть его вслепую, а unknown — сначала просветить рентгеном и убедиться в безопасности.",
        challenge="Добавьте поддержку массивов через Array.isArray(val).",
        task_steps=["Проверьте if (typeof val === 'string')", "Верните val.length или 0", "Выведите результат вызова (8)"],
        checklist=["Использован тип unknown", "Есть проверка typeof", "Результат равен 8"],
        common_mistakes="Не вызывайте свойства у unknown без предварительного сужения типа."
    )

    # 12. Readonly
    add(
        key="readonly",
        order=12,
        title="Модификатор readonly",
        section="Объекты",
        level="Junior",
        minutes=20,
        xp=50,
        theory="Модификатор readonly делает свойство объекта неизменяемым после создания:\ninterface Config {\n  readonly host: string;\n  port: number;\n}\nПопытка перезаписать config.host = 'new' будет запрещена компилятором.",
        syntax="interface Point {\n  readonly x: number;\n  readonly y: number;\n}",
        example_code="interface User {\n  readonly id: number;\n  name: string;\n}\nconst u: User = { id: 1, name: 'Анна' };\nu.name = 'Аня';\nconsole.log(`${u.id}: ${u.name}`);",
        expected_example="1: Аня\n",
        idea="readonly защищает важные идентификаторы и конфигурации от случайного изменения другими частями программы.",
        steps=[
            "u.id помечен как readonly: его нельзя менять после инициализации.",
            "u.name — обычное свойство, его значение успешно меняется на 'Аня'.",
            "Попытка u.id = 2 вызовет ошибку компиляции."
        ],
        experiment="Попробуйте раскомментировать строку u.id = 2; и проверьте ошибку.",
        terms=[{"term": "readonly", "meaning": "Модификатор, запрещающий изменение свойства после его инициализации."}],
        task="Объявите interface Settings { readonly apiKey: string; theme: string; }. Создайте объект const s: Settings = { apiKey: 'secret-123', theme: 'dark' }; и выведите s.apiKey.",
        starter="// Объявите interface Settings с readonly свойством\n",
        solution="interface Settings {\n  readonly apiKey: string;\n  theme: string;\n}\nconst s: Settings = {\n  apiKey: 'secret-123',\n  theme: 'dark'\n};\nconsole.log(s.apiKey);",
        tests=[{"id": "t1", "label": "Ключ API", "expected": "secret-123"}],
        analogy="Представьте VIN-номер автомобиля: он выбит на кузове при сборке (readonly) и не меняется, в отличие от цвета или номера владельца.",
        challenge="Попробуйте изменить s.theme = 'light' — это разрешено?",
        task_steps=["Объявите интерфейс с readonly apiKey", "Создайте объект s", "Выведите s.apiKey"],
        checklist=["Свойство помечено readonly", "Вывод равен 'secret-123'"],
        common_mistakes="readonly защищает только на этапе компиляции TypeScript, в рантайме это обычное свойство JS."
    )

    # 13. Generics in functions
    add(
        key="generics-function",
        order=13,
        title="Обобщения (Generics) в функциях",
        section="Дженерики",
        level="Junior",
        minutes=30,
        xp=60,
        theory="Дженерики позволяют писать универсальные функции, сохраняющие конкретный тип данных при вызове:\nfunction first<T>(arr: T[]): T {\n  return arr[0];\n}\nБуква T — это типовой параметр (переменная для типа). Если передать массив чисел, T станет number; если строк — T станет string.",
        syntax="function wrap<T>(value: T): { data: T } {\n  return { data: value };\n}",
        example_code="function identity<T>(arg: T): T {\n  return arg;\n}\nconst str = identity('привет');\nconst num = identity(42);\nconsole.log(`${str} — ${num}`);",
        expected_example="привет — 42\n",
        idea="Дженерик позволяет функции работать с любым типом, не теряя информацию о том, какой именно тип был передан.",
        steps=[
            "<T> объявляет параметр типа T.",
            "При вызове identity('привет') компилятор автоматически определяет T = string.",
            "Возвращаемое значение str имеет тип string, а num — number."
        ],
        experiment="Напишите функцию firstElement<T>(arr: T[]): T, возвращающую arr[0].",
        terms=[{"term": "дженерик (Generic)", "meaning": "Обобщённый тип, позволяющий создавать универсальные компоненты без потери точности типов."}],
        task="Напишите дженерик-функцию getLast<T>(items: T[]): T, возвращающую последний элемент массива (items[items.length - 1]). Вызовите getLast([10, 20, 30]) и выведите результат.",
        starter="// Объявите функцию getLast<T>(items: T[]): T\n\nconsole.log(getLast([10, 20, 30]));",
        solution="function getLast<T>(items: T[]): T {\n  return items[items.length - 1];\n}\nconsole.log(getLast([10, 20, 30]));",
        tests=[
            {"id": "t1", "label": "Последний элемент", "expected": "30"},
            {"id": "t2", "label": "Проверка со строками", "expression": "getLast(['яблоко', 'банан'])", "expected": "банан"}
        ],
        analogy="Представьте прозрачную транспортировочную коробку: она может упаковать любой груз (T), но снаружи отчётливо видно, что внутри лежит книга или тостер.",
        challenge="Вызовите getLast со строковым массивом.",
        task_steps=["Объявите параметр типа <T>", "Примите items: T[] и верните T", "Вызовите для [10, 20, 30]"],
        checklist=["Синтаксис <T> использован верно", "Возвращён последний элемент 30"],
        common_mistakes="Не забывайте объявлять <T> сразу после имени функции: function fn<T>(...)."
    )

    # 14. Generic interfaces
    add(
        key="generics-interface",
        order=14,
        title="Обобщённые интерфейсы",
        section="Дженерики",
        level="Junior",
        minutes=30,
        xp=60,
        theory="Интерфейсы также могут быть параметризованы типами:\ninterface ApiResponse<T> {\n  status: number;\n  data: T;\n}\nЭто стандартный подход к типизации сетевых ответов и контейнеров данных.",
        syntax="interface Box<T> {\n  content: T;\n}\nconst numBox: Box<number> = { content: 100 };",
        example_code="interface Result<T> {\n  success: boolean;\n  payload: T;\n}\nconst res: Result<string> = { success: true, payload: 'OK' };\nconsole.log(`${res.success}: ${res.payload}`);",
        expected_example="true: OK\n",
        idea="Один интерфейс Result<T> описывает ответ сервера, где полезной нагрузкой payload может быть пользователь, список товаров или число.",
        steps=[
            "interface Result<T> принимает тип T.",
            "res: Result<string> связывает payload со строкой.",
            "TypeScript контролирует типы всех полей."
        ],
        experiment="Создайте Result<number[]> со списком оценок в payload.",
        terms=[{"term": "обобщённый интерфейс", "meaning": "Интерфейс, тип полей которого определяется через передаваемый параметр типа <T>."}],
        task="Объявите interface Container<T> { value: T; label: string; }. Создайте объект const box: Container<number> = { value: 42, label: 'Возраст' }; и выведите `${box.label}: ${box.value}`.",
        starter="// Объявите interface Container<T> и объект box\n",
        solution="interface Container<T> {\n  value: T;\n  label: string;\n}\nconst box: Container<number> = {\n  value: 42,\n  label: 'Возраст'\n};\nconsole.log(`${box.label}: ${box.value}`);",
        tests=[{"id": "t1", "label": "Контейнер значения", "expected": "Возраст: 42"}],
        analogy="Представьте капсулу: она всегда имеет пластиковую оболочку с этикеткой (label), а внутри может быть витамин C, кальций или любое другое вещество (T).",
        challenge="Создайте Container<string> со строковым значением.",
        task_steps=["Объявите interface Container<T>", "Создайте объект box: Container<number>", "Выведите информацию в консоль"],
        checklist=["Интерфейс параметризован <T>", "Вывод 'Возраст: 42'"],
        common_mistakes="При объявлении переменной обязательно укажите конкретный тип в угловых скобках: Container<number>."
    )

    # 15. Utility types: Partial & Required
    add(
        key="utility-partial",
        order=15,
        title="Служебные типы: Partial и Required",
        section="Служебные типы",
        level="Junior+",
        minutes=30,
        xp=65,
        theory="В TypeScript есть готовые служебные типы (Utility Types) для трансформации существующих типов:\nPartial<T> делает ВСЕ поля типа T опциональными (удобно для обновлений patch/update);\nRequired<T> наоборот делает все поля строго обязательными.",
        syntax="interface User { id: number; name: string; email: string; }\ntype UpdateUser = Partial<User>; // все поля стали опциональными!",
        example_code="interface Profile {\n  name: string;\n  bio: string;\n}\nconst update: Partial<Profile> = { bio: 'Люблю код' };\nconsole.log(update.bio);",
        expected_example="Люблю код\n",
        idea="Partial<T> избавляет от необходимости вручную переписывать интерфейс со знаками вопроса для функций редактирования профиля.",
        steps=[
            "Profile требует и name, и bio.",
            "Partial<Profile> делает и name, и bio опциональными (name?, bio?).",
            "Объект { bio: 'Люблю код' } валиден, несмотря на отсутствие name."
        ],
        experiment="Попробуйте применить Required к интерфейсу с опциональным полем: Required<{ a?: number }>.",
        terms=[
            {"term": "Partial<T>", "meaning": "Служебный тип, превращающий все свойства типа T в опциональные."},
            {"term": "Required<T>", "meaning": "Служебный тип, превращающий все свойства типа T в обязательные."}
        ],
        task="Дан interface Task { title: string; completed: boolean; }. Создайте объект update: Partial<Task> = { completed: true }; и выведите update.completed.",
        starter="interface Task {\n  title: string;\n  completed: boolean;\n}\n// Создайте объект update типа Partial<Task>\n",
        solution="interface Task {\n  title: string;\n  completed: boolean;\n}\nconst update: Partial<Task> = {\n  completed: true\n};\nconsole.log(update.completed);",
        tests=[{"id": "t1", "label": "Обновление задачи", "expected": "true"}],
        analogy="Представьте анкету редактирования аккаунта: вы можете обновить только фамилию или только город, не перезаполняя всю анкету заново (Partial).",
        challenge="Создайте объект patch: Partial<Task> только с полем title.",
        task_steps=["Объявите const update: Partial<Task>", "Задайте { completed: true }", "Выведите update.completed"],
        checklist=["Использован тип Partial<Task>", "Вывод true"],
        common_mistakes="Не забывайте оборачивать имя исходного типа в угловые скобки Partial<Task>."
    )

    # 16. Utility types: Pick & Omit
    add(
        key="utility-pick-omit",
        order=16,
        title="Служебные типы: Pick и Omit",
        section="Служебные типы",
        level="Junior+",
        minutes=30,
        xp=65,
        theory="Pick<T, Keys> выбирает только указанные поля из типа T:\ntype UserPreview = Pick<User, 'id' | 'name'>;\nOmit<T, Keys> исключает указанные поля, оставляя все остальные:\ntype UserWithoutPassword = Omit<User, 'password'>;",
        syntax="interface Article {\n  id: number;\n  title: string;\n  text: string;\n}\ntype ArticleHeader = Pick<Article, 'id' | 'title'>;",
        example_code="interface Product {\n  id: number;\n  name: string;\n  price: number;\n}\ntype SimpleProduct = Pick<Product, 'name' | 'price'>;\nconst item: SimpleProduct = { name: 'Чай', price: 150 };\nconsole.log(`${item.name}: ${item.price}`);",
        expected_example="Чай: 150\n",
        idea="Pick и Omit позволяют конструировать точные DTO и представления без копирования свойств.",
        steps=[
            "Product содержит три свойства: id, name, price.",
            "Pick<Product, 'name' | 'price'> оставляет только name и price.",
            "Поле id исключено из SimpleProduct."
        ],
        experiment="Используйте Omit<Product, 'id'> — результат будет идентичен SimpleProduct.",
        terms=[
            {"term": "Pick<T, Keys>", "meaning": "Служебный тип для извлечения подмножества свойств."},
            {"term": "Omit<T, Keys>", "meaning": "Служебный тип для исключения определённых свойств из типа."}
        ],
        task="Дан interface Employee { id: number; name: string; salary: number; }. Создайте тип PublicEmployee = Omit<Employee, 'salary'>;. Создайте объект emp: PublicEmployee = { id: 1, name: 'Сергей' }; и выведите emp.name.",
        starter="interface Employee {\n  id: number;\n  name: string;\n  salary: number;\n}\n// Создайте тип PublicEmployee через Omit и выведите emp.name\n",
        solution="interface Employee {\n  id: number;\n  name: string;\n  salary: number;\n}\ntype PublicEmployee = Omit<Employee, 'salary'>;\nconst emp: PublicEmployee = {\n  id: 1,\n  name: 'Сергей'\n};\nconsole.log(emp.name);",
        tests=[{"id": "t1", "label": "Имя сотрудника без зарплаты", "expected": "Сергей"}],
        analogy="Представьте публичный профиль пользователя: поле «пароль» скрыто (Omit), а имя и аватарка видны всем (Pick).",
        challenge="Создайте тип IdOnly = Pick<Employee, 'id'>.",
        task_steps=["Объявите type PublicEmployee = Omit<Employee, 'salary'>", "Создайте emp: PublicEmployee", "Выведите emp.name"],
        checklist=["Использован служебный тип Omit", "Вывод равен 'Сергей'"],
        common_mistakes="Имена исключаемых свойств передаются как строковые литералы через вертикальную черту: 'salary' | 'password'."
    )

    # 17. Classes with Access Modifiers
    add(
        key="classes",
        order=17,
        title="Классы: public, private и protected",
        section="ООП",
        level="Junior+",
        minutes=30,
        xp=65,
        theory="В TypeScript классы поддерживают модификаторы доступа:\npublic — доступен отовсюду (по умолчанию);\nprivate — доступен только внутри этого класса;\nprotected — доступен внутри этого класса и его наследников.\n\nКраткий синтаксис конструктора: constructor(private balance: number) сразу создаёт и инициализирует поле.",
        syntax="class BankAccount {\n  private balance: number;\n  constructor(initial: number) {\n    this.balance = initial;\n  }\n  public getBalance(): number {\n    return this.balance;\n  }\n}",
        example_code="class Wallet {\n  private coins: number;\n  constructor(coins: number) {\n    this.coins = coins;\n  }\n  public add(amount: number): void {\n    this.coins += amount;\n  }\n  public get(): number {\n    return this.coins;\n  }\n}\nconst w = new Wallet(50);\nw.add(25);\nconsole.log(w.get());",
        expected_example="75\n",
        idea="Модификатор private защищает внутреннее состояние от несанкционированного изменения извне в обход методов валидации.",
        steps=[
            "coins объявлен как private: прямое обращение w.coins вызовет ошибку компиляции.",
            "Изменение баланса происходит строго через метод add.",
            "Метод get возвращает текущее значение."
        ],
        experiment="Попробуйте прочитать w.coins напрямую. Посмотрите на сообщение компилятора.",
        terms=[
            {"term": "private", "meaning": "Модификатор доступа: свойство скрыто внутри класса."},
            {"term": "public", "meaning": "Модификатор доступа: свойство открыто для внешнего кода."}
        ],
        task="Создайте класс Counter с приватным полем private count: number = 0;. Добавьте публичные методы increment(): void (увеличивает count на 1) и getValue(): number (возвращает count). Создайте экземпляр, дважды вызовите increment() и выведите getValue().",
        starter="// Объявите класс Counter с private count\n",
        solution="class Counter {\n  private count: number = 0;\n  public increment(): void {\n    this.count++;\n  }\n  public getValue(): number {\n    return this.count;\n  }\n}\nconst c = new Counter();\nc.increment();\nc.increment();\nconsole.log(c.getValue());",
        tests=[
            {"id": "t1", "label": "Счётчик после двух инкрементов", "expected": "2"},
            {"id": "t2", "label": "Проверка отдельного счётчика", "expression": "(() => { const x = new Counter(); x.increment(); return x.getValue(); })()", "expected": 1}
        ],
        analogy="Представьте механический шагомер: внутри есть шестерёнки (private), но снаружи доступна только кнопка сброса и экран с числом шагов (public).",
        challenge="Добавьте метод decrement(): void.",
        task_steps=["Объявите class Counter", "Сделайте private count: number = 0", "Реализуйте increment и getValue", "Вызовите методы и выведите результат (2)"],
        checklist=["Поле count закрыто модификатором private", "Методы public", "Вывод равен 2"],
        common_mistakes="Не забывайте ключевое слово this при обращении к this.count."
    )

    # 18. Practical Junior+ Project: Generic Repository
    add(
        key="project",
        order=18,
        title="Итоговый проект: типизированный Repository",
        section="Практика Junior+",
        level="Junior+",
        minutes=35,
        xp=75,
        theory="Паттерн Repository (Хранилище) используется во всех современных корпоративных приложениях.\nМы создаём обобщённый класс DataStore<T extends { id: number }>, который умеет добавлять элементы любого типа, искать по id и возвращать весь список.\nОграничение extends { id: number } гарантирует, что у любого типа сущности обязательно есть числовой id.",
        syntax="class Store<T extends { id: number }> {\n  private items: T[] = [];\n  add(item: T): void { this.items.push(item); }\n}",
        example_code="interface BaseItem { id: number; name: string; }\nclass Storage<T extends BaseItem> {\n  private list: T[] = [];\n  add(item: T): void { this.list.push(item); }\n  getAll(): T[] { return this.list; }\n}\nconst s = new Storage<{ id: number; name: string }>();\ns.add({ id: 1, name: 'Книга' });\nconsole.log(s.getAll().length);",
        expected_example="1\n",
        idea="Дженерик с ограничением (generic constraint) сочетает гибкость универсального кода со строгой гарантией наличия нужных полей.",
        steps=[
            "T extends { id: number } требует обязательного наличия id.",
            "Метод findById(id) может безопасно сравнивать item.id === id.",
            "Хранилище работает одинаково надёжно и с товарами, и с пользователями."
        ],
        experiment="Добавьте в Storage метод findById(id: number): T | undefined.",
        terms=[
            {"term": "generic constraint (extends)", "meaning": "Ограничение на дженерик, требующее наличия определённых свойств у типа T."},
            {"term": "Repository", "meaning": "Паттерн проектирования, инкапсулирующий логику доступа к данным и коллекциям."}
        ],
        task="Создайте класс InMemoryRepo<T extends { id: number }>. Реализуйте методы:\n- add(item: T): void — добавляет элемент в приватный массив;\n- getById(id: number): T | undefined — находит элемент по id;\n- count(): number — возвращает количество элементов.\n\nПротестируйте: создайте repo для сущности { id: number; title: string }, добавьте { id: 1, title: 'Урок 1' } и { id: 2, title: 'Урок 2' }. Выведите count() и найденный title для id = 2 через пробел (2 Урок 2).",
        starter="class InMemoryRepo<T extends { id: number }> {\n  // Реализуйте приватный массив items и методы add, getById, count\n}\n\n// Протестируйте хранилище\n",
        solution="class InMemoryRepo<T extends { id: number }> {\n  private items: T[] = [];\n  public add(item: T): void {\n    this.items.push(item);\n  }\n  public getById(id: number): T | undefined {\n    return this.items.find(x => x.id === id);\n  }\n  public count(): number {\n    return this.items.length;\n  }\n}\n\nconst repo = new InMemoryRepo<{ id: number; title: string }>();\nrepo.add({ id: 1, title: 'Урок 1' });\nrepo.add({ id: 2, title: 'Урок 2' });\nconst item = repo.getById(2);\nconsole.log(`${repo.count()} ${item ? item.title : ''}`);",
        tests=[
            {"id": "t1", "label": "Подсчёт и поиск", "expected": "2 Урок 2"},
            {"id": "t2", "label": "Проверка структуры класса", "expression": "(() => { const r = new InMemoryRepo<{ id: number }>(); r.add({ id: 5 }); return r.getById(5)?.id; })()", "expected": 5}
        ],
        analogy="Представьте картотечный шкаф с ящиками: на каждом ящике обязательно выбит инвентарный номер (id: number). Библиотекарь может мгновенно найти любую карточку по её номеру.",
        challenge="Добавьте метод removeById(id: number): boolean.",
        task_steps=["Объявите class InMemoryRepo<T extends { id: number }>", "Реализуйте приватный массив и методы add, getById, count", "Проверьте добавление и поиск элемента с id=2"],
        checklist=["Класс параметризован с ограничением extends { id: number }", "Методы типизированы", "Вывод точно равен '2 Урок 2'"],
        common_mistakes="Не забывайте ключевое слово this при обращении к this.items внутри методов класса."
    )

    return lessons

if __name__ == "__main__":
    items = get_ts_lessons()
    print(f"TypeScript lessons authored: {len(items)}")
