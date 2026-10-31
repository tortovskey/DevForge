# Executed by curriculum03.py; all checks run against fresh real databases.
for lang in ['sql','postgresql']:
 def sql(key,title,concept,analogy,theory,task,code,expected,setup='',query='$result',**kw):
  add(lang,key,title,concept,analogy,theory,task,code,[(title,query,expected)],setup=setup,**kw)
 sql('left-join','LEFT JOIN: сохранить строки без пары','joins','В списке жильцов остаётся человек без парковочного места. INNER JOIN потерял бы его, LEFT JOIN сохраняет.',
  'FROM задаёт левую таблицу. LEFT JOIN добавляет совпавшие строки правой; если пары нет, её колонки становятся NULL.\n\nУсловие связи пишется в ON. Фильтр правой таблицы в WHERE может убрать строки с NULL и превратить результат в поведение INNER JOIN. Для понятного порядка добавьте ORDER BY.',
  'Выведите имя каждого клиента и число его заказов, включая ноль. Колонки name, n; порядок по имени.',
  'SELECT c.name,COUNT(o.id) AS n FROM clients c LEFT JOIN orders o ON o.client_id=c.id GROUP BY c.id,c.name ORDER BY c.name;',
  [['Ada',2],['Linus',0]],'CREATE TABLE clients(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,client_id INTEGER); INSERT INTO clients VALUES(1,\'Ada\'),(2,\'Linus\'); INSERT INTO orders VALUES(1,1),(2,1);',mistake='COUNT(*) посчитает строку клиента без заказа. COUNT(o.id) пропускает NULL.')
 sql('case','CASE: понятные категории','expressions','Термометр показывает число, а человек говорит «холодно» или «тепло». CASE переводит значения в категории.',
  'CASE WHEN условие THEN значение ELSE значение END возвращает одно значение. Проверки идут сверху вниз до первого совпадения.\n\nВсе ветки должны иметь совместимые типы. NULL не равен никакому числу: если его нужно выделить, используйте IS NULL.',
  'Для temperatures выведите id и label: ниже 10 cold, иначе warm, NULL unknown. Порядок id.',
  "SELECT id,CASE WHEN degrees IS NULL THEN 'unknown' WHEN degrees<10 THEN 'cold' ELSE 'warm' END AS label FROM temperatures ORDER BY id;",
  [[1,'cold'],[2,'warm'],[3,'unknown']], 'CREATE TABLE temperatures(id INTEGER,degrees INTEGER);INSERT INTO temperatures VALUES(1,5),(2,10),(3,NULL);')
 sql('coalesce','NULL и COALESCE','null','В анкете пустое поле не означает число ноль. Можно показать понятную замену, сохранив исходное отсутствие данных.',
  'COALESCE(a,b,c) возвращает первое значение, которое не NULL. Пустая строка и ноль не считаются NULL.\n\nАгрегаты SUM/AVG пропускают NULL. Замена NULL на ноль до AVG изменяет смысл среднего — делайте её только по правилам задачи.',
  'Выведите id и phone, заменив только NULL на unknown, порядок id.',
  "SELECT id,COALESCE(phone,'unknown') FROM contacts ORDER BY id;",[[1,'unknown'],[2,''],[3,'123']],"CREATE TABLE contacts(id INTEGER,phone TEXT);INSERT INTO contacts VALUES(1,NULL),(2,''),(3,'123');")
 sql('exists','EXISTS: есть ли связанная запись','subqueries','Чтобы понять, покупал ли человек хоть раз, не нужно перечислять все покупки.',
  'EXISTS(подзапрос) проверяет наличие хотя бы одной строки. Коррелированный подзапрос использует ключ внешней строки.\n\nВ отличие от JOIN, EXISTS не размножает клиента по числу покупок. NOT EXISTS находит отсутствие пары и удобен, когда в данных возможен NULL.',
  'Найдите имена клиентов, у которых нет заказов. Отсортируйте по имени.',
  'SELECT c.name FROM clients c WHERE NOT EXISTS(SELECT 1 FROM orders o WHERE o.client_id=c.id) ORDER BY c.name;', [['Linus']],"CREATE TABLE clients(id INTEGER,name TEXT);CREATE TABLE orders(client_id INTEGER);INSERT INTO clients VALUES(1,'Ada'),(2,'Linus');INSERT INTO orders VALUES(1),(1),(NULL);")
 sql('having','WHERE и HAVING: фильтры на разных этапах','aggregation','Сначала убираем отменённые чеки, потом считаем выручку магазинов и выбираем крупные магазины.',
  'WHERE фильтрует исходные строки до GROUP BY. HAVING фильтрует уже сформированные группы и может использовать SUM или COUNT.\n\nПорядок мышления: отобрать строки → сгруппировать → вычислить агрегаты → отобрать группы → отсортировать результат.',
  'Для неотменённых продаж найдите категории с общей суммой >=100. Выведите category,total по имени.',
  'SELECT category,SUM(amount) AS total FROM sales WHERE cancelled=0 GROUP BY category HAVING SUM(amount)>=100 ORDER BY category;', [['food',150]],"CREATE TABLE sales(category TEXT,amount INTEGER,cancelled INTEGER);INSERT INTO sales VALUES('food',80,0),('food',70,0),('bus',40,0),('bus',200,1);")
 sql('transaction','Транзакция: перевод целиком или никак','transactions','Перевод денег — списание и зачисление вместе. Остановка посередине не должна уничтожить деньги.',
  'BEGIN начинает транзакцию. COMMIT сохраняет все её изменения, ROLLBACK отменяет их.\n\nВ задании сумма балансов должна остаться 150. Проверяйте количество обновлённых строк и ограничения. В реальном многопользовательском приложении нужны также подходящая изоляция и блокировки; один учебный клиент не моделирует гонки между людьми.',
  'Переведите 30 со счёта 1 на счёт 2 одной транзакцией и зафиксируйте её.',
  'BEGIN; UPDATE accounts SET balance=balance-30 WHERE id=1; UPDATE accounts SET balance=balance+30 WHERE id=2; COMMIT;', [[1,70],[2,80]], 'CREATE TABLE accounts(id INTEGER PRIMARY KEY,balance INTEGER CHECK(balance>=0));INSERT INTO accounts VALUES(1,100),(2,50);',query='SELECT id,balance FROM accounts ORDER BY id;',level='Junior+')
 sql('savepoint','SAVEPOINT: отменить часть изменений','transactions','В черновике можно отменить последнее исправление, сохранив более ранние.',
  'SAVEPOINT name ставит отметку внутри транзакции. ROLLBACK TO name отменяет изменения после неё. RELEASE убирает отметку, но не заменяет внешний COMMIT.\n\nОбычный ROLLBACK откатывает всю транзакцию. После отката к отметке можно продолжать работу.',
  'Добавьте good, поставьте отметку, добавьте bad, откатите только bad и зафиксируйте good.',
  "BEGIN;INSERT INTO notes VALUES('good');SAVEPOINT draft;INSERT INTO notes VALUES('bad');ROLLBACK TO draft;RELEASE draft;COMMIT;", [['good']], 'CREATE TABLE notes(text TEXT);',query='SELECT text FROM notes;',level='Junior+')
 sql('recursive','Рекурсивный CTE: дерево папок','cte','Чтобы найти содержимое папки, сначала берём её детей, затем детей каждого ребёнка.',
  'WITH RECURSIVE объединяет начальные строки и повторяющийся шаг через UNION ALL. Шаг ссылается на уже найденные строки.\n\nОбязательно продумайте остановку и циклы. Здесь дерево без циклов и ограничение depth<10. В реальной схеме проверяйте корректность дерева; лимит глубины — дополнительная защита, а не доказательство отсутствия цикла.',
  'Найдите корень id=1 и всех его потомков. Выведите id,depth, порядок id.',
  'WITH RECURSIVE tree(id,depth) AS (SELECT id,0 FROM folders WHERE id=1 UNION ALL SELECT f.id,t.depth+1 FROM folders f JOIN tree t ON f.parent=t.id WHERE t.depth<10) SELECT id,depth FROM tree ORDER BY id;', [[1,0],[2,1],[3,2]],'CREATE TABLE folders(id INTEGER,parent INTEGER);INSERT INTO folders VALUES(1,NULL),(2,1),(3,2),(4,NULL);',level='Junior+')
 sql('running-total','Оконные функции: накопленная сумма','windows','В банковской выписке каждая операция остаётся отдельной строкой, рядом показан баланс после неё.',
  'SUM(amount) OVER(ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) считает сумму от первой строки до текущей.\n\nGROUP BY уменьшает число строк, оконная функция сохраняет их. Укажите стабильный порядок и рамку ROWS: одинаковые значения сортировки иначе могут дать неожиданные группы.',
  'Выведите id и накопленную сумму движений, порядок id.',
  'SELECT id,SUM(amount) OVER(ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance FROM movements ORDER BY id;', [[1,100],[2,70],[3,120]],'CREATE TABLE movements(id INTEGER,amount INTEGER);INSERT INTO movements VALUES(1,100),(2,-30),(3,50);',level='Junior+')
 sql('view','VIEW: именованный запрос','views','Сохранённый фильтр в каталоге показывает свежие данные каждый раз, а не старую фотографию.',
  'CREATE VIEW name AS SELECT... сохраняет определение запроса. Обычное представление не хранит отдельную копию результата.\n\nИзменения базовой таблицы видны при следующем SELECT из VIEW. Представление помогает повторно использовать сложный запрос, но само по себе не ускоряет вычисления.',
  'Создайте available с id,name товаров со stock>0.',
  'CREATE VIEW available AS SELECT id,name FROM products WHERE stock>0;', [[1,'Tea']],"CREATE TABLE products(id INTEGER,name TEXT,stock INTEGER);INSERT INTO products VALUES(1,'Tea',2),(2,'Milk',0);",query='SELECT id,name FROM available ORDER BY id;')
 sql('upsert','UPSERT: добавить или обновить','constraints','Если товар уже есть в накладной, прибавляем количество, иначе заводим новую строку.',
  'INSERT ... ON CONFLICT(key) DO UPDATE разрешает конфликт уникального ключа. excluded содержит значения, которые пытались вставить.\n\nУказывайте нужный ключ явно. В отличие от SQLite REPLACE, UPSERT обновляет существующую строку без обязательного удаления и повторного создания.',
  'Прибавьте 3 к количеству tea через UPSERT и добавьте milk с количеством 2.',
  "INSERT INTO stock VALUES('tea',3) ON CONFLICT(name) DO UPDATE SET qty=stock.qty+excluded.qty; INSERT INTO stock VALUES('milk',2) ON CONFLICT(name) DO UPDATE SET qty=stock.qty+excluded.qty;", [['milk',2],['tea',8]],"CREATE TABLE stock(name TEXT PRIMARY KEY,qty INTEGER);INSERT INTO stock VALUES('tea',5);",query='SELECT name,qty FROM stock ORDER BY name;')
 sql('normalization','Проектирование: связи и внешние ключи','schema','Если адрес клиента повторяется в каждой покупке, его придётся исправлять много раз. Отдельная таблица клиентов устраняет эту проблему.',
  'Первичный ключ идентифицирует строку. Внешний ключ связывает заказ с существующим клиентом. NOT NULL запрещает отсутствие обязательной связи.\n\nЭто основа нормализации: один факт хранится в одном месте. Для связи многие-ко-многим нужна промежуточная таблица с двумя внешними ключами. SQLite в DevForge включает foreign_keys для каждой базы.',
  'Создайте orders(id INTEGER PRIMARY KEY,client_id INTEGER NOT NULL REFERENCES clients(id),amount INTEGER CHECK(amount>=0)). Добавьте заказ 1 для клиента 1 на 200.',
  'CREATE TABLE orders(id INTEGER PRIMARY KEY,client_id INTEGER NOT NULL REFERENCES clients(id),amount INTEGER CHECK(amount>=0));INSERT INTO orders VALUES(1,1,200);', [[1,200]],"CREATE TABLE clients(id INTEGER PRIMARY KEY,name TEXT);INSERT INTO clients VALUES(1,'Ada');",query='SELECT client_id,amount FROM orders;',level='Junior+',challenge='Расширьте проект до каталога товаров и order_items. Нарисуйте связи на бумаге; объясните, почему имя клиента не нужно повторять в каждой позиции заказа.')
 # Verify actual integrity, not only that a row was inserted.
 lessons[-1]['tests'].append({'id':lang+'-normalization-fk','label':'Несуществующий клиент отклонён','query':'$reject:INSERT INTO orders VALUES(2,999,10);','expected':True})
 sql('capstone','Проект: отчёт магазина без двойного подсчёта','project','Заказ состоит из нескольких позиций. Соединение с товарами не должно превращать один заказ в несколько полных сумм.',
  'Сначала определите зерно данных: одна строка позиции, заказа или клиента. Для выручки позиций умножьте quantity на unit_price, затем суммируйте по клиенту.\n\nLEFT JOIN сохраняет клиентов без покупок. COALESCE превращает пустой SUM в ноль. Цена позиции сохраняется на момент покупки: изменение каталога не должно менять историю.',
  'Выведите name и total каждого клиента: сумма qty*price, ноль без покупок. Порядок по name.',
  'SELECT c.name,COALESCE(SUM(i.qty*i.price),0) AS total FROM clients c LEFT JOIN orders o ON o.client_id=c.id LEFT JOIN items i ON i.order_id=o.id GROUP BY c.id,c.name ORDER BY c.name;', [['Ada',350],['Linus',0]],"CREATE TABLE clients(id INTEGER PRIMARY KEY,name TEXT);CREATE TABLE orders(id INTEGER PRIMARY KEY,client_id INTEGER REFERENCES clients(id));CREATE TABLE items(order_id INTEGER REFERENCES orders(id),qty INTEGER,price INTEGER);INSERT INTO clients VALUES(1,'Ada'),(2,'Linus');INSERT INTO orders VALUES(1,1),(2,1);INSERT INTO items VALUES(1,2,100),(1,1,50),(2,1,100);",level='Junior+',challenge='Добавьте отменённые заказы, возвраты и ежемесячный отчёт. Подготовьте схему, начальные данные и 5 запросов. Объясните, где нужны индексы и как вы проверили план запроса.')
 if lang=='sql':
  sql('index','Индекс и план запроса','performance','Алфавитный указатель книги помогает искать тему без чтения всех страниц, но его нужно обновлять при изменении книги.',
   'CREATE INDEX ускоряет подходящие условия поиска и сортировки ценой места и более дорогой записи. EXPLAIN QUERY PLAN показывает SCAN или SEARCH и выбранный индекс.\n\nНе индексируйте каждую колонку наугад. Составной индекс (a,b) обычно полезен для поиска по a и по a,b; запрос только по b может им не воспользоваться.',
   'Создайте индекс idx_events_kind на events(kind). Изучите план EXPLAIN QUERY PLAN SELECT * FROM events WHERE kind=\'login\'.',
   'CREATE INDEX idx_events_kind ON events(kind);', [['idx_events_kind']],"CREATE TABLE events(id INTEGER,kind TEXT);INSERT INTO events VALUES(1,'login'),(2,'logout');",query="SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_kind';",level='Junior+')
  sql('trigger','Триггер: журнал изменений','triggers','На проходной автоматически записывают вход каждого посетителя. Главное действие и запись в журнале происходят вместе.',
   'AFTER INSERT запускает триггер после добавления строки. NEW содержит новую строку, OLD используется при UPDATE/DELETE.\n\nТриггеры скрывают дополнительную работу за обычным SQL, поэтому документируйте их. Не создавайте взаимно вызывающиеся циклы.',
   'Создайте триггер audit_insert: после вставки в notes добавляйте NEW.text в audit. Добавьте hello в notes.',
   "CREATE TRIGGER audit_insert AFTER INSERT ON notes BEGIN INSERT INTO audit VALUES(NEW.text); END;INSERT INTO notes VALUES('hello');", [['hello']], 'CREATE TABLE notes(text TEXT);CREATE TABLE audit(text TEXT);',query='SELECT text FROM audit;')
  sql('migration','Миграция схемы без потери данных','schema','В картотеку добавляют новое поле, сохраняя существующие карточки.',
   'ALTER TABLE ADD COLUMN расширяет таблицу. DEFAULT задаёт значение для существующих строк и будущих вставок без поля.\n\nИзменение схемы оформляйте отдельной версионированной миграцией. Перед реальными миграциями делают резервную копию и проверяют обновление на копии базы.',
   'Добавьте в tasks колонку done INTEGER NOT NULL DEFAULT 0 и отметьте задачу id=1 выполненной.',
   'ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0;UPDATE tasks SET done=1 WHERE id=1;', [[1,'Read',1],[2,'Write',0]],"CREATE TABLE tasks(id INTEGER PRIMARY KEY,title TEXT);INSERT INTO tasks VALUES(1,'Read'),(2,'Write');",query='SELECT id,title,done FROM tasks ORDER BY id;',level='Junior+')
 else:
  sql('arrays','Массивы PostgreSQL и ANY','types','Теги заметки можно хранить рядом с ней, если это небольшой набор. Для больших связей и отдельных сущностей лучше таблица связей.',
   'ARRAY[...] создаёт массив. value=ANY(array) проверяет наличие значения. Индексы массивов PostgreSQL обычно начинаются с 1, в отличие от Python и C.\n\nМассив не заменяет нормализацию автоматически. Выбирайте его для цельного атрибута, а отдельные сущности связывайте внешними ключами.',
   'Найдите title заметок, где tags содержит sql. Отсортируйте title.',
   "SELECT title FROM notes WHERE 'sql'=ANY(tags) ORDER BY title;",[['Learn']],"CREATE TABLE notes(title TEXT,tags TEXT[]);INSERT INTO notes VALUES('Learn',ARRAY['sql','python']),('Draw',ARRAY['art']);")
  sql('jsonb-path','JSONB: вложенные значения','json','Дополнительные характеристики товаров могут различаться, но основные поля и ограничения лучше держать в колонках.',
   '-> возвращает JSON, ->> возвращает текст. Для вложенного пути используется #>> с массивом ключей. Текстовое число нужно привести к типу перед сравнением.\n\nJSONB удобен для гибких атрибутов, но не отменяет проверку структуры. Отсутствующий ключ даёт NULL.',
   'Выведите id товаров с целым stock.count >=2, порядок id.',
   "SELECT id FROM products WHERE (data #>> '{stock,count}')::integer>=2 ORDER BY id;",[[1]],'''CREATE TABLE products(id INTEGER,data JSONB);INSERT INTO products VALUES(1,'{"stock":{"count":3}}'),(2,'{"stock":{"count":0}}'),(3,'{}');''',level='Junior+')
  sql('date','Даты и интервалы','dates','Срок сдачи книги считают от даты выдачи, не предполагая, что каждый месяц имеет 30 дней.',
   'DATE хранит календарную дату, TIMESTAMP — дату и время, TIMESTAMPTZ — момент времени с отображением в выбранном часовом поясе. INTERVAL описывает длительность.\n\nДля воспроизводимого отчёта передавайте фиксированные границы вместо неявного now(). Диапазон >= начало AND < конец удобен для соседних периодов без пересечения.',
   'Верните текст даты через 7 дней после 2024-02-26: учтите високосный февраль.',
   "SELECT ((DATE '2024-02-26' + INTERVAL '7 days')::date)::text;",[['2024-03-04']])
  sql('partial-index','Частичный индекс и EXPLAIN','performance','Отдельная полка только для открытых заказов меньше полного склада и помогает искать именно текущую работу.',
   'CREATE INDEX ... WHERE condition создаёт частичный индекс. Запрос должен подразумевать это условие, иначе индекс не подходит.\n\nEXPLAIN показывает оценку плана; EXPLAIN ANALYZE реально выполняет запрос. На маленькой таблице последовательное чтение может быть дешевле индекса — это не ошибка.',
   'Создайте idx_open на tickets(owner) только для closed=false.',
   'CREATE INDEX idx_open ON tickets(owner) WHERE closed=false;', [['idx_open']], 'CREATE TABLE tickets(id INTEGER PRIMARY KEY,owner TEXT,closed BOOLEAN NOT NULL);',query="SELECT indexname FROM pg_indexes WHERE schemaname='public' AND indexname='idx_open';",level='Junior+')
  sql('function','SQL-функция с явным контрактом','functions','Рецепт блюда один, а число порций меняется. Функция получает аргумент и возвращает результат.',
   'CREATE FUNCTION задаёт типы аргументов и результата. LANGUAGE SQL подходит для вычисления через SQL-выражение.\n\nIMMUTABLE обещает одинаковый результат при одинаковых аргументах и не подходит для чтения изменяемых таблиц. Не ставьте его только ради скорости.',
   'Создайте add_tax(cents integer) RETURNS integer: прибавляет 20 процентов с целочисленным делением.',
   'CREATE FUNCTION add_tax(cents integer) RETURNS integer LANGUAGE SQL IMMUTABLE AS $$ SELECT cents*120/100 $$;', [[120,0]],query='SELECT add_tax(100),add_tax(0);',level='Junior+')
  sql('materialized','Материализованное представление','views','Фотография склада открывается быстро, но новые поставки на ней не появятся до нового снимка.',
   'MATERIALIZED VIEW хранит результат запроса. REFRESH MATERIALIZED VIEW пересчитывает его.\n\nОбычное VIEW показывает актуальные данные, материализованное может быть устаревшим. Определите допустимую задержку обновления перед выбором.',
   'Создайте summary с SUM(amount) AS total, добавьте продажу 50 и обновите summary.',
   'CREATE MATERIALIZED VIEW summary AS SELECT SUM(amount) AS total FROM sales;INSERT INTO sales VALUES(50);REFRESH MATERIALIZED VIEW summary;',[[150]],'CREATE TABLE sales(amount INTEGER);INSERT INTO sales VALUES(100);',query='SELECT total FROM summary;',level='Junior+')
