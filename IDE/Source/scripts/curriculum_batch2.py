# -*- coding: utf-8 -*-
"""
Curriculum Batch 2: Merging C++, C#, Objective-C, Rust, and 1C
Adds 87 new lessons (total 309), 87 solutions (total 309), 87 documentation articles (total 309),
and 40 assessment questions (8 for each of the 5 new languages, total 104 questions across 13 languages).
"""

import os
import sys
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(CURRENT_DIR)

import lessons_cpp
import lessons_csharp
import lessons_objc
import lessons_rust
import lessons_1c

ALL_NEW_LESSONS = (
    lessons_cpp.LESSONS +
    lessons_csharp.LESSONS +
    lessons_objc.LESSONS +
    lessons_rust.LESSONS +
    lessons_1c.LESSONS
)

def validate_pedagogy(lessons):
    errors = []
    ids = set()
    for l in lessons:
        lid = l["id"]
        if lid in ids:
            errors.append(f"Duplicate lesson id: {lid}")
        ids.add(lid)

        guide = l.get("guide", {})
        idea = guide.get("idea", "")
        if len(idea) < 150:
            errors.append(f"{lid}: idea length ({len(idea)}) is less than 150 characters")
        if not l.get("lifeExample"):
            errors.append(f"{lid}: missing lifeExample")
        if not guide.get("terms"):
            errors.append(f"{lid}: missing terms")
        if not guide.get("solution"):
            errors.append(f"{lid}: missing solution")
        if not guide.get("example") or not guide["example"].get("code"):
            errors.append(f"{lid}: missing example code")
        if not l.get("tests"):
            errors.append(f"{lid}: missing tests")
    return errors

