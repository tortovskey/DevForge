# -*- coding: utf-8 -*-
"""Assembly (x86-64 NASM) 18-lesson complete curriculum with 8-point pedagogical standard."""

ASSEMBLY_LESSONS = [
    {
        "id": "asm-first-exit",
        "language": "assembly",
        "title": "Первая программа на x86-64: Структура и завершение процесса",
        "topic": "Основы ассемблера",
        "section": "Архитектура x86-64",
        "order": 1,
        "level": "Начальный",
        "minutes": 12,
        "theory": "Ассемблер — это символический язык машинных команд, где каждая инструкция напрямую соответствует одной операции центрального процессора (CPU).\n\nВ платформе DevForge используется стандартная 64-битная архитектура x86-64 и ассемблер NASM (Netwide Assembler) с синтаксисом Intel (где приемник пишется слева, а источник справа: `mov приемник, источник`).\n\nСтруктура базовой программы:\n- `section .text`: секция, содержащая исполняемый машинный код.\n- `global _start`: объявляет точку входа в программу, видимую для линковщика ОС Linux.\n- `_start:`: метка (адрес в памяти), с которой процессор начинает выполнение.\n\nСистемные вызовы (syscall):\nВ современных 64-битных ОС Linux общение программы с ядром происходит через инструкцию `syscall`. Номер требуемого вызова помещается в регистр `rax`, а аргументы — в регистры `rdi`, `rsi`, `rdx` и др.\n\nСистемный вызов `sys_exit` (номер 60):\n- `mov rax, 60` — номер системного вызова завершения процесса.\n- `mov rdi, 0` — код возврата (0 означает успешное завершение).\n- `syscall` — переключение в режим ядра для завершения программы.",
        "syntax": "section .text\n    global _start\n_start:\n    mov rax, 60    ; sys_exit\n    mov rdi, 0     ; код возврата\n    syscall",
        "examples": [
            "; Завершение с кодом 42\nsection .text\n    global _start\n_start:\n    mov rax, 60\n    mov rdi, 42\n    syscall"
        ],
        "task": "Напишите минимальную программу на ассемблере x86-64 NASM, которая завершается с кодом возврата 0 через системный вызов sys_exit (rax = 60, rdi = 0, syscall).",
        "starterCode": "; Напишите секцию .text, метку _start и системный вызов выхода\n",
        "tests": [
            {
                "id": "t1",
                "label": "Код возврата sys_exit равен 0",
                "expression": "exit_code",
                "expected": 0
            }
        ],
        "hints": [
            "Объявите секцию: section .text и global _start.",
            "Поместите 60 в регистр rax: mov rax, 60.",
            "Поместите 0 в регистр rdi: mov rdi, 0 и выполните syscall."
        ],
        "commonMistakes": "Забыть ключевое слово global _start; опечатка в названии регистра rdi (например, rsi вместо rdi).",
        "solutionExplanation": "Инструкция syscall передает управление ядру Linux, которое считывает номер вызова 60 из RAX и код возврата 0 из RDI.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["x86-64", "NASM", "syscall", "sys_exit", "rax", "rdi", "_start"],
        "walkthrough": [
            "Укажите секцию кода section .text.",
            "Сделайте точку входа доступной: global _start.",
            "Запишите номер вызова 60 в rax и код 0 в rdi.",
            "Вызовите syscall."
        ],
        "prerequisites": [],
        "resources": [{"title": "NASM Documentation", "url": "https://www.nasm.us/doc/", "language": "EN"}],
        "lifeExample": "Кнопка выключения питания: вы даете процессору команду аккуратно завершить работу и передать отчет операционной системе.",
        "guide": {
            "version": 1,
            "idea": "Познакомиться со структурой ассемблерной программы и системным вызовом выхода.",
            "steps": ["Создать секцию .text.", "Определить _start.", "Выполнить mov rax, 60; mov rdi, 0; syscall."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 60\n    mov rdi, 0\n    syscall"
        }
    },
    {
        "id": "asm-registers-mov",
        "language": "assembly",
        "title": "Регистры общего назначения и инструкция MOV",
        "topic": "Регистры и память",
        "section": "Архитектура x86-64",
        "order": 2,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Регистры процессора — это самые быстрые ячейки памяти, расположенные прямо на кристалле CPU. В архитектуре x86-64 имеется 16 основных 64-битных регистров общего назначения:\n- `rax`: аккумулятор (результаты вычислений, возвращаемые значения функций, номер syscall)\n- `rbx`: базовый регистр\n- `rcx`: счетчик (используется в циклах и строковых операциях)\n- `rdx`: регистр данных (используется при умножении, делении, длина буфера в syscall)\n- `rsi`: индекс источника (Source Index)\n- `rdi`: индекс приемника (Destination Index, первый аргумент функций и syscall)\n- `rbp`: указатель базы стекового кадра (Base Pointer)\n- `rsp`: указатель вершины стека (Stack Pointer)\n- `r8` – `r15`: дополнительные 64-битные регистры общего назначения\n\nИнструкция `mov приемник, источник` копирует значение из источника в приемник. Источником может быть непосредственное число (immediate) или другой регистр. Копирование из памяти в память одной инструкцией mov в x86 ЗАПРЕЩЕНО архитектурой (требуется промежуточный регистр).",
        "syntax": "mov rax, 42       ; число в регистр\nmov rbx, rax      ; из регистра в регистр\nmov rcx, 100",
        "examples": [
            "mov r8, 15\nmov r9, r8"
        ],
        "task": "Поместите в регистр rax число 100, скопируйте значение из rax в регистр rbx, а затем поместите в регистр rdi число 42. Завершите программу системным вызовом sys_exit с кодом из rdi.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Поместите 100 в rax, скопируйте в rbx, поместите 42 в rdi\n    \n    ; Завершите программу (sys_exit)\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Проверка значения регистра rbx",
                "expression": "rbx",
                "expected": 100
            },
            {
                "id": "t2",
                "label": "Проверка кода возврата в rdi",
                "expression": "exit_code",
                "expected": 42
            }
        ],
        "hints": [
            "Напишите mov rax, 100.",
            "Скопируйте в rbx: mov rbx, rax.",
            "Запишите mov rdi, 42 перед вызовом mov rax, 60 и syscall."
        ],
        "commonMistakes": "Перезапись rdi значением 60 вместо rax; перепутать порядок операндов (в Intel-синтаксисе mov DST, SRC — приемник слева).",
        "solutionExplanation": "Инструкция mov rbx, rax переносит 64-битное значение 100 из аккумулятора в базовый регистр rbx, а rdi сохраняет код завершения 42.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["mov", "rax", "rbx", "rdi", "регистры общего назначения"],
        "walkthrough": [
            "Запишите mov rax, 100.",
            "Запишите mov rbx, rax.",
            "Запишите mov rdi, 42.",
            "Завершите процесс с mov rax, 60 и syscall."
        ],
        "prerequisites": ["asm-first-exit"],
        "resources": [{"title": "Регистры x86-64", "url": "https://en.wikipedia.org/wiki/X86-64#Registers", "language": "EN"}],
        "lifeExample": "Рабочий стол мастера: регистры — это инструменты в руках, куда можно мгновенно положить нужную деталь.",
        "guide": {
            "version": 1,
            "idea": "Научиться перемещать данные между регистрами с помощью инструкции mov.",
            "steps": ["Записать 100 в rax.", "Скопировать в rbx.", "Записать 42 в rdi и выйти."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 100\n    mov rbx, rax\n    mov rdi, 42\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-subregisters",
        "language": "assembly",
        "title": "Младшие регистры и обнуление старших бит",
        "topic": "Регистры и память",
        "section": "Архитектура x86-64",
        "order": 3,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Каждый 64-битный регистр содержит в себе более узкие регистры для обратной совместимости с 32-, 16- и 8-битными поколениями x86:\n\nИерархия для регистра RAX:\n- `rax`: 64 бита (биты 0..63)\n- `eax`: 32 бита (биты 0..31)\n- `ax`: 16 бит (биты 0..15)\n- `al`: младшие 8 бит (биты 0..7)\n- `ah`: старшие 8 бит от ax (биты 8..15)\n\nАналогично для RBX (ebx, bx, bl, bh), RCX (ecx, cx, cl, ch), RDX (edx, dx, dl, dh).\nДля новых регистров r8-r15: `r8d` (32 бит), `r8w` (16 бит), `r8b` (8 бит).\n\nВАЖНЕЙШЕЕ ПРАВИЛО x86-64:\nКогда вы записываете значение в 32-битный регистр (например, `mov eax, 5`), процессор АВТОМАТИЧЕСКИ ОБНУЛЯЕТ старшие 32 бита соответствующего 64-битного регистра `rax`! При записи в 16- или 8-битные регистры старшие биты сохраняются.",
        "syntax": "mov rax, 0xffffffffffffffff  ; все биты установлены в 1\nmov eax, 10                  ; rax становится 0x000000000000000a (старшие биты обнулены!)\nmov al, 5                    ; изменились только младшие 8 бит",
        "examples": [
            "mov ebx, 255\nmov bl, 10"
        ],
        "task": "Инициализируйте регистр rax числом 0x123456789abcdef0. Затем выполните запись в 32-битный субрегистр eax значения 1000. Проверьте результат обнуления старших бит (в тесте проверяется значение rax). Завершите программу с sys_exit (rdi = 0).",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Запишите 0x123456789abcdef0 в rax\n    ; Запишите 1000 в eax\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Значение rax после записи в eax равно 1000",
                "expression": "rax",
                "expected": 1000
            }
        ],
        "hints": [
            "Запишите: mov rax, 0x123456789abcdef0.",
            "Затем запишите: mov eax, 1000.",
            "В x86-64 запись в 32-битный регистр обнуляет верхние 32 бита, поэтому rax станет равен 1000."
        ],
        "commonMistakes": "Ожидание, что верхние 32 бита сохранятся (в x86-64 запись в 32-битный регистр всегда обнуляет верхнюю половину 64-битного регистра).",
        "solutionExplanation": "Инструкция mov eax, 1000 обнуляет верхнюю половину регистра rax, устанавливая все 64 бита в значение 1000.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["субрегистры", "eax", "ax", "al", "zero-extension"],
        "walkthrough": [
            "Установите начальное 64-битное значение в rax.",
            "Выполните запись в субрегистр eax.",
            "Убедитесь, что rax стал равен 1000.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-registers-mov"],
        "resources": [{"title": "Субрегистры x86-64", "url": "https://www.felixcloutier.com/x86/", "language": "EN"}],
        "lifeExample": "Шкатулка с отделениями: вы можете заменить содержимое всей нижней секции, и это автоматически очистит верхний навесной отсек.",
        "guide": {
            "version": 1,
            "idea": "Понять правило обнуления старших 32 бит при записи в субрегистры.",
            "steps": ["Записать 64-битное число в rax.", "Записать 1000 в eax.", "Выйти через syscall."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 0x123456789abcdef0\n    mov eax, 1000\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-arithmetic-add-sub",
        "language": "assembly",
        "title": "Базовая арифметика: ADD, SUB, INC, DEC",
        "topic": "Арифметика",
        "section": "Инструкции",
        "order": 4,
        "level": "Начальный",
        "minutes": 15,
        "theory": "Арифметические инструкции процессора x86-64 изменяют значение операнда-приемника и обновляют флаги состояния процессора:\n- `add dst, src`: сложение (`dst = dst + src`)\n- `sub dst, src`: вычитание (`dst = dst - src`)\n- `inc dst`: инкремент (`dst = dst + 1`, не изменяет флаг переноса CF!)\n- `dec dst`: декремент (`dst = dst - 1`)\n- `neg dst`: изменение знака числа на противоположный (дополнительный код, `dst = -dst`)\n\nВсе эти инструкции поддерживают работу как с регистрами, так и с ячейками оперативной памяти.",
        "syntax": "add rax, 10      ; rax += 10\nsub rbx, 5       ; rbx -= 5\ninc rcx          ; rcx++\ndec rdx          ; rdx--\nneg rax          ; rax = -rax",
        "examples": [
            "mov rax, 20\nadd rax, 22\n; теперь rax = 42"
        ],
        "task": "Инициализируйте rax = 50. Вычтите из rax 15 (получится 35), прибавьте 7 (получится 42) и сделайте inc rax (получится 43). Передайте итоговое значение в rdi и завершите программу с кодом 43 через sys_exit.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Выполните цепочку: 50 - 15 + 7 + 1\n    \n    ; Завершите программу с кодом из rdi\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Итоговое значение в rdi равно 43",
                "expression": "exit_code",
                "expected": 43
            }
        ],
        "hints": [
            "Поместите 50: mov rax, 50.",
            "Выполните sub rax, 15, затем add rax, 7, затем inc rax.",
            "Скопируйте результат: mov rdi, rax перед mov rax, 60 и syscall."
        ],
        "commonMistakes": "Перезапись rax значением 60 до копирования результата в rdi.",
        "solutionExplanation": "50 - 15 = 35; 35 + 7 = 42; inc(42) = 43. Результат копируется в RDI для передачи кодом выхода.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["add", "sub", "inc", "dec", "neg"],
        "walkthrough": [
            "Инициализируйте rax числом 50.",
            "Вычтите 15 с sub rax, 15.",
            "Прибавьте 7 с add rax, 7.",
            "Увеличьте на 1 с inc rax.",
            "Скопируйте rax в rdi и завершите программу."
        ],
        "prerequisites": ["asm-registers-mov"],
        "resources": [{"title": "Арифметика x86-64", "url": "https://www.felixcloutier.com/x86/add", "language": "EN"}],
        "lifeExample": "Счетчик в магазине: взяли товар (+), применили скидку (-), добавили бонусный балл (inc).",
        "guide": {
            "version": 1,
            "idea": "Научиться применять инструкции add, sub, inc и передавать результат в sys_exit.",
            "steps": ["Выполнить 50 - 15 + 7 + 1.", "Скопировать в rdi.", "Выйти через syscall."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 50\n    sub rax, 15\n    add rax, 7\n    inc rax\n    mov rdi, rax\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-multiplication-division",
        "language": "assembly",
        "title": "Умножение и деление: IMUL и IDIV",
        "topic": "Арифметика",
        "section": "Инструкции",
        "order": 5,
        "level": "Средний",
        "minutes": 18,
        "theory": "Умножение и деление в x86-64 имеют специфические особенности:\n\n1. Знаковое умножение `imul`:\n- Двухоперандная форма: `imul dst, src` (`dst = dst * src`). Самый удобный и частый вариант.\n- Трехоперандная форма: `imul dst, src, imm` (`dst = src * imm`).\n\n2. Знаковое деление `idiv divisor`:\nДеление в x86-64 делит 128-битное составное число `[rdx:rax]` на делитель `divisor`!\n- Перед вызовом `idiv` необходимо расширить знак из `rax` в `rdx` (для этого используется инструкция `cqo` или обнуление `xor rdx, rdx` для положительных чисел).\n- После деления:\n  - Частное (quotient) помещается в регистр `rax`!\n  - Остаток (remainder) помещается в регистр `rdx`!\n\nДеление на ноль вызывает аппаратное прерывание процессора `#DE` (Divide Error) и немедленный крах программы.",
        "syntax": "imul rax, rbx     ; rax = rax * rbx\n\nmov rax, 100\nmov rbx, 7\nxor rdx, rdx      ; обнуляем старшую часть делимого\nidiv rbx          ; rax = 100 / 7 = 14, rdx = 100 % 7 = 2",
        "examples": [
            "mov rax, 6\nimul rax, 7 ; rax = 42"
        ],
        "task": "Даны числа a = 12 и b = 5. С помощью imul вычислите их произведение (12 * 5 = 60) и сохраните в регистре rbx. Затем разделите число 60 на 8 с помощью idiv (не забудьте xor rdx, rdx): частное останется в rax, а остаток в rdx. В тесте проверяется значение остатка в rdx (остаток равен 4). Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; 1. Умножьте 12 на 5 в rbx\n    ; 2. Разделите 60 на 8 через idiv\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Произведение в rbx равно 60",
                "expression": "rbx",
                "expected": 60
            },
            {
                "id": "t2",
                "label": "Остаток от деления 60 на 8 в rdx равен 4",
                "expression": "rdx",
                "expected": 4
            }
        ],
        "hints": [
            "Напишите mov rbx, 12; imul rbx, 5.",
            "Для деления скопируйте 60 в rax: mov rax, rbx.",
            "Обнулите rdx: xor rdx, rdx.",
            "Задайте делитель: mov rcx, 8 и вызовите idiv rcx."
        ],
        "commonMistakes": "Забыть обнулить rdx перед idiv (если в rdx будет мусор, делимое станет гигантским числом и возникнет ошибка переполнения деления).",
        "solutionExplanation": "imul rbx, 5 вычисляет 60. Инструкция idiv rcx делит составное число [rdx:rax] (60) на 8, записывая частное 7 в rax и остаток 4 в rdx.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["imul", "idiv", "rdx:rax", "частное", "остаток"],
        "walkthrough": [
            "Вычислите 12 * 5 в rbx.",
            "Поместите 60 в rax.",
            "Обнулите rdx с помощью xor rdx, rdx.",
            "Разделите на 8 с idiv.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-arithmetic-add-sub"],
        "resources": [{"title": "Инструкции imul и idiv в x86", "url": "https://www.felixcloutier.com/x86/idiv", "language": "EN"}],
        "lifeExample": "Раскладывание конфет по коробкам: деление определяет, сколько полных коробок получилось (rax), и сколько лишних конфет осталось (rdx).",
        "guide": {
            "version": 1,
            "idea": "Научиться выполнять умножение imul и деление idiv с получением частного и остатка.",
            "steps": ["Вычислить imul.", "Подготовить rax и rdx.", "Выполнить idiv."],
            "solution": "section .text\n    global _start\n_start:\n    mov rbx, 12\n    imul rbx, 5\n    mov rax, rbx\n    xor rdx, rdx\n    mov rcx, 8\n    idiv rcx\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-bitwise-logic",
        "language": "assembly",
        "title": "Побитовые операции: AND, OR, XOR, NOT",
        "topic": "Логика и биты",
        "section": "Инструкции",
        "order": 6,
        "level": "Средний",
        "minutes": 15,
        "theory": "Побитовые инструкции выполняют логические операции над каждым отдельным битом операндов:\n- `and dst, src`: побитовое И. Бит результата равен 1 только если оба соответствующих бита равны 1. Применяется для наложения масок (маскирования).\n- `or dst, src`: побитовое ИЛИ. Применяется для установки конкретных бит в 1.\n- `xor dst, src`: побитовое исключающее ИЛИ. Бит равен 1, если биты операндов различаются.\n- `not dst`: побитовое отрицание (инвертирует все биты: 0 становится 1, 1 становится 0).\n\nВАЖНЕЙШАЯ ИДИОМА x86: Обнуление регистра через XOR:\nИнструкция `xor rax, rax` — самый быстрый и канонический способ обнулить регистр в x86. Она кодируется короче, чем `mov rax, 0` (2 байта против 7) и распознается процессором на аппаратном уровне без зависимости от предыдущего значения регистра.",
        "syntax": "xor rax, rax      ; быстрое обнуление rax\nand rbx, 0x0f     ; выделить младшие 4 бита (маска)\nor  rcx, 0x80     ; установить старший бит\nnot rdx           ; инверсия всех бит",
        "examples": [
            "mov rax, 0b1010\nand rax, 0b1100 ; rax = 0b1000 (8)"
        ],
        "task": "Инициализируйте rax = 0xAA (бинарно 10101010) и rbx = 0x55 (бинарно 01010101). Выполните побитовое OR: or rax, rbx (результат станет 0xFF = 255). Затем с помощью xor обнулите регистр rcx (xor rcx, rcx). В тестах проверяются значения rax и rcx. Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Выполните операции OR и XOR\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Результат побитового OR в rax равен 255",
                "expression": "rax",
                "expected": 255
            },
            {
                "id": "t2",
                "label": "Обнуление rcx через xor",
                "expression": "rcx",
                "expected": 0
            }
        ],
        "hints": [
            "Напишите mov rax, 0xaa и mov rbx, 0x55.",
            "Выполните or rax, rbx.",
            "Обнулите rcx: xor rcx, rcx.",
            "Завершите программу: mov rdi, 0; mov rax, 60; syscall."
        ],
        "commonMistakes": "Использование mov rcx, 0 вместо канонического xor rcx, rcx.",
        "solutionExplanation": "Побитовое ИЛИ объединяет биты 10101010 и 01010101 в 11111111 (255), а XOR самого с собой всегда дает чистый ноль.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["and", "or", "xor", "not", "обнуление через xor"],
        "walkthrough": [
            "Запишите числа в rax и rbx.",
            "Примените or rax, rbx.",
            "Обнулите rcx через xor rcx, rcx.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-arithmetic-add-sub"],
        "resources": [{"title": "Побитовые операции x86", "url": "https://www.felixcloutier.com/x86/xor", "language": "EN"}],
        "lifeExample": "Трафарет для покраски: побитовое AND пропускает краску только через вырезанные отверстия маски.",
        "guide": {
            "version": 1,
            "idea": "Освоить логические побитовые операции и идиому обнуления регистра через XOR.",
            "steps": ["Применить or.", "Применить xor для обнуления.", "Завершить работу."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 0xaa\n    mov rbx, 0x55\n    or rax, rbx\n    xor rcx, rcx\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-shifts-rotates",
        "language": "assembly",
        "title": "Битовые сдвиги: SHL и SHR",
        "topic": "Логика и биты",
        "section": "Инструкции",
        "order": 7,
        "level": "Средний",
        "minutes": 15,
        "theory": "Инструкции битового сдвига сдвигают битовую цепочку влево или вправо на указанное число позиций:\n- `shl dst, count`: логический сдвиг влево (Shift Logical Left). Биты сдвигаются влево, освободившиеся младшие биты заполняются нулями. Сдвиг влево на `k` бит эквивалентен быстрому умножению на `2^k`!\n- `shr dst, count`: логический сдвиг вправо (Shift Logical Right). Освободившиеся старшие биты заполняются нулями. Эквивалентен делению беззнакового числа на `2^k`.\n- `sar dst, count`: арифметический сдвиг вправо (Shift Arithmetic Right). Сохраняет знаковый старший бит для корректного деления отрицательных чисел.\n\nПроцессоры выполняют битовый сдвиг всего за 1 такт, поэтому компиляторы заменяют умножение на 2, 4, 8, 16 сдвигами `shl`.",
        "syntax": "shl rax, 1        ; rax = rax * 2\nshl rax, 3        ; rax = rax * 8 (2^3)\nshr rbx, 2        ; rbx = rbx / 4 (2^2)",
        "examples": [
            "mov rax, 5\nshl rax, 3 ; 5 * 8 = 40"
        ],
        "task": "Инициализируйте rax числом 6. С помощью инструкции shl умножьте его на 4 (сдвиг влево на 2 бита, результат 24). Затем прибавьте 1 (inc rax, результат 25). Передайте результат в rdi и завершите программу с этим кодом.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Умножьте 6 на 4 с помощью сдвига shl, прибавьте 1\n    \n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Результат сдвига и инкремента в exit_code равен 25",
                "expression": "exit_code",
                "expected": 25
            }
        ],
        "hints": [
            "Поместите 6 в rax: mov rax, 6.",
            "Сдвиньте влево на 2 бита: shl rax, 2.",
            "Сделайте inc rax, скопируйте в rdi: mov rdi, rax.",
            "Завершите программу: mov rax, 60; syscall."
        ],
        "commonMistakes": "Сдвиг на 4 вместо 2 (сдвиг на 4 умножает на 2^4 = 16, а на 4 умножает сдвиг на 2).",
        "solutionExplanation": "6 в двоичном виде: 0110. Сдвиг влево на 2 позиции дает 011000 (24 в десятичной). Добавление 1 дает 25.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["shl", "shr", "битовые сдвиги", "быстрое умножение"],
        "walkthrough": [
            "Инициализируйте rax = 6.",
            "Выполните shl rax, 2.",
            "Выполните inc rax.",
            "Скопируйте в rdi и завершите программу."
        ],
        "prerequisites": ["asm-bitwise-logic"],
        "resources": [{"title": "Инструкция SHL в x86", "url": "https://www.felixcloutier.com/x86/sal:sar:shl:shr", "language": "EN"}],
        "lifeExample": "Счеты: перенос костяшки на одну проволоку влево мгновенно умножает разряд на десять, а в двоичной системе сдвиг бита влево умножает число на два.",
        "guide": {
            "version": 1,
            "idea": "Освоить умножение чисел с помощью логического сдвига shl.",
            "steps": ["mov rax, 6.", "shl rax, 2.", "inc rax и выход."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 6\n    shl rax, 2\n    inc rax\n    mov rdi, rax\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-flags-cmp",
        "language": "assembly",
        "title": "Флаги процессора и инструкция сравнения CMP",
        "topic": "Управление потоком",
        "section": "Ветвление",
        "order": 8,
        "level": "Средний",
        "minutes": 18,
        "theory": "Регистр флагов `RFLAGS` содержит биты состояния, отражающие результат последней выполненной инструкции:\n- `ZF` (Zero Flag) — устанавливается в 1, если результат операции равен нулю.\n- `SF` (Sign Flag) — равен старшему (знаковому) биту результата (1 для отрицательных чисел).\n- `CF` (Carry Flag) — флаг переноса/заема при беззнаковых операциях.\n- `OF` (Overflow Flag) — флаг переполнения при знаковых операциях.\n\nИнструкция `cmp op1, op2` выполняет вычитание `op1 - op2`, НЕ СОХРАНЯЯ результат ни в один регистр, а ТОЛЬКО ОБНОВЛЯЯ ФЛАГИ!\n- Если `op1 == op2`, то `op1 - op2 = 0` -> флаг `ZF = 1`.\n- Если `op1 < op2`, то возникает заем -> флаг `CF = 1` (для беззнаковых) или `SF != OF` (для знаковых).\n- Если `op1 > op2`, то `ZF = 0` и `SF == OF`.",
        "syntax": "cmp rax, 42       ; сравнивает rax с 42\n; если rax == 42, то флаг ZF = 1",
        "examples": [
            "mov rax, 10\ncmp rax, 10 ; ZF становится 1"
        ],
        "task": "Инициализируйте регистр rax числом 77. Выполните инструкцию cmp rax, 77 (сравнение с 77). Проверьте, что флаг нуля ZF установился в 1. Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n_start:\n    ; Сравните rax с 77\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Флаг ZF равен 1 после сравнения равных чисел",
                "expression": "flags.zf",
                "expected": 1
            }
        ],
        "hints": [
            "Запишите mov rax, 77.",
            "Затем напишите cmp rax, 77.",
            "Завершите программу: mov rdi, 0; mov rax, 60; syscall."
        ],
        "commonMistakes": "Попытка сохранить результат cmp в регистр (cmp не принимает третий операнд, она меняет только флаги).",
        "solutionExplanation": "77 - 77 = 0, поэтому инструкция cmp выставляет флаг нуля ZF (Zero Flag) в единицу.",
        "xp": 50,
        "setupSql": "",
        "concepts": ["RFLAGS", "ZF", "SF", "CF", "OF", "cmp"],
        "walkthrough": [
            "Поместите 77 в rax.",
            "Выполните cmp rax, 77.",
            "Завершите программу через syscall."
        ],
        "prerequisites": ["asm-arithmetic-add-sub"],
        "resources": [{"title": "Регистр RFLAGS и инструкция CMP", "url": "https://www.felixcloutier.com/x86/cmp", "language": "EN"}],
        "lifeExample": "Аптекарские весы: сравнение двух чаш весов. Если грузы равны, стрелка весов указывает точно на ноль (Zero Flag).",
        "guide": {
            "version": 1,
            "idea": "Понять работу инструкции cmp и установку флагов процессора.",
            "steps": ["mov rax, 77.", "cmp rax, 77.", "Выйти через syscall."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 77\n    cmp rax, 77\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-conditional-jumps",
        "language": "assembly",
        "title": "Условные переходы: JMP, JE, JNE, JL, JG",
        "topic": "Управление потоком",
        "section": "Ветвление",
        "order": 9,
        "level": "Средний",
        "minutes": 18,
        "theory": "Инструкции переходов изменяют регистр указателя команд `RIP`, заставляя процессор перепрыгнуть к указанной метке.\n\n1. Безусловный переход:\n- `jmp label` — безусловный переход к метке.\n\n2. Условные переходы (анализируют флаги после `cmp` или арифметики):\n- `je label` (или `jz`) — Jump if Equal (переход, если ZF = 1, то есть операнды равны).\n- `jne label` (или `jnz`) — Jump if Not Equal (переход, если ZF = 0).\n- `jl label` — Jump if Less (переход, если меньше при знаковом сравнении).\n- `jg label` — Jump if Greater (переход, если больше при знаковом сравнении).\n- `jle label` — меньше или равно.\n- `jge label` — больше или равно.",
        "syntax": "cmp rax, 10\nje is_ten       ; если rax == 10, прыжок на is_ten\nmov rdi, 1      ; иначе выполняется этот код\njmp finish\n\nis_ten:\n    mov rdi, 0\nfinish:\n    mov rax, 60\n    syscall",
        "examples": [
            "cmp rbx, 0\njne not_zero"
        ],
        "task": "Дано число в rax = 15. Сравните его с 10 (cmp rax, 10). Если rax > 10, перейдите по метке greater и установите rbx = 100. Если нет, установите rbx = 50. В тесте проверяется значение rbx (должно быть 100).",
        "starterCode": "section .text\n    global _start\n_start:\n    mov rax, 15\n    ; Сравните rax с 10 и выполните ветвление jg\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Ветвление по условию больше: rbx равен 100",
                "expression": "rbx",
                "expected": 100
            }
        ],
        "hints": [
            "Выполните cmp rax, 10.",
            "Используйте jg greater.",
            "В основной ветке напишите mov rbx, 50; jmp finish.",
            "По метке greater: напишите mov rbx, 100.",
            "По метке finish: выполните выход sys_exit."
        ],
        "commonMistakes": "Забыть jmp finish после ветки else (тогда выполнение 'провалится' в метку greater и перезапишет rbx).",
        "solutionExplanation": "Поскольку 15 > 10, инструкция jg greater срабатывает, минуя блок else и устанавливая rbx в 100.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["je", "jne", "jg", "jl", "jmp", "ветвление в ассемблере"],
        "walkthrough": [
            "Сравните rax с 10.",
            "Сделайте переход jg на метку greater.",
            "В ветке else запишите rbx = 50 и сделайте jmp finish.",
            "По метке greater запишите rbx = 100.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-flags-cmp"],
        "resources": [{"title": "Инструкции условных переходов x86", "url": "https://www.felixcloutier.com/x86/jcc", "language": "EN"}],
        "lifeExample": "Развилка на дороге: дорожный указатель (CMP) показывает поворот, и вы сворачиваете (JG) на нужную трассу.",
        "guide": {
            "version": 1,
            "idea": "Понять организацию условий if-else на ассемблере с помощью cmp и jg/jmp.",
            "steps": ["Сравнить rax с 10.", "Перейти на greater при успехе.", "Установить rbx и выйти."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 15\n    cmp rax, 10\n    jg greater\n    mov rbx, 50\n    jmp finish\ngreater:\n    mov rbx, 100\nfinish:\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-loops",
        "language": "assembly",
        "title": "Организация циклов на ассемблере",
        "topic": "Управление потоком",
        "section": "Циклы",
        "order": 10,
        "level": "Средний",
        "minutes": 20,
        "theory": "В ассемблере нет ключевых слов `while` или `for`. Любой цикл строится вручную комбинацией метки, счетчика, проверки условия и условного перехода назад.\n\nПаттерн цикла со счетчиком:\n```nasm\n    mov rcx, 5        ; счетчик итераций\nloop_start:\n    ; полезная работа\n    dec rcx           ; уменьшить счетчик\n    jnz loop_start    ; пока не ноль, повторять!\n```\n\nТакже в x86 есть специализированная инструкция `loop label`:\nОна автоматически выполняет `dec rcx` и, если `rcx != 0`, прыгает по метке `label`.",
        "syntax": "    mov rcx, 10\n.repeat:\n    ; тело цикла\n    dec rcx\n    jnz .repeat",
        "examples": [
            "mov rax, 0\nmov rcx, 4\n.loop:\n    add rax, 10\n    dec rcx\n    jnz .loop ; rax станет 40"
        ],
        "task": "Используя цикл, вычислите сумму чисел от 1 до 5 (1 + 2 + 3 + 4 + 5 = 15). Накапливайте сумму в регистре rax. В тесте проверяется итоговое значение регистра rax (должно быть 15). Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n_start:\n    xor rax, rax      ; сумма = 0\n    mov rcx, 1        ; i = 1\n    ; Напишите цикл суммирования до 5\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Сумма чисел от 1 до 5 в rax равна 15",
                "expression": "rax",
                "expected": 15
            }
        ],
        "hints": [
            "Поставьте метку loop_start:.",
            "Прибавьте счетчик: add rax, rcx.",
            "Увеличьте счетчик: inc rcx.",
            "Сравните с 5: cmp rcx, 5.",
            "Сделайте условный переход назад: jle loop_start."
        ],
        "commonMistakes": "Забыть inc rcx внутри цикла (бесконечный цикл и ошибка превышения тактов процессора).",
        "solutionExplanation": "Цикл выполняет 5 итераций, прибавляя 1, 2, 3, 4, 5 к rax, в результате чего rax становится равен 15.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["циклы", "loop_start", "dec rcx", "jnz", "jle"],
        "walkthrough": [
            "Инициализируйте rax = 0 и rcx = 1.",
            "Создайте метку цикла.",
            "Выполните add rax, rcx и inc rcx.",
            "Проверьте cmp rcx, 5 и jle на начало цикла.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-conditional-jumps"],
        "resources": [{"title": "Инструкция LOOP в x86", "url": "https://www.felixcloutier.com/x86/loop:loopcc", "language": "EN"}],
        "lifeExample": "Счетчик кругов на стадионе: пробежал круг, отметил в блокноте, побежал следующий, пока не набралось пять.",
        "guide": {
            "version": 1,
            "idea": "Научиться строить циклы на ассемблере с помощью меток и условных переходов.",
            "steps": ["Создать метку цикла.", "Складывать числа в rax.", "Проверить границу и повторить."],
            "solution": "section .text\n    global _start\n_start:\n    xor rax, rax\n    mov rcx, 1\nloop_start:\n    add rax, rcx\n    inc rcx\n    cmp rcx, 5\n    jle loop_start\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-data-section",
        "language": "assembly",
        "title": "Секция данных: DB, DW, DD, DQ и вычисление длины EQU",
        "topic": "Память и данные",
        "section": "Память",
        "order": 11,
        "level": "Средний",
        "minutes": 18,
        "theory": "Секция `.data` содержит статические инициализированные константы и переменные, размещаемые в памяти программы.\n\nДирективы выделения данных:\n- `db` (Define Byte): 1 байт (8 бит). Используется для символов и строк.\n- `dw` (Define Word): 2 байта (16 бит).\n- `dd` (Define Doubleword): 4 байта (32 бита).\n- `dq` (Define Quadword): 8 байтов (64 бита).\n\nСтроки объявляются байтами символов:\n`msg db \"Hello, World!\", 10, 0`\n(10 — это код перевода строки `\\n`, 0 — нуль-терминатор).\n\nАвтоматический расчет длины строки через `equ`:\nСимвол `$` в ассемблере означает текущий адрес памяти.\nВыражение `len equ $ - msg` вычисляет расстояние между текущей позицией и началом строки `msg`, давая точную длину строки во время ассемблирования!",
        "syntax": "section .data\n    msg db \"Hello!\", 10\n    len equ $ - msg\n    num dq 123456",
        "examples": [
            "section .data\n    title db \"DevForge\"\n    title_len equ $ - title"
        ],
        "task": "Объявите в секции .data строку greeting со значением 'Hello, Assembly!', символом перевода строки (код 10), и вычислите её длину с помощью greeting_len equ $ - greeting. В секции .text загрузите вычисленную длину greeting_len в регистр rdx. В тесте проверяется значение rdx (должно быть 17). Завершите программу с exit_code = 0.",
        "starterCode": "; Объявите section .data и строку greeting с вычислением длины\n\nsection .text\n    global _start\n_start:\n    ; Поместите greeting_len в rdx\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вычисленная длина строки в rdx равна 17",
                "expression": "rdx",
                "expected": 17
            }
        ],
        "hints": [
            "В начале напишите section .data.",
            "Объявите greeting db \"Hello, Assembly!\", 10.",
            "Объявите greeting_len equ $ - greeting.",
            "В секции .text напишите mov rdx, greeting_len."
        ],
        "commonMistakes": "Забыть символ $ при вычислении длины ($ - greeting); перепутать section .data и section .text.",
        "solutionExplanation": "Строка 'Hello, Assembly!' содержит 16 символов, плюс 1 символ перевода строки (код 10), итого 17 байт. Конструкция $ - greeting вычисляет 17.",
        "xp": 60,
        "setupSql": "",
        "concepts": ["section .data", "db", "dq", "equ", "$", "длина строки"],
        "walkthrough": [
            "Создайте секцию .data.",
            "Объявите greeting db 'Hello, Assembly!', 10.",
            "Определите greeting_len equ $ - greeting.",
            "В _start загрузите mov rdx, greeting_len и выйдите."
        ],
        "prerequisites": ["asm-loops"],
        "resources": [{"title": "Директивы данных в NASM", "url": "https://www.nasm.us/doc/nasmdoc3.html#section-3.2", "language": "EN"}],
        "lifeExample": "Книга с содержанием: на странице печатается текст, а внизу закладка отмечает номер страницы и длину главы.",
        "guide": {
            "version": 1,
            "idea": "Научиться объявлять статические строки и вычислять их длину через equ $ - метка.",
            "steps": ["Создать section .data.", "Объявить строку и len equ $ - str.", "Загрузить в rdx."],
            "solution": "section .data\n    greeting db \"Hello, Assembly!\", 10\n    greeting_len equ $ - greeting\n\nsection .text\n    global _start\n_start:\n    mov rdx, greeting_len\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-sys-write",
        "language": "assembly",
        "title": "Вывод текста в консоль: системный вызов sys_write",
        "topic": "Системные вызовы",
        "section": "Ввод и вывод",
        "order": 12,
        "level": "Средний",
        "minutes": 20,
        "theory": "Для вывода текста в стандартный поток вывода stdout в 64-битной Linux используется системный вызов `sys_write` (номер 1).\n\nСоглашение о вызове `sys_write`:\n- `rax = 1`: номер системного вызова `sys_write`.\n- `rdi = 1`: файловый дескриптор потока вывода (1 означает стандартный вывод `stdout`; 2 — поток ошибок `stderr`).\n- `rsi = адрес_буфера`: указатель на начало строки в памяти (метка строки).\n- `rdx = количество_байт`: сколько байт необходимо вывести.\n- `syscall`: выполнение вызова ядром.\n\nПосле возврата из `sys_write` в регистре `rax` содержится фактическое количество записанных байт.",
        "syntax": "mov rax, 1        ; sys_write\nmov rdi, 1        ; stdout\nmov rsi, msg      ; адрес строки\nmov rdx, msg_len  ; длина строки\nsyscall",
        "examples": [
            "section .data\n    msg db \"OK\", 10\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, 3\n    syscall"
        ],
        "task": "Напишите законченную программу на ассемблере x86-64 NASM, которая выводит в консоль строку 'Hello, NASM!' с символом перевода строки, а затем завершается с кодом 0 через sys_exit.",
        "starterCode": "; Реализуйте вывод строки Hello, NASM! через sys_write\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вывод строки Hello, NASM!",
                "expected": "Hello, NASM!"
            },
            {
                "id": "t2",
                "label": "Код завершения равен 0",
                "expression": "exit_code",
                "expected": 0
            }
        ],
        "hints": [
            "В section .data объявите text db \"Hello, NASM!\", 10 и text_len equ $ - text.",
            "В _start настройте sys_write: mov rax, 1; mov rdi, 1; mov rsi, text; mov rdx, text_len; syscall.",
            "После этого вызовите sys_exit: mov rax, 60; mov rdi, 0; syscall."
        ],
        "commonMistakes": "Забыть вызвать sys_exit после sys_write (процессор продолжит читать память дальше и упадет с ошибкой).",
        "solutionExplanation": "Системный вызов sys_write с дескриптором 1 передает буфер в stdout, после чего sys_exit корректно закрывает процесс.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["sys_write", "stdout", "файловый дескриптор", "syscall"],
        "walkthrough": [
            "Объявите строку и её длину в section .data.",
            "В section .text настройте параметры sys_write (rax=1, rdi=1, rsi=text, rdx=text_len).",
            "Выполните syscall.",
            "Настройте sys_exit (rax=60, rdi=0) и выполните syscall."
        ],
        "prerequisites": ["asm-data-section"],
        "resources": [{"title": "Таблица системных вызовов Linux x86-64", "url": "https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/", "language": "EN"}],
        "lifeExample": "Подача телеграммы: вы передаете телеграфисту текст, адрес получателя (stdout) и длину бланка.",
        "guide": {
            "version": 1,
            "idea": "Освоить вывод строк в стандартный вывод с помощью sys_write.",
            "steps": ["Объявить строку в .data.", "Вызвать sys_write.", "Вызвать sys_exit."],
            "solution": "section .data\n    msg db \"Hello, NASM!\", 10\n    len equ $ - msg\n\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, len\n    syscall\n\n    mov rax, 60\n    mov rdi, 0\n    syscall"
        }
    },
    {
        "id": "asm-memory-addressing",
        "language": "assembly",
        "title": "Адресация памяти и чтение по указателю",
        "topic": "Память и данные",
        "section": "Память",
        "order": 13,
        "level": "Продвинутый",
        "minutes": 20,
        "theory": "Квадратные скобки `[...]` в ассемблере означают разыменование указателя (чтение или запись значения в памяти по указанному адресу).\n\nЕсли написать `mov rax, my_var` — в регистр запишется АДРЕС метки `my_var`.\nЕсли написать `mov rax, [my_var]` — в регистр запишется ЗНАЧЕНИЕ, хранящееся по этому адресу!\n\nРежимы адресации x86-64:\n1. Прямой адрес: `[label]`\n2. Косвенный через регистр: `[rax]`\n3. База со смещением: `[rbp - 8]`, `[rsi + 16]`\n4. Сложная индексная адресация: `[base + index * scale + disp]`, где scale может быть 1, 2, 4 или 8!\nПример: `mov rax, [rdi + rsi * 8]` — идеальный способ обратиться к `i`-му элементу массива 64-битных чисел!",
        "syntax": "mov rax, [my_val]          ; прочитать 8 байт из памяти\nmov [my_val], rbx          ; записать в память\nmov cl, byte [rsi + rdx]   ; прочитать байт по смещению",
        "examples": [
            "section .data\n    arr dq 10, 20, 30\nsection .text\n    mov rax, [arr + 8] ; читает 20 (второй элемент массива)"
        ],
        "task": "В секции .data объявлен массив из трех 64-битных чисел: numbers dq 15, 27, 42. Прочитайте третий элемент массива (число 42, смещение 16 байт: [numbers + 16]) в регистр rax. Завершите программу с exit_code = 0.",
        "starterCode": "section .data\n    numbers dq 15, 27, 42\n\nsection .text\n    global _start\n_start:\n    ; Прочитайте третий элемент массива в rax\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Третий элемент массива в rax равен 42",
                "expression": "rax",
                "expected": 42
            }
        ],
        "hints": [
            "Каждый элемент dq занимает 8 байт. Первый элемент: [numbers], второй: [numbers + 8], третий: [numbers + 16].",
            "Напишите: mov rax, [numbers + 16].",
            "Завершите программу через sys_exit."
        ],
        "commonMistakes": "Использование смещения 2 вместо 16 (смещение в ассемблере задается в байтах; 2 элемента по 8 байт = 16 байт).",
        "solutionExplanation": "Директива dq выделяет по 8 байт на число. Смещение третьего элемента равно 2 * 8 = 16 байт. Разыменование [numbers + 16] считывает 42.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["квадратные скобки", "разыменование", "адресация", "смещение"],
        "walkthrough": [
            "Вычислите байтовое смещение третьего элемента: 2 * 8 = 16.",
            "Прочитайте значение: mov rax, [numbers + 16].",
            "Завершите программу с exit_code = 0."
        ],
        "prerequisites": ["asm-sys-write"],
        "resources": [{"title": "Режимы адресации в x86-64", "url": "https://www.cs.cmu.edu/~fp/courses/15213-s07/misc/asm64-handout.pdf", "language": "EN"}],
        "lifeExample": "Почтовые ячейки: numbers — это номер подъезда, а + 16 — номер квартиры, из которой вы забираете письмо.",
        "guide": {
            "version": 1,
            "idea": "Научиться считывать значения из оперативной памяти по смещению.",
            "steps": ["mov rax, [numbers + 16].", "Выйти через syscall."],
            "solution": "section .data\n    numbers dq 15, 27, 42\n\nsection .text\n    global _start\n_start:\n    mov rax, [numbers + 16]\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-stack-push-pop",
        "language": "assembly",
        "title": "Аппаратный стек процессора: PUSH и POP",
        "topic": "Стек и подпрограммы",
        "section": "Стек",
        "order": 14,
        "level": "Продвинутый",
        "minutes": 20,
        "theory": "Стек — это область оперативной памяти, работающая по принципу LIFO (Last In, First Out — последним пришел, первым ушел).\n\nКлючевая особенность x86-64: СТЕК РАСТЕТ ВНИЗ (в сторону уменьшения адресов памяти)!\nУказатель вершины стека хранится в регистре `RSP` (Stack Pointer).\n\nИнструкции для работы со стеком:\n- `push src`:\n  1. Вычитает 8 из регистра `rsp` (`rsp = rsp - 8`)\n  2. Записывает 64-битное значение `src` в память по новому адресу: `[rsp] = src`\n- `pop dst`:\n  1. Считывает 64-битное значение с вершины стека: `dst = [rsp]`\n  2. Прибавляет 8 к регистру `rsp` (`rsp = rsp + 8`)\n\nСтек используется для:\n- Временного сохранения регистров\n- Передачи адресов возврата при вызове функций (`call` / `ret`)\n- Выделения памяти под локальные переменные",
        "syntax": "push rax          ; сохранить rax в стек\npush rbx          ; сохранить rbx в стек\n\npop rbx           ; восстановить (обратный порядок!)\npop rax",
        "examples": [
            "mov rax, 10\nmov rbx, 20\npush rax\npush rbx\npop rax ; теперь rax = 20\npop rbx ; теперь rbx = 10 (обмен значений!)"
        ],
        "task": "Используя инструкции push и pop, поменяйте местами значения в регистрах rax и rbx: изначально rax = 100 и rbx = 200. После обмена через стек в rax должно оказаться 200, а в rbx — 100. Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n_start:\n    mov rax, 100\n    mov rbx, 200\n    ; Поменяйте значения местами с помощью push и pop\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Значение rax после обмена равно 200",
                "expression": "rax",
                "expected": 200
            },
            {
                "id": "t2",
                "label": "Значение rbx после обмена равно 100",
                "expression": "rbx",
                "expected": 100
            }
        ],
        "hints": [
            "Поместите сначала rax, затем rbx в стек: push rax; push rbx.",
            "Извлеките значения в обратном порядке: pop rax (заберет 200); pop rbx (заберет 100).",
            "Завершите программу через sys_exit."
        ],
        "commonMistakes": "Извлечение в том же порядке (pop rbx; pop rax сохранит исходные значения вместо обмена).",
        "solutionExplanation": "Поскольку стек работает по принципу LIFO, последнее помещенное число (200) извлекается первым в регистр rax.",
        "xp": 70,
        "setupSql": "",
        "concepts": ["стек", "push", "pop", "rsp", "LIFO"],
        "walkthrough": [
            "Инициализируйте rax = 100 и rbx = 200.",
            "Выполните push rax и push rbx.",
            "Выполните pop rax и pop rbx.",
            "Завершите программу."
        ],
        "prerequisites": ["asm-memory-addressing"],
        "resources": [{"title": "Работа со стеком в x86-64", "url": "https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_27_stack.html", "language": "EN"}],
        "lifeExample": "Стопка чистых тарелок: тарелка, положенная наверх последней, берется первой.",
        "guide": {
            "version": 1,
            "idea": "Понять принцип работы стека LIFO и инструкции push/pop.",
            "steps": ["push rax; push rbx.", "pop rax; pop rbx.", "Выйти через syscall."],
            "solution": "section .text\n    global _start\n_start:\n    mov rax, 100\n    mov rbx, 200\n    push rax\n    push rbx\n    pop rax\n    pop rbx\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-calling-convention",
        "language": "assembly",
        "title": "Функции и соглашение о вызовах System V AMD64 ABI",
        "topic": "Стек и подпрограммы",
        "section": "Функции",
        "order": 15,
        "level": "Продвинутый",
        "minutes": 22,
        "theory": "Подпрограммы (функции) в ассемблере вызываются парой инструкций:\n- `call label`:\n  1. Помещает адрес следующей инструкции (адрес возврата) в стек (`push RIP`)\n  2. Переходит по метке `label` (`jmp label`)\n- `ret`:\n  1. Извлекает адрес возврата из стека (`pop RIP`)\n  2. Возобновляет выполнение после инструкции `call`\n\nСоглашение о вызовах System V AMD64 ABI (стандарт Linux и macOS x86-64):\n1. Первые 6 целочисленных аргументов передаются строго через регистры:\n   `RDI` (1-й), `RSI` (2-й), `RDX` (3-й), `RCX` (4-й), `R8` (5-й), `R9` (6-й)\n2. Результат функции всегда возвращается в регистре `RAX`!\n3. Сохраняемые регистры (Callee-saved, функция обязана восстановить их исходное значение при выходе): `RBX`, `RSP`, `RBP`, `R12`, `R13`, `R14`, `R15`.\n4. Несохраняемые регистры (Caller-saved, функция может перезаписать их без предупреждения): `RAX`, `RCX`, `RDX`, `RSI`, `RDI`, `R8`, `R9`, `R10`, `R11`.",
        "syntax": "; Вызов функции my_add(10, 20)\nmov rdi, 10       ; 1-й аргумент\nmov rsi, 20       ; 2-й аргумент\ncall my_add\n; результат в rax!\n\nmy_add:\n    mov rax, rdi\n    add rax, rsi\n    ret",
        "examples": [
            "square:\n    mov rax, rdi\n    imul rax, rdi\n    ret"
        ],
        "task": "Реализуйте функцию square, которая принимает один аргумент в регистре rdi и возвращает его квадрат (rdi * rdi) в регистре rax. В функции _start вызовите square(9), после чего скопируйте результат из rax в rbx. Завершите программу с exit_code = 0.",
        "starterCode": "section .text\n    global _start\n\nsquare:\n    ; Вычислите квадрат rdi и верните результат в rax\n    \n    ret\n\n_start:\n    mov rdi, 9\n    call square\n    mov rbx, rax      ; сохраняем результат в rbx\n    \n    mov rdi, 0\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Квадрат числа 9 в rbx равен 81",
                "expression": "rbx",
                "expected": 81
            }
        ],
        "hints": [
            "В функции square напишите: mov rax, rdi; imul rax, rdi; ret.",
            "Инструкция call square запишет адрес возврата в стек и перейдет в square.",
            "Инструкция ret вернется обратно в _start, где rax будет равен 81."
        ],
        "commonMistakes": "Забыть инструкцию ret в конце функции (процессор не поймет, куда возвращаться, и пойдет исполнять код дальше).",
        "solutionExplanation": "Инструкция call square сохраняет RIP в стеке. Функция вычисляет 9 * 9 = 81 в RAX и возвращается по ret. В _start результат сохраняется в RBX.",
        "xp": 80,
        "setupSql": "",
        "concepts": ["call", "ret", "ABI", "System V", "rdi", "rax"],
        "walkthrough": [
            "Определите функцию square.",
            "Поместите rdi в rax и умножьте на rdi.",
            "Завершите функцию с ret.",
            "В _start передайте 9 в rdi, вызовите call square и сохраните в rbx."
        ],
        "prerequisites": ["asm-stack-push-pop"],
        "resources": [{"title": "System V AMD64 Calling Convention", "url": "https://wiki.osdev.org/System_V_ABI", "language": "EN"}],
        "lifeExample": "Служебная записка в отдел расчетов: вы передаете бланк с числом 9 курьеру (RDI), он уходит в кабинет (CALL), производит расчет и возвращает результат в папке (RAX).",
        "guide": {
            "version": 1,
            "idea": "Освоить вызов функций с передачей параметров через регистры ABI и возврат через ret.",
            "steps": ["Реализовать функцию square.", "Вызвать через call.", "Проверить результат."],
            "solution": "section .text\n    global _start\n\nsquare:\n    mov rax, rdi\n    imul rax, rdi\n    ret\n\n_start:\n    mov rdi, 9\n    call square\n    mov rbx, rax\n    mov rdi, 0\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-local-variables",
        "language": "assembly",
        "title": "Локальные переменные и стековый кадр (Stack Frame)",
        "topic": "Стек и подпрограммы",
        "section": "Функции",
        "order": 16,
        "level": "Продвинутый",
        "minutes": 22,
        "theory": "Когда функции требуются локальные переменные, память под них выделяется прямо на стеке в так называемом стековом кадре (stack frame).\n\nКлассический пролог функции (Prologue):\n```nasm\npush rbp          ; сохраняем старый указатель базы стека\nmov rbp, rsp      ; устанавливаем текущую вершину как новую базу\nsub rsp, 16       ; выделяем 16 байт под локальные переменные!\n```\nТеперь к локальным переменным можно обращаться со стабильным смещением относительно `rbp`:\n- `[rbp - 8]`: первая 64-битная локальная переменная\n- `[rbp - 16]`: вторая 64-битная локальная переменная\n\nКлассический эпилог функции (Epilogue):\n```nasm\nmov rsp, rbp      ; освобождаем выделенную локальную память\npop rbp           ; восстанавливаем исходный rbp\nret               ; возврат вызывающему коду\n```",
        "syntax": "; Пролог\npush rbp\nmov rbp, rsp\nsub rsp, 16\n\n; Работа с переменными\nmov qword [rbp - 8], 100\n\n; Эпилог\nmov rsp, rbp\npop rbp\nret",
        "examples": [
            "my_func:\n    push rbp\n    mov rbp, rsp\n    sub rsp, 16\n    mov qword [rbp-8], rdi\n    mov rax, [rbp-8]\n    mov rsp, rbp\n    pop rbp\n    ret"
        ],
        "task": "Напишите функцию sum_locals(), которая создает стековый кадр на 16 байт, сохраняет число 30 по адресу [rbp - 8], число 12 по адресу [rbp - 16], считывает их, складывает и возвращает сумму в регистре rax (30 + 12 = 42). Восстановите стек в эпилоге. В _start вызовите sum_locals, а результат сохраните в rdi для exit_code.",
        "starterCode": "section .text\n    global _start\n\nsum_locals:\n    ; 1. Пролог: push rbp; mov rbp, rsp; sub rsp, 16\n    ; 2. Запишите 30 в [rbp-8] и 12 в [rbp-16]\n    ; 3. Сложите их в rax\n    ; 4. Эпилог: mov rsp, rbp; pop rbp; ret\n\n_start:\n    call sum_locals\n    mov rdi, rax\n    mov rax, 60\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Сумма локальных переменных на стеке равна 42",
                "expression": "exit_code",
                "expected": 42
            }
        ],
        "hints": [
            "Напишите пролог: push rbp; mov rbp, rsp; sub rsp, 16.",
            "Запишите числа: mov qword [rbp - 8], 30; mov qword [rbp - 16], 12.",
            "Сложите: mov rax, [rbp - 8]; add rax, [rbp - 16].",
            "Напишите эпилог: mov rsp, rbp; pop rbp; ret."
        ],
        "commonMistakes": "Забыть mov rsp, rbp перед pop rbp (если rsp не выровнен, pop rbp снимет с вершины стека мусор, а ret упадет с ошибкой памяти).",
        "solutionExplanation": "Стековый кадр выделяет изолированную область памяти под локальные переменные функции, которая автоматически очищается в эпилоге.",
        "xp": 80,
        "setupSql": "",
        "concepts": ["stack frame", "rbp", "пролог", "эпилог", "локальные переменные"],
        "walkthrough": [
            "Сформируйте пролог функции с sub rsp, 16.",
            "Запишите локальные переменные со смещением от rbp.",
            "Сложите их в rax.",
            "Восстановите кадр в эпилоге и вернитесь.",
            "Передайте rax в rdi и завершите программу."
        ],
        "prerequisites": ["asm-calling-convention"],
        "resources": [{"title": "Стековые кадры x86-64", "url": "https://www.cs.cornell.edu/courses/cs3410/2019sp/schedule/slides/12-calling-conventions-notes.pdf", "language": "EN"}],
        "lifeExample": "Временный рабочий блокнот: при входе в комнату вы отрываете чистый лист для расчетов (sub rsp, 16), а при выходе выбрасываете его (mov rsp, rbp).",
        "guide": {
            "version": 1,
            "idea": "Освоить канонический пролог и эпилог функции для безопасного хранения локальных переменных на стеке.",
            "steps": ["Сформировать пролог.", "Записать и сложить переменные.", "Выполнить эпилог."],
            "solution": "section .text\n    global _start\n\nsum_locals:\n    push rbp\n    mov rbp, rsp\n    sub rsp, 16\n    mov qword [rbp - 8], 30\n    mov qword [rbp - 16], 12\n    mov rax, [rbp - 8]\n    add rax, [rbp - 16]\n    mov rsp, rbp\n    pop rbp\n    ret\n\n_start:\n    call sum_locals\n    mov rdi, rax\n    mov rax, 60\n    syscall"
        }
    },
    {
        "id": "asm-sys-read",
        "language": "assembly",
        "title": "Ввод данных: системный вызов sys_read",
        "topic": "Системные вызовы",
        "section": "Ввод и вывод",
        "order": 17,
        "level": "Продвинутый",
        "minutes": 22,
        "theory": "Для чтения данных из стандартного потока ввода stdin в Linux x86-64 используется системный вызов `sys_read` (номер 0).\n\nПараметры `sys_read`:\n- `rax = 0`: номер системного вызова `sys_read`\n- `rdi = 0`: файловый дескриптор потока ввода (0 означает `stdin`)\n- `rsi = адрес_буфера`: указатель на выделенный буфер в памяти (в секции `.bss` или `.data`)\n- `rdx = максимальный_размер`: сколько максимум байт можно прочитать в буфер\n- `syscall`: выполнение вызова\n\nВозвращаемое значение:\nПосле выполнения `sys_read` в регистре `rax` возвращается ФАКТИЧЕСКОЕ КОЛИЧЕСТВО ПРОЧИТАННЫХ БАЙТ! Если поток закрыт (EOF), `rax` вернет 0.",
        "syntax": "section .bss\n    buffer resb 64\n\nsection .text\n    mov rax, 0        ; sys_read\n    mov rdi, 0        ; stdin\n    mov rsi, buffer   ; буфер для ввода\n    mov rdx, 64       ; размер буфера\n    syscall\n    ; в rax теперь количество прочитанных байт!",
        "examples": [
            "mov rax, 0\nmov rdi, 0\nmov rsi, buf\nmov rdx, 32\nsyscall"
        ],
        "task": "Напишите программу, которая считывает имя пользователя из stdin через sys_read в буфер buffer (размер 64 байта), а затем выводит прочитанное имя обратно в консоль через sys_write (используя количество фактически прочитанных байт из rax!). При вводе 'DevForge' программа должна вывести 'DevForge'.",
        "starterCode": "; Прочитайте строку из stdin и выведите её в stdout\nsection .bss\n    buffer resb 64\n\nsection .text\n    global _start\n_start:\n    ; 1. Вызовите sys_read в buffer\n    ; 2. Вызовите sys_write из buffer\n    ; 3. Вызовите sys_exit\n",
        "tests": [
            {
                "id": "t1",
                "label": "Чтение и эхо-вывод строки",
                "stdin": "DevForge",
                "expected": "DevForge"
            }
        ],
        "hints": [
            "Для sys_read: mov rax, 0; mov rdi, 0; mov rsi, buffer; mov rdx, 64; syscall.",
            "Сохраните количество прочитанных байт в rdx для вывода: mov rdx, rax.",
            "Для sys_write: mov rax, 1; mov rdi, 1; mov rsi, buffer; syscall.",
            "Завершите программу: mov rax, 60; mov rdi, 0; syscall."
        ],
        "commonMistakes": "Забыть, что sys_read возвращает длину в rax, и перезаписать rax до того, как скопировать длину в rdx.",
        "solutionExplanation": "sys_read заполняет буфер и возвращает число прочитанных байт в rax, которое сразу передается в rdx для вызова sys_write.",
        "xp": 80,
        "setupSql": "",
        "concepts": ["sys_read", "stdin", "section .bss", "resb", "буфер"],
        "walkthrough": [
            "Выполните sys_read в buffer.",
            "Скопируйте полученную длину из rax в rdx.",
            "Выполните sys_write для вывода buffer.",
            "Завершите программу через sys_exit."
        ],
        "prerequisites": ["asm-sys-write"],
        "resources": [{"title": "Ввод-вывод в Linux на x86-64", "url": "https://cs.lmu.edu/~ray/notes/nasmtutorial/", "language": "EN"}],
        "lifeExample": "Почтовый ящик: sys_read забирает входящие письма в корзину и сообщает точное число полученных писем.",
        "guide": {
            "version": 1,
            "idea": "Научиться считывать пользовательский ввод через sys_read и передавать в sys_write.",
            "steps": ["Считать через sys_read.", "Вывести через sys_write.", "Выйти через syscall."],
            "solution": "section .bss\n    buffer resb 64\n\nsection .text\n    global _start\n_start:\n    mov rax, 0\n    mov rdi, 0\n    mov rsi, buffer\n    mov rdx, 64\n    syscall\n\n    mov rdx, rax\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, buffer\n    syscall\n\n    mov rax, 60\n    mov rdi, 0\n    syscall"
        }
    },
    {
        "id": "asm-project-string-lib",
        "language": "assembly",
        "title": "Итоговый проект: Низкоуровневая библиотека strlen и print_str",
        "topic": "Итоговый проект",
        "section": "Проекты",
        "order": 18,
        "level": "Продвинутый",
        "minutes": 35,
        "theory": "Поздравляем с выходом на итоговый проект трека Ассемблер x86-64!\nВ этом проекте вы реализуете настоящую низкоуровневую библиотеку строковых процедур на чистом x86-64 NASM:\n\n1. Функция `strlen(str_ptr)`:\n- Принимает указатель на нуль-терминированную строку в регистре `rdi`.\n- Проходит по байтам строки в цикле, пока не встретит нулевой байт `0`.\n- Возвращает точную длину строки в регистре `rax`.\n\n2. Функция `print_str(str_ptr)`:\n- Принимает указатель на строку в `rdi`.\n- Сохраняет `rdi` в стек или callee-saved регистр.\n- Вызывает `strlen(rdi)` для вычисления точной длины.\n- Выполняет системный вызов `sys_write(1, str_ptr, length)`.\n- Корректно восстанавливает стек и возвращается через `ret`.\n\n3. Главная программа `_start`:\n- Вызывает `print_str` для строки `\"DevForge x86-64 Assembly OK!\\n\"`.\n- Завершает процесс с кодом `0`.",
        "syntax": "; Алгоритм strlen:\nxor rax, rax\n.loop:\ncmp byte [rdi + rax], 0\nje .done\ninc rax\njmp .loop\n.done:\nret",
        "examples": [
            "mov rdi, msg\ncall print_str"
        ],
        "task": "Реализуйте функцию strlen(rdi) -> rax, вычисляющую длину нуль-терминированной строки, и функцию print_str(rdi), которая с помощью strlen вычисляет длину и выводит строку в stdout через sys_write. В _start выведите строку 'DevForge x86-64 Assembly OK!' (с переводом строки 10 и нулем 0) и завершите программу с exit_code = 0.",
        "starterCode": "; Итоговый проект: Строковая библиотека на x86-64 NASM\nsection .data\n    msg db \"DevForge x86-64 Assembly OK!\", 10, 0\n\nsection .text\n    global _start\n\n; Реализуйте strlen(rdi) -> rax\nstrlen:\n    ret\n\n; Реализуйте print_str(rdi)\nprint_str:\n    ret\n\n_start:\n    mov rdi, msg\n    call print_str\n\n    mov rax, 60\n    mov rdi, 0\n    syscall\n",
        "tests": [
            {
                "id": "t1",
                "label": "Вывод строки через библиотечную функцию print_str",
                "expected": "DevForge x86-64 Assembly OK!"
            },
            {
                "id": "t2",
                "label": "Код возврата равен 0",
                "expression": "exit_code",
                "expected": 0
            }
        ],
        "hints": [
            "В strlen: xor rax, rax; .loop: cmp byte [rdi + rax], 0; je .done; inc rax; jmp .loop; .done: ret.",
            "В print_str: push rdi; call strlen; mov rdx, rax; pop rsi; mov rax, 1; mov rdi, 1; syscall; ret.",
            "В _start передайте mov rdi, msg и вызовите call print_str."
        ],
        "commonMistakes": "Потеря указателя на строку rdi при вызове strlen (strlen использует rdi, поэтому перед вызовом strlen нужно сохранить rdi на стеке push rdi, а затем извлечь в rsi pop rsi для sys_write).",
        "solutionExplanation": "Функция strlen находит нулевой терминатор, возвращая точный размер строки. Функция print_str передает адрес и размер в системный вызов sys_write ядра ОС.",
        "xp": 150,
        "setupSql": "",
        "concepts": ["Итоговый проект", "strlen", "print_str", "нуль-терминатор", "сохранение регистров"],
        "walkthrough": [
            "Реализуйте цикл strlen со счетчиком в rax.",
            "Реализуйте print_str: сохраните указатель строки, вызовите strlen, передайте длину в rdx и адрес в rsi для sys_write.",
            "Вызовите print_str в точке входа _start.",
            "Завершите программу через sys_exit с кодом 0."
        ],
        "prerequisites": ["asm-sys-read"],
        "resources": [{"title": "Реализация libc функций на ассемблере x86-64", "url": "https://github.com/bminor/glibc/tree/master/sysdeps/x86_64", "language": "EN"}],
        "lifeExample": "Стандартная библиотека C (glibc): функции strlen и puts в glibc написаны именно на ассемблере x86-64 для достижения абсолютной предельной скорости процессора.",
        "guide": {
            "version": 1,
            "idea": "Создать законченную библиотеку строковых процедур на ассемблере x86-64.",
            "steps": ["Реализовать strlen.", "Реализовать print_str через sys_write.", "Проверить вывод."],
            "solution": "section .data\n    msg db \"DevForge x86-64 Assembly OK!\", 10, 0\n\nsection .text\n    global _start\n\nstrlen:\n    xor rax, rax\n.loop:\n    cmp byte [rdi + rax], 0\n    je .done\n    inc rax\n    jmp .loop\n.done:\n    ret\n\nprint_str:\n    push rdi\n    call strlen\n    mov rdx, rax\n    pop rsi\n    mov rax, 1\n    mov rdi, 1\n    syscall\n    ret\n\n_start:\n    mov rdi, msg\n    call print_str\n\n    mov rax, 60\n    mov rdi, 0\n    syscall"
        }
    }
]
