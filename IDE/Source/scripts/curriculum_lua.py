# -*- coding: utf-8 -*-
"""Lua 18-lesson complete curriculum with 8-point pedagogical standard."""

LUA_LESSONS = [
    {
        "id": "lua-first-print",
        "language": "lua",
        "title": "Первая программа на Lua и вывод данных",
        "topic": "Основы языка",
        "section": "Введение в Lua",
        "order": 1,
        "level": "Начальный",
        "minutes": 10,
        "theory": "Lua — это компактный, высокопроизводительный встраиваемый язык программирования, разработанный в 1993 году в Папском католическом университете Рио-де-Жанейро. Он широко используется в игровой индустрии (Roblox, World of Warcraft, Baldur's Gate), в сетевых серверах (Nginx, OpenResty, Redis) и встраиваемых системах.\n\nОсновная функция для вывода данных на экран — `print(...)`. Она принимает произвольное количество аргументов любого типа, преобразует их в строки и выводит в консоль через знак табуляции, завершая вывод переводом строки.\n\nКомментарии в Lua начинаются с двух дефисов `--`. Многострочные комментарии оформляются блоком `--[[ ... ]]`.\n\nВ отличие от многих языков, в Lua точка с запятой `;` в конце инструкций необязательна и ставится только при объединении нескольких инструкций на одной строке.",
        "syntax": "print(\"Текст для вывода\")\n-- Однострочный комментарий\n--[[ Многострочный комментарий ]]",
        "examples": [
            "print(\"Привет, мир!\")\nprint(\"Один\", \"Два\", 3)"
        ],
        "task": "Напишите программу на Lua, которая выводит в консоль строку 'Hello, Lua!'.",
        "starterCode": "-- Выведите строку Hello, Lua!\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вывод строки Hello, Lua!",
                "expected": "Hello, Lua!"
            }
        ],
        "hints": [
            "Используйте стандартную функцию вывода print().",
            "Передайте строку в круглых скобках: print(\"...\").",
            "Напишите: print(\"Hello, Lua!\")"
        ],
        "commonMistakes": "Опечатка в названии функции (Print с заглавной буквы вызовет nil value, так как Lua чувствителен к регистру); пропуск кавычек вокруг строки.",
        "solutionExplanation": "Функция print отправляет переданный строковый литерал в стандартный поток вывода stdout.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["print", "комментарии", "синтаксис"],
        "walkthrough": [
            "Вызовите функцию print.",
            "В качестве аргумента передайте строку \"Hello, Lua!\".",
            "Запустите код и проверьте вывод."
        ],
        "prerequisites": [],
        "resources": [{"title": "Официальная документация Lua 5.3", "url": "https://www.lua.org/manual/5.3/", "language": "EN"}],
        "lifeExample": "Как приветствие в начале разговора: print отправляет первое сообщение от вашей программы наружу.",
        "guide": {
            "version": 1,
            "idea": "Познакомиться со средой исполнения Lua и функцией вывода print.",
            "steps": ["Написать вызов print(\"Hello, Lua!\")."],
            "solution": "print(\"Hello, Lua!\")"
        }
    },
    {
        "id": "lua-variables-types",
        "language": "lua",
        "title": "Переменные и динамическая типизация",
        "topic": "Основы языка",
        "section": "Введение в Lua",
        "order": 2,
        "level": "Начальный",
        "minutes": 12,
        "theory": "Lua — язык с динамической типизацией. Переменные не имеют фиксированного типа; тип имеет само значение, хранящееся в переменной.\n\nВ Lua существует 8 основных базовых типов данных:\n1. `nil` — отсутствие значения или неопределенность.\n2. `boolean` — логические значения `true` и `false`.\n3. `number` — числа (в Lua 5.3 поддерживаются как 64-битные целые integer, так и вещественные float).\n4. `string` — неизменяемые последовательности байт/символов.\n5. `table` — единственный составной тип данных (массивы, словари, объекты).\n6. `function` — функции (являются значениями первого класса).\n7. `thread` — сопрограммы (корутины).\n8. `userdata` — C-структуры данных, передаваемые из хост-программы.\n\nПо умолчанию переменные в Lua являются глобальными. Для объявления локальной переменной используется ключевое слово `local`. Всегда рекомендуется объявлять переменные с `local` для инкапсуляции и максимальной скорости доступа.",
        "syntax": "local name = \"Алиса\"\nlocal age = 25\nlocal is_online = true\nlocal nothing = nil\nprint(type(name)) -- вернет \"string\"",
        "examples": [
            "local x = 10\nprint(x, type(x))\nx = \"текст\"\nprint(x, type(x))"
        ],
        "task": "Объявите локальную переменную level со значением 42 и локальную переменную hero со значением 'Warrior'. Выведите их на экран через запятую и пробел: 'Warrior, уровень: 42'.",
        "starterCode": "-- Объявите переменные level и hero и выведите сообщение\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вывод характеристик героя",
                "expected": "Warrior, уровень: 42"
            }
        ],
        "hints": [
            "Объявите переменные: local level = 42 и local hero = \"Warrior\".",
            "Для склеивания строк в Lua используется оператор .. (две точки).",
            "Напишите: print(hero .. \", уровень: \" .. level)"
        ],
        "commonMistakes": "Использование оператора + для конкатенации строк (в Lua + пытается преобразовать операнды в числа; для строк используется ..).",
        "solutionExplanation": "Оператор .. объединяет строку hero, текстовый разделитель и число level в итоговую строку.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["local", "type", "конкатенация", "переменные"],
        "walkthrough": [
            "Объявите локальные переменные с помощью ключевого слова local.",
            "Сконструируйте строку с помощью оператора ..",
            "Выведите результат с помощью print."
        ],
        "prerequisites": ["lua-first-print"],
        "resources": [{"title": "Типы данных в Lua", "url": "https://www.lua.org/pil/2.html", "language": "EN"}],
        "lifeExample": "Как ярлыки на коробках: переменная — это ярлык, а внутри может лежать число, текст или список вещей.",
        "guide": {
            "version": 1,
            "idea": "Понять динамическую типизацию и использование локальных переменных.",
            "steps": ["Создать local hero и local level.", "Сконкатенировать через .. и вывести."],
            "solution": "local hero = \"Warrior\"\nlocal level = 42\nprint(hero .. \", уровень: \" .. level)"
        }
    },
    {
        "id": "lua-arithmetic-logic",
        "language": "lua",
        "title": "Арифметика и логические операторы",
        "topic": "Основы языка",
        "section": "Операторы",
        "order": 3,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Lua предоставляет полный набор арифметических операторов:\n- Сложение `+`, вычитание `-`, умножение `*`\n- Вещественное деление `/` (всегда дает float)\n- Целочисленное деление `//` (деление нацело с округлением вниз)\n- Остаток от деления `%`\n- Возведение в степень `^`\n\nОператоры сравнения: `==`, `~=` (не равно!), `<`, `>`, `<=`, `>=`.\nОбратите внимание: оператор «не равно» в Lua пишется как `~=`, а не `!=`!\n\nЛогические операторы: `and`, `or`, `not`.\nВ Lua действуют правила короткого замыкания (short-circuit evaluation):\n- `a and b` возвращает `a`, если `a` ложно; иначе возвращает `b`.\n- `a or b` возвращает `a`, если `a` истинно; иначе возвращает `b`.\n\nКРИТИЧЕСКИ ВАЖНО: В Lua ложными (`false`) считаются ТОЛЬКО `false` и `nil`! Число `0` и пустая строка `\"\"` в Lua являются ИСТИННЫМИ (truthy) значениями!",
        "syntax": "local a = 10 // 3   -- 3\nlocal b = 2 ^ 3      -- 8.0\nlocal c = (x ~= 5)   -- сравнение на неравенство\nlocal res = x or \"default\" -- тернарная идиома",
        "examples": [
            "local hp = 100\nlocal damage = 25\nlocal is_alive = (hp - damage) > 0\nprint(is_alive) -- true"
        ],
        "task": "Даны переменные a = 17 и b = 5. Вычислите и выведите в одной строке: результат целочисленного деления (a // b), остаток от деления (a % b) и результат возведения в степень (b ^ 2). Разделите их пробелом.",
        "starterCode": "local a = 17\nlocal b = 5\n-- Вычислите div, rem, pwr и выведите их\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка арифметических операций",
                "expected": "3 2 25"
            }
        ],
        "hints": [
            "Используйте a // b для целочисленного деления.",
            "Используйте a % b для остатка и b ^ 2 для квадрата.",
            "Для вывода в строку с пробелами соедините: div .. \" \" .. rem .. \" \" .. pwr."
        ],
        "commonMistakes": "Использование != вместо ~=; попытка использовать ** вместо ^ для степени.",
        "solutionExplanation": "17 // 5 = 3, 17 % 5 = 2, 5 ^ 2 = 25. Оператор .. преобразует числа в строку с пробелами.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["//", "%", "^", "~=", "and", "or"],
        "walkthrough": [
            "Вычислите div = a // b.",
            "Вычислите rem = a % b.",
            "Вычислите pwr = math.floor(b ^ 2).",
            "Выведите print(div .. \" \" .. rem .. \" \" .. pwr)."
        ],
        "prerequisites": ["lua-variables-types"],
        "resources": [{"title": "Выражения и операторы в Lua", "url": "https://www.lua.org/pil/3.html", "language": "EN"}],
        "lifeExample": "Сдача монет: целочисленное деление определяет количество купюр, а остаток — оставшиеся копейки.",
        "guide": {
            "version": 1,
            "idea": "Освоить операторы //, %, ^ и вывод.",
            "steps": ["Вычислить три значения.", "Вывести через пробел."],
            "solution": "local a = 17\nlocal b = 5\nlocal d = a // b\nlocal m = a % b\nlocal p = math.floor(b ^ 2)\nprint(d .. \" \" .. m .. \" \" .. p)"
        }
    },
    {
        "id": "lua-strings",
        "language": "lua",
        "title": "Строки и строковые функции",
        "topic": "Основы языка",
        "section": "Типы данных",
        "order": 4,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Строки в Lua неизменяемы (immutable). Оператор длины `#` перед строкой возвращает ее длину в байтах: `#\"hello\"` вернет `5`.\n\nСтандартная библиотека `string` предоставляет богатый набор функций:\n- `string.upper(s)` / `string.lower(s)` — изменение регистра\n- `string.len(s)` — длина строки\n- `string.sub(s, i, j)` — извлечение подстроки с индекса `i` по `j` (индексация с 1, отрицательные индексы отсчитываются с конца!)\n- `string.format(fmt, ...)` — форматирование по аналогии с printf\n- `string.rep(s, n)` — повторение строки `n` раз\n\nСинтаксический сахар: к строке можно применять методы через двоеточие: `s:upper()` эквивалентно `string.upper(s)`.",
        "syntax": "local s = \"DevForge\"\nprint(#s)               -- 8\nprint(s:upper())        -- DEVFORGE\nprint(s:sub(1, 3))      -- Dev\nprint(string.format(\"Score: %04d\", 42)) -- Score: 0042",
        "examples": [
            "local name = \"lua programmer\"\nprint(name:upper())\nprint(name:sub(-10)) -- programmer"
        ],
        "task": "Дана строка msg = 'welcome to lua'. С помощью строковых методов преобразуйте её в верхний регистр и выведите в формате: 'Длина: [длина], Текст: [ТЕКСТ В ВЕРХНЕМ РЕГИСТРЕ]'.",
        "starterCode": "local msg = \"welcome to lua\"\n-- Преобразуйте строку и выведите требуемый текст\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка форматирования строки",
                "expected": "Длина: 14, Текст: WELCOME TO LUA"
            }
        ],
        "hints": [
            "Длина строки вычисляется через #msg.",
            "Верхний регистр получается через msg:upper().",
            "Сформируйте строку: string.format(\"Длина: %d, Текст: %s\", #msg, msg:upper())"
        ],
        "commonMistakes": "Попытка изменить символ по индексу msg[1] = 'W' (в Lua строки неизменяемы; используйте string.sub или string.format).",
        "solutionExplanation": "Метод :upper() возвращает новую строку в верхнем регистре, а #msg дает точное число символов.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["string.upper", "string.sub", "string.format", "#"],
        "walkthrough": [
            "Получите длину через #msg.",
            "Преобразуйте строку через msg:upper().",
            "Выведите результат через string.format или конкатенацию."
        ],
        "prerequisites": ["lua-variables-types"],
        "resources": [{"title": "Строки в Lua", "url": "https://www.lua.org/pil/2.4.html", "language": "EN"}],
        "lifeExample": "Штамп на конверте: вы берете готовый текст, переводите в заглавные буквы и измеряете размер поля.",
        "guide": {
            "version": 1,
            "idea": "Научиться работать со строковыми методами и форматированием в Lua.",
            "steps": ["Использовать # и :upper().", "Сформировать нужный формат."],
            "solution": "local msg = \"welcome to lua\"\nprint(string.format(\"Длина: %d, Текст: %s\", #msg, msg:upper()))"
        }
    },
    {
        "id": "lua-conditionals",
        "language": "lua",
        "title": "Условные конструкции if-then-else",
        "topic": "Управление потоком",
        "section": "Условия и ветвления",
        "order": 5,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Условная конструкция в Lua имеет следующий синтаксис:\n```lua\nif условие then\n    -- код, если условие истинно\nelseif другое_условие then\n    -- код, если другое_условие истинно\nelse\n    -- код во всех остальных случаях\nend\n```\nОбратите внимание:\n- Ключевое слово `then` обязательно после каждого условия.\n- Конструкция всегда завершается словом `end`.\n- `elseif` пишется слитно в одно слово.\n- Круглые скобки вокруг условия необязательны.\n\nПомните: значение `0` в Lua — это `true`! Поэтому проверка `if x then` сработает, даже если `x == 0`. Проверяйте явно: `if x ~= 0 then`.",
        "syntax": "if score >= 90 then\n    grade = \"A\"\nelseif score >= 75 then\n    grade = \"B\"\nelse\n    grade = \"C\"\nend",
        "examples": [
            "local mana = 20\nif mana >= 30 then\n    print(\"Кастуем фаербол\")\nelse\n    print(\"Недостаточно маны\")\nend"
        ],
        "task": "Дана переменная health = 45. Напишите проверку:\n- если health > 70, вывести 'Отличное состояние'\n- если health >= 30 и health <= 70, вывести 'Ранен'\n- если health < 30, вывести 'Критическое состояние'",
        "starterCode": "local health = 45\n-- Напишите проверку с if-elseif-else\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка диапазона здоровья",
                "expected": "Ранен"
            }
        ],
        "hints": [
            "Используйте конструкцию if health > 70 then ... elseif health >= 30 then ... else ... end.",
            "Порядок условий важен: сначала проверьте больше 70, затем больше или равно 30.",
            "Завершите блок ключевым словом end."
        ],
        "commonMistakes": "Написание else if раздельно вместо elseif; пропуск ключевого слова then или end.",
        "solutionExplanation": "При health = 45 первое условие ложно, второе условие health >= 30 истинно, поэтому выводится 'Ранен'.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["if", "then", "elseif", "else", "end"],
        "walkthrough": [
            "Напишите if health > 70 then print('Отличное состояние').",
            "Добавьте elseif health >= 30 then print('Ранен').",
            "Добавьте else print('Критическое состояние').",
            "Закройте блок с end."
        ],
        "prerequisites": ["lua-arithmetic-logic"],
        "resources": [{"title": "Управляющие конструкции Lua", "url": "https://www.lua.org/pil/4.3.html", "language": "EN"}],
        "lifeExample": "Светофор: зеленый — едем, желтый — готовимся, красный — стоим.",
        "guide": {
            "version": 1,
            "idea": "Освоить ветвление с if-elseif-else-end.",
            "steps": ["Написать ветвления по диапазонам health.", "Вывести соответствующее сообщение."],
            "solution": "local health = 45\nif health > 70 then\n    print(\"Отличное состояние\")\nelseif health >= 30 then\n    print(\"Ранен\")\nelse\n    print(\"Критическое состояние\")\nend"
        }
    },
    {
        "id": "lua-loops-while",
        "language": "lua",
        "title": "Циклы while и repeat-until",
        "topic": "Управление потоком",
        "section": "Циклы",
        "order": 6,
        "level": "Начальный",
        "minutes": 15,
        "theory": "В Lua есть два цикла с условием:\n\n1. `while условие do ... end` — цикл с предусловием. Тело выполняется, пока условие истинно.\n2. `repeat ... until условие` — цикл с постусловием. Тело выполняется как минимум один раз, и цикл продолжается ДО ТЕХ ПОР, ПОКА условие НЕ станет истинным (то есть пока оно false!).\n\nИнструкция `break` позволяет досрочно прервать выполнение любого цикла.",
        "syntax": "local i = 1\nwhile i <= 5 do\n    print(i)\n    i = i + 1\nend\n\nrepeat\n    i = i - 1\nuntil i == 0",
        "examples": [
            "local n = 8\nwhile n > 0 do\n    n = n // 2\nend"
        ],
        "task": "Используя цикл while, найдите сумму всех четных чисел от 1 до 20 включительно (2 + 4 + ... + 20) и выведите полученную сумму: 'Сумма: [число]'.",
        "starterCode": "local sum = 0\nlocal i = 1\n-- Напишите цикл while для суммирования четных чисел\n",
        "tests": [
            {
                "id": "t1",
                "label": "Сумма четных чисел от 1 до 20",
                "expected": "Сумма: 110"
            }
        ],
        "hints": [
            "В цикле while i <= 20 проверяйте i % 2 == 0.",
            "Если число четное, прибавляйте его к sum: sum = sum + i.",
            "Не забывайте увеличивать счетчик: i = i + 1 на каждой итерации."
        ],
        "commonMistakes": "Забыть увеличить i = i + 1, что приведет к бесконечному циклу; неверная верхняя граница (i < 20 вместо i <= 20).",
        "solutionExplanation": "Сумма четных чисел от 2 до 20 равна 2 + 4 + 6 + 8 + 10 + 12 + 14 + 16 + 18 + 20 = 110.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["while", "repeat", "until", "break"],
        "walkthrough": [
            "Запустите цикл while i <= 20 do.",
            "Внутри проверяйте if i % 2 == 0 then sum = sum + i end.",
            "Увеличивайте i = i + 1.",
            "После цикла выведите print('Сумма: ' .. sum)."
        ],
        "prerequisites": ["lua-conditionals"],
        "resources": [{"title": "Циклы в Lua", "url": "https://www.lua.org/pil/4.3.html", "language": "EN"}],
        "lifeExample": "Счетчик шагов: пока вы не дошли до цели (20 шагов), каждый второй шаг прибавляет очки.",
        "guide": {
            "version": 1,
            "idea": "Научиться использовать цикл while для накопления суммы с шагом.",
            "steps": ["Написать цикл while i <= 20.", "Складывать четные числа.", "Вывести сумму."],
            "solution": "local sum = 0\nlocal i = 1\nwhile i <= 20 do\n    if i % 2 == 0 then\n        sum = sum + i\n    end\n    i = i + 1\nend\nprint(\"Сумма: \" .. sum)"
        }
    },
    {
        "id": "lua-loops-for",
        "language": "lua",
        "title": "Числовой цикл for",
        "topic": "Управление потоком",
        "section": "Циклы",
        "order": 7,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Числовой цикл `for` в Lua имеет вид:\n```lua\nfor var = start, stop, step do\n    -- тело цикла\nend\n```\nПараметр `step` (шаг) необязателен и по умолчанию равен `1`.\nЕсли `step` отрицательный, цикл идет в обратном направлении (убывание).\n\nВажные свойства числового `for` в Lua:\n1. Переменная цикла `var` автоматически является локальной для тела цикла.\n2. Границы цикла вычисляются один раз перед началом выполнения.\n3. Изменять переменную цикла внутри тела категорически не рекомендуется.",
        "syntax": "for i = 1, 5 do\n    print(i)\nend\n\nfor i = 10, 2, -2 do\n    print(i) -- 10, 8, 6, 4, 2\nend",
        "examples": [
            "for i = 1, 3 do\n    print(\"Раунд \" .. i)\nend"
        ],
        "task": "Используя числовой цикл for с отрицательным шагом, выведите обратный отсчет от 5 до 1, а после цикла выведите 'Старт!'. Каждое число и слово 'Старт!' должны быть на новой строке.",
        "starterCode": "-- Реализуйте обратный отсчет от 5 до 1 и вывод Старт!\n",
        "tests": [
            {
                "id": "t1",
                "label": "Обратный отсчет",
                "expected": "5\n4\n3\n2\n1\nСтарт!"
            }
        ],
        "hints": [
            "Используйте for i = 5, 1, -1 do.",
            "Внутри цикла вызывайте print(i).",
            "После завершения цикла (после слова end) вызовите print('Старт!')."
        ],
        "commonMistakes": "Пропуск шага -1 (цикл for i = 5, 1 do не выполнится ни разу, так как шаг по умолчанию +1).",
        "solutionExplanation": "При шаге -1 цикл последовательно принимает значения 5, 4, 3, 2, 1, а после выхода выводится 'Старт!'.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["for", "step", "обратный отсчет"],
        "walkthrough": [
            "Напишите for i = 5, 1, -1 do print(i) end.",
            "Добавьте print('Старт!') после end.",
            "Проверьте вывод."
        ],
        "prerequisites": ["lua-loops-while"],
        "resources": [{"title": "Числовой for в Lua", "url": "https://www.lua.org/pil/4.3.4.html", "language": "EN"}],
        "lifeExample": "Обратный отсчет перед запуском космической ракеты: 5, 4, 3, 2, 1, Поехали!",
        "guide": {
            "version": 1,
            "idea": "Освоить числовой цикл for с отрицательным шагом.",
            "steps": ["Написать for i = 5, 1, -1.", "Вывести каждое число.", "Вывести Старт!"],
            "solution": "for i = 5, 1, -1 do\n    print(i)\nend\nprint(\"Старт!\")"
        }
    },
    {
        "id": "lua-functions-basic",
        "language": "lua",
        "title": "Функции и множественные возвращаемые значения",
        "topic": "Функции",
        "section": "Функции",
        "order": 8,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Функции в Lua объявляются ключевым словом `function` и завершаются `end`.\n\nУникальная особенность Lua — встроенная поддержка множественных возвращаемых значений через запятую: `return x, y`.\n\nЕсли функция возвращает несколько значений, их можно сразу присвоить нескольким переменным:\n`local min_val, max_val = find_min_max(a, b)`.\n\nФункции в Lua — значения первого класса (first-class citizens). Это значит, что функция может храниться в переменной, передаваться как аргумент другой функции или возвращаться из нее.",
        "syntax": "local function add(a, b)\n    return a + b\nend\n\nlocal function divide_rem(a, b)\n    return a // b, a % b\nend\nlocal q, r = divide_rem(10, 3)",
        "examples": [
            "local function square(x)\n    return x * x\nend\nprint(square(6)) -- 36"
        ],
        "task": "Напишите функцию calc_rectangle(w, h), которая принимает ширину и высоту прямоугольника и возвращает два значения: его площадь (w * h) и его периметр (2 * (w + h)). Вызовите функцию для w = 5, h = 8 и выведите результат: 'Площадь: [площадь], Периметр: [периметр]'.",
        "starterCode": "-- Определите функцию calc_rectangle и вызовите её\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вычисление площади и периметра",
                "expected": "Площадь: 40, Периметр: 26"
            }
        ],
        "hints": [
            "Объявите local function calc_rectangle(w, h).",
            "Верните два значения: return w * h, 2 * (w + h).",
            "Примите результат: local area, perimeter = calc_rectangle(5, 8) и выведите."
        ],
        "commonMistakes": "Возврат таблицы return {w*h, 2*(w+h)} вместо возврата двух значений через запятую return a, p.",
        "solutionExplanation": "Lua помещает оба возвращенных значения на стек виртуальной машины, присваивая их переменным area и perimeter.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["function", "return", "множественный возврат"],
        "walkthrough": [
            "Создайте local function calc_rectangle(w, h).",
            "Верните return w * h, 2 * (w + h).",
            "Вызовите функцию и выведите строку с площадью и периметром."
        ],
        "prerequisites": ["lua-loops-for"],
        "resources": [{"title": "Функции в Lua", "url": "https://www.lua.org/pil/5.html", "language": "EN"}],
        "lifeExample": "Банкомат при выдаче наличных возвращает сразу два значения: запрошенную сумму купюрами и квитанцию с остатком на счете.",
        "guide": {
            "version": 1,
            "idea": "Научиться объявлять функции с множественным возвратом значений.",
            "steps": ["Написать calc_rectangle(w, h).", "Вернуть площадь и периметр.", "Вывести результат."],
            "solution": "local function calc_rectangle(w, h)\n    return w * h, 2 * (w + h)\nend\nlocal area, perimeter = calc_rectangle(5, 8)\nprint(string.format(\"Площадь: %d, Периметр: %d\", area, perimeter))"
        }
    },
    {
        "id": "lua-closures",
        "language": "lua",
        "title": "Замыкания и лексическая область видимости",
        "topic": "Функции",
        "section": "Продвинутые функции",
        "order": 9,
        "level": "Средний",
        "minutes": 18,
        "theory": "Замыкание (closure) — это функция вместе с окружением, в котором она была создана. В Lua любая функция имеет доступ к локальным переменным внешней функции, даже после того, как внешняя функция завершила работу!\n\nТакие внешние локальные переменные в Lua называются upvalues (внешние локальные переменные).\n\nЗамыкания позволяют создавать:\n- Фабрики функций с предустановленными параметрами\n- Приватные счетчики и генераторы уникальных ID\n- Инкапсуляцию данных без использования громоздких классов",
        "syntax": "local function make_counter(start)\n    local count = start\n    return function()\n        count = count + 1\n        return count\n    end\nend\nlocal c1 = make_counter(0)\nprint(c1()) -- 1\nprint(c1()) -- 2",
        "examples": [
            "local function multiplier(factor)\n    return function(x) return x * factor end\nend\nlocal double = multiplier(2)\nprint(double(10)) -- 20"
        ],
        "task": "Создайте функцию-генератор make_accumulator(initial), которая хранит текущую сумму (начиная с initial) и возвращает функцию. Возвращаемая функция принимает число amount, прибавляет его к сумме и возвращает новую накопленную сумму. Проверьте работу: создайте acc = make_accumulator(10), вызовите acc(5), затем acc(20) и выведите последнее значение: 'Итог: [сумма]'.",
        "starterCode": "-- Реализуйте make_accumulator и продемонстрируйте замыкание\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка замыкания-аккумулятора",
                "expected": "Итог: 35"
            }
        ],
        "hints": [
            "Внутри make_accumulator объявите local total = initial.",
            "Верните анонимную функцию function(amount) total = total + amount; return total end.",
            "Вызовите acc(5), затем local res = acc(20) и напечатайте 'Итог: ' .. res."
        ],
        "commonMistakes": "Объявление total глобальной переменной (тогда разные аккумуляторы будут перезаписывать общее состояние).",
        "solutionExplanation": "Переменная total захватывается возвращаемой функцией как upvalue, сохраняя состояние между вызовами.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["замыкания", "closures", "upvalues", "инкапсуляция"],
        "walkthrough": [
            "Создайте make_accumulator(initial).",
            "Инкапсулируйте local total = initial.",
            "Верните функцию, прибавляющую amount к total.",
            "Проверьте работу и выведите 'Итог: 35'."
        ],
        "prerequisites": ["lua-functions-basic"],
        "resources": [{"title": "Замыкания в Lua", "url": "https://www.lua.org/pil/6.1.html", "language": "EN"}],
        "lifeExample": "Копилка с монетами: фабрика создает копилку с начальной суммой, и каждая брошенная монета увеличивает внутренний баланс.",
        "guide": {
            "version": 1,
            "idea": "Понять механизм upvalues и создание замыканий.",
            "steps": ["Написать функцию высшего порядка make_accumulator.", "Проверить сохранение внутреннего состояния."],
            "solution": "local function make_accumulator(initial)\n    local total = initial\n    return function(amount)\n        total = total + amount\n        return total\n    end\nend\nlocal acc = make_accumulator(10)\nacc(5)\nlocal res = acc(20)\nprint(\"Итог: \" .. res)"
        }
    },
    {
        "id": "lua-tables-arrays",
        "language": "lua",
        "title": "Таблицы как массивы и модуль table",
        "topic": "Структуры данных",
        "section": "Таблицы",
        "order": 10,
        "level": "Средний",
        "minutes": 18,
        "theory": "Таблица (`table`) — это единственный и фундаментальный составной тип данных в Lua. Все остальные структуры (массивы, списки, множества, хеш-таблицы, деревья, классы) реализуются на базе таблиц.\n\nКогда таблица используется как массив:\n1. Индексация начинается с 1 (единицы!), а не с 0.\n2. Длина массива получается с помощью оператора `#`: `#arr`.\n3. Модуль `table` предоставляет полезные функции:\n   - `table.insert(t, [pos,] val)` — вставка элемента\n   - `table.remove(t, [pos])` — удаление элемента\n   - `table.sort(t [, comp])` — сортировка на месте\n   - `table.concat(t, sep)` — склеивание элементов в строку\n4. Для перебора массива используется функция `ipairs(t)`.",
        "syntax": "local fruits = {\"яблоко\", \"банан\", \"груша\"}\ntable.insert(fruits, \"апельсин\")\nprint(#fruits) -- 4\nfor index, value in ipairs(fruits) do\n    print(index, value)\nend",
        "examples": [
            "local nums = {5, 2, 8, 1}\ntable.sort(nums)\nprint(table.concat(nums, \", \")) -- 1, 2, 5, 8"
        ],
        "task": "Дан массив scores = {10, 45, 20, 80, 30}. Добавьте в конец массива число 50 с помощью table.insert, отсортируйте массив по возрастанию с помощью table.sort и выведите отсортированные элементы через дефис с пробелами: '10 - 20 - 30 - 45 - 50 - 80'.",
        "starterCode": "local scores = {10, 45, 20, 80, 30}\n-- Добавьте 50, отсортируйте и выведите через table.concat\n",
        "tests": [
            {
                "id": "t1",
                "label": "Сортировка и объединение массива",
                "expected": "10 - 20 - 30 - 45 - 50 - 80"
            }
        ],
        "hints": [
            "Используйте table.insert(scores, 50).",
            "Отсортируйте массив: table.sort(scores).",
            "Выведите результат: print(table.concat(scores, \" - \"))."
        ],
        "commonMistakes": "Индексация с 0 (scores[0] в Lua не учитывается оператором длины #); использование print(scores) напрямую (выведет адрес таблицы table: 0x... вместо содержимого).",
        "solutionExplanation": "table.insert помещает 50 в конец, table.sort упорядочивает по возрастанию, а table.concat соединяет элементы разделителем.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["table", "ipairs", "table.insert", "table.sort", "table.concat"],
        "walkthrough": [
            "Вызовите table.insert(scores, 50).",
            "Вызовите table.sort(scores).",
            "Вызовите print(table.concat(scores, ' - '))."
        ],
        "prerequisites": ["lua-functions-basic"],
        "resources": [{"title": "Массивы в Lua", "url": "https://www.lua.org/pil/11.1.html", "language": "EN"}],
        "lifeExample": "Список покупок на холодильнике: пункты пронумерованы с 1, можно дописать новый в конец или вычеркнуть купленный.",
        "guide": {
            "version": 1,
            "idea": "Освоить базовые операции с массивами в Lua через модуль table.",
            "steps": ["Вставить элемент.", "Отсортировать.", "Склеить через table.concat."],
            "solution": "local scores = {10, 45, 20, 80, 30}\ntable.insert(scores, 50)\ntable.sort(scores)\nprint(table.concat(scores, \" - \"))"
        }
    },
    {
        "id": "lua-tables-dicts",
        "language": "lua",
        "title": "Таблицы как словари и итератор pairs",
        "topic": "Структуры данных",
        "section": "Таблицы",
        "order": 11,
        "level": "Средний",
        "minutes": 18,
        "theory": "Таблица в Lua может связывать ключи любого типа (кроме `nil`) с любыми значениями. Это ассоциативный массив (словарь, хеш-таблица, Map).\n\nЗапись и чтение по ключу:\n- Точечная нотация: `hero.name = \"Артур\"` (работает, если ключ — валидный идентификатор)\n- Скобочная нотация: `hero[\"hp\"] = 100` или `hero[variable] = val`\n\nДля перебора ВСЕХ пар ключ-значение используется итератор `pairs(t)`:\n```lua\nfor key, value in pairs(hero) do\n    print(key, value)\nend\n```\nРазница между `ipairs` и `pairs`:\n- `ipairs`: перебирает только непрерывную числовую последовательность с 1 до первого nil.\n- `pairs`: перебирает абсолютно все ключи таблицы в произвольном порядке хеш-таблицы.",
        "syntax": "local player = {\n    name = \"Hero\",\n    level = 5,\n    gold = 150\n}\nplayer.hp = 100\nprint(player.name, player[\"gold\"])",
        "examples": [
            "local inventory = { potion = 3, sword = 1 }\nfor item, count in pairs(inventory) do\n    print(item, count)\nend"
        ],
        "task": "Создайте словарь цен товаров prices = { apple = 50, bread = 40, milk = 80 }. Найдите общую стоимость корзины cart = { apple = 2, bread = 1, milk = 3 } (количество товара * цену из словаря prices) и выведите: 'Итоговая стоимость: [сумма]'.",
        "starterCode": "local prices = { apple = 50, bread = 40, milk = 80 }\nlocal cart = { apple = 2, bread = 1, milk = 3 }\n-- Рассчитайте сумму и выведите результат\n",
        "tests": [
            {
                "id": "t1",
                "label": "Расчет стоимости корзины",
                "expected": "Итоговая стоимость: 380"
            }
        ],
        "hints": [
            "Заведите local total = 0.",
            "Пройдитесь циклом for item, count in pairs(cart) do ... end.",
            "Внутри прибавляйте: total = total + count * prices[item].",
            "Выведите print('Итоговая стоимость: ' .. total)."
        ],
        "commonMistakes": "Использование ipairs для ассоциативного словаря (ipairs не увидит строковые ключи и цикл не выполнится).",
        "solutionExplanation": "2*50 + 1*40 + 3*80 = 100 + 40 + 240 = 380.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["pairs", "словари", "хеш-таблицы", "ассоциативные массивы"],
        "walkthrough": [
            "Объявите total = 0.",
            "Используйте pairs(cart) для прохода по товарам.",
            "Умножайте количество на цену prices[item].",
            "Выведите итоговую сумму."
        ],
        "prerequisites": ["lua-tables-arrays"],
        "resources": [{"title": "Таблицы как ассоциативные массивы", "url": "https://www.lua.org/pil/2.5.html", "language": "EN"}],
        "lifeExample": "Прайс-лист в магазине: каждому названию товара соответствует его стоимость, а чек суммирует покупки.",
        "guide": {
            "version": 1,
            "idea": "Научиться работать с ассоциативными таблицами и итератором pairs.",
            "steps": ["Обойти cart через pairs.", "Умножить на prices[item].", "Вывести сумму."],
            "solution": "local prices = { apple = 50, bread = 40, milk = 80 }\nlocal cart = { apple = 2, bread = 1, milk = 3 }\nlocal total = 0\nfor item, count in pairs(cart) do\n    total = total + count * prices[item]\nend\nprint(\"Итоговая стоимость: \" .. total)"
        }
    },
    {
        "id": "lua-tables-nested",
        "language": "lua",
        "title": "Вложенные таблицы и структуры данных",
        "topic": "Структуры данных",
        "section": "Таблицы",
        "order": 12,
        "level": "Средний",
        "minutes": 18,
        "theory": "Поскольку значением в таблице может быть любая другая таблица, в Lua легко строить сложные многомерные структуры: матрицы, списки объектов, графы и деревья.\n\nДвумерная матрица 3x3:\n```lua\nlocal matrix = {\n    {1, 2, 3},\n    {4, 5, 6},\n    {7, 8, 9}\n}\nprint(matrix[2][3]) -- 6 (2-я строка, 3-й столбец)\n```\n\nСписок записей (объектов):\n```lua\nlocal team = {\n    { name = \"Артур\", role = \"Воин\", level = 10 },\n    { name = \"Мерлин\", role = \"Маг\", level = 12 }\n}\nprint(team[1].name) -- Артур\n```",
        "syntax": "local grid = {}\nfor r = 1, 3 do\n    grid[r] = {}\n    for c = 1, 3 do\n        grid[r][c] = r * c\n    end\nend",
        "examples": [
            "local party = {\n    { name = \"Лучник\", hp = 80 },\n    { name = \"Танк\", hp = 200 }\n}\nprint(party[2].hp) -- 200"
        ],
        "task": "Дана вложенная таблица гильдии:\nlocal guild = {\n    { name = 'Alex', rank = 'Leader', points = 250 },\n    { name = 'Dmitry', rank = 'Member', points = 120 },\n    { name = 'Elena', rank = 'Officer', points = 180 }\n}\nНайдите участника с максимальным количеством points и выведите: 'Лучший участник: [name] ([points] очков)'.",
        "starterCode": "local guild = {\n    { name = 'Alex', rank = 'Leader', points = 250 },\n    { name = 'Dmitry', rank = 'Member', points = 120 },\n    { name = 'Elena', rank = 'Officer', points = 180 }\n}\n-- Найдите участника с максимальными points\n",
        "tests": [
            {
                "id": "t1",
                "label": "Поиск лучшего участника",
                "expected": "Лучший участник: Alex (250 очков)"
            }
        ],
        "hints": [
            "Инициализируйте local best = guild[1].",
            "Пройдитесь циклом for i = 2, #guild do ... end.",
            "Если guild[i].points > best.points, обновите best = guild[i].",
            "Выведите string.format('Лучший участник: %s (%d очков)', best.name, best.points)."
        ],
        "commonMistakes": "Обращение guild.points вместо guild[i].points (guild — это список таблиц, а не отдельный участник).",
        "solutionExplanation": "Алгоритм поиска максимума последовательно сравнивает очки каждого участника и находит запись Алекса с 250 очками.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["вложенные таблицы", "матрицы", "структуры"],
        "walkthrough": [
            "Возьмите первого участника как начального лучшего.",
            "Сравните в цикле остальных участников по полю points.",
            "Выведите имя и очки победителя."
        ],
        "prerequisites": ["lua-tables-dicts"],
        "resources": [{"title": "Вложенные таблицы в Lua", "url": "https://www.lua.org/pil/11.2.html", "language": "EN"}],
        "lifeExample": "Таблица лидеров в компьютерной игре: список игроков, где у каждого есть имя, аватар и счет.",
        "guide": {
            "version": 1,
            "idea": "Научиться обрабатывать списки структур в Lua.",
            "steps": ["Инициализировать best = guild[1].", "Сравнить в цикле.", "Вывести результат."],
            "solution": "local guild = {\n    { name = 'Alex', rank = 'Leader', points = 250 },\n    { name = 'Dmitry', rank = 'Member', points = 120 },\n    { name = 'Elena', rank = 'Officer', points = 180 }\n}\nlocal best = guild[1]\nfor i = 2, #guild do\n    if guild[i].points > best.points then\n        best = guild[i]\n    end\nend\nprint(string.format(\"Лучший участник: %s (%d очков)\", best.name, best.points))"
        }
    },
    {
        "id": "lua-metatables-basics",
        "language": "lua",
        "title": "Метатаблицы и метаметод __tostring",
        "topic": "Метапрограммирование",
        "section": "Метатаблицы",
        "order": 13,
        "level": "Средний",
        "minutes": 20,
        "theory": "Метатаблица (metatable) — это мощный механизм в Lua, позволяющий изменять поведение таблицы при выполнении различных операций (сложение, строковое представление, обращение к несуществующим полям).\n\nФункции для работы с метатаблицами:\n- `setmetatable(table, metatable)` — устанавливает метатаблицу для таблицы и возвращает саму таблицу.\n- `getmetatable(table)` — возвращает метатаблицу.\n\nПоля метатаблицы, начинающиеся с двух подчеркиваний, называются метаметодами:\n- `__tostring`: функция, определяющая, как таблица преобразуется в строку при вызове `tostring(t)` или `print(t)`.\nБез `__tostring` печать таблицы выводит шестнадцатеричный адрес вроде `table: 0x1a2b3c`. С метаметодом `__tostring` вы можете вернуть красивое пользовательское строковое представление!",
        "syntax": "local mt = {\n    __tostring = function(self)\n        return \"Пользователь: \" .. self.name\n    end\n}\nlocal user = { name = \"Иван\" }\nsetmetatable(user, mt)\nprint(user) -- Пользователь: Иван",
        "examples": [
            "local ItemMt = {\n    __tostring = function(i) return string.format(\"[%s x%d]\", i.title, i.qty) end\n}\nlocal item = setmetatable({ title = \"Зелье\", qty = 5 }, ItemMt)\nprint(item) -- [Зелье x5]"
        ],
        "task": "Создайте метатаблицу VectorMt с метаметодом __tostring, который возвращает координаты вектора в формате 'Vector(x, y)'. Создайте вектор v = { x = 3, y = 7 }, установите для него метатаблицу и выведите его через print(v).",
        "starterCode": "-- Создайте VectorMt с __tostring и выведите вектор v\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка __tostring метаметода",
                "expected": "Vector(3, 7)"
            }
        ],
        "hints": [
            "Объявите local VectorMt = { __tostring = function(v) return string.format(\"Vector(%d, %d)\", v.x, v.y) end }.",
            "Создайте local v = { x = 3, y = 7 }.",
            "Привяжите метатаблицу: setmetatable(v, VectorMt) и сделайте print(v)."
        ],
        "commonMistakes": "Опечатка в названии метаметода (_tostring с одним подчеркиванием вместо двух __tostring).",
        "solutionExplanation": "Функция print вызывает tostring() для своих аргументов, которая обращается к метаметоду __tostring метатаблицы.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["metatable", "setmetatable", "__tostring", "метаметоды"],
        "walkthrough": [
            "Создайте таблицу VectorMt с полем __tostring.",
            "Создайте таблицу v с полями x и y.",
            "Свяжите их через setmetatable(v, VectorMt).",
            "Выведите print(v)."
        ],
        "prerequisites": ["lua-tables-nested"],
        "resources": [{"title": "Метатаблицы в Lua", "url": "https://www.lua.org/pil/13.html", "language": "EN"}],
        "lifeExample": "Паспорт объекта: когда вас просят представиться (tostring), метатаблица дает точный шаблон представления.",
        "guide": {
            "version": 1,
            "idea": "Понять концепцию метатаблиц и перегрузить вывод объекта через __tostring.",
            "steps": ["Создать VectorMt с __tostring.", "Создать вектор.", "Установить метатаблицу и напечатать."],
            "solution": "local VectorMt = {\n    __tostring = function(v)\n        return string.format(\"Vector(%d, %d)\", v.x, v.y)\n    end\n}\nlocal v = setmetatable({ x = 3, y = 7 }, VectorMt)\nprint(v)"
        }
    },
    {
        "id": "lua-operator-overloading",
        "language": "lua",
        "title": "Перегрузка операторов через метаметоды",
        "topic": "Метапрограммирование",
        "section": "Метатаблицы",
        "order": 14,
        "level": "Средний",
        "minutes": 20,
        "theory": "С помощью метатаблиц в Lua можно перегружать стандартные операторы для своих структур данных:\n- `__add`: оператор сложения `+`\n- `__sub`: оператор вычитания `-`\n- `__mul`: оператор умножения `*`\n- `__div`: оператор деления `/`\n- `__concat`: оператор конкатенации `..`\n- `__eq`: оператор равенства `==`\n- `__lt`: оператор меньше `<`\n- `__le`: оператор меньше или равно `<=`\n\nКогда Lua встречает выражение `a + b`, интерпретатор проверяет, есть ли у `a` или `b` метатаблица с полем `__add`. Если есть, вызывается эта функция: `mt.__add(a, b)`.",
        "syntax": "local PointMt = {\n    __add = function(p1, p2)\n        return setmetatable({ x = p1.x + p2.x, y = p1.y + p2.y }, PointMt)\n    end,\n    __tostring = function(p) return string.format(\"(%d, %d)\", p.x, p.y) end\n}\nlocal a = setmetatable({ x = 1, y = 2 }, PointMt)\nlocal b = setmetatable({ x = 3, y = 4 }, PointMt)\nlocal c = a + b\nprint(c) -- (4, 6)",
        "examples": [
            "local MoneyMt = {\n    __add = function(m1, m2) return setmetatable({ rub = m1.rub + m2.rub }, MoneyMt) end\n}"
        ],
        "task": "Создайте метатаблицу с метаметодами __add (сложение векторов {x, y}) и __tostring ('Vector(x, y)'). Сложите два вектора v1 = {x=10, y=20} и v2 = {x=5, y=15} с помощью оператора + и выведите полученный результирующий вектор.",
        "starterCode": "-- Реализуйте перегрузку сложения векторов\n",
        "tests": [
            {
                "id": "t1",
                "label": "Сложение векторов оператором +",
                "expected": "Vector(15, 35)"
            }
        ],
        "hints": [
            "Объявите local VecMt = {}.",
            "Определите VecMt.__add = function(a, b) return setmetatable({ x = a.x + b.x, y = a.y + b.y }, VecMt) end.",
            "Определите VecMt.__tostring = function(v) return string.format('Vector(%d, %d)', v.x, v.y) end.",
            "Свяжите v1 и v2 с VecMt, вычислите v3 = v1 + v2 и напечатайте print(v3)."
        ],
        "commonMistakes": "Забыть привязать метатаблицу к возвращаемому из __add новому вектору (тогда к нему нельзя будет применить следующий + или print).",
        "solutionExplanation": "Оператор + автоматически вызывает VecMt.__add, возвращая новый вектор со сложенными координатами.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["__add", "__sub", "перегрузка операторов", "метаметоды"],
        "walkthrough": [
            "Создайте метатаблицу VecMt.",
            "Добавьте метаметоды __add и __tostring.",
            "Создайте v1 и v2 с метатаблицей VecMt.",
            "Выполните v3 = v1 + v2 и выведите результат."
        ],
        "prerequisites": ["lua-metatables-basics"],
        "resources": [{"title": "Арифметические метаметоды в Lua", "url": "https://www.lua.org/pil/13.1.html", "language": "EN"}],
        "lifeExample": "Сложение валют: вместо ручного сложения m1.rub + m2.rub вы просто пишете m1 + m2, получая новый кошелек с итоговой суммой.",
        "guide": {
            "version": 1,
            "idea": "Научиться перегружать арифметические операторы с помощью метаметода __add.",
            "steps": ["Создать VecMt с __add и __tostring.", "Сложить два вектора.", "Вывести результат."],
            "solution": "local VecMt = {}\nVecMt.__add = function(a, b)\n    return setmetatable({ x = a.x + b.x, y = a.y + b.y }, VecMt)\nend\nVecMt.__tostring = function(v)\n    return string.format(\"Vector(%d, %d)\", v.x, v.y)\nend\nlocal v1 = setmetatable({ x = 10, y = 20 }, VecMt)\nlocal v2 = setmetatable({ x = 5, y = 15 }, VecMt)\nlocal v3 = v1 + v2\nprint(v3)"
        }
    },
    {
        "id": "lua-oop-prototypes",
        "language": "lua",
        "title": "Объектно-ориентированное программирование на прототипах",
        "topic": "ООП в Lua",
        "section": "ООП",
        "order": 15,
        "level": "Продвинутый",
        "minutes": 22,
        "theory": "В Lua нет встроенного ключевого слова `class`. Вместо этого ООП строится на прототипном наследовании через ключевой метаметод `__index`.\n\nКак работает `__index`:\nКогда вы обращаетесь к полю таблицы `obj.foo`, и этого поля нет в самом `obj`, Lua смотрит в метатаблицу `obj`. Если там есть поле `__index`, поиск продолжается в таблице, на которую указывает `__index`!\n\nЕсли установить `Account.__index = Account`, то любой экземпляр `setmetatable({}, Account)` будет автоматически наследовать все методы из `Account`!\n\nСинтаксис двоеточия `:`:\n- `function Account:deposit(amount)` автоматически добавляет скрытый первый аргумент `self`.\n- Вызов `acc:deposit(100)` автоматически передает `acc` в качестве `self`.",
        "syntax": "local Hero = {}\nHero.__index = Hero\n\nfunction Hero.new(name, hp)\n    local self = setmetatable({}, Hero)\n    self.name = name\n    self.hp = hp\n    return self\nend\n\nfunction Hero:take_damage(dmg)\n    self.hp = self.hp - dmg\nend",
        "examples": [
            "local h = Hero.new(\"Воин\", 100)\nh:take_damage(30)\nprint(h.hp) -- 70"
        ],
        "task": "Создайте класс Character с конструктором new(name, hp) и методом attack(target, damage), который уменьшает target.hp на величину damage и возвращает строку '[attacker] атакует [target] на [dmg] урона!'. Создайте двух персонажей: hero ('Воин', 100) и enemy ('Орк', 80). Вызовите hero:attack(enemy, 25), выведите сообщение об атаке и на следующей строке выведите: 'Остаток HP орка: [hp]'.",
        "starterCode": "-- Создайте класс Character и проведите атаку\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка прототипного ООП и вызова метода",
                "expected": "Воин атакует Орк на 25 урона!\nОстаток HP орка: 55"
            }
        ],
        "hints": [
            "Создайте таблицу Character = {} и укажите Character.__index = Character.",
            "Напишите Character.new(name, hp): local self = setmetatable({}, Character); self.name = name; self.hp = hp; return self.",
            "Напишите метод Character:attack(target, dmg): target.hp = target.hp - dmg; return string.format('%s атакует %s на %d урона!', self.name, target.name, dmg).",
            "Создайте объекты, проведите атаку и напечатайте результаты."
        ],
        "commonMistakes": "Использование точки вместо двоеточия при вызове hero.attack(enemy, 25) (в этом случае self не передается и self.name вызовет ошибку).",
        "solutionExplanation": "Метаметод __index делегирует поиск метода attack классу Character, а синтаксис : передает hero в качестве self.",
        "xp": 80,
        "setupSql": "",
        "concepts": ["__index", "ООП", "прототипы", "self", "методы через двоеточие"],
        "walkthrough": [
            "Объявите таблицу Character и свяжите Character.__index = Character.",
            "Реализуйте конструктор Character.new.",
            "Реализуйте метод attack со скрытым параметром self.",
            "Создайте hero и enemy, проведите атаку и выведите вывод."
        ],
        "prerequisites": ["lua-operator-overloading"],
        "resources": [{"title": "Объектно-ориентированное программирование в Lua", "url": "https://www.lua.org/pil/16.html", "language": "EN"}],
        "lifeExample": "Чертеж автомобиля: класс — это чертеж с функциями завода, а каждый собранный экземпляр пользуется инструкциями из этого чертежа.",
        "guide": {
            "version": 1,
            "idea": "Освоить классический паттерн реализации классов в Lua с помощью __index.",
            "steps": ["Создать класс Character.", "Определить new и attack.", "Проверить атаку между персонажами."],
            "solution": "local Character = {}\nCharacter.__index = Character\n\nfunction Character.new(name, hp)\n    local self = setmetatable({}, Character)\n    self.name = name\n    self.hp = hp\n    return self\nend\n\nfunction Character:attack(target, damage)\n    target.hp = target.hp - damage\n    return string.format(\"%s атакует %s на %d урона!\", self.name, target.name, damage)\nend\n\nlocal hero = Character.new(\"Воин\", 100)\nlocal enemy = Character.new(\"Орк\", 80)\nlocal log_msg = hero:attack(enemy, 25)\nprint(log_msg)\nprint(\"Остаток HP орка: \" .. enemy.hp)"
        }
    },
    {
        "id": "lua-coroutines",
        "language": "lua",
        "title": "Сопрограммы (корутины) и кооперативная многозадачность",
        "topic": "Продвинутый Lua",
        "section": "Корутины",
        "order": 16,
        "level": "Продвинутый",
        "minutes": 22,
        "theory": "Корутина (сопрограмма, coroutine) — это поток выполнения с собственной локальной памятью и стеком вызовов, но в отличие от системных потоков ОС, корутины переключаются кооперативно.\n\nКорутина выполняется до тех пор, пока сама явно не приостановит свое выполнение с помощью `coroutine.yield()`. Управление возвращается коду, вызвавшему `coroutine.resume()`.\n\nОсновные функции модуля `coroutine`:\n- `coroutine.create(f)`: создает новую корутину из функции `f` и возвращает объект типа `thread`.\n- `coroutine.resume(co, ...)`: запускает или возобновляет выполнение `co`. Возвращает `true, ...` в случае успеха или `false, error_message` при ошибке.\n- `coroutine.yield(...)`: приостанавливает выполнение текущей корутины и передает аргументы наружу в `resume`.\n- `coroutine.status(co)`: возвращает статус корутины (`\"suspended\"`, `\"running\"`, `\"dead\"`).",
        "syntax": "local co = coroutine.create(function()\n    for i = 1, 3 do\n        coroutine.yield(i * 10)\n    end\nend)\n\nprint(coroutine.resume(co)) -- true, 10\nprint(coroutine.resume(co)) -- true, 20\nprint(coroutine.resume(co)) -- true, 30",
        "examples": [
            "local co = coroutine.create(function(name)\n    print(\"Привет, \" .. name)\n    coroutine.yield(\"жду\")\n    print(\"Пока!\")\nend)\ncoroutine.resume(co, \"Lua\")"
        ],
        "task": "Создайте корутину-генератор четных чисел. Корутина в цикле от 2 до 8 (шаг 2) делает coroutine.yield очередного числа. Возобновите корутину 4 раза с помощью coroutine.resume, собирая полученные значения, и выведите их через пробел: 'Четные: 2 4 6 8'.",
        "starterCode": "-- Создайте корутину и получите 4 четных числа\n",
        "tests": [
            {
                "id": "t1",
                "label": "Генерация чисел через корутины",
                "expected": "Четные: 2 4 6 8"
            }
        ],
        "hints": [
            "Создайте co = coroutine.create(function() for i = 2, 8, 2 do coroutine.yield(i) end end).",
            "В цикле 4 раза вызовите local ok, val = coroutine.resume(co) и сохраните val в массив.",
            "Склейте числа через пробел и выведите: print('Четные: ' .. table.concat(nums, ' '))."
        ],
        "commonMistakes": "Забыть, что resume возвращает первым аргументом статус успешности boolean (ok, val), а само возвращенное значение идет вторым.",
        "solutionExplanation": "Корутина приостанавливается на каждом yield, сохраняя позицию счетчика цикла for, и возобновляется при следующем resume.",
        "xp": 80,
        "setupSql": "",
        "concepts": ["coroutine.create", "coroutine.resume", "coroutine.yield", "кооперативная многозадачность"],
        "walkthrough": [
            "Объявите корутину с циклом for i = 2, 8, 2 do coroutine.yield(i) end.",
            "Соберите 4 значения через coroutine.resume.",
            "Выведите результат с префиксом 'Четные: '."
        ],
        "prerequisites": ["lua-oop-prototypes"],
        "resources": [{"title": "Корутины в Lua", "url": "https://www.lua.org/pil/9.html", "language": "EN"}],
        "lifeExample": "Театральное представление: актер выходит на сцену, говорит монолог (yield), уходит за кулисы, а затем возвращается во втором акте (resume) с того же момента.",
        "guide": {
            "version": 1,
            "idea": "Освоить создание и возобновление сопрограмм через coroutine.create, yield и resume.",
            "steps": ["Создать корутину.", "Возобновить 4 раза и собрать результаты.", "Вывести."],
            "solution": "local co = coroutine.create(function()\n    for i = 2, 8, 2 do\n        coroutine.yield(i)\n    end\nend)\nlocal nums = {}\nfor i = 1, 4 do\n    local ok, val = coroutine.resume(co)\n    if ok and val then\n        table.insert(nums, val)\n    end\nend\nprint(\"Четные: \" .. table.concat(nums, \" \"))"
        }
    },
    {
        "id": "lua-modules-io",
        "language": "lua",
        "title": "Модули, обработка ошибок и pcall",
        "topic": "Продвинутый Lua",
        "section": "Модули и безопасность",
        "order": 17,
        "level": "Продвинутый",
        "minutes": 20,
        "theory": "Модуль в Lua — это обычная таблица, содержащая функции и константы, которую файл возвращает через `return` в самом конце.\n\nПодключение модулей выполняется функцией `require(\"имя_модуля\")`:\n- Результат кэшируется в таблице `package.loaded`.\n- Модуль выполняется ровно один раз.\n\nОбработка ошибок в Lua:\nВместо традиционного try/catch в Lua используется защищенный вызов `pcall(f, ...)` (protected call):\n- Если функция `f` выполнилась успешно, `pcall` возвращает `true` и все результаты функции.\n- Если произошла ошибка (вызов `error()` или сбой), `pcall` перехватывает ошибку и возвращает `false` и сообщение об ошибке, не аварийно останавливая программу!",
        "syntax": "local function divide(a, b)\n    if b == 0 then error(\"Деление на ноль!\") end\n    return a / b\nend\n\nlocal ok, res = pcall(divide, 10, 0)\nif not ok then\n    print(\"Перехвачена ошибка:\", res)\nend",
        "examples": [
            "local ok, val = pcall(function() return 10 + 20 end)\nprint(ok, val) -- true, 30"
        ],
        "task": "Напишите функцию safe_sqrt(x), которая при x < 0 вызывает error('Число должно быть неотрицательным'), а при x >= 0 возвращает math.sqrt(x). Вызовите safe_sqrt(-9) через pcall и, если произошла ошибка, выведите: 'Ошибка перехвачена: число меньше нуля'. Затем вызовите safe_sqrt(16) через pcall и выведите: 'Успех: [корень]'.",
        "starterCode": "-- Реализуйте safe_sqrt и защищенный вызов pcall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Защищенный вызов и обработка ошибок",
                "expected": "Ошибка перехвачена: число меньше нуля\nУспех: 4"
            }
        ],
        "hints": [
            "Объявите local function safe_sqrt(x) if x < 0 then error('error') end return math.floor(math.sqrt(x)) end.",
            "Проверьте safe_sqrt(-9): local ok1, err = pcall(safe_sqrt, -9). При not ok1 напечатайте 'Ошибка перехвачена: число меньше нуля'.",
            "Проверьте safe_sqrt(16): local ok2, val = pcall(safe_sqrt, 16). При ok2 напечатайте 'Успех: ' .. val."
        ],
        "commonMistakes": "Вызов pcall(safe_sqrt(-9)) вместо pcall(safe_sqrt, -9) (в первом случае ошибка произойдет ДО вызова pcall при передаче аргумента).",
        "solutionExplanation": "pcall запускает функцию в изолированном защищенном контексте виртуальной машины Lua, перехватывая runtime-исключения.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["pcall", "error", "require", "модули"],
        "walkthrough": [
            "Создайте функцию safe_sqrt с проверкой x < 0.",
            "Протестируйте вызов safe_sqrt(-9) через pcall.",
            "Протестируйте вызов safe_sqrt(16) через pcall.",
            "Выведите сообщения для обоих случаев."
        ],
        "prerequisites": ["lua-coroutines"],
        "resources": [{"title": "Обработка ошибок и pcall в Lua", "url": "https://www.lua.org/pil/8.4.html", "language": "EN"}],
        "lifeExample": "Подушка безопасности в автомобиле: pcall смягчает любой сбой в пути и дает возможность продолжить движение.",
        "guide": {
            "version": 1,
            "idea": "Научиться использовать pcall для перехвата исключений в Lua.",
            "steps": ["Написать safe_sqrt.", "Вызвать с отрицательным числом через pcall.", "Вызвать с положительным числом."],
            "solution": "local function safe_sqrt(x)\n    if x < 0 then\n        error(\"Число должно быть неотрицательным\")\n    end\n    return math.floor(math.sqrt(x))\nend\n\nlocal ok1, err = pcall(safe_sqrt, -9)\nif not ok1 then\n    print(\"Ошибка перехвачена: число меньше нуля\")\nend\n\nlocal ok2, val = pcall(safe_sqrt, 16)\nif ok2 then\n    print(\"Успех: \" .. val)\nend"
        }
    },
    {
        "id": "lua-project-text-rpg",
        "language": "lua",
        "title": "Итоговый проект: Движок текстовой RPG игры",
        "topic": "Итоговый проект",
        "section": "Проекты",
        "order": 18,
        "level": "Продвинутый",
        "minutes": 35,
        "theory": "Поздравляем с выходом на итоговый проект трека Lua!\nВ этом проекте вы объедините все изученные концепции:\n- Локальные переменные и функции\n- Таблицы как словари и списки\n- Вложенные структуры данных\n- Прототипное ООП с классами\n- Инкапсуляцию игрового состояния\n\nАрхитектура текстового RPG движка:\n1. Класс `Player`: имя, здоровье, инвентарь (таблица предметов), текущая локация, методы `add_item(item)` и `move_to(location)`.\n2. Карта мира `WorldMap`: словарь локаций с описанием и переходами.\n3. Игровой цикл и журнал действий: обработка команд игрока и вывод обновленного состояния мира.",
        "syntax": "local Game = {\n    locations = {\n        forest = { desc = \"Темный лес\", exits = { north = \"castle\" } },\n        castle = { desc = \"Замок короля\", exits = { south = \"forest\" } }\n    }\n}",
        "examples": [
            "local player = Player.new(\"Артур\", \"forest\")\nplayer:add_item(\"Факел\")\nplayer:move_to(\"castle\")"
        ],
        "task": "Реализуйте движок текстового квеста:\n1. Класс Player с полями name, location, inventory (список строк).\n2. Методы Player: add_item(item) (добавляет предмет в инвентарь) и move_to(new_loc) (меняет location).\n3. Метод Player:status(), возвращающий строку: '[name] находится в: [location] | Инвентарь: [список через запятую]'.\n4. Создайте героя 'Рыцарь' в локации 'Деревня'.\n5. Подберите предмет 'Меч', затем переместитесь в 'Пещера', подберите 'Щит'.\n6. Выведите итоговый статус героя через print(hero:status()).",
        "starterCode": "-- Итоговый проект: Движок текстовой RPG\nlocal Player = {}\nPlayer.__index = Player\n\n-- Реализуйте new, add_item, move_to и status\n",
        "tests": [
            {
                "id": "t1",
                "label": "Итоговый статус персонажа в RPG игре",
                "expected": "Рыцарь находится в: Пещера | Инвентарь: Меч, Щит"
            }
        ],
        "hints": [
            "В конструкторе new(name, loc) создайте self = setmetatable({}, Player); self.name = name; self.location = loc; self.inventory = {}; return self.",
            "В add_item(item) вызовите table.insert(self.inventory, item).",
            "В move_to(new_loc) обновите self.location = new_loc.",
            "В status() верните string.format('%s находится в: %s | Инвентарь: %s', self.name, self.location, table.concat(self.inventory, ', '))."
        ],
        "commonMistakes": "Использование двоеточия при вызове Player.new (new — функция-конструктор, вызывается через точку; а методы экземпляра hero:add_item вызываются через двоеточие).",
        "solutionExplanation": "Полноценный класс Player инкапсулирует состояние персонажа, его вещи и координаты на карте, представляя законченную модель RPG-игры.",
        "xp": 150,
        "setupSql": "",
        "concepts": ["Итоговый проект", "ООП", "RPG", "Инвентарь", "Карта мира"],
        "walkthrough": [
            "Объявите класс Player с таблицей и __index.",
            "Реализуйте методы new, add_item, move_to и status.",
            "Создайте персонажа 'Рыцарь' в локации 'Деревня'.",
            "Добавьте Меч, перейдите в Пещеру, добавьте Щит.",
            "Выведите hero:status()."
        ],
        "prerequisites": ["lua-modules-io"],
        "resources": [{"title": "Разработка игр на Lua", "url": "https://www.lua.org/pil/index.html", "language": "EN"}],
        "lifeExample": "Архитектура игрового движка в World of Warcraft или Baldur's Gate: игровые скрипты создают персонажей и управляют их квестами через вызовы методов объекта игрока.",
        "guide": {
            "version": 1,
            "idea": "Создать законченную игровую систему персонажа текстовой RPG на Lua.",
            "steps": ["Создать класс Player.", "Реализовать инвентарь и перемещение.", "Проверить сценарий игры."],
            "solution": "local Player = {}\nPlayer.__index = Player\n\nfunction Player.new(name, location)\n    local self = setmetatable({}, Player)\n    self.name = name\n    self.location = location\n    self.inventory = {}\n    return self\nend\n\nfunction Player:add_item(item)\n    table.insert(self.inventory, item)\nend\n\nfunction Player:move_to(new_loc)\n    self.location = new_loc\nend\n\nfunction Player:status()\n    return string.format(\"%s находится в: %s | Инвентарь: %s\", self.name, self.location, table.concat(self.inventory, \", \"))\nend\n\nlocal hero = Player.new(\"Рыцарь\", \"Деревня\")\nhero:add_item(\"Меч\")\nhero:move_to(\"Пещера\")\nhero:add_item(\"Щит\")\nprint(hero:status())"
        }
    }
]