# Assessment questions for the 5 new languages (8 per language = 40 total)
ASSESSMENT_NEW = [
    # C++ (8 questions)
    {
        "id": "cpp-q1", "language": "cpp", "tag": "start",
        "text": "Какой поток используется в стандартной библиотеке C++ для вывода текста в консоль?",
        "options": ["std::cout", "std::cin", "std::print", "Console.Write"],
        "correct": 0, "explanation": "std::cout (character output) направляет символы в стандартный поток вывода через оператор <<."
    },
    {
        "id": "cpp-q2", "language": "cpp", "tag": "start",
        "text": "Каким оператором данные направляются в поток std::cout?",
        "options": ["<<", ">>", "<-", "->"],
        "correct": 0, "explanation": "Оператор << направляет поток данных в std::cout."
    },
    {
        "id": "cpp-q3", "language": "cpp", "tag": "start",
        "text": "Что означает модификатор const перед типом переменной в C++?",
        "options": ["Значение переменной нельзя изменять после инициализации", "Переменная хранится в динамической куче", "Переменная видна только внутри функции main", "Значение переменной всегда равно нулю"],
        "correct": 0, "explanation": "Ключевое слово const гарантирует неизменяемость значения переменной."
    },
    {
        "id": "cpp-q4", "language": "cpp", "tag": "start",
        "text": "Какой символ используется для объявления ссылки на переменную в C++?",
        "options": ["&", "*", "@", "#"],
        "correct": 0, "explanation": "Символ & используется для создания ссылки (псевдонима существующей переменной)."
    },
    {
        "id": "cpp-q5", "language": "cpp", "tag": "start",
        "text": "Какой контейнер STL представляет собой динамический массив в C++?",
        "options": ["std::vector", "std::array", "std::list", "std::map"],
        "correct": 0, "explanation": "std::vector — это последовательный динамический массив с автоматическим выделением памяти."
    },
    {
        "id": "cpp-q6", "language": "cpp", "tag": "start",
        "text": "Какая секция видимости в классе C++ делает члены доступными только внутри класса?",
        "options": ["private", "public", "protected", "internal"],
        "correct": 0, "explanation": "Секция private скрывает поля и методы от внешнего доступа."
    },
    {
        "id": "cpp-q7", "language": "cpp", "tag": "start",
        "text": "Как вызвать метод push_back у вектора std::vector<int> v?",
        "options": ["v.push_back(10);", "v->push_back(10);", "push_back(v, 10);", "v.add(10);"],
        "correct": 0, "explanation": "Метод push_back вызывается через точку для добавления элемента в конец вектора."
    },
    {
        "id": "cpp-q8", "language": "cpp", "tag": "start",
        "text": "Для чего служат шаблоны функций (template<typename T>) в C++?",
        "options": ["Для написания обобщенного кода, работающего с любыми типами", "Для ускорения компиляции программы", "Для создания графического интерфейса", "Для работы с файловой системой"],
        "correct": 0, "explanation": "Шаблоны позволяют параметризовать функции и классы типами данных."
    },

    # C# (8 questions)
    {
        "id": "csharp-q1", "language": "csharp", "tag": "start",
        "text": "Какой статический метод класса Console выводит строку с переводом курсора в C#?",
        "options": ["Console.WriteLine", "Console.Write", "Console.Print", "System.Out.Println"],
        "correct": 0, "explanation": "Console.WriteLine выводит текст и завершает строку символом перевода строки."
    },
    {
        "id": "csharp-q2", "language": "csharp", "tag": "start",
        "text": "Какой символ ставится перед строкой для использования интерполяции в C#?",
        "options": ["$", "@", "#", "&"],
        "correct": 0, "explanation": "Знак доллара $\"текст {переменная}\" включает механизм строковой интерполяции."
    },
    {
        "id": "csharp-q3", "language": "csharp", "tag": "start",
        "text": "Какой тип данных используется в C# для хранения логических значений true и false?",
        "options": ["bool", "boolean", "int", "BooleanValue"],
        "correct": 0, "explanation": "В языке C# базовый булев тип обозначается ключевым словом bool."
    },
    {
        "id": "csharp-q4", "language": "csharp", "tag": "start",
        "text": "С помощью какого цикла безопаснее всего перебрать все элементы коллекции в C#?",
        "options": ["foreach", "for", "while", "repeat"],
        "correct": 0, "explanation": "foreach последовательно перебирает элементы коллекции без риска выхода за границы массива."
    },
    {
        "id": "csharp-q5", "language": "csharp", "tag": "start",
        "text": "Какое свойство возвращает размер массива int[] arr в C#?",
        "options": ["arr.Length", "arr.Count", "arr.Size()", "arr.Length()"],
        "correct": 0, "explanation": "Массивы в .NET имеют встроенное свойство Length, возвращающее общее количество элементов."
    },
    {
        "id": "csharp-q6", "language": "csharp", "tag": "start",
        "text": "Какой класс из System.Collections.Generic реализует динамический список?",
        "options": ["List<T>", "ArrayList", "Vector<T>", "DynamicArray"],
        "correct": 0, "explanation": "List<T> — стандартная обобщенная коллекция динамического списка."
    },
    {
        "id": "csharp-q7", "language": "csharp", "tag": "start",
        "text": "Что представляют собой автоматические свойства { get; set; } в C#?",
        "options": ["Свойства с автоматически сгенерированным компилятором скрытым полем", "Методы, доступные только для чтения", "Глобальные константы класса", "Функции обратного вызова"],
        "correct": 0, "explanation": "Автоматические свойства избавляют от необходимости вручную объявлять приватные backing-поля."
    },
    {
        "id": "csharp-q8", "language": "csharp", "tag": "start",
        "text": "Как называется специальный метод класса, имя которого совпадает с именем класса?",
        "options": ["Конструктор", "Деструктор", "Инициализатор", "Фабрика"],
        "correct": 0, "explanation": "Конструктор автоматически вызывается при создании нового экземпляра оператором new."
    },

    # Objective-C (8 questions)
    {
        "id": "objc-q1", "language": "objc", "tag": "start",
        "text": "Какая функция Foundation используется для вывода сообщений в консоль в Objective-C?",
        "options": ["NSLog", "printf", "Console.Log", "System.print"],
        "correct": 0, "explanation": "NSLog — стандартная функция логирования фреймворка Foundation."
    },
    {
        "id": "objc-q2", "language": "objc", "tag": "start",
        "text": "Какой префикс используется перед строковыми литералами NSString?",
        "options": ["@", "$", "#", "&"],
        "correct": 0, "explanation": "Символ @ перед кавычками @\"...\" создает объект NSString вместо const char*."
    },
    {
        "id": "objc-q3", "language": "objc", "tag": "start",
        "text": "Какой спецификатор формата в NSLog используется для отображения объектов Objective-C?",
        "options": ["%@", "%d", "%s", "%o"],
        "correct": 0, "explanation": "Спецификатор %@ выводит строковое описание объекта (метод description)."
    },
    {
        "id": "objc-q4", "language": "objc", "tag": "start",
        "text": "Какими скобками оформляется отправка сообщения объекту [получатель сообщение]?",
        "options": ["Квадратными [ ]", "Круглыми ( )", "Фигурными { }", "Угловыми < >"],
        "correct": 0, "explanation": "В синтаксисе Smalltalk Objective-C посылка сообщения оформляется квадратными скобками [obj msg]."
    },
    {
        "id": "objc-q5", "language": "objc", "tag": "start",
        "text": "Что обозначает знак минус (-) в объявлении метода в Objective-C?",
        "options": ["Метод экземпляра объекта", "Метод класса (статический)", "Приватный метод", "Удаленный метод"],
        "correct": 0, "explanation": "Знак минус указывает на метод экземпляра, а знак плюс (+) — на метод класса."
    },
    {
        "id": "objc-q6", "language": "objc", "tag": "start",
        "text": "Какая директива объявляет свойства класса с автоматическими геттерами и сеттерами?",
        "options": ["@property", "@synthesize", "@interface", "@dynamic"],
        "correct": 0, "explanation": "Директива @property объявляет открытое свойство объекта."
    },
    {
        "id": "objc-q7", "language": "objc", "tag": "start",
        "text": "Какой класс фреймворка Foundation используется для неизменяемого массива?",
        "options": ["NSArray", "NSMutableArray", "Vector", "List"],
        "correct": 0, "explanation": "NSArray представляет неизменяемый упорядоченный список объектов в Cocoa."
    },
    {
        "id": "objc-q8", "language": "objc", "tag": "start",
        "text": "Что произойдет при отправке сообщения объекту, равному nil в Objective-C?",
        "options": ["Вызов безопасно проигнорируется, программа продолжит работу", "Программа немедленно завершится с ошибкой NullPointerException", "Возникнет исключение компилятора", "Объект автоматически создастся"],
        "correct": 0, "explanation": "В рантайме Objective-C отправка сообщений nil безопасна и возвращает ноль / nil без сбоя."
    },

    # Rust (8 questions)
    {
        "id": "rust-q1", "language": "rust", "tag": "start",
        "text": "Какой макрос используется в Rust для вывода строки в консоль с переводом строки?",
        "options": ["println!", "print!", "console.log!", "fmt::println"],
        "correct": 0, "explanation": "Макрос println! форматирует и печатает строку в стандартный вывод."
    },
    {
        "id": "rust-q2", "language": "rust", "tag": "start",
        "text": "Каковы переменные в Rust по умолчанию при объявлении через let?",
        "options": ["Неизменяемые (immutable)", "Изменяемые (mutable)", "Глобальные", "Статические"],
        "correct": 0, "explanation": "По умолчанию все переменные в Rust неизменяемы для гарантии безопасности."
    },
    {
        "id": "rust-q3", "language": "rust", "tag": "start",
        "text": "Какое ключевое слово делает переменную изменяемой в Rust?",
        "options": ["mut", "var", "mutable", "change"],
        "correct": 0, "explanation": "Ключевое слово mut разрешает модификацию значения переменной: let mut x = 5;"
    },
    {
        "id": "rust-q4", "language": "rust", "tag": "start",
        "text": "Какой плейсхолдер используется внутри форматирующей строки println!?",
        "options": ["{}", "%s", "$1", "<>"],
        "correct": 0, "explanation": "Фигурные скобки {} служат позиционным плейсхолдером для подстановки значений."
    },
    {
        "id": "rust-q5", "language": "rust", "tag": "start",
        "text": "Как вернуть значение из функции в Rust без использования слова return?",
        "options": ["Написать выражение последней строкой без точки с запятой", "Поставить точку с запятой в конце", "Указать стрелку ->", "Rust требует return обязательно"],
        "correct": 0, "explanation": "Хвостовое выражение (без точки с запятой) автоматически становится результатом функции."
    },
    {
        "id": "rust-q6", "language": "rust", "tag": "start",
        "text": "Какой символ используется для создания неизменяемой ссылки (заимствования) в Rust?",
        "options": ["&", "*", "ref", "@"],
        "correct": 0, "explanation": "Символ & создает заимствованную ссылку на значение без передачи владения."
    },
    {
        "id": "rust-q7", "language": "rust", "tag": "start",
        "text": "Какой макрос используется для удобной инициализации вектора в Rust?",
        "options": ["vec![...]", "array![...]", "new_vec(...)", "Vector::new[...]"],
        "correct": 0, "explanation": "Макрос vec![1, 2, 3] создает динамический вектор с начальными элементами."
    },
    {
        "id": "rust-q8", "language": "rust", "tag": "start",
        "text": "Какая конструкция используется для исчерпывающего сопоставления с образцом в Rust?",
        "options": ["match", "switch", "when", "case"],
        "correct": 0, "explanation": "Конструкция match проверяет все возможные шаблоны значений выражения."
    },

    # 1C (8 questions)
    {
        "id": "1c-q1", "language": "1c", "tag": "start",
        "text": "Какая встроенная процедура используется в языке 1С для вывода сообщений?",
        "options": ["Сообщить()", "Печать()", "Вывести()", "Console.Write()"],
        "correct": 0, "explanation": "Процедура Сообщить('...') выводит переданный текст в служебное окно сообщений 1С."
    },
    {
        "id": "1c-q2", "language": "1c", "tag": "start",
        "text": "Какими ключевыми словами оформляется блок условного оператора в 1С?",
        "options": ["Если ... Тогда ... КонецЕсли;", "Если ... То ... Конец;", "If ... Then ... EndIf;", "Пока ... Тогда ... Конец;"],
        "correct": 0, "explanation": "В 1С условие всегда открывается 'Если ... Тогда' и закрывается 'КонецЕсли;'."
    },
    {
        "id": "1c-q3", "language": "1c", "tag": "start",
        "text": "Каковы литералы логического типа Булево в языке 1С?",
        "options": ["Истина и Ложь", "Да и Нет", "True и False", "Вкл и Выкл"],
        "correct": 0, "explanation": "В 1С значениями булева типа являются литералы Истина и Ложь."
    },
    {
        "id": "1c-q4", "language": "1c", "tag": "start",
        "text": "Какая встроенная функция 1С преобразует текст в верхний регистр (заглавные буквы)?",
        "options": ["ВРег()", "НРег()", "СтрДлина()", "Верхний()"],
        "correct": 0, "explanation": "Функция ВРег(Строка) переводит все символы строки в верхний регистр."
    },
    {
        "id": "1c-q5", "language": "1c", "tag": "start",
        "text": "Как создать новый динамический массив в языке 1С?",
        "options": ["Новый Массив", "Создать Массив()", "new Array()", "Массив.Новый()"],
        "correct": 0, "explanation": "Оператор 'Новый' с типом 'Массив' создает экземпляр одномерной динамической коллекции."
    },
    {
        "id": "1c-q6", "language": "1c", "tag": "start",
        "text": "Какой метод добавляет новое свойство в коллекцию Структура в 1С?",
        "options": ["Вставить()", "Добавить()", "Присвоить()", "Установить()"],
        "correct": 0, "explanation": "У структуры метод Вставить('Имя', Значение) создает или обновляет именованное свойство."
    },
    {
        "id": "1c-q7", "language": "1c", "tag": "start",
        "text": "Какая конструкция предназначена для последовательного обхода элементов коллекции в 1С?",
        "options": ["Для Каждого Элемент Из Коллекция Цикл ... КонецЦикла;", "Для Сч = 1 По 10 Цикл", "Пока Истина Цикл", "Перебор Коллекция"],
        "correct": 0, "explanation": "Конструкция 'Для Каждого ... Из ... Цикл' безопасно перебирает элементы коллекций 1С."
    },
    {
        "id": "1c-q8", "language": "1c", "tag": "start",
        "text": "Какой объект 1С представляет собой таблицу в памяти с динамическими колонками и строками?",
        "options": ["ТаблицаЗначений", "СписокЗначений", "МассивТаблиц", "НаборДанных"],
        "correct": 0, "explanation": "ТаблицаЗначений — универсальная коллекция 1С для работы с двумерными строками и колонками."
    }
]

