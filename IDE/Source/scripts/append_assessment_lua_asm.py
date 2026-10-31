import json

LUA_QUESTIONS = [
    {
        "id": "lua-q1",
        "language": "lua",
        "tag": "start",
        "text": "С какого индекса по умолчанию начинается индексация массивов (таблиц) в языке Lua?",
        "options": [
            "С 1",
            "С 0",
            "С -1"
        ],
        "correct": 0,
        "explanation": "В Lua индексы последовательностей и массивов начинаются с 1, в отличие от C или Python."
    },
    {
        "id": "lua-q2",
        "language": "lua",
        "tag": "basics",
        "text": "Какое ключевое слово используется для объявления локальной переменной в Lua?",
        "options": [
            "local",
            "let",
            "var"
        ],
        "correct": 0,
        "explanation": "В Lua переменные по умолчанию глобальны; для объявления локальной области видимости используется ключевое слово local."
    },
    {
        "id": "lua-q3",
        "language": "lua",
        "tag": "strings",
        "text": "Какой оператор используется для конкатенации (склеивания) строк в Lua?",
        "options": [
            ".. (две точки)",
            "+ (плюс)",
            "& (амперсанд)"
        ],
        "correct": 0,
        "explanation": "В Lua оператор сложения '+' выполняет числовое сложение, а конкатенация строк выполняется оператором '..'."
    },
    {
        "id": "lua-q4",
        "language": "lua",
        "tag": "tables",
        "text": "Какая функция стандартной библиотеки используется для перебора пар 'ключ-значение' в таблице?",
        "options": [
            "pairs()",
            "ipairs()",
            "table.keys()"
        ],
        "correct": 0,
        "explanation": "pairs(t) перебирает все ключи таблицы (включая строковые), а ipairs(t) перебирает только числовую последовательность 1..n."
    },
    {
        "id": "lua-q5",
        "language": "lua",
        "tag": "operators",
        "text": "Какой оператор возвращает длину таблицы или строки в Lua?",
        "options": [
            "# (решетка)",
            "len()",
            ".length"
        ],
        "correct": 0,
        "explanation": "Унарный оператор длины '#' возвращает длину строки в байтах или количество элементов в числовой последовательности таблицы."
    },
    {
        "id": "lua-q6",
        "language": "lua",
        "tag": "functions",
        "text": "Может ли функция в Lua возвращать несколько значений одновременно?",
        "options": [
            "Да, через запятую в return a, b",
            "Нет, только одно значение или массив",
            "Только если возвращаются числа"
        ],
        "correct": 0,
        "explanation": "Lua нативно поддерживает множественный возврат значений: function f() return 1, 2 end; local x, y = f()."
    },
    {
        "id": "lua-q7",
        "language": "lua",
        "tag": "oop",
        "text": "Какое метаполе в метатаблице отвечает за поиск недостающих ключей и реализацию ООП-наследования?",
        "options": [
            "__index",
            "__newindex",
            "__call"
        ],
        "correct": 0,
        "explanation": "Метаметод __index вызывается, когда запрашиваемый ключ отсутствует в основной таблице, что лежит в основе ООП в Lua."
    },
    {
        "id": "lua-q8",
        "language": "lua",
        "tag": "advanced",
        "text": "С помощью какого механизма в Lua реализуется кооперативная многозадачность?",
        "options": [
            "Корутины (coroutine.create, coroutine.yield, coroutine.resume)",
            "Системные потоки pthread",
            "Event Loop промисов"
        ],
        "correct": 0,
        "explanation": "Корутины в Lua — это легковесные сопрограммы с явной передачей управления через yield и resume."
    }
]

