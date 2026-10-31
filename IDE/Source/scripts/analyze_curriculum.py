import json
from collections import Counter

with open('content/lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

print(f"Total lessons: {len(lessons)}")
by_lang = Counter(l['language'] for l in lessons)
for lang, count in by_lang.items():
    print(f"  {lang}: {count} lessons")

print("\nContent metrics by language (average chars):")
header = f"{'Language':<12} | {'Theory':<8} | {'Syntax':<8} | {'Task':<8} | {'Hints':<6} | {'Guide Idea':<10} | {'Terms':<5}"
print(header)
print("-" * len(header))

for lang, count in by_lang.items():
    lang_lessons = [l for l in lessons if l['language'] == lang]
    avg_theory = sum(len(l.get('theory', '')) for l in lang_lessons) / len(lang_lessons)
    avg_syntax = sum(len(l.get('syntax', '')) for l in lang_lessons) / len(lang_lessons)
    avg_task = sum(len(l.get('task', '')) for l in lang_lessons) / len(lang_lessons)
    avg_hints = sum(len(l.get('hints', [])) for l in lang_lessons) / len(lang_lessons)
    avg_idea = sum(len(l.get('guide', {}).get('idea', '')) for l in lang_lessons) / len(lang_lessons)
    avg_terms = sum(len(l.get('guide', {}).get('terms', [])) for l in lang_lessons) / len(lang_lessons)
    print(f"{lang:<12} | {avg_theory:<8.1f} | {avg_syntax:<8.1f} | {avg_task:<8.1f} | {avg_hints:<6.1f} | {avg_idea:<10.1f} | {avg_terms:<5.1f}")
