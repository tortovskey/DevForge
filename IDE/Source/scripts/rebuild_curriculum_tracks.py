import json

# We can import BACKEND_LESSONS from a safe backup or clean up curriculum_tracks.py
# Let's inspect the original BACKEND_LESSONS from curriculum_tracks.py
with open('scripts/curriculum_tracks.py', 'r', encoding='utf-8') as f:
    text = f.read()

# BACKEND_LESSONS is between "BACKEND_LESSONS = [" and "print(f\"Loaded {len(BACKEND_LESSONS)}"
idx_backend_start = text.find('BACKEND_LESSONS = [')
idx_backend_end = text.find('print(f"Loaded {len(BACKEND_LESSONS)}')

backend_block = text[idx_backend_start:idx_backend_end].strip()

# Now extract make_guide function at top
idx_top_end = idx_backend_start
top_block = text[:idx_top_end]

from scripts.append_tracks_curriculum import FRONTEND_CONTENT, JAVA_CONTENT
from scripts.append_more_track_lessons import MORE_FRONTEND, MORE_JAVA

# In FRONTEND_CONTENT:
# FRONTEND_LESSONS = [ ... ]
# We can parse the lessons or assemble the list properly:
# We want:
# frontend-js-async-promises
# frontend-js-dom-events
# frontend-ts-frontend-props (from MORE_FRONTEND)
# frontend-react-hooks-state
# frontend-react-hooks-advanced
# frontend-network-fetch (from MORE_FRONTEND)
# frontend-project-catalog-cart

clean_fe = '''
FRONTEND_LESSONS = [
''' + FRONTEND_CONTENT[FRONTEND_CONTENT.find('{'):FRONTEND_CONTENT.rfind('}')+1] + ''',
''' + MORE_FRONTEND.strip().lstrip(',').rstrip(',') + '''
]
'''

clean_java = '''
JAVA_LESSONS = [
''' + JAVA_CONTENT[JAVA_CONTENT.find('{'):JAVA_CONTENT.rfind('}')+1] + ''',
''' + MORE_JAVA.strip().lstrip(',').rstrip(',') + '''
]
'''

clean_file = top_block + '\n' + backend_block + '\n\n' + clean_fe + '\n\n' + clean_java + '''

print(f"Loaded {len(BACKEND_LESSONS)} backend lessons, {len(FRONTEND_LESSONS)} frontend lessons, {len(JAVA_LESSONS)} java lessons.")
'''

# Fix booleans
clean_file = clean_file.replace('"expected": [true, 0]', '"expected": [True, 0]')
clean_file = clean_file.replace('"expected": [false,', '"expected": [False,')
clean_file = clean_file.replace('"expected": false', '"expected": False')
clean_file = clean_file.replace('"expected": true', '"expected": True')

with open('scripts/curriculum_tracks.py', 'w', encoding='utf-8') as f:
    f.write(clean_file)

print("Rebuilt curriculum_tracks.py cleanly!")
