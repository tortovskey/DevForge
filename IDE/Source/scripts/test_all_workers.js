const fs = require('fs');
const path = require('path');

const lessons = JSON.parse(fs.readFileSync('content/lessons.json', 'utf8'));

// Helper to test transpiled worker
function testWorkerRunner(lang, workerFile, transpileFnName, polyfills = () => {}, wrapperFn = null, customScope = {}) {
  const langLessons = lessons.filter(l => l.language === lang);
  console.log(`\n================ Testing ${lang.toUpperCase()} (${langLessons.length} lessons) ================`);

  const workerContent = fs.readFileSync(path.join('frontend/public/workers', workerFile), 'utf8');
  
  // Extract transpile function
  const transpileMatch = workerContent.match(new RegExp(`function ${transpileFnName}\\([\\s\\S]*?\\n\\}`));
  if (!transpileMatch) {
    console.log(`[SKIP] Could not extract ${transpileFnName} from ${workerFile}`);
    return;
  }

  eval(transpileMatch[0]);
  const transpile = eval(transpileFnName);

  polyfills();

  let passed = 0, failed = 0, errors = 0;

  for (const l of langLessons) {
    const code = l.guide.solution;
    let transpiled;
    try {
      transpiled = transpile(code);
    } catch (e) {
      console.log(`[FAIL TRANSPILE] ${l.id}: ${e.message}`);
      errors++;
      continue;
    }

    let output = '';
    const scope = {
      __println__: (...args) => { output += args.join(' ') + '\n'; },
      __print__: (...args) => { output += args.join(' '); },
      __prompt__: () => ((l.tests[0] && l.tests[0].stdin !== undefined) ? String(l.tests[0].stdin) : (l.stdin || '')),
      __parse_val__: (s) => (isNaN(s) ? s : parseFloat(s)),
      Math: Math,
      String: String,
      Array: Array,
      Boolean: Boolean,
      Number: Number,
      parseInt: parseInt,
      parseFloat: parseFloat,
      JSON: JSON,
      ...customScope
    };
    if (lang === '1c') {
      scope.Сообщить = (...args) => { output += args.join(' ') + '\n'; };
    }

    try {
      let codeToExec = transpiled;
      if (wrapperFn) {
        codeToExec = wrapperFn(transpiled);
      }
      new Function('__scope__', `with (__scope__) { ${codeToExec} }`)(scope);
      
      const expected = l.tests[0] && l.tests[0].expected !== undefined ? String(l.tests[0].expected).trim() : null;
      const actual = output.trim();

      if (expected === null || actual === expected) {
        passed++;
      } else {
        console.log(`[FAIL] ${l.id}: expected: ${JSON.stringify(expected)} | got: ${JSON.stringify(actual)}`);
        failed++;
      }
    } catch (err) {
      console.log(`[ERROR] ${l.id}: ${err.message}`);
      errors++;
    }
  }

  console.log(`Result for ${lang.toUpperCase()}: ${passed} PASSED, ${failed} FAILED, ${errors} ERRORS (out of ${langLessons.length})`);
}

// 1. C#
testWorkerRunner('csharp', 'csharp.js', 'transpileCSharp', () => {
  if (!Array.prototype.Add) {
    Object.defineProperty(Array.prototype, 'Length', { get() { return this.length; }, configurable: true });
    Object.defineProperty(Array.prototype, 'Count', { get() { return this.length; }, configurable: true });
    Array.prototype.Add = function(v) { this.push(v); return this.length; };
  }
}, (code) => `${code}\nif (typeof __main__ === 'function') { __main__(); } else if (typeof Program !== 'undefined' && typeof Program.Main === 'function') { Program.Main(); }`);

