import json

lessons = json.load(open('content/lessons.json', encoding='utf-8'))
by_id = {l['id']: l for l in lessons}
ids = set(by_id.keys())

issues = []
for l in lessons:
    for p in l.get('prerequisites', []):
        if p not in ids:
            issues.append(f"{l['id']}: missing prereq {p}")
        elif by_id[p]['language'] == l['language'] and by_id[p]['order'] >= l['order']:
            issues.append(f"{l['id']} (order {l['order']}): prereq {p} has higher/equal order ({by_id[p]['order']})")
    for r in l.get('resources', []):
        if not r.get('url', '').startswith('https://'):
            issues.append(f"{l['id']}: resource url invalid {r}")

if issues:
    print(f"Found {len(issues)} issues:")
    for iss in issues:
        print("  -", iss)
else:
    print(f"Zero issues found across all {len(lessons)} lessons!")
