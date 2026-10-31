import json

def sync_docs():
    lessons = json.load(open('content/lessons.json', 'r', encoding='utf-8'))
    docs = json.load(open('content/documentation.json', 'r', encoding='utf-8'))

    doc_ids = {d['id']: d for d in docs}
    added = 0

    for l in lessons:
        lid = l['id']
        if lid not in doc_ids:
            example = l.get('examples', [''])[0] if l.get('examples') else l.get('starterCode', '')
            entry = {
                'id': lid,
                'title': l.get('title', ''),
                'language': l.get('language', ''),
                'category': l.get('section', l.get('topic', 'Общее')),
                'explanation': l.get('theory', ''),
                'syntax': l.get('syntax', ''),
                'example': example,
                'mistakes': l.get('commonMistakes', ''),
                'relatedLessons': [lid]
            }
            docs.append(entry)
            doc_ids[lid] = entry
            added += 1

    docs.sort(key=lambda d: (d.get('language', ''), d.get('title', '')))

    with open('content/documentation.json', 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f"Synced documentation. Added {added} entries. Total docs: {len(docs)}.")

if __name__ == '__main__':
    sync_docs()
