/* DevForge Java Worker: transpiles educational Java code to JavaScript and runs in Web Worker */
if (typeof String.join !== 'function') {
  String.join = (sep, arr) => (Array.isArray(arr) ? arr.join(sep) : String(arr));
}
class Exception extends Error {
  constructor(msg) { super(msg); this.message = msg; }
  getMessage() { return this.message; }
}

let output = '', errors = '';

class ArrayList extends Array {
  add(val) { this.push(val); return true; }
  get(i) { return this[i]; }
  size() { return this.length; }
  contains(val) { return this.includes(val); }
  remove(i) { return typeof i === 'number' ? this.splice(i, 1)[0] : false; }
}

class HashMap extends Map {
  put(k, v) { this.set(k, v); return v; }
  get(k) { return super.get(k); }
  containsKey(k) { return this.has(k); }
  remove(k) { return this.delete(k); }
  size() { return this.size; }
  values() { return Array.from(super.values()); }
}

const Arrays = {
  asList: (...args) => (Array.isArray(args[0]) ? args[0] : args)
};

const Collections = {
  sort: (list, comp) => list.sort(comp)
};

function append(val, isError = false) {
  const limit = 24000;
  const str = String(val);
  if (isError) {
    if (errors.length < limit) errors += str.slice(0, limit - errors.length);
  } else {
    if (output.length < limit) output += str.slice(0, limit - output.length);
  }
}

/**
 * Transpiles simple educational Java code into executable JavaScript.
 */
