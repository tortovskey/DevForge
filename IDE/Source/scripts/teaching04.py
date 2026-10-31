"""Build the reviewed teaching layer without changing tasks, IDs or progress."""
from pathlib import Path
import json,re,sqlite3
import teaching_python,teaching_sql,teaching_web,teaching_c
from teaching_analogies import LIFE_ANALOGIES
ROOT=Path(__file__).resolve().parents[1]
guides={}
def add(language,keys,idea,code,expected,trace,experiment,setup='',dom=None):
 for key in keys.split():
  identifier=f'{language}-{key}'
  assert identifier not in guides,identifier
  guides[identifier]={'version':1,'idea':idea,'steps':trace.split('|'),'experiment':experiment,'example':{'code':code,'expected':expected,'setupSql':setup,'kind':'html' if dom else 'table' if language in ('sql','postgresql') else 'stdout',**({'dom':dom} if dom else {})}}
for module in (teaching_python,teaching_sql,teaching_web,teaching_c):module.build(add)
lessons=json.loads((ROOT/'content/lessons.json').read_text(encoding='utf-8'))
solutions=json.loads((ROOT/'frontend/tests/solutions.json').read_text(encoding='utf-8'))
missing=set(l['id'] for l in lessons)-guides.keys()
extra=guides.keys()-set(l['id'] for l in lessons)
assert not missing,sorted(missing)
assert not extra,sorted(extra)
GLOSSARY={
 'python':{
 'print':'Показать значение внизу в выводе. Само показанное значение не становится результатом другой функции.',
 'int':'Целое число без дробной части. int(text) пытается превратить текст в такое число.',
 'input':'Получить одну строку ввода. Возвращает текст, даже если человек ввёл цифры.',
 'str':'Тип текстовой строки. str(value) получает текстовое представление значения.',
 'def':'Начать описание функции — действия с собственным именем.',
 'return':'Закончить вызов функции и отдать результат в место вызова.',
 'for':'По очереди взять элементы набора и выполнить блок для каждого.',
 'range':'Получить последовательность целых чисел. Правая граница не включается.',
 'while':'Повторять блок, пока условие истинно. Условие проверяется перед каждым проходом.',
 'if':'Выполнить блок с отступом, только если условие истинно.',
 'else':'Запасная ветка, когда условие if не выполнилось.',
 'True':'Логическое «да», истина. Важна большая буква T.',
 'False':'Логическое «нет», ложь. Важна большая буква F.',
 'None':'Отсутствие значения. Это не ноль, не False и не пустая строка.',
 'len':'Количество элементов списка или символов строки.',
 'append':'Добавить один элемент в конец существующего списка.',
 'get':'Для словаря: прочитать значение по ключу, при отсутствии вернуть запасное.',
 'class':'Описать тип объектов с данными и действиями.',
 'self':'Текущий объект: тот экземпляр, у которого вызвали метод.',
 'import':'Подключить готовый модуль — набор инструментов.',
 'try':'Попробовать действие, ошибка которого может быть обработана ниже.',
 'except':'Обработать указанную ошибку и выбрать запасное действие.',
 'with':'Работать с ресурсом, автоматически завершив его использование при выходе из блока.',
 'yield':'Отдать очередное значение генератора и запомнить место остановки.',
 'lambda':'Короткая функция без отдельного имени: параметры слева от :, результат справа.',
 'sorted':'Создать новый отсортированный список, не переставляя элементы исходного.',
 'assert':'Проверить утверждение. При ложном результате возникает AssertionError.',
 'await':'Дождаться асинхронного результата, позволяя другим задачам продвигаться.',
 'async':'Объявить функцию, в которой можно использовать асинхронное ожидание.'},
 'sql':{
 'SELECT':'Выбрать столбцы или вычисления, которые попадут в ответ.',
 'FROM':'Указать таблицу или промежуточный результат для чтения.',
 'WHERE':'Оставить только строки с истинным условием до группировки.',
 'ORDER BY':'Задать порядок строк ответа. Без него база не обещает определённый порядок.',
 'AS':'Дать столбцу или таблице короткое имя в текущем запросе.',
 'NULL':'Значение неизвестно или отсутствует; отличается от нуля и пустого текста.',
 'COUNT':'Посчитать строки (*) или непустые значения указанного столбца.',
 'SUM':'Сложить непустые значения. При отсутствии значений результат NULL.',
 'AVG':'Среднее арифметическое непустых значений.',
 'GROUP BY':'Собрать строки с одинаковыми ключами в группы для отдельного подсчёта итогов.',
 'HAVING':'Отобрать группы после расчёта итогов.',
 'JOIN':'Найти пары строк из двух источников по условию ON.',
 'LEFT JOIN':'Сохранить все строки слева, даже без найденной пары справа.',
 'ON':'Условие, определяющее, какие две строки образуют пару.',
 'INSERT':'Добавить новые строки.', 'UPDATE':'Изменить существующие строки.',
 'DELETE':'Удалить выбранные строки. Без WHERE затрагивает всю таблицу.',
 'CREATE TABLE':'Создать структуру новой таблицы.',
 'PRIMARY KEY':'Уникальный идентификатор строки таблицы.',
 'REFERENCES':'Связь с существующим ключом другой таблицы — внешний ключ.',
 'CHECK':'Правило допустимости значения или сочетания значений.',
 'WITH':'Назвать промежуточный результат внутри одного SQL-выражения.',
 'OVER':'Описать окно строк, по которым считает оконная функция.',
 'COALESCE':'Взять первое значение, которое не NULL.',
 'BEGIN':'Начать транзакцию — группу согласованных изменений.',
 'COMMIT':'Подтвердить изменения транзакции.',
 'ROLLBACK':'Отменить неподтверждённые изменения транзакции.',
 'RETURNING':'Получить значения строк, изменённых текущей командой.',
 'DISTINCT':'Убрать одинаковые строки из ответа.',
 'LIMIT':'Ограничить число возвращаемых строк.',
 'CASE':'Выбрать значение по первой подходящей ветке WHEN.',
 'EXISTS':'Проверить, есть ли хотя бы одна строка в результате подзапроса.'},
 'c':{
 'stdio.h':'Стандартный заголовок с объявлениями функций ввода и вывода.',
 'stdlib.h':'Стандартный заголовок с malloc, free, strtol, qsort и другими инструментами.',
 'string.h':'Заголовок с функциями обработки строк и памяти.',
 'main':'Главная функция, с которой начинается выполнение программы.',
 'int':'Целочисленный тип. Его диапазон ограничен; он не хранит любое большое число.',
 'void':'В main(void) — отсутствие аргументов; перед именем функции — отсутствие возвращаемого значения.',
 'printf':'Вывести форматированный текст. Маркеры % должны соответствовать типам аргументов.',
 'puts':'Напечатать строку и добавить перевод строки.',
 'scanf':'Прочитать значения из ввода. Возвращает число успешных преобразований.',
 'sscanf':'Прочитать значения из уже существующей строки по формату.',
 'return':'Завершить функцию и вернуть указанное значение.',
 'double':'Тип для дробных чисел; многие десятичные дроби хранятся приближённо.',
 'char':'Тип для одного байта/символа. Массив char может хранить строку.',
 'size_t':'Беззнаковый тип для размеров. В printf соответствует %zu.',
 'sizeof':'Размер объекта или типа в байтах.',
 'NULL':'Нулевой указатель: действительного адреса объекта здесь нет.',
 'const':'Запретить изменение значения через это объявление или указатель.',
 'struct':'Объединить именованные поля в один тип записи.',
 'malloc':'Выделить блок памяти; проверить результат и позже освободить free.',
 'free':'Освободить ранее выделенную память. После этого к ней нельзя обращаться.',
 'realloc':'Изменить размер блока. При успехе адрес может измениться.',
 'break':'Выйти из ближайшего цикла или switch.',
 'assert':'Тестовое утверждение. При ложном условии проверка прерывает программу.'},
 'html-css':{
 'h1':'Главный заголовок страницы, а не просто способ сделать крупный текст.',
 'h2':'Заголовок раздела внутри общей темы страницы.',
 'class':'Метка группы элементов для общего оформления.',
 'id':'Уникальное имя элемента в документе; используется ссылками и подписями.',
 'style':'Контейнер правил CSS внутри HTML-документа.',
 'color':'Цвет текста, не фон элемента.',
 'padding':'Внутренний отступ между содержимым и границей элемента.',
 'border':'Рамка вокруг содержимого и внутреннего отступа.',
 'width':'Заданная ширина; её смысл зависит от box-sizing.',
 'display':'Способ раскладки элемента и его детей.',
 'gap':'Расстояние между элементами flex/grid.',
 'label':'Текстовая подпись поля, связанная через for и id.',
 'input':'Поле ввода данных пользователем.',
 'button':'Кнопка, доступная мышью и клавиатурой.',
 'article':'Самостоятельный фрагмент содержания, например карточка работы.',
 'section':'Тематический раздел документа, обычно со своим заголовком.',
 'main':'Основное содержание страницы.',
 'footer':'Завершающая информация страницы или раздела.',
 'alt':'Текстовая альтернатива изображению.',
 'opacity':'Прозрачность: от 0 (прозрачно) до 1 (непрозрачно).'}
}
GLOSSARY['postgresql']=GLOSSARY['sql']
def table_preview(setup):
 if not setup:return []
 db=sqlite3.connect(':memory:')
 try:
  db.executescript(setup)
  tables=[]
  for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
   quoted='"'+name.replace('"','""')+'"'
   cursor=db.execute(f'SELECT * FROM {quoted} LIMIT 12')
   tables.append({'name':name,'columns':[c[0] for c in cursor.description],'values':[list(row) for row in cursor.fetchall()]})
  return tables
 except sqlite3.Error:return [] # PostgreSQL-only setup remains visible as source SQL.
 finally:db.close()
