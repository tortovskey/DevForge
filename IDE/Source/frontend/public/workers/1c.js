/* DevForge 1C BSL Worker: executes 1C:Enterprise code natively inside disposable Web Worker */
let output = '', errors = '';

function append(val, isError = false) {
  const limit = 24000;
  const str = String(val);
  if (isError) {
    if (errors.length < limit) errors += str.slice(0, limit - errors.length);
  } else {
    if (output.length < limit) output += str.slice(0, limit - output.length);
  }
}

class BslArray extends Array {
  Добавить(val) { this.push(val); }
  Количество() { return this.length; }
  Очистить() { this.length = 0; }
  Удалить(idx) { this.splice(idx, 1); }
  Вставить(idx, val) { this.splice(idx, 0, val); }
  Найти(val) { const i = this.indexOf(val); return i === -1 ? null : i; }
}

class BslStructure {
  constructor(keysStr, ...vals) {
    if (keysStr && typeof keysStr === 'string') {
      const keys = keysStr.split(',').map(s => s.trim()).filter(Boolean);
      for (let i = 0; i < keys.length; i++) {
        this[keys[i]] = vals[i] !== undefined ? vals[i] : null;
      }
    }
  }
  Вставить(key, val) { this[key] = val; }
  Свойство(key, outVal) { return Object.prototype.hasOwnProperty.call(this, key); }
  Удалить(key) { delete this[key]; }
  Количество() { return Object.keys(this).length; }
}

class BslValueTable {
  constructor() {
    this.Колонки = {
      _cols: [],
      Добавить: (name) => { this.Колонки._cols.push(name); },
      Количество: () => this.Колонки._cols.length
    };
    this.Строки = new BslArray();
  }
  Добавить() {
    const row = {};
    for (const c of this.Колонки._cols) row[c] = null;
    this.Строки.push(row);
    return row;
  }
  Количество() { return this.Строки.length; }
}