function transpileJava(javaCode) {
  let js = javaCode;

  // 0. Casts and catch clauses
  js = js.replace(/\(\s*\([A-Za-z_]\w*\)\s*([A-Za-z_][\w\.]*)\s*\)/g, '$1');
  js = js.replace(/catch\s*\(\s*[A-Za-z_]\w*\s+(\w+)\s*\)/g, 'catch ($1)');
  // 1. Remove imports and package
  js = js.replace(/import\s+[\w\.*]+;/g, '');
  js = js.replace(/package\s+[\w\.*]+;/g, '');
  js = js.replace(/@\w+\b/g, '');

  // 2. Scanner
  js = js.replace(/Scanner\s+\w+\s*=\s*new\s+Scanner\s*\(\s*System\.in\s*\)\s*;/g, '');
  js = js.replace(/\b\w+\.nextInt\s*\(\s*\)/g, 'parseInt(__prompt__())');
  js = js.replace(/\b\w+\.nextDouble\s*\(\s*\)/g, 'parseFloat(__prompt__())');
  js = js.replace(/\b\w+\.nextLine\s*\(\s*\)/g, '__prompt__()');
  js = js.replace(/\b\w+\.next\s*\(\s*\)/g, '__prompt__()');

  // 3. System.out.println and print
  js = js.replace(/System\.out\.println\s*\(/g, '__println__(');
  js = js.replace(/System\.out\.print\s*\(/g, '__print__(');

  // 4. Array initializers: int[] a = {1, 2, 3}; -> [1, 2, 3]
  js = js.replace(/(\b[\w\[\]<>]+\s+\w+\s*=\s*)\{([^}]+)\};/g, '$1[$2];');
  js = js.replace(/new\s+(?:int|double|float|long|short|byte)\s*\[\s*([^\]]+)\s*\]/g, 'new Array($1).fill(0)');
  js = js.replace(/new\s+(?:boolean)\s*\[\s*([^\]]+)\s*\]/g, 'new Array($1).fill(false)');
  js = js.replace(/new\s+(?:String|Object|\w+)\s*\[\s*([^\]]+)\s*\]/g, 'new Array($1).fill(null)');

  // 5. Enhanced for loop: for (int x : arr) -> for (let x of arr)
  js = js.replace(/for\s*\(\s*(?:final\s+)?[\w\[\]<>]+\s+(\w+)\s*:\s*([^)]+)\)/g, 'for (let $1 of $2)');

  // 6. String .equals(other) -> === other
  js = js.replace(/\.equals\s*\(([^)]+)\)/g, ' === $1');

  // 7. Extract Main class methods as top-level functions so they can be called directly
  js = js.replace(/\b(?:public\s+)?class\s+(?:Main|Program)\s*\{([\s\S]*?)\}\s*$/g, (match, body) => {
    let transformed = body;

    // Convert main: public static void main(...) -> function __main__()
    transformed = transformed.replace(/\b(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:void|int)\s+main\s*\([^)]*\)\s*\{/g, 'function __main__() {');

    // Handle method overloading: collect method names and param counts
    const methodSignatures = {};
    const methodScanRegex = /\b(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:void|int|double|float|boolean|String|long|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g;
    let m;
    while ((m = methodScanRegex.exec(transformed)) !== null) {
      const name = m[1];
      if (name !== 'if' && name !== 'while' && name !== 'for' && name !== 'switch' && name !== '__main__') {
        const argCount = m[2].trim() ? m[2].split(',').length : 0;
        if (!methodSignatures[name]) methodSignatures[name] = [];
        methodSignatures[name].push({ argCount });
      }
    }

    const overloadedIdx = {};

    // Convert other methods inside Main to functions
    transformed = transformed.replace(/\b(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:void|int|double|float|boolean|String|long|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (m, name, args) => {
      if (name === 'if' || name === 'while' || name === 'for' || name === 'switch' || name === '__main__' || name === 'function') return m;
      
      const cleanArgs = args.split(',').map(arg => {
        const parts = arg.trim().split(/\s+/);
        return parts[parts.length - 1];
      }).filter(Boolean).join(', ');

      if (methodSignatures[name] && methodSignatures[name].length > 1) {
        overloadedIdx[name] = (overloadedIdx[name] || 0) + 1;
        const fnName = `${name}__overload${overloadedIdx[name]}`;
        return `/* overload */ function ${fnName}(${cleanArgs}) {`;
      }

      return `function ${name}(${cleanArgs}) {`;
    });

    // If there were overloaded functions, create the dispatcher
    for (const [name, sigs] of Object.entries(methodSignatures)) {
      if (sigs.length > 1) {
        let dispatcher = `\nfunction ${name}(...__args) {\n`;
        for (let i = 0; i < sigs.length; i++) {
          const sig = sigs[i];
          const fnName = `${name}__overload${i + 1}`;
          if (i === sigs.length - 1) {
            dispatcher += `    return ${fnName}(...__args);\n`;
          } else {
            dispatcher += `    if (__args.length === ${sig.argCount}) return ${fnName}(...__args);\n`;
          }
        }
        dispatcher += `}\n`;
        transformed += dispatcher;
      }
    }

    return transformed;
  });

  // 8. If main is outside:
  js = js.replace(/\b(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:void|int)\s+main\s*\([^)]*\)\s*\{/g, 'function __main__() {');

  // 9. Find custom class names
  const classNames = [];
  const classRegex = /\bclass\s+(\w+)/g;
  let cm;
  while ((cm = classRegex.exec(js)) !== null) {
    if (cm[1] !== 'Main' && cm[1] !== 'Program') classNames.push(cm[1]);
  }

  // 10. Handle custom classes: fields, constructors, methods
  for (const cname of classNames) {
    const classBlockRegex = new RegExp(`(\\bclass\\s+${cname}(?:\\s+extends\\s+\\w+)?\\s*\\{)([\\s\\S]*?)(\\n\\})`, 'g');
    js = js.replace(classBlockRegex, (_, head, body, tail) => {
      let classBody = body;

      // Depth-aware extraction of class fields at depth 0
      let depth = 0;
      let stmt = '';
      const fields = [];
      for (let i = 0; i < classBody.length; i++) {
        const ch = classBody[i];
        if (ch === '{') {
          depth++;
          stmt = '';
        } else if (ch === '}') {
          depth--;
          stmt = '';
        } else if (ch === ';') {
          if (depth === 0) {
            const beforeAssign = stmt.split('=')[0].trim();
            const m = beforeAssign.match(/\b([A-Za-z_]\w*)$/);
            if (m && m[1] !== 'return' && m[1] !== cname && m[1] !== 'class') {
              fields.push(m[1]);
            }
          }
          stmt = '';
        } else {
          stmt += ch;
        }
      }

      // Convert constructor: [public] ClassName(args) { ... } -> constructor(cleanArgs) { ... }
      const ctorRegex = new RegExp(`\\b(?:(?:public|private|protected)\\s+)?${cname}\\s*\\(([^)]*)\\)\\s*\\{([\\s\\S]*?)\\}`, 'g');
      classBody = classBody.replace(ctorRegex, (m, args, ctorContent) => {
        const cleanArgs = args.split(',').map(arg => {
          const parts = arg.trim().split(/\s+/);
          return parts[parts.length - 1];
        }).filter(Boolean).join(', ');

        return `constructor(${cleanArgs}) {${ctorContent}}`;
      });

      // Convert methods inside class
      classBody = classBody.replace(/\b(?:(?:public|private|protected)\s+)?(?:(static)\s+)?(?:void|int|double|float|boolean|String|long|char|Object|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+[\w,\s]+)?\s*\{/g, (m, isStatic, name, args) => {
        if (name === 'if' || name === 'while' || name === 'for' || name === 'switch' || name === 'constructor' || name === cname) return m;
        const cleanArgs = args.split(',').map(arg => {
          const parts = arg.trim().split(/\s+/);
          return parts[parts.length - 1];
        }).filter(Boolean).join(', ');
        return `${isStatic ? 'static ' : ''}${name}(${cleanArgs}) {`;
      });

      // In methods, replace field references with this.field
      for (const f of fields) {
        classBody = classBody.replace(/(\b\w+\s*\([^)]*\)\s*\{)([\s\S]*?)(\})/g, (methodMatch, mHead, mBody, mTail) => {
          if (mHead.includes('constructor')) return methodMatch;
          const fieldUseRegex = new RegExp(`(?<!this\\.|let |const |var )\\b${f}\\b`, 'g');
          const updatedBody = mBody.replace(fieldUseRegex, `this.${f}`);
          return mHead + updatedBody + mTail;
        });
      }

      // Clean field declarations at depth 0: Type f [= val]; -> f [= val];
      for (const f of fields) {
        const fDeclRegex = new RegExp(`\\b(?:(?:public|private|protected)\\s+)?(?:static\\s+)?(?:final\\s+)?(?:int|double|float|boolean|String|long|char|Object|[A-Za-z_]\\w*(?:<[^>]+>)?)(?:\\[\\])*\\s+${f}\\s*(=\\s*[^;]+)?;`, 'g');
        classBody = classBody.replace(fDeclRegex, (m, init) => `${f}${init ? ' ' + init : ''};`);
      }

      return head + classBody + tail;
    });
  }

  // 10.5 Remove diamond/generic operators from instantiation: new ArrayList<>() -> new ArrayList()
  js = js.replace(/new\s+([A-Za-z_]\w*)\s*<[^>]*>\s*\(/g, 'new $1(');

  // 11. In top-level / functions, clean local variable declarations: int x = 5;
  js = js.replace(/\b(?:int|double|float|boolean|String|long|char|Object|var|[A-Z]\w*(?:<[^>]+>)?)(?:\[\])*\s+(\w+)\s*(=|;)/g, (match, vname, rest) => {
    if (vname === 'return' || vname === 'if' || vname === 'while' || vname === 'for' || vname === 'class' || vname === 'switch') return match;
    return `let ${vname} ${rest}`;
  });

  // 12. Clean leftover access modifiers
  js = js.replace(/\b(?:public|private|protected|final)\s+/g, '');

  return js;
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

    const println = (...args) => {
      const str = args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ');
      append(str + '\n');
    };

    const print = (...args) => {
      const str = args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ');
      append(str);
    };

    self.postMessage({ type: 'phase', phase: 'compile' });
    const jsTranspiled = transpileJava(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });

    const wrappedCode = `
      ${jsTranspiled}

      // Auto-invoke main if defined in a class
      if (typeof __main__ === 'function') {
        __main__();
      } else if (typeof Main !== 'undefined' && typeof Main.main === 'function') {
        Main.main();
      } else if (typeof Program !== 'undefined' && typeof Program.main === 'function') {
        Program.main();
      } else if (typeof Solution !== 'undefined' && typeof Solution.main === 'function') {
        Solution.main();
      } else if (typeof App !== 'undefined' && typeof App.main === 'function') {
        App.main();
      } else if (typeof main === 'function') {
        main();
      }
    `;

    const userScope = {
      __println__: println,
      __print__: print,
      __prompt__: fakePrompt,
      Math: Math,
      String: String,
      Integer: {
        parseInt: (s) => parseInt(s, 10),
        MAX_VALUE: 2147483647,
        MIN_VALUE: -2147483648
      },
      Double: {
        parseDouble: (s) => parseFloat(s)
      }
    };

    const execFn = new Function('__scope__', `with (__scope__) { ${wrappedCode} }`);
    execFn(userScope);

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
            const testScope = { ...userScope, __prompt__: testPrompt };
            new Function('__scope__', `with (__scope__) { ${wrappedCode} }`)(testScope);
            actualVal = output.trim();
          } else if (test.expression) {
            const strippedExpr = transpileJava(test.expression);
            try {
              const testFn = new Function('__scope__', `with (__scope__) { ${jsTranspiled}\n;return (${strippedExpr}); }`);
              actualVal = testFn(userScope);
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
