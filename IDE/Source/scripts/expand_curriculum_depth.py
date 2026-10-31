import json
import os
import sys

# Add scripts directory to path to import curriculum modules
sys.path.insert(0, os.path.dirname(__file__))

from curriculum_data.cpp_data import CPP_ENHANCEMENTS
from curriculum_data.csharp_data import CSHARP_ENHANCEMENTS
from curriculum_data.rust_data import RUST_ENHANCEMENTS
from curriculum_data.bsl_data import BSL_ENHANCEMENTS
from curriculum_data.objc_data import OBJC_ENHANCEMENTS
from curriculum_data.web_languages_data import WEB_LANGUAGES_ENHANCEMENTS

def main():
    lessons_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'lessons.json')
    with open(lessons_path, 'r', encoding='utf-8') as f:
        lessons = json.load(f)

    all_enhancements = {}
    all_enhancements.update(CPP_ENHANCEMENTS)
    all_enhancements.update(CSHARP_ENHANCEMENTS)
    all_enhancements.update(RUST_ENHANCEMENTS)
    all_enhancements.update(BSL_ENHANCEMENTS)
    all_enhancements.update(OBJC_ENHANCEMENTS)
    all_enhancements.update(WEB_LANGUAGES_ENHANCEMENTS)

    updated_count = 0

    for lesson in lessons:
        l_id = lesson.get('id')
        if l_id in all_enhancements:
            enh = all_enhancements[l_id]
            
            # 1. Theory
            if 'theory' in enh:
                lesson['theory'] = enh['theory']

            # 2. LifeExample
            if 'lifeExample' in enh:
                lesson['lifeExample'] = enh['lifeExample']

            # 3. Walkthrough
            if 'walkthrough' in enh:
                lesson['walkthrough'] = enh['walkthrough']

            # 4. CommonMistakes
            if 'commonMistakes' in enh:
                lesson['commonMistakes'] = enh['commonMistakes']

            # 5. SolutionExplanation
            if 'solutionExplanation' in enh:
                lesson['solutionExplanation'] = enh['solutionExplanation']

            # 6. Guide subfields
            guide = lesson.get('guide', {})
            if 'guideSteps' in enh:
                guide['steps'] = enh['guideSteps']
            elif guide.get('steps') == ['Изучите синтаксис команды и ее назначение.', 'Запустите мини-пример и разберите полученный результат.', 'Выполните самостоятельное задание в редакторе.']:
                if 'walkthrough' in enh:
                    guide['steps'] = enh['walkthrough']

            if 'terms' in enh:
                existing_terms = guide.get('terms', [])
                existing_keys = {t.get('term') for t in existing_terms}
                for t in enh['terms']:
                    if t.get('term') not in existing_keys:
                        existing_terms.append(t)
                guide['terms'] = existing_terms

            if 'theory' in enh and (not guide.get('idea') or len(guide.get('idea', '')) < 100):
                guide['idea'] = enh['theory'][:300] + '...'

            lesson['guide'] = guide
            updated_count += 1

        # Also replace any remaining generic walkthroughs if still present
        if lesson.get('walkthrough') == ['Прочитайте условие', 'Напишите решение', 'Запустите проверку']:
            title = lesson.get('title', '')
            lesson['walkthrough'] = [
                f'Изучите теоретические концепции и пример темы "{title}".',
                'Наберите решение задачи в окне редактора кода DevForge.',
                'Запустите тесты и проверьте совпадение вывода с ожидаемым результатом.'
            ]

    with open(lessons_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)

    print(f"Successfully enriched {updated_count} lessons in content/lessons.json!")

if __name__ == '__main__':
    main()