def main():
    print("=== Validating new lessons pedagogy ===")
    pedagogy_errors = validate_pedagogy(ALL_NEW_LESSONS)
    if pedagogy_errors:
        print(f"Validation FAILED with {len(pedagogy_errors)} errors:")
        for err in pedagogy_errors[:10]:
            print(" -", err)
        sys.exit(1)
    print(f"Pedagogy check PASSED for all {len(ALL_NEW_LESSONS)} new lessons!")

    # 1. Update content/lessons.json
    lessons_path = os.path.join(BASE_DIR, "content", "lessons.json")
    with open(lessons_path, "r", encoding="utf-8") as f:
        existing_lessons = json.load(f)
    print(f"Existing lessons count: {len(existing_lessons)}")

    existing_ids = {l["id"] for l in existing_lessons}
    new_to_add = [l for l in ALL_NEW_LESSONS if l["id"] not in existing_ids]
    print(f"New lessons to add: {len(new_to_add)}")

    combined_lessons = existing_lessons + new_to_add
    with open(lessons_path, "w", encoding="utf-8") as f:
        json.dump(combined_lessons, f, ensure_ascii=False, indent=2)
    print(f"Updated content/lessons.json (total: {len(combined_lessons)})")

    # 2. Update frontend/tests/solutions.json
    sols_path = os.path.join(BASE_DIR, "frontend", "tests", "solutions.json")
    with open(sols_path, "r", encoding="utf-8") as f:
        existing_sols = json.load(f)
    print(f"Existing solutions count: {len(existing_sols)}")

    for l in ALL_NEW_LESSONS:
        lid = l["id"]
        sol = l.get("guide", {}).get("solution") or l.get("starterCode")
        existing_sols[lid] = sol

    with open(sols_path, "w", encoding="utf-8") as f:
        json.dump(existing_sols, f, ensure_ascii=False, indent=2)
    print(f"Updated frontend/tests/solutions.json (total: {len(existing_sols)})")

    # 3. Update content/documentation.json
    docs_path = os.path.join(BASE_DIR, "content", "documentation.json")
    with open(docs_path, "r", encoding="utf-8") as f:
        existing_docs = json.load(f)
    print(f"Existing docs count: {len(existing_docs)}")

    existing_doc_ids = {d["id"] for d in existing_docs}
    for l in ALL_NEW_LESSONS:
        lid = l["id"]
        if lid not in existing_doc_ids:
            doc_entry = {
                "id": lid,
                "title": f"{l['language'].upper()}: {l['title']}",
                "language": l["language"],
                "category": l["section"],
                "explanation": l.get("guide", {}).get("idea", l.get("theory", "")),
                "syntax": l.get("syntax", ""),
                "example": l.get("examples", [""])[0],
                "mistakes": l.get("commonMistakes", "Следите за синтаксисом и типами данных."),
                "relatedLessons": [lid]
            }
            existing_docs.append(doc_entry)

    with open(docs_path, "w", encoding="utf-8") as f:
        json.dump(existing_docs, f, ensure_ascii=False, indent=2)
    print(f"Updated content/documentation.json (total: {len(existing_docs)})")

    # 4. Update content/assessment.json
    assess_path = os.path.join(BASE_DIR, "content", "assessment.json")
    with open(assess_path, "r", encoding="utf-8") as f:
        existing_assess = json.load(f)
    print(f"Existing assessment questions count: {len(existing_assess)}")

    existing_q_ids = {q["id"] for q in existing_assess}
    for q in ASSESSMENT_NEW:
        if q["id"] not in existing_q_ids:
            existing_assess.append(q)

    with open(assess_path, "w", encoding="utf-8") as f:
        json.dump(existing_assess, f, ensure_ascii=False, indent=2)
    print(f"Updated content/assessment.json (total: {len(existing_assess)})")

    print("\nSUCCESS: All curriculum batch 2 files generated and merged cleanly!")

if __name__ == "__main__":
    main()
