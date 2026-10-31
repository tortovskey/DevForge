import json
from .database import ROOT

def read(name: str):
    return json.loads((ROOT / 'content' / name).read_text(encoding='utf-8'))

LANGUAGES = read('languages.json')
LESSONS = read('lessons.json')
DOCS = read('documentation.json')
TRACKS = read('tracks.json')
BY_ID = {lesson['id']: lesson for lesson in LESSONS}