// 2. Java
class JavaArrayList extends Array {
  add(val) { this.push(val); return true; }
  get(i) { return this[i]; }
  size() { return this.length; }
  contains(val) { return this.includes(val); }
  remove(i) { return typeof i === 'number' ? this.splice(i, 1)[0] : false; }
}
class JavaHashMap extends Map {
  put(k, v) { this.set(k, v); return v; }
  get(k) { return super.get(k); }
  containsKey(k) { return this.has(k); }
  remove(k) { return this.delete(k); }
  size() { return this.size; }
  values() { return Array.from(super.values()); }
}
const JavaArrays = {
  asList: (...args) => (Array.isArray(args[0]) ? args[0] : args)
};
const JavaCollections = {
  sort: (list, comp) => list.sort(comp)
};

class JavaException extends Error {
  constructor(msg) { super(msg); this.message = msg; }
  getMessage() { return this.message; }
}

if (!String.prototype.isEmpty) {
  String.prototype.isEmpty = function() { return this.length === 0; };
}
if (!String.join) {
  String.join = (sep, arr) => (Array.isArray(arr) ? arr.join(sep) : String(arr));
}

testWorkerRunner('java', 'java.js', 'transpileJava', () => {}, (code) => `${code}\nif (typeof __main__ === 'function') { __main__(); } else if (typeof Main !== 'undefined' && typeof Main.main === 'function') { Main.main(); } else if (typeof Program !== 'undefined' && typeof Program.main === 'function') { Program.main(); } else if (typeof main === 'function') { main(); }`, {
  ArrayList: JavaArrayList,
  HashMap: JavaHashMap,
  Arrays: JavaArrays,
  Collections: JavaCollections,
  Exception: JavaException,
  OverdraftException: class extends JavaException {}
});

// 3. 1C
class __BslArray__ extends Array {
  Добавить(val) { this.push(val); }
  Количество() { return this.length; }
  Очистить() { this.length = 0; }
  Удалить(idx) { this.splice(idx, 1); }
  Вставить(idx, val) { this.splice(idx, 0, val); }
  Найти(val) { const i = this.indexOf(val); return i === -1 ? null : i; }
}
class __BslStructure__ {
  constructor(keysStr, ...vals) {
    if (keysStr && typeof keysStr === 'string') {
      const keys = keysStr.split(',').map(s => s.trim()).filter(Boolean);
      for (let i = 0; i < keys.length; i++) this[keys[i]] = vals[i] !== undefined ? vals[i] : null;
    }
  }
  Вставить(key, val) { this[key] = val; }
  Свойство(key) { return Object.prototype.hasOwnProperty.call(this, key); }
  Удалить(key) { delete this[key]; }
  Количество() { return Object.keys(this).length; }
}
class __BslValueTable__ {
  constructor() {
    this.Колонки = { _cols: [], Добавить: (name) => { this.Колонки._cols.push(name); }, Количество: () => this.Колонки._cols.length };
    this.Строки = new __BslArray__();
  }
  Добавить() {
    const row = {};
    for (const c of this.Колонки._cols) row[c] = null;
    this.Строки.push(row);
    return row;
  }
  Количество() { return this.Строки.length; }
}

testWorkerRunner('1c', '1c.js', 'transpileBsl', () => {}, (code) => `${code}`, {
  __BslArray__,
  __BslStructure__,
  __BslValueTable__,
  СтрДлина: (s) => String(s).length,
  ВРег: (s) => String(s).toUpperCase(),
  НРег: (s) => String(s).toLowerCase(),
  СокрЛП: (s) => String(s).trim(),
  Формат: (v) => String(v),
  Окр: (v) => Math.round(v),
  Цел: (v) => Math.floor(v),
  ТекущаяДата: () => new Date()
});

// 4. Objective-C
testWorkerRunner('objc', 'objc.js', 'transpileObjC', () => {}, (code) => `${code}\nif (typeof main === 'function') { main(); }`);

// 5. C++
testWorkerRunner('cpp', 'cpp.js', 'transpileCpp', () => {}, (code) => `${code}\nif (typeof main === 'function') { main(); }`);

// 6. Rust
testWorkerRunner('rust', 'rust.js', 'transpileRust', () => {}, (code) => `${code}\nif (typeof main === 'function') { main(); }`);