function transpileBsl(bslCode) {
  let js = bslCode;

  const cyrWord = (w, flags = 'gi') => new RegExp(`(?<![а-яА-ЯёЁ\\w])${w}(?![а-яА-ЯёЁ\\w])`, flags);

  // 1. Comments: // already match JS

  // 2. Constants / Booleans / Null
  js = js.replace(cyrWord('Истина'), 'true');
  js = js.replace(cyrWord('Ложь'), 'false');
  js = js.replace(cyrWord('Неопределено'), 'null');
  js = js.replace(cyrWord('Null'), 'null');

  // 3. Comparisons: <> -> !==
  js = js.replace(/<>/g, '!==');

  // 4. Logical operators
  js = js.replace(cyrWord('И'), '&&');
  js = js.replace(cyrWord('ИЛИ'), '||');
  js = js.replace(cyrWord('НЕ'), '!');

  // 5. Built-in constructors:
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Новый\\s+Массив(?![а-яА-ЯёЁ\\w])`, 'gi'), 'new __BslArray__()');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Новый\\s+Структура\\s*\\(([^)]*)\\)`, 'gi'), 'new __BslStructure__($1)');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Новый\\s+Структура(?![а-яА-ЯёЁ\\w])`, 'gi'), 'new __BslStructure__()');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Новый\\s+ТаблицаЗначений(?![а-яА-ЯёЁ\\w])`, 'gi'), 'new __BslValueTable__()');

  // 6. Procedures: Процедура Имя(Args) ... КонецПроцедуры
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Процедура\\s+([а-яА-ЯёЁ\\w]+)\\s*\\(([^)]*)\\)`, 'gi'), 'function $1($2) {');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])КонецПроцедуры;?`, 'gi'), '}');

  // 7. Functions: Функция Имя(Args) ... КонецФункции
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Функция\\s+([а-яА-ЯёЁ\\w]+)\\s*\\(([^)]*)\\)`, 'gi'), 'function $1($2) {');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])КонецФункции;?`, 'gi'), '}');
  js = js.replace(cyrWord('Возврат'), 'return');

  // 8. If / ElseIf / Else / EndIf
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Если\\s+([\\s\\S]+?)\\s+Тогда(?![а-яА-ЯёЁ\\w])`, 'gi'), (_, cond) => {
    const jsCond = cond.replace(/([^=!<>]|^)=([^=]|$)/g, '$1===$2');
    return `if (${jsCond}) {`;
  });
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])ИначеЕсли\\s+([\\s\\S]+?)\\s+Тогда(?![а-яА-ЯёЁ\\w])`, 'gi'), (_, cond) => {
    const jsCond = cond.replace(/([^=!<>]|^)=([^=]|$)/g, '$1===$2');
    return `} else if (${jsCond}) {`;
  });
  js = js.replace(cyrWord('Иначе'), '} else {');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])КонецЕсли;?`, 'gi'), '}');

  // 9. While loops: Пока Условие Цикл ... КонецЦикла
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Пока\\s+([\\s\\S]+?)\\s+Цикл(?![а-яА-ЯёЁ\\w])`, 'gi'), (_, cond) => {
    const jsCond = cond.replace(/([^=!<>]|^)=([^=]|$)/g, '$1===$2');
    return `while (${jsCond}) {`;
  });

  // 10. For loops:
  // Для Сч = 1 По 10 Цикл -> for (let Сч = 1; Сч <= 10; Сч++) {
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Для\\s+([а-яА-ЯёЁ\\w]+)\\s*=\\s*([^П]+?)\\s+По\\s+([^Ц]+?)\\s+Цикл(?![а-яА-ЯёЁ\\w])`, 'gi'), 'for (let $1 = $2; $1 <= $3; $1++) {');

  // Для Каждого Элемент Из Коллекция Цикл -> for (let Элемент of Коллекция) {
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Для\\s+Каждого\\s+([а-яА-ЯёЁ\\w]+)\\s+Из\\s+([^Ц]+?)\\s+Цикл(?![а-яА-ЯёЁ\\w])`, 'gi'), 'for (let $1 of $2) {');
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])КонецЦикла;?`, 'gi'), '}');
  js = js.replace(cyrWord('Прервать'), 'break;');
  js = js.replace(cyrWord('Продолжить'), 'continue;');

  // 11. Variables: Перем Имя, Возраст; -> let Имя, Возраст;
  js = js.replace(new RegExp(`(?<![а-яА-ЯёЁ\\w])Перем\\s+([^;]+);`, 'gi'), 'let $1;');

  // 12. Prepend variable declarations for assigned variables
  const assignedVars = new Set();
  const assignRegex = /(?:^|\n)\s*([а-яА-ЯёЁ\w]+)\s*=[^=]/g;
  let am;
  while ((am = assignRegex.exec(js)) !== null) {
    const vname = am[1];
    if (vname !== 'if' && vname !== 'while' && vname !== 'for' && vname !== 'return') {
      assignedVars.add(vname);
    }
  }

  let varDecls = '';
  if (assignedVars.size > 0) {
    varDecls = `var ${Array.from(assignedVars).join(', ')};\n`;
  }

  return varDecls + js;
}

self.postMessage({ type: 'ready' });

self.onmessage = async ({ data }) => {
  output = '';
  errors = '';
  const results = [];

  try {
    const text = String(data.stdin || '').replace(/\r\n/g, '\n');
    const stdinLines = text ? text.split('\n') : [];
    if (text.endsWith('\n')) stdinLines.pop();
    let stdinPos = 0;

    const fakePrompt = () => {
      if (stdinPos < stdinLines.length) return stdinLines[stdinPos++];
      return '';
    };

    const сообщить = (...args) => {
      const str = args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ');
      append(str + '\n');
    };

    const bslScope = {
      Сообщить: сообщить,
      сообщить: сообщить,
      __BslArray__: BslArray,
      __BslStructure__: BslStructure,
      __BslValueTable__: BslValueTable,
      СтрДлина: (s) => String(s || '').length,
      НРег: (s) => String(s || '').toLowerCase(),
      ВРег: (s) => String(s || '').toUpperCase(),
      Лев: (s, n) => String(s || '').slice(0, n),
      Прав: (s, n) => String(s || '').slice(-n),
      СокрЛП: (s) => String(s || '').trim(),
      Окр: (n) => Math.round(Number(n)),
      Цел: (n) => Math.trunc(Number(n)),
      Макс: (...args) => Math.max(...args),
      Мин: (...args) => Math.min(...args),
      ВвестиСтроку: (promptText) => fakePrompt(),
      ВвестиЧисло: (promptText) => Number(fakePrompt() || 0),
      ТипЗнч: (v) => typeof v
    };

    self.postMessage({ type: 'phase', phase: 'compile' });
    const jsCode = transpileBsl(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });

    // Use with (__scope__) in non-strict mode so undeclared vars attach to scope
    const execFn = new Function('__scope__', `with (__scope__) {\n${jsCode}\n}`);
    execFn(bslScope);

    // Tests evaluation
    if (data.check && Array.isArray(data.tests)) {
      for (const test of data.tests) {
        try {
          let actualVal;
          if (test.stdin !== undefined) {
            output = '';
            errors = '';
            const testStdinLines = String(test.stdin).split('\n');
            let testPos = 0;
            const testPrompt = () => (testPos < testStdinLines.length ? testStdinLines[testPos++] : '');
            const testScope = { ...bslScope, ВвестиСтроку: testPrompt, ВвестиЧисло: () => Number(testPrompt() || 0) };
            new Function('__scope__', `with (__scope__) {\n${jsCode}\n}`)(testScope);
            actualVal = output.trim();
          } else if (test.expression) {
            const strippedExpr = transpileBsl(test.expression);
            try {
              const testFn = new Function('__scope__', `with (__scope__) {\n${jsCode}\n;return (${strippedExpr});\n}`);
              actualVal = testFn(bslScope);
            } catch (evalErr) {
              actualVal = undefined;
              throw evalErr;
            }
            if (actualVal === undefined && output.trim()) {
              actualVal = output.trim();
            }
          } else {
            actualVal = output.trim();
          }

          let serialized = actualVal;
          if (typeof actualVal === 'object' && actualVal !== null) {
            serialized = JSON.parse(JSON.stringify(actualVal));
          }
          results.push({ id: test.id, actual: serialized, error: null });
        } catch (e) {
          results.push({ id: test.id, actual: null, error: String(e).slice(0, 8000) });
        }
      }
    }

    self.postMessage({
      type: 'result',
      result: {
        stdout: output,
        stderr: errors,
        tables: [],
        results
      }
    });
  } catch (err) {
    const errorMsg = (output + '\n' + errors + '\n' + String(err)).trim();
    self.postMessage({
      type: 'result',
      result: {
        stdout: output,
        stderr: errors,
        tables: [],
        results,
        error: errorMsg.slice(0, 10000)
      }
    });
  }
};