for lesson in lessons:
 guide=guides[lesson['id']]
 haystack=guide['example']['code']+'\n'+lesson['syntax']
 guide['terms']=[{'term':term,'meaning':meaning} for term,meaning in GLOSSARY[lesson['language']].items() if re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',haystack,re.I)]
 guide['solution']=solutions[lesson['id']]
 guide['example']['tables']=table_preview(guide['example']['setupSql'])
 guide['taskTables']=table_preview(lesson.get('setupSql','')) if lesson['language'] in ('sql','postgresql') else []
 guide['taskSteps']=[x.strip().rstrip('.')+'.' for x in re.split(r'(?<=[.!?])\s+',lesson['task']) if x.strip()]
 guide['checklist']={
 'python':['Если задача просит функцию, сохраните её имя и параметры из условия.','Если нужен результат функции, используйте return. print нужен только для вывода.','Проверьте обычный пример, затем ноль или пустые данные, если они разрешены условием.'],
 'sql':['Найдите нужные таблицы и столбцы в исходных данных.','Отделите выбор строк (WHERE) от выбора столбцов (SELECT).','Если условие задаёт порядок, укажите ORDER BY. Перед повтором изменения используйте сброс.'],
 'postgresql':['Сверьте типы и имена столбцов с исходными данными.','Сначала проверьте маленький промежуточный SELECT, затем добавляйте остальные части.','Если условие задаёт порядок, укажите ORDER BY. Изменения проверяются на новой базе.'],
 'html-css':['Сначала создайте нужные элементы и тексты без оформления.','Затем свяжите классы HTML с селекторами CSS.','Посмотрите предпросмотр и выполните проверку: внешнее сходство не гарантирует правильную структуру.'],
 'c':['Сохраните include и main; каждую обычную инструкцию завершайте ;.','До использования введённого значения проверьте успех чтения.','Сверьте типы с форматами printf и не выходите за границы массивов.']}[lesson['language']]
 lesson['guide']=guide
 lesson['minutes']=max(lesson['minutes'],15 if lesson['level']=='Beginner' else 25)
 # Progressive hints now refer to the concrete example before exposing the answer.
 lesson['hints']=[guide['taskSteps'][0],guide['steps'][-1],lesson['commonMistakes']]
 lesson['challenge']=guide['experiment']
 if not lesson.get('lifeExample') and lesson['id'] in LIFE_ANALOGIES:
  lesson['lifeExample']=LIFE_ANALOGIES[lesson['id']]
(ROOT/'content/lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
docs=json.loads((ROOT/'content/documentation.json').read_text(encoding='utf-8'))
for doc in docs:
 if doc['id'] in guides:
  g=guides[doc['id']];doc['explanation']=g['idea']+'\n\n'+'\n\n'.join(f'{i+1}. {t}' for i,t in enumerate(g['steps']));doc['example']=g['example']['code']
(ROOT/'content/documentation.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Authored guides: {len(guides)}; coverage: {len(lessons)}/{len(lessons)}')