ASSEMBLY_QUESTIONS = [
    {
        "id": "asm-q1",
        "language": "assembly",
        "tag": "start",
        "text": "Какую разрядность имеют регистры RAX, RBX, RCX, RDX в архитектуре x86-64?",
        "options": [
            "64 бита (8 байт)",
            "32 бита (4 байта)",
            "128 бит (16 байт)"
        ],
        "correct": 0,
        "explanation": "Префикс 'R' в x86-64 обозначает 64-битные регистры общего назначения (RAX, RBX, RCX, RDX, RSI, RDI, RSP, RBP, R8-R15)."
    },
    {
        "id": "asm-q2",
        "language": "assembly",
        "tag": "registers",
        "text": "Какая младшая 32-битная часть соответствует 64-битному регистру RAX?",
        "options": [
            "EAX",
            "AX",
            "AL"
        ],
        "correct": 0,
        "explanation": "RAX — 64 бита, EAX — младшие 32 бита, AX — младшие 16 бит, AL — младшие 8 бит."
    },
    {
        "id": "asm-q3",
        "language": "assembly",
        "tag": "instructions",
        "text": "Что выполняет инструкция `mov rax, 42`?",
        "options": [
            "Записывает число 42 в регистр RAX",
            "Сравнивает значение RAX с числом 42",
            "Складывает RAX с 42"
        ],
        "correct": 0,
        "explanation": "Инструкция mov (move) копирует операнд-источник в операнд-приёмник (первый аргумент в синтаксисе NASM/Intel)."
    },
    {
        "id": "asm-q4",
        "language": "assembly",
        "tag": "control-flow",
        "text": "Какая пара инструкций обычно используется для условного перехода по равенству?",
        "options": [
            "cmp a, b затем je метка (jump if equal)",
            "mov a, b затем jmp метка",
            "xor a, b затем call метка"
        ],
        "correct": 0,
        "explanation": "cmp выполняет вычитание и выставляет флаги (включая ZF — Zero Flag), а je выполняет переход, если ZF = 1 (числа равны)."
    },
    {
        "id": "asm-q5",
        "language": "assembly",
        "tag": "stack",
        "text": "Какая инструкция помещает 64-битное значение на вершину аппаратного стека?",
        "options": [
            "push",
            "pop",
            "load"
        ],
        "correct": 0,
        "explanation": "Инструкция push уменьшает указатель стека RSP на 8 байт и записывает значение в память по адресу [RSP]."
    },
    {
        "id": "asm-q6",
        "language": "assembly",
        "tag": "functions",
        "text": "Какая инструкция завершает подпрограмму и возвращает управление в точку вызова?",
        "options": [
            "ret",
            "exit",
            "leave"
        ],
        "correct": 0,
        "explanation": "Инструкция ret (return) извлекает из вершины стека сохраненный адрес возврата и передает на него управление."
    },
    {
        "id": "asm-q7",
        "language": "assembly",
        "tag": "syscalls",
        "text": "Какой номер системного вызова (syscall) в Linux x86-64 соответствует sys_write?",
        "options": [
            "1 (в RAX)",
            "0 (в RAX)",
            "60 (в RAX)"
        ],
        "correct": 0,
        "explanation": "В таблице системных вызовов Linux x86-64: RAX=0 — sys_read, RAX=1 — sys_write, RAX=60 — sys_exit."
    },
    {
        "id": "asm-q8",
        "language": "assembly",
        "tag": "optimization",
        "text": "Какой идиоматичный и быстрый способ обнулить регистр в x86 ассемблере без лишних байт кода?",
        "options": [
            "xor rax, rax",
            "mov rax, 0",
            "sub rax, rax"
        ],
        "correct": 0,
        "explanation": "Инструкция `xor eax, eax` (или xor rax, rax) занимает меньше байт в машинном коде и эффективно распознается декодером процессора."
    }
]

def append_assessment():
    path = 'content/assessment.json'
    items = json.load(open(path, 'r', encoding='utf-8'))
    existing_ids = {x['id'] for x in items}

    added = 0
    for q in LUA_QUESTIONS + ASSEMBLY_QUESTIONS:
        if q['id'] not in existing_ids:
            items.append(q)
            existing_ids.add(q['id'])
            added += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Appended {added} assessment questions. Total questions: {len(items)} across {len({x['language'] for x in items})} languages.")

if __name__ == '__main__':
    append_assessment()
