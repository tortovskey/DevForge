import json

langs = json.load(open('content/languages.json', encoding='utf-8'))
lang_order = {l['id']: i for i, l in enumerate(langs)}

lessons = json.load(open('content/lessons.json', encoding='utf-8'))
lessons.sort(key=lambda x: (lang_order.get(x['language'], 999), x['order']))

with open('content/lessons.json', 'w', encoding='utf-8') as f:
    json.dump(lessons, f, indent=2, ensure_ascii=False)

print(f"Reordered {len(lessons)} lessons according to languages.json order (Python first)!")
