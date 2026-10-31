import json
import subprocess
import sys
from pathlib import Path

with open('content/lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

print(f"Loaded {len(lessons)} lessons.")

# Check fields integrity
missing_fields = []
for l in lessons:
    lid = l['id']
    for req in ['id', 'language', 'title', 'topic', 'task', 'starterCode', 'tests', 'hints', 'theory']:
        if req not in l or not l[req]:
            missing_fields.append((lid, req))
    if 'guide' not in l or not l['guide']:
        missing_fields.append((lid, 'guide'))
    else:
        g = l['guide']
        for greq in ['idea', 'steps', 'solution']:
            if greq not in g or not g[greq]:
                missing_fields.append((lid, f'guide.{greq}'))

if missing_fields:
    print(f"WARNING: {len(missing_fields)} missing required fields found:")
    for mf in missing_fields[:10]:
        print("  ", mf)
else:
    print("ALL 309 lessons have required fields present.")

# Check lessons count per language
by_lang = {}
for l in lessons:
    by_lang.setdefault(l['language'], []).append(l)

for lang, llist in sorted(by_lang.items()):
    print(f"{lang:<12}: {len(llist):>3} lessons")
