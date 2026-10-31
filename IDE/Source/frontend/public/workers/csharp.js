/* DevForge C# Worker: transpiles educational C# code to JavaScript and runs in Web Worker */
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

// Polyfills for C# collections in JavaScript
if (!Array.prototype.Add) {
  Object.defineProperty(Array.prototype, 'Length', {
    get() { return this.length; },
    configurable: true
  });
  Object.defineProperty(Array.prototype, 'Count', {
    get() { return this.length; },
    configurable: true
  });
  Array.prototype.Add = function(v) {
    this.push(v);
    return this.length;
  };
}

function transpileCSharp(csCode) {
  let js = csCode;

  // 1. Remove using directives
  js = js.replace(/using\s+[\w\.]+;/g, '');

  // 2. Remove file-scoped namespace or block namespace
  js = js.replace(/namespace\s+[\w\.]+\s*;?/g, '');

  // 3. Handle Console.WriteLine and Console.Write
  js = js.replace(/Console\.WriteLine\s*\(/g, '__println__(');
  js = js.replace(/Console\.Write\s*\(/g, '__print__(');

  // 4. Handle Console.ReadLine()
  js = js.replace(/Console\.ReadLine\s*\(\s*\)/g, '__prompt__()');

  // 5. Handle type conversions
  js = js.replace(/\b(?:int|Int32)\.Parse\s*\(/g, 'parseInt(');
  js = js.replace(/\b(?:double|float)\.Parse\s*\(/g, 'parseFloat(');
  js = js.replace(/Convert\.ToInt32\s*\(/g, 'parseInt(');
  js = js.replace(/Convert\.ToDouble\s*\(/g, 'parseFloat(');

  // 6. Handle C# string interpolation: $"...{x}..." -> `...${x}...`
  js = js.replace(/\$"([^"]*)"/g, (_, content) => {
    const interpolated = content.replace(/\{([^}]+)\}/g, '${$1}');
    return '`' + interpolated + '`';
  });

  // 7. Handle C# auto-properties: public int Age { get; set; } = 0; -> Age = 0;
  js = js.replace(/\b(?:(?:public|private|protected|internal)\s+)?[\w<>\[\]]+\s+(\w+)\s*\{\s*get;\s*set;\s*\}\s*(?:=\s*([^;]+);)?/g, (_, name, val) => {
    return val ? `${name} = ${val};` : `${name};`;
  });

  // 8. Handle foreach (var x in list) -> for (let x of list)
  js = js.replace(/foreach\s*\(\s*(?:var|[\w<>\[\]]+)\s+(\w+)\s+in\s+([^)]+)\)/g, 'for (let $1 of $2)');

  // 9. Handle List<T> creation
  js = js.replace(/List<[^>]+>\s+(\w+)\s*=\s*new\s*(?:List<[^>]+>)?\s*\(\s*\)\s*;/g, 'let $1 = [];');
  js = js.replace(/new\s+List<[^>]+>\s*\(\s*\)/g, '[]');

  // 10. Handle array initialization: int[] arr = new int[] { 1, 2 } or { 1, 2 }
  js = js.replace(/(\b[\w<>\[\]]+\s+\w+\s*=\s*)(?:new\s+[\w<>\[\]]+\s*)?\{([^}]+)\};/g, '$1[$2];');

  // 11. Extract and transform Program class
  js = js.replace(/\bclass\s+Program\s*\{([\s\S]*?)\}\s*$/g, (match, body) => {
    let transformed = body;

    // Convert Main: [public|private] [static] void|int Main(...) -> function __main__()
    transformed = transformed.replace(/\b(?:(?:public|private|protected|internal)\s+)?(?:static\s+)?(?:void|int)\s+Main\s*\([^)]*\)\s*\{/g, 'function __main__() {');

    // Handle method overloading: collect method names
    const methodCounts = {};
    const methodScanRegex = /\b(?:(?:public|private|protected|internal)\s+)?(?:static\s+)?(?:void|int|double|float|bool|string|long|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g;
    let m;
    while ((m = methodScanRegex.exec(transformed)) !== null) {
      const name = m[1];
      if (name !== 'if' && name !== 'while' && name !== 'for' && name !== 'switch' && name !== '__main__') {
        methodCounts[name] = (methodCounts[name] || 0) + 1;
      }
    }

    const overloadedIdx = {};

    // Convert other methods inside Program to functions: static int Add(int a, int b) { ... } -> function Add(a, b) { ... }
    transformed = transformed.replace(/\b(?:(?:public|private|protected|internal)\s+)?(?:static\s+)?(?:void|int|double|float|bool|string|long|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (m, name, args) => {
      if (name === 'if' || name === 'while' || name === 'for' || name === 'switch' || name === '__main__' || name === 'function') return m;
      
      const cleanArgs = args.split(',').map(arg => {
        const parts = arg.trim().split(/\s+/);
        return parts[parts.length - 1];
      }).filter(Boolean).join(', ');

      if (methodCounts[name] > 1) {
        overloadedIdx[name] = (overloadedIdx[name] || 0) + 1;
        const fnName = `${name}__overload${overloadedIdx[name]}`;
        return `/* overload */ function ${fnName}(${cleanArgs}) {`;
      }

      return `function ${name}(${cleanArgs}) {`;
    });

    // If there were overloaded functions, create the dispatcher
    for (const [name, count] of Object.entries(methodCounts)) {
      if (count > 1) {
        let dispatcher = `\nfunction ${name}(...__args) {\n`;
        for (let i = 1; i <= count; i++) {
          if (i === 1) {
            dispatcher += `    if (typeof __args[0] === 'string') return ${name}__overload1(...__args);\n`;
          } else if (i === 2) {
            dispatcher += `    if (typeof __args[0] === 'number') return ${name}__overload2(...__args);\n`;
          } else {
            dispatcher += `    return ${name}__overload${i}(...__args);\n`;
          }
        }
        dispatcher += `    return ${name}__overload1(...__args);\n}\n`;
        transformed += dispatcher;
      }
    }

    return transformed;
  });

  // 12. If Main is outside or still present as static void Main:
  js = js.replace(/\b(?:(?:public|private|protected|internal)\s+)?(?:static\s+)?(?:void|int)\s+Main\s*\([^)]*\)\s*\{/g, 'function __main__() {');

  // 13. Find custom classes
  const classNames = [];
  const classRegex = /\bclass\s+(\w+)/g;
  let cm;
  while ((cm = classRegex.exec(js)) !== null) {
    if (cm[1] !== 'Program') classNames.push(cm[1]);
  }

  // 14. Handle constructors in custom classes
  for (const cname of classNames) {
    const ctorRegex = new RegExp(`\\b(?:(?:public|private|protected|internal)\\s+)?${cname}\\s*\\(([^)]*)\\)\\s*\\{([\\s\\S]*?)\\}`, 'g');
    js = js.replace(ctorRegex, (_, args, ctorBody) => {
      const cleanArgs = args.split(',').map(arg => {
        const parts = arg.trim().split(/\s+/);
        return parts[parts.length - 1];
      }).filter(Boolean).join(', ');
      let cleanBody = ctorBody.replace(/(\b\w+)\s*=\s*([^;]+);/g, (m, f, v) => {
        if (f.startsWith('this.') || f === 'let' || f === 'var' || f === 'const') return m;
        return `this.${f} = ${v};`;
      });
      return `constructor(${cleanArgs}) {${cleanBody}}`;
    });
  }

  // 15. Handle methods in custom classes
  js = js.replace(/\b(?:(?:public|private|protected|internal)\s+)?(?:(static)\s+)?(?:virtual\s+|override\s+)?(?:void|int|double|float|bool|string|long|[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (match, isStatic, name, args) => {
    if (name === 'if' || name === 'while' || name === 'for' || name === 'switch' || name === '__main__' || name === 'constructor' || match.trim().startsWith('function')) {
      return match;
    }
    const cleanArgs = args.split(',').map(arg => {
      const parts = arg.trim().split(/\s+/);
      return parts[parts.length - 1];
    }).filter(Boolean).join(', ');
    return `${isStatic ? 'static ' : ''}${name}(${cleanArgs}) {`;
  });

  // 16. In class bodies, clean field declarations: public string Name; -> Name;
  js = js.replace(/\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:[\w<>\[\]]+)\s+(\w+)\s*(=|;)/g, '$1 $2');

  // 17. In methods/functions, clean local variable declarations: int x = 5;
  js = js.replace(/\b(?:int|double|float|bool|string|var|long|char|decimal|[A-Z]\w*(?:<[^>]+>)?)(?:\[\])*\s+(\w+)\s*(=|;)/g, (match, vname, rest) => {
    if (vname === 'return' || vname === 'if' || vname === 'while' || vname === 'for' || vname === 'class') return match;
    return `let ${vname} ${rest}`;
  });

  // 18. Clean leftover access modifiers
  js = js.replace(/\b(?:public|private|protected|internal)\s+/g, '');

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
    const jsCode = transpileCSharp(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });

    const wrappedCode = `
      ${jsCode}

      // Auto-invoke entrypoint
      if (typeof __main__ === 'function') {
        __main__();
      } else if (typeof Program !== 'undefined' && typeof Program.Main === 'function') {
        Program.Main();
      } else if (typeof Main === 'function') {
        Main();
      }
    `;

    const userScope = {
      __print__: print,
      __println__: println,
      __prompt__: fakePrompt,
      Math: Math,
      String: String,
      Array: Array,
      Boolean: Boolean,
      Number: Number
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
            const strippedExpr = transpileCSharp(test.expression);
            try {
              const testFn = new Function('__scope__', `with (__scope__) { ${jsCode}\n;return (${strippedExpr}); }`);
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
