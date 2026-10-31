"""Rebuild the 0.3 additions without changing stable lesson IDs or user progress."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
lessons=[l for l in read('content/lessons.json') if not l.get('release03')]
solutions=read('frontend/tests/solutions.json')
videos={
 'python':('CS50 Python: функции, переменные и input','https://cs50.harvard.edu/python/weeks/0/','EN'),
 'sql':('CS50 SQL: индексы и транзакции','https://cs50.harvard.edu/sql/weeks/5/','EN'),
 'postgresql':('Postgres Professional: разработка приложений','https://postgrespro.ru/education/courses/DEV1','RU'),
 'html-css':('Kevin Powell: адаптивная вёрстка','https://www.freecodecamp.org/news/master-responsive-website-design','EN'),
 'c':('CS50: основы C','https://cs50.harvard.edu/x/2025/weeks/1/','EN')}
def add(lang,key,title,concept,analogy,explain,task,solution,tests,starter=None,mistake='',challenge='',stdin='',setup='',level='Junior',steps=None):
 id=f'{lang}-{key}';prior=[l for l in lessons if l['language']==lang]
 checks=[]
 for i,t in enumerate(tests):
  if isinstance(t,dict):checks.append({'id':f'{id}-t{i+1}',**t});continue
  label,expr,expected=t
  checks.append({'id':f'{id}-t{i+1}','label':label,'expression' if lang=='python' else 'query':expr,'expected':expected})
 if starter is None:starter='# Напишите решение\n' if lang=='python' else '-- Напишите запрос\n' if lang in ['sql','postgresql'] else ''
 steps=steps or [f'Определите входные данные. {task.split(". ")[0]}.',explain.split('\n\n')[0], 'Запустите пример, затем измените одно входное значение и предскажите результат. Сравните свой прогноз с OUTPUT.']
 lessons.append(dict(id=id,language=lang,title=title,topic=concept,section='Основы' if level=='Beginner' else 'Практика Junior+' if level=='Junior+' else 'Прикладные навыки',order=len(prior)+1,level=level,minutes=20 if level=='Beginner' else 35,theory=explain,syntax=solution,examples=[solution],task=task,starterCode=starter,tests=checks,hints=[steps[0],steps[1],f'Сверьте имена и формат результата с заданием. {mistake}'],commonMistakes=mistake or 'Проверьте граничные случаи: пустые данные, ноль и повторяющиеся значения.',solutionExplanation=explain,walkthrough=steps,prerequisites=[prior[-1]['id']] if prior else [],concepts=[concept],xp=60 if level=='Beginner' else 100,setupSql=setup,stdin=stdin,lifeExample=analogy,challenge=challenge or 'Измените пример под собственные данные. Добавьте обычный, граничный и ошибочный случай. Объясните результат каждого без запуска.',release03=True))
 solutions[id]=solution
def py(key,title,concept,analogy,explain,task,code,checks,**kw):add('python',key,title,concept,analogy,explain,task,code,checks,**kw)

py('input','Диалог с программой: input и int','types','Кассир слышит «два», но для подсчёта ему нужно число. input получает текст, int превращает подходящий текст в целое число.',
 'input() читает одну строку без завершающего Enter и всегда возвращает str. int(input()) сначала читает строку, затем преобразует её в int.\n\nВ DevForge нажмите Run и введите 18 в появившемся окне. Каждый input запрашивает следующую строку. Можно заранее заполнить «Ввод для программы». Кнопка «Конец ввода» вызывает EOFError, а int("кот") даёт ValueError — это разные ситуации.\n\nПодсказка input("Возраст: ") выводится на экран, но не входит в прочитанное значение.',
 'Прочитайте age через int(input()). Сохраните next_age=age+1. Для ввода 18 ожидается 19. Выведите next_age.',
 'age = int(input())\nnext_age = age + 1\nprint(next_age)', [('Число','[age, next_age, type(age).__name__]',[18,19,'int'])],stdin='18',level='Beginner',mistake='Не пишите int("input()"): это попытка преобразовать буквальный текст.')
py('input-validation','Неверный ввод — обычная ситуация','exceptions','Турникет возвращает неподходящий билет, а не ломается. Программа тоже может объяснить ошибку и продолжить.',
 'try содержит действие, которое может не получиться. except ValueError ловит только ошибку преобразования числа.\n\nФункция parse_age(text) должна возвращать неотрицательное целое, иначе None. Отрицательное число успешно проходит int, поэтому его проверяют отдельно. Не ловите все ошибки через голый except: так легко спрятать опечатку в имени.',
 'Напишите parse_age(text): верните int для неотрицательного возраста, None для отрицательного числа и нечисловой строки.',
 'def parse_age(text):\n    try:\n        age = int(text)\n    except ValueError:\n        return None\n    return age if age >= 0 else None', [('Обычный и нулевой','[parse_age("18"), parse_age("0")]',[18,0]),('Ошибки','[parse_age("cat"),parse_age("-1"),parse_age("")]',[None,None,None])])
py('format','Чек магазина: f-строки','strings','В шаблон чека подставляются товар, цена и количество. Сам шаблон остаётся одним.',
 'f перед кавычкой включает подстановку выражений в фигурных скобках. Формат :.2f показывает два знака после точки.\n\nДля money=2 результат f"{money:.2f}" — строка "2.00". Формат меняет представление, а не исходное число. Для настоящих денежных расчётов позже используйте Decimal или целые копейки.',
 'Функция receipt(name,price,qty) возвращает строку вида Tea: 7.50 для Tea,2.5,3.',
 'def receipt(name, price, qty):\n    return f"{name}: {price * qty:.2f}"', [('Покупка','receipt("Tea",2.5,3)','Tea: 7.50'),('Ноль','receipt("Bread",10,0)','Bread: 0.00')])
py('slices','Срезы и нормализация текста','strings','Перед сортировкой писем убирают лишние пробелы на конверте. Данные тоже полезно привести к единому виду.',
 'strip удаляет пробелы по краям, lower приводит буквы к нижнему регистру. Методы возвращают новую строку. Срез text[a:b] включает a и исключает b.\n\ntext[::-1] читает строку с шагом -1. Это удобно для упражнения с палиндромом; удалять все символы подряд в реальных именах нельзя без правил предметной области.',
 'is_palindrome(text) убирает краевые пробелы, приводит текст к lower и сравнивает с обратной строкой.',
 'def is_palindrome(text):\n    text = text.strip().lower()\n    return text == text[::-1]', [('Разный регистр','[is_palindrome(" Anna "),is_palindrome("cat")]',[True,False]),('Пустая строка','is_palindrome("")',True)])
py('comprehensions','Списковые включения: отбор и преобразование','collections','Из корзины берём только спелые яблоки, каждое режем пополам. Сначала отбор, затем действие с каждым выбранным элементом.',
 '[expression for item in items if condition] создаёт новый список. Условие решает, попадёт ли элемент в результат, выражение — во что он превратится.\n\nНе меняйте входной список без необходимости. Для сложного действия с несколькими ветками обычный for часто понятнее.',
 'positive_squares(values) возвращает квадраты только положительных значений, сохраняя порядок.',
 'def positive_squares(values):\n    return [x * x for x in values if x > 0]', [('Отбор','positive_squares([-2,0,3,2])',[9,4]),('Пустые данные','positive_squares([])',[])])
py('sets','Множества и уникальность','collections','Список гостей хранит порядок приглашений, множество отвечает на вопрос «кто уже приглашён?».',
 'set хранит уникальные элементы без обещания порядка. Пересечение & находит общие элементы. sorted возвращает новый упорядоченный список.\n\nПустое множество создаётся set(), а {} создаёт словарь. Элемент множества должен быть хешируемым: число или строка подходят, изменяемый список — нет.',
 'common(a,b) возвращает отсортированный список общих уникальных значений.',
 'def common(a,b):\n    return sorted(set(a) & set(b))', [('Повторы','common([3,2,2,1],[2,3,4])',[2,3]),('Нет общих','common([1],[])',[])])
py('sort-key','Сортировка записей по ключу','functions','Книги можно расставить по автору, а внутри автора — по названию. Это два ключа сортировки.',
 'sorted(items,key=...) вычисляет ключ для каждого элемента. Кортеж (price,name) сначала сравнивает цену, затем имя при равной цене.\n\nlambda — короткая безымянная функция. sorted создаёт новый список; list.sort меняет исходный и возвращает None.',
 'by_price(products) сортирует словари по price, затем name; исходный список не меняется.',
 'def by_price(products):\n    return sorted(products, key=lambda p: (p["price"],p["name"]))', [('Два ключа','[p["name"] for p in by_price([{"name":"B","price":2},{"name":"A","price":2},{"name":"C","price":1}])]', ['C','A','B']),('Пустой','by_price([])',[])])
py('counting','Словарь частот','collections','Кладовщик ведёт счётчик товаров: увидел ещё одну коробку — прибавил один к нужной строке.',
 'dict.get(key,0) возвращает старый счётчик или ноль для нового ключа. Затем присваивание сохраняет увеличенное значение.\n\nЭто один проход по данным, O(n) в среднем. Подсчёт через list.count для каждого слова повторно просматривает список и может стоить O(n²).',
 'counts(words) возвращает словарь количества каждого слова.',
 'def counts(words):\n    result = {}\n    for word in words:\n        result[word] = result.get(word,0) + 1\n    return result', [('Повторы','counts(["tea","tea","milk"])',{'tea':2,'milk':1}),('Пустой','counts([])',{})])
py('mutable-default','Изменяемые аргументы по умолчанию','functions','Если всем посетителям выдавать одну корзину, покупки смешаются. Новой покупке нужна своя корзина.',
 'Значения параметров по умолчанию создаются при определении функции один раз. Поэтому items=[] может сохранить старое содержимое между вызовами.\n\nИспользуйте items=None и создавайте список внутри. Когда передан список, явно решите: изменить его или вернуть копию. В этом задании возвращаем копию.',
 'add_item(value,items=None) возвращает новый список с value в конце и не меняет переданный список.',
 'def add_item(value,items=None):\n    result = list(items) if items is not None else []\n    result.append(value)\n    return result', [('Независимые вызовы','[add_item(1),add_item(2)]',[[1],[2]]),('Копирование','(lambda a: [add_item(2,a),a])([1])',[[1,2],[1]])])
py('enumerate-zip','Номера и пары: enumerate, zip','collections','В школьном журнале номер строки, имя и оценка связаны. enumerate даёт номер, zip соединяет две колонки.',
 'enumerate(items,start=1) возвращает пары номер/элемент. zip(names,scores) возвращает пары соответствующих элементов.\n\nПо умолчанию zip заканчивается на более коротком входе. Если потеря данных недопустима, сначала проверьте длины или используйте strict=True.',
 'ranked(names) возвращает строки "1. Ada", "2. Linus" и так далее.',
 'def ranked(names):\n    return [f"{i}. {name}" for i,name in enumerate(names,1)]', [('Нумерация','ranked(["Ada","Linus"])',['1. Ada','2. Linus']),('Пустой','ranked([])',[])])
py('dataclass','Модель данных: dataclass и типы','objects','Карточка товара всегда имеет одинаковые поля: имя, цена, количество. Класс задаёт форму карточки.',
 '@dataclass создаёт конструктор и сравнение по полям. Аннотации str/int помогают читателю и анализатору, но сами по себе не проверяют значения при выполнении.\n\nМетод получает self — конкретную карточку. Цена в копейках хранится целым числом, чтобы избежать погрешности float.',
 'Создайте @dataclass Product с name:str, cents:int, qty:int=1. Метод total() возвращает cents*qty.',
 'from dataclasses import dataclass\n@dataclass\nclass Product:\n    name: str\n    cents: int\n    qty: int = 1\n    def total(self):\n        return self.cents * self.qty', [('Экземпляры','[Product("Tea",250,3).total(),Product("Milk",120).total()]',[750,120]),('Равенство','Product("Tea",250)==Product("Tea",250)',True)])
py('composition','Композиция: один объект содержит другие','objects','Корзина состоит из покупок. Она не является особым видом покупки, поэтому здесь нужна композиция, а не наследование.',
 'Композиция объединяет объекты через поля. __init__ создаёт отдельное состояние каждого экземпляра.\n\nМетоды add и total скрывают внутренний список от остального кода. Это помогает менять реализацию, сохраняя способ использования.',
 'Cart хранит цены в копейках. add(cents) добавляет цену, total() возвращает сумму. Корзины независимы.',
 'class Cart:\n    def __init__(self):\n        self.items=[]\n    def add(self,cents):\n        self.items.append(cents)\n    def total(self):\n        return sum(self.items)', [('Независимость','(lambda a,b: (a.add(100),a.add(50),[a.total(),b.total()])[-1])(Cart(),Cart())',[150,0])])
py('generators','Генератор: выдавать по одному','iterators','Водопровод подаёт воду по мере надобности. Не нужно заранее ставить в комнате все вёдра.',
 'yield отдаёт значение и приостанавливает функцию до следующего next. Генератор хранит своё состояние, но не весь будущий результат.\n\nПосле исчерпания тот же генератор не начинается заново. Создайте новый вызовом функции. Это полезно для больших потоков данных.',
 'countdown(n) — генератор чисел от n до 1, для n<=0 он пуст.',
 'def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1', [('Порядок','list(countdown(3))',[3,2,1]),('Граница','list(countdown(0))',[])])
py('decorators','Декоратор и сохранение интерфейса','functions','Чехол добавляет защиту телефону, но кнопки работают как прежде. Обёртка функции добавляет поведение вокруг вызова.',
 'Декоратор принимает функцию и возвращает функцию. *args и **kwargs передают любые позиционные и именованные аргументы.\n\nfunctools.wraps сохраняет имя и документацию исходной функции. Обязательно верните результат вызова — иначе снаружи получится None.',
 'double_result(fn) возвращает обёртку, умножающую результат fn на 2, с сохранением имени.',
 'from functools import wraps\ndef double_result(fn):\n    @wraps(fn)\n    def wrapper(*args,**kwargs):\n        return 2 * fn(*args,**kwargs)\n    return wrapper', [('Аргументы','double_result(lambda a,b=1:a+b)(3,b=4)',14),('Метаданные','double_result(sum).__name__','sum')],level='Junior+')
py('files','Файл и контекстный менеджер with','files','Книгу берут, читают и возвращают. with гарантирует закрытие файла даже при ошибке чтения.',
 'open(path,"w",encoding="utf-8") записывает текст и заменяет прежнее содержимое. Режим "a" дописывает, "r" читает.\n\nwith закрывает файл при выходе из блока. Учебный Python хранит файлы в виртуальной памяти браузера: сброс среды удалит их, это не файлы ноутбука.',
 'Запишите строку Привет в note.txt через with, прочитайте её в переменную text.',
 'with open("note.txt","w",encoding="utf-8") as f:\n    f.write("Привет")\nwith open("note.txt",encoding="utf-8") as f:\n    text=f.read()', [('UTF-8','text','Привет'),('Файл закрыт','f.closed',True)])
py('json','JSON: обмен структурированными данными','files','Опись чемодана позволяет восстановить содержимое по списку. JSON описывает простые структуры в текстовом виде.',
 'json.dumps превращает словарь в строку, json.loads — строку в Python-значения. JSON поддерживает строки, числа, массивы, объекты, true/false/null.\n\nНе используйте eval для чтения данных. Невалидный JSON вызывает JSONDecodeError. После чтения проверяйте структуру: корректный JSON может оказаться числом вместо ожидаемого словаря.',
 'load_names(text) читает JSON-массив объектов и возвращает их поля name в исходном порядке.',
 'import json\ndef load_names(text):\n    return [item["name"] for item in json.loads(text)]', [('Объекты','load_names(\'[ {"name":"Ada"}, {"name":"Linus"} ]\')',['Ada','Linus']),('Пустой','load_names("[]")',[])])
py('csv','CSV: запятые внутри значений','files','Адрес может содержать запятую. Если слепо делить строку по каждой запятой, один адрес превратится в несколько колонок.',
 'csv.DictReader читает заголовки как имена ключей и учитывает кавычки CSV. Значения остаются строками: числа преобразуются явно.\n\nio.StringIO позволяет обращаться с текстом как с файлом. При работе с настоящим CSV-файлом используйте newline="".',
 'csv_total(text) читает CSV с колонками name,qty и возвращает сумму qty. Кавычки в name должны обрабатываться правильно.',
 'import csv, io\ndef csv_total(text):\n    return sum(int(row["qty"]) for row in csv.DictReader(io.StringIO(text)))', [('Кавычки','csv_total(\'name,qty\\n"Tea, green",2\\nMilk,3\\n\')',5),('Только заголовок','csv_total("name,qty\\n")',0)])
py('regex','Регулярные выражения и полная проверка','strings','Почтовый индекс имеет фиксированный формат. Проверить часть адреса недостаточно: проверяем всю строку.',
 're.fullmatch требует соответствия всей строки. [0-9]{6} означает ровно шесть ASCII-цифр.\n\nsearch ищет подходящий фрагмент и мог бы принять строку с лишним текстом. Сырые строки r"..." уменьшают путаницу с обратными слешами. Не усложняйте шаблон там, где достаточно методов строк.',
 'postal(text) возвращает bool: ровно 6 цифр от 0 до 9.',
 'import re\ndef postal(text):\n    return re.fullmatch(r"[0-9]{6}",text) is not None', [('Формат','[postal("123456"),postal("12345"),postal("x123456"),postal("1234567")]',[True,False,False,False])])
py('testing','Автоматические тесты и границы','testing','Весы проверяют пустыми, обычным грузом и на пределе. Одного удобного примера недостаточно.',
 'assert сравнивает фактическое и ожидаемое поведение и выбрасывает AssertionError при несовпадении.\n\nПишите тест на граничное значение отдельно: clamp(-1), clamp(0), clamp(100), clamp(101). Тесты должны проверять контракт, а не копировать формулу реализации.',
 'clamp(value) ограничивает число диапазоном 0..100. Добавьте функцию self_test() с assert для четырёх границ; возвращайте True после проверок.',
 'def clamp(value):\n    return max(0,min(100,value))\ndef self_test():\n    assert clamp(-1)==0\n    assert clamp(0)==0\n    assert clamp(100)==100\n    assert clamp(101)==100\n    return True', [('Границы','[clamp(-10),clamp(50),clamp(200)]',[0,50,100]),('Самопроверка','self_test()',True)])
py('sqlite-params','Python и SQLite: параметры запроса','database','Письмо — это данные, а не новая инструкция почтальону. Параметры отделяют данные от команд SQL.',
 'sqlite3.connect(":memory:") создаёт временную базу. execute(sql,(value,)) передаёт значение отдельно через ?. Один элемент кортежа требует запятой.\n\nНе собирайте SQL через f-строки с пользовательским текстом. Параметр сохраняет апострофы и не позволяет значению стать частью синтаксиса запроса.',
 'Сделайте count_name(name): в памяти таблица people(name) с Ada и O\'Neil. Посчитайте совпадения параметризованным запросом.',
 'import sqlite3\ndef count_name(name):\n    db=sqlite3.connect(":memory:")\n    try:\n        db.execute("CREATE TABLE people(name TEXT)")\n        db.executemany("INSERT INTO people VALUES (?)",[("Ada",),("O\'Neil",)])\n        return db.execute("SELECT count(*) FROM people WHERE name=?",(name,)).fetchone()[0]\n    finally:\n        db.close()', [('Апостроф','count_name("O\'Neil")',1),('Данные не SQL','count_name("\' OR 1=1 --")',0)],level='Junior+')
py('decimal','Точные суммы: Decimal','numbers','Деньги считают копейками. Незаметная ошибка округления в каждой покупке может накопиться.',
 'Двоичный float не представляет некоторые десятичные дроби точно. Decimal("0.1") получает точное десятичное значение из строки.\n\nНе создавайте Decimal из float, если хотите сохранить исходное десятичное число. Для денежных систем договоритесь о правилах округления.',
 'money_sum(values) принимает список строк с суммами, возвращает строку суммы с двумя знаками после точки.',
 'from decimal import Decimal\ndef money_sum(values):\n    total=sum((Decimal(x) for x in values),Decimal("0"))\n    return f"{total:.2f}"', [('Десятичные дроби','money_sum(["0.10","0.20"])','0.30'),('Пустой','money_sum([])','0.00')])
py('async','Асинхронность: ожидание без блокировки','async','Пока чайник греется, можно приготовить чашки. Это перекрытие ожидания, а не ускорение самого нагрева.',
 'async def создаёт корутину; await позволяет дождаться результата, уступив управление другим задачам. asyncio.gather запускает несколько ожидающих корутин и сохраняет порядок результатов.\n\nЭто полезно для ввода-вывода, но не ускоряет тяжёлые вычисления Python. В браузерной среде уже есть цикл событий: используйте await, а не asyncio.run.',
 'Создайте async square(n), которая делает await asyncio.sleep(0) и возвращает n*n. В results сохраните await gather для 2 и 3.',
 'import asyncio\nasync def square(n):\n    await asyncio.sleep(0)\n    return n*n\nresults=await asyncio.gather(square(2),square(3))', [('Результаты в порядке','results',[4,9])],level='Junior+')
py('capstone','Проект: отчёт о личных расходах','project','В конце месяца хочется узнать расходы по категориям и отсеять ошибочные записи, не теряя весь отчёт.',
 'Разделите решение на чтение данных, проверку записей и суммирование. Контракт функции описывает вход, выход и ошибочные случаи.\n\nВ задании суммы — целые копейки. Принимаются только словари с непустой строкой category и неотрицательным int cents; bool не считается суммой. Невалидные записи пропускаем. Такой явный контракт помогает написать независимые тесты.\n\nДля самостоятельного проекта добавьте JSON-файл, ввод нескольких расходов, редактирование и тесты. Объясните, какие изменения потребуются для нескольких валют.',
 'expense_report(rows) возвращает суммы cents по category, пропуская невалидные записи. Входные данные не менять.',
 'def expense_report(rows):\n    totals={}\n    for row in rows:\n        if not isinstance(row,dict):\n            continue\n        category=row.get("category")\n        cents=row.get("cents")\n        if not isinstance(category,str) or not category.strip() or type(cents) is not int or cents<0:\n            continue\n        totals[category]=totals.get(category,0)+cents\n    return totals', [('Группировка','expense_report([{"category":"food","cents":250},{"category":"food","cents":150},{"category":"bus","cents":50}])',{'food':400,'bus':50}),('Невалидные','expense_report([None,{}, {"category":"x","cents":True},{"category":"x","cents":-1},{"category":" ","cents":2}])',{}),('Ноль','expense_report([{"category":"gift","cents":0}])',{'gift':0})],level='Junior+',challenge='Соберите отдельный проект: ввод, JSON-хранилище, отчёт и тесты. Укажите способ запуска и ограничения. Проверьте пустой файл и ошибочную запись. Это самостоятельная работа, а не автоматическая сертификация уровня.')

# The remaining tracks are authored in separate, reviewable source modules.
exec((ROOT/'scripts/sql03.py').read_text(encoding='utf-8'))
exec((ROOT/'scripts/web_c03.py').read_text(encoding='utf-8'))
for lang in ['python','sql','postgresql','html-css','c']:
 track=[l for l in lessons if l['language']==lang]
 if lang=='python':
  intro=next(l for l in track if l['id']=='python-input');track.remove(intro);track.insert(next(i for i,l in enumerate(track) if l['id']=='python-conversion')+1,intro)
 capstone=next(l for l in track if l['id']==lang+'-capstone');track.remove(capstone);track.append(capstone)
 for i,l in enumerate(track):
  l['order']=i+1
  l['prerequisites']=[track[i-1]['id']] if i else []
  title,url,locale=videos[lang];l['resources']=[dict(title=title,url=url,language=locale)]
  if lang=='python':
   lecture={'files':(6,'файлы и CSV'),'testing':(5,'автоматические тесты'),'objects':(8,'классы и объекты'),'exceptions':(3,'обработка ошибок')}.get(l['concepts'][0] if l.get('concepts') else '')
   if lecture:l['resources']=[dict(title='CS50 Python: '+lecture[1],url=f'https://cs50.harvard.edu/python/weeks/{lecture[0]}/',language='EN')]
  if lang=='sql' and any(t in l.get('concepts',[]) for t in ['schema','constraints']):l['resources']=[dict(title='CS50 SQL: проектирование базы',url='https://cs50.harvard.edu/sql/weeks/2/',language='EN')]
  if lang=='c' and l['order']>=16:l['resources']=[dict(title='CS50: указатели, память и файлы',url='https://www.youtube.com/watch?v=kcRdFGbzR1I',language='EN')]
  if not l.get('challenge'):l['challenge']='Повторите задание без подсказок на собственных данных. Перед запуском запишите ожидаемый результат; затем объясните расхождение, если оно появится.'
write('content/lessons.json',lessons)
write('frontend/tests/solutions.json',solutions)
write('content/documentation.json',[dict(id=l['id'],title=l['title'],language=l['language'],category=l['section'],explanation=l['theory']+'\n\n'+l.get('lifeExample',''),syntax=l['syntax'],example='\n\n'.join(l['examples']),mistakes=l['commonMistakes'],relatedLessons=[l['id']]) for l in lessons])
languages=read('content/languages.json');languages=[l for l in languages if l['id']!='c']
languages.append(dict(id='c',name='C',extension='.c',editorLanguage='c',runnerType='clang-wasi-worker',status='available',description='C11: компиляция Clang в браузере, указатели, память и проекты без установки.',supportedFeatures=['run','check','reset','files','stdin']))
write('content/languages.json',languages)
questions=[q for q in read('content/assessment.json') if q['language']!='c']
for i,(tag,text,options,correct,explanation) in enumerate([
 ('start','Где начинается программа C?',['В main','В последней строке','В printf'],0,'main — точка входа обычной программы.'),
 ('types','Что даёт 5 / 2 для двух int?',['2.5','2','Ошибка'],1,'Целочисленное деление отбрасывает дробную часть.'),
 ('conditions','Как проверить равенство x и 3?',['x=3','x==3','x===3'],1,'= присваивает, == сравнивает.'),
 ('loops','Какие индексы у int a[3]?',['1,2,3','0,1,2','0,1,2,3'],1,'Допустимо от нуля до длины минус один.'),
 ('pointers','Что означает &x?',['Значение x','Адрес x','Удвоение x'],1,'& получает адрес объекта.'),
 ('memory','Что нужно сделать с успешно выделенной malloc памятью?',['Освободить free после использования','Ничего','Вызвать printf'],0,'Память освобождает владелец; после free указатель нельзя разыменовывать.'),
 ('strings','Чем заканчивается C-строка?',['Символом NUL','Пробелом','Точкой'],0,'Нулевой байт отмечает конец строки и требует места в буфере.'),
 ('project','Как проверить scanf("%d",&x)?',['Сравнить результат с 1','Сравнить x с 0','Не проверять'],0,'scanf возвращает количество успешно записанных значений.')]):
 questions.append(dict(id=f'c-q{i+1}',language='c',tag=tag,text=text,options=options,correct=correct,explanation=explanation))
write('content/assessment.json',questions)
print({lang:sum(l['language']==lang for l in lessons) for lang in videos})
