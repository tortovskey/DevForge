#!/usr/bin/env python3
"""Build and integrate curriculum for JavaScript, TypeScript, and Java."""
import json
from pathlib import Path
from lessons_javascript import get_js_lessons
from lessons_typescript import get_ts_lessons
from lessons_java import get_java_lessons

ROOT = Path(__file__).resolve().parent.parent

def main():
    print("Generating curriculum for JavaScript, TypeScript, and Java...")
    js_lessons = get_js_lessons()
    ts_lessons = get_ts_lessons()
    java_lessons = get_java_lessons()
    new_lessons = js_lessons + ts_lessons + java_lessons

    print(f"  Authored: JS={len(js_lessons)}, TS={len(ts_lessons)}, Java={len(java_lessons)} -> Total new = {len(new_lessons)}")

    # 1. Update lessons.json
    lessons_path = ROOT / "content" / "lessons.json"
    existing_lessons = json.loads(lessons_path.read_text(encoding="utf-8"))
    
    # Filter out previous versions of new languages if any, preserving the 166 original lessons
    clean_lessons = [l for l in existing_lessons if l.get("language") not in ("javascript", "typescript", "java")]
    print(f"  Existing base lessons count: {len(clean_lessons)}")
    
    all_lessons = clean_lessons + new_lessons
    print(f"  Total lessons after addition: {len(all_lessons)}")
    lessons_path.write_text(json.dumps(all_lessons, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Update solutions.json
    solutions_path = ROOT / "frontend" / "tests" / "solutions.json"
    solutions = json.loads(solutions_path.read_text(encoding="utf-8"))
    for l in new_lessons:
        solutions[l["id"]] = l["guide"]["solution"]
    solutions_path.write_text(json.dumps(solutions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Updated solutions.json ({len(solutions)} solutions)")

    # 3. Update documentation.json
    docs_path = ROOT / "content" / "documentation.json"
    existing_docs = json.loads(docs_path.read_text(encoding="utf-8"))
    clean_docs = [d for d in existing_docs if d.get("language") not in ("javascript", "typescript", "java")]
    
    new_docs = []
    for l in new_lessons:
        guide = l["guide"]
        new_docs.append({
            "id": l["id"],
            "title": l["title"],
            "language": l["language"],
            "category": l["section"],
            "explanation": f"{guide['idea']}\n\n1. {guide['steps'][0]}\n\n2. {guide['steps'][1] if len(guide['steps'])>1 else ''}\n\n3. {guide['steps'][2] if len(guide['steps'])>2 else ''}".strip(),
            "syntax": l["syntax"],
            "example": guide["example"]["code"],
            "mistakes": l["commonMistakes"],
            "relatedLessons": [l["id"]]
        })
    all_docs = clean_docs + new_docs
    docs_path.write_text(json.dumps(all_docs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Updated documentation.json ({len(all_docs)} articles)")

    # 4. Update assessment.json
    assessment_path = ROOT / "content" / "assessment.json"
    existing_questions = json.loads(assessment_path.read_text(encoding="utf-8"))
    clean_questions = [q for q in existing_questions if q.get("language") not in ("javascript", "typescript", "java")]

    new_questions = [
        # JavaScript (8 questions)
        {
            "id": "js-q1",
            "language": "javascript",
            "tag": "first-console",
            "text": "Что выведет console.log('Привет')?",
            "options": ["Привет", "'Привет'", "Ничего: нужна переменная"],
            "correct": 0,
            "explanation": "console.log выводит содержимое строки без окружающих кавычек."
        },
        {
            "id": "js-q2",
            "language": "javascript",
            "tag": "variables",
            "text": "Чем отличается let от const в JavaScript?",
            "options": [
                "let объявляет изменяемую переменную, а const — неизменяемую константу",
                "const работает только со строками",
                "Ничем, это полные синонимы"
            ],
            "correct": 0,
            "explanation": "Переменную let можно перезаписать другим значением, а повторное присваивание в const вызовет TypeError."
        },
        {
            "id": "js-q3",
            "language": "javascript",
            "tag": "numbers",
            "text": "Чему равен результат выражения '5' + 2 в JavaScript?",
            "options": ["'52' (склеивание строк)", "7", "NaN (ошибка вычисления)"],
            "correct": 0,
            "explanation": "Если один из операндов строка, оператор + выполняет конкатенацию строк."
        },
        {
            "id": "js-q4",
            "language": "javascript",
            "tag": "comparison",
            "text": "Что вернёт строгое сравнение 5 === '5'?",
            "options": ["false (число не равно строке)", "true", "TypeError"],
            "correct": 0,
            "explanation": "Оператор === проверяет и значение, и тип данных без неявного приведения типов."
        },
        {
            "id": "js-q5",
            "language": "javascript",
            "tag": "map",
            "text": "Какой метод массива создаёт новый массив той же длины, преобразуя каждый элемент?",
            "options": ["map", "filter", "forEach"],
            "correct": 0,
            "explanation": "Метод map применяет функцию к каждому элементу и возвращает новый массив результатов."
        },
        {
            "id": "js-q6",
            "language": "javascript",
            "tag": "objects",
            "text": "Как получить доступ к свойству name объекта user?",
            "options": ["user.name или user['name']", "только user.name", "user->name"],
            "correct": 0,
            "explanation": "В JavaScript доступ к свойствам объекта возможен через точку или через квадратные скобки со строковым ключом."
        },
        {
            "id": "js-q7",
            "language": "javascript",
            "tag": "json-project",
            "text": "Что делает функция JSON.parse(str)?",
            "options": [
                "Превращает строку формата JSON в объект или массив JavaScript",
                "Превращает объект JavaScript в текст JSON",
                "Проверяет валидность файла"
            ],
            "correct": 0,
            "explanation": "JSON.parse разбирает текстовую строку JSON и восстанавливает структуры объектов и массивов."
        },
        {
            "id": "js-q8",
            "language": "javascript",
            "tag": "arrays",
            "text": "Какой индекс имеет первый элемент массива arr в JavaScript?",
            "options": ["0", "1", "-1"],
            "correct": 0,
            "explanation": "Индексация массивов в JavaScript начинается с нуля."
        },

        # TypeScript (8 questions)
        {
            "id": "ts-q1",
            "language": "typescript",
            "tag": "first-type",
            "text": "Как правильно указать строковый тип для переменной в TypeScript?",
            "options": ["let name: string = 'Иван';", "let string name = 'Иван';", "let name(string) = 'Иван';"],
            "correct": 0,
            "explanation": "В TypeScript аннотация типа указывается через двоеточие после имени переменной."
        },
        {
            "id": "ts-q2",
            "language": "typescript",
            "tag": "union-types",
            "text": "Что означает тип string | number?",
            "options": [
                "Значение может быть либо строкой, либо числом (Union тип)",
                "Строка и число одновременно",
                "Синтаксическая ошибка"
            ],
            "correct": 0,
            "explanation": "Вертикальная черта | обозначает объединение типов: допускаются значения любого из указанных типов."
        },
        {
            "id": "ts-q3",
            "language": "typescript",
            "tag": "interfaces",
            "text": "Какое ключевое слово используется для описания структуры объекта (контракта)?",
            "options": ["interface", "contract", "struct"],
            "correct": 0,
            "explanation": "Ключевое слово interface описывает контракт формы объекта в TypeScript."
        },
        {
            "id": "ts-q4",
            "language": "typescript",
            "tag": "optional-params",
            "text": "Что означает знак вопроса в объявлении function greet(name?: string)?",
            "options": [
                "Параметр name опционален (необязателен для передачи)",
                "Параметр имеет тип boolean",
                "Переменная name может быть удалена"
            ],
            "correct": 0,
            "explanation": "Знак ? после имени параметра делает его необязательным: его тип становится string | undefined."
        },
        {
            "id": "ts-q5",
            "language": "typescript",
            "tag": "any-unknown",
            "text": "Чем тип unknown безопаснее any в TypeScript?",
            "options": [
                "unknown требует предварительной проверки типа перед вызовом методов",
                "unknown быстрее компилируется",
                "Ничем, это полные синонимы"
            ],
            "correct": 0,
            "explanation": "TypeScript не позволит вызвать метод у unknown без предварительного сужения типа через typeof или instanceof."
        },
        {
            "id": "ts-q6",
            "language": "typescript",
            "tag": "readonly",
            "text": "Какой модификатор запрещает изменение свойства объекта после создания?",
            "options": ["readonly", "static", "private"],
            "correct": 0,
            "explanation": "Свойство с модификатором readonly нельзя перезаписать после первоначальной инициализации."
        },
        {
            "id": "ts-q7",
            "language": "typescript",
            "tag": "utility-partial",
            "text": "Что делает служебный тип Partial<User>?",
            "options": [
                "Делает все свойства типа User опциональными",
                "Удаляет обязательные свойства",
                "Делает все свойства доступными только для чтения"
            ],
            "correct": 0,
            "explanation": "Partial<T> трансформирует тип, делая каждое его поле опциональным (добавляет ?)."
        },
        {
            "id": "ts-q8",
            "language": "typescript",
            "tag": "generics-function",
            "text": "Для чего служат обобщения (Generics, <T>) в TypeScript?",
            "options": [
                "Для создания универсальных функций и классов с сохранением точных типов данных",
                "Для генерации случайных чисел",
                "Для ускорения работы сборщика мусора"
            ],
            "correct": 0,
            "explanation": "Дженерики позволяют писать гибкий переиспользуемый код без потери информации о конкретных типах."
        },

        # Java (8 questions)
        {
            "id": "java-q1",
            "language": "java",
            "tag": "first-main",
            "text": "Какая сигнатура является точкой входа в программу на Java?",
            "options": [
                "public static void main(String[] args)",
                "public void start()",
                "void main()"
            ],
            "correct": 0,
            "explanation": "Метод public static void main(String[] args) — стандартная точка входа JVM в приложение."
        },
        {
            "id": "java-q2",
            "language": "java",
            "tag": "arithmetic",
            "text": "Чему равен результат целочисленного деления 7 / 2 в Java?",
            "options": ["3", "3.5", "4"],
            "correct": 0,
            "explanation": "Деление целых чисел int / int в Java отбрасывает дробную часть, результат равен 3."
        },
        {
            "id": "java-q3",
            "language": "java",
            "tag": "variables",
            "text": "Какой тип данных используется в Java для логических значений true и false?",
            "options": ["boolean", "bool", "bit"],
            "correct": 0,
            "explanation": "В Java логический тип данных называется boolean."
        },
        {
            "id": "java-q4",
            "language": "java",
            "tag": "arrays",
            "text": "Как узнать длину массива int[] arr в Java?",
            "options": ["arr.length (свойство)", "arr.length() (метод)", "arr.size()"],
            "correct": 0,
            "explanation": "У массивов в Java длина хранится в специальном свойстве .length без круглых скобок."
        },
        {
            "id": "java-q5",
            "language": "java",
            "tag": "inheritance",
            "text": "Какое ключевое слово используется для наследования одного класса от другого?",
            "options": ["extends", "implements", "inherits"],
            "correct": 0,
            "explanation": "Ключевое слово extends объявляет класс-наследник (например, class Dog extends Animal)."
        },
        {
            "id": "java-q6",
            "language": "java",
            "tag": "encapsulation",
            "text": "Какой модификатор доступа скрывает поле внутри класса (инкапсуляция)?",
            "options": ["private", "public", "protected"],
            "correct": 0,
            "explanation": "Модификатор private делает поле доступным только из методов того же класса."
        },
        {
            "id": "java-q7",
            "language": "java",
            "tag": "scanner",
            "text": "Какой класс стандартного пакета java.util удобен для чтения ввода чисел и строк?",
            "options": ["Scanner", "InputReader", "Parser"],
            "correct": 0,
            "explanation": "Класс Scanner(System.in) предоставляет удобные методы nextInt(), nextLine() и др."
        },
        {
            "id": "java-q8",
            "language": "java",
            "tag": "math",
            "text": "Как найти наибольшее из двух чисел a и b в Java?",
            "options": ["Math.max(a, b)", "max(a, b)", "Math.highest(a, b)"],
            "correct": 0,
            "explanation": "Статический метод Math.max(a, b) возвращает максимальное из двух значений."
        }
    ]

    all_questions = clean_questions + new_questions
    assessment_path.write_text(json.dumps(all_questions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Updated assessment.json ({len(all_questions)} questions across 8 languages)")

    print("\nCurriculum generation completed successfully!")

if __name__ == "__main__":
    main()
