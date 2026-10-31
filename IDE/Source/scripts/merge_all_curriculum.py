import json
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath('.'))

import scripts.curriculum_lua as cl
import scripts.curriculum_assembly as ca
import scripts.curriculum_tracks as ct

def enrich_guide(lesson):
    g = lesson.get('guide') or {}
    examples = lesson.get('examples') or []
    starter = lesson.get('starterCode') or ''
    code = examples[0] if examples else starter
    solution = g.get('solution') or starter

    walkthrough = lesson.get('walkthrough') or [lesson.get('task') or 'Выполните задание']
    terms = g.get('terms') or [{'term': lesson.get('title', '').split(':')[0], 'meaning': lesson.get('topic', '')}]

    return {
        'version': g.get('version', 1),
        'idea': g.get('idea') or f"Практическое освоение темы: {lesson.get('title', '')}.",
        'steps': g.get('steps') or [
            f"Изучите теоретическую часть темы: {lesson.get('topic', '')}.",
            "Разберите пример кода и обратите внимание на синтаксис.",
            "Напишите решение задачи и запустите проверку тестов."
        ],
        'experiment': g.get('experiment') or "Попробуйте изменить параметры в коде и посмотреть на результат работы.",
        'terms': terms,
        'solution': solution,
        'taskSteps': g.get('taskSteps') or walkthrough,
        'checklist': g.get('checklist') or [
            "Код компилируется/выполняется без синтаксических ошибок",
            f"Реализованы требования задачи: {lesson.get('title', '')}"
        ],
        'taskTables': g.get('taskTables') or [],
        'example': g.get('example') or {
            'code': code,
            'expected': '',
            'setupSql': '',
            'kind': 'output',
            'tables': []
        }
    }

def main():
    lessons_path = 'content/lessons.json'
    existing = json.load(open(lessons_path, 'r', encoding='utf-8'))
    print(f"Existing lessons count: {len(existing)}")

    by_id = {l['id']: l for l in existing}

    all_to_add = []
    all_to_add.extend(cl.LUA_LESSONS)
    all_to_add.extend(ca.ASSEMBLY_LESSONS)
    all_to_add.extend(ct.BACKEND_LESSONS)
    all_to_add.extend(ct.FRONTEND_LESSONS)
    all_to_add.extend(ct.JAVA_LESSONS)

    added_count = 0
    updated_count = 0

    for l in all_to_add:
        lid = l['id']
        l['guide'] = enrich_guide(l)
        if lid in by_id:
            by_id[lid].update(l)
            updated_count += 1
        else:
            by_id[lid] = l
            added_count += 1

    # Also enrich any existing lessons that might have incomplete guides
    for lid, l in by_id.items():
        l['guide'] = enrich_guide(l)

    # Sort lessons by language and order
    merged_list = list(by_id.values())
    merged_list.sort(key=lambda x: (x.get('language', ''), x.get('order', 0), x.get('id', '')))

    print(f"Total merged lessons: {len(merged_list)} (added: {added_count}, updated: {updated_count})")

    # Validate schema
    valid_langs = {
        'python', 'sql', 'postgresql', 'html-css', 'c', 'javascript',
        'typescript', 'java', 'cpp', 'csharp', 'objc', 'rust', '1c', 'lua', 'assembly'
    }

    errors = []
    for l in merged_list:
        if not l.get('id'):
            errors.append("Empty id in lesson")
        if l.get('language') not in valid_langs:
            errors.append(f"Invalid language {l.get('language')} in lesson {l.get('id')}")
        if not l.get('title'):
            errors.append(f"Missing title in {l.get('id')}")
        if not l.get('tests') or len(l['tests']) == 0:
            errors.append(f"Missing tests in {l.get('id')}")
        if not l.get('guide') or not l['guide'].get('example') or 'code' not in l['guide']['example']:
            errors.append(f"Invalid guide in {l.get('id')}")

    if errors:
        print(f"Validation FAILED with {len(errors)} errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        sys.exit(1)

    print("All lessons passed strict schema validation!")

    with open(lessons_path, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {len(merged_list)} lessons to {lessons_path}!")

if __name__ == '__main__':
    main()
