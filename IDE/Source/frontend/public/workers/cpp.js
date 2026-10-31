/* DevForge C++ Worker: transpiles educational C++ code to JavaScript and runs in Web Worker */
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

function transpileCpp(cppCode) {
  let js = cppCode;

  // 1. Remove #include <...> and #include "..."
  js = js.replace(/#include\s+[<"][^>"]+[>"]/g, '');

  // 2. Remove using namespace std;
  js = js.replace(/using\s+namespace\s+std\s*;/g, '');

  // 3. Handle std::endl and '\n' in cout
  js = js.replace(/\b(?:std::)?endl\b/g, '"\\n"');

  // 4. Handle template <typename T> or template <class T>
  js = js.replace(/template\s*<[^>]+>/g, '');

  // 5. Handle reference parameters: void doubleVal(int& n)
  const refParamFuncs = [];
  const refFuncRegex = /\b(?:void|int|double|float|[\w:]+)\s+(\w+)\s*\(([^)]*&[^)]*)\)\s*\{/g;
  let rfm;
  while ((rfm = refFuncRegex.exec(js)) !== null) {
    const fnName = rfm[1];
    const params = rfm[2].split(',').map(p => p.trim());
    const refIndices = [];
    params.forEach((p, idx) => {
      if (p.includes('&')) {
        const pName = p.split(/\s+/).pop().replace('&', '');
        refIndices.push({ idx, name: pName });
      }
    });
    refParamFuncs.push({ name: fnName, refIndices });
  }

  // 6. Handle custom structs and classes with balanced brace parser
  const customTypes = new Set();

  function processClass(kind, typeName, body) {
    customTypes.add(typeName);
    let classBody = body;

    // Remove access specifiers: public:, private:, protected:
    classBody = classBody.replace(/\b(public|private|protected)\s*:/g, '');

    // Extract fields
    const fields = [];
    const lines = classBody.split(';');
    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line || line.includes('(') || line.includes('{') || line.includes('}') || line.includes('return') || line.includes('class') || line.includes('struct')) continue;
      
      const vecMatch = line.match(/(?:std::)?vector<[^>]+>\s+(\w+)/);
      if (vecMatch) {
        fields.push({ name: vecMatch[1], isVector: true });
        continue;
      }

      const declMatch = line.match(/^(?:const\s+)?(?:std::)?(?:string|int|double|float|bool|char|[\w:]+)\s+([\w\s,=]+)$/);
      if (declMatch) {
        const varList = declMatch[1].split(',');
        for (const v of varList) {
          const varNameMatch = v.trim().match(/^(\w+)/);
          if (varNameMatch) {
            fields.push({ name: varNameMatch[1], isVector: false });
          }
        }
      }
    }

    // Convert operator overloading header: Point operator+(...) const { -> add(...) {
    classBody = classBody.replace(/[\w:]+\s+operator\s*([+\-*/%])\s*\(([^)]*)\)(?:\s*const)?\s*\{/g, (m, op, opArgs) => {
      const cleanArgs = opArgs.split(',').map(a => a.trim().split(/\s+/).pop().replace(/[&*]/g, '')).filter(Boolean).join(', ');
      return `add(${cleanArgs}) {`;
    });

    // Convert explicit constructor header: ClassName(args) { -> constructor(args) {
    let hasExplicitCtor = false;
    const ctorHeaderRegex = new RegExp(`\\b${typeName}\\s*\\(([^)]*)\\)\\s*\\{`, 'g');
    classBody = classBody.replace(ctorHeaderRegex, (m, ctorArgs) => {
      hasExplicitCtor = true;
      const cleanArgs = ctorArgs.split(',').map(a => a.trim().split(/\s+/).pop().replace(/[&*]/g, '')).filter(Boolean).join(', ');
      return `constructor(${cleanArgs}) {`;
    });

    // If no explicit constructor, generate one
    let generatedCtor = '';
    if (!hasExplicitCtor) {
      const assignments = fields.map((f, i) => {
        const defaultVal = f.isVector ? '[]' : '0';
        return `this.${f.name} = (__args[${i}] !== undefined ? __args[${i}] : (this.${f.name} !== undefined ? this.${f.name} : ${defaultVal}));`;
      }).join(' ');
      generatedCtor = `\n  constructor(...__args) { ${assignments} }\n`;
    }

    // Convert member method headers: Type methodName(args) { -> methodName(cleanArgs) {
    classBody = classBody.replace(/\b(?:void|int|double|float|bool|char|string|[\w:]+)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (m, mName, mArgs) => {
      if (mName === 'if' || mName === 'while' || mName === 'for' || mName === 'switch' || mName === 'constructor' || mName === 'add') return m;
      const cleanArgs = mArgs.split(',').map(a => a.trim().split(/\s+/).pop().replace(/[&*]/g, '')).filter(Boolean).join(', ');
      return `${mName}(${cleanArgs}) {`;
    });

    // Remove field declaration lines BEFORE this. prefixing
    for (const f of fields) {
      const cleanFieldDeclRegex = new RegExp(`^[^({;\\n]*?\\b(?:vector<[^>]+>|string|int|double|float|bool|char|long|size_t|[A-Z]\\w*)\\s+[^({;\\n]*?\\b${f.name}\\b[^({;\\n]*?;\\s*$`, 'gm');
      classBody = classBody.replace(cleanFieldDeclRegex, '');
    }

    // Prefix fields with this. inside the class body
    for (const f of fields) {
      const fieldRegex = new RegExp(`(?<![\\w.])${f.name}\\b`, 'g');
      classBody = classBody.replace(fieldRegex, `this.${f.name}`);
    }

    // Vector operations inside class
    classBody = classBody.replace(/\.push_back\s*\(/g, '.push(');

    return `class ${typeName} {\n${generatedCtor}${classBody}\n}`;
  }

  // Parse classes with balanced braces
  let classTransformed = '';
  let lastIdx = 0;
  const classDeclRegex = /\b(class|struct)\s+([A-Za-z]\w*)\s*\{/g;
  let cm;
  while ((cm = classDeclRegex.exec(js)) !== null) {
    classTransformed += js.slice(lastIdx, cm.index);
    const kind = cm[1];
    const typeName = cm[2];
    let braceDepth = 1;
    let bStart = cm.index + cm[0].length;
    let bEnd = bStart;
    while (bEnd < js.length && braceDepth > 0) {
      if (js[bEnd] === '{') braceDepth++;
      else if (js[bEnd] === '}') braceDepth--;
      bEnd++;
    }
    const rawBody = js.slice(bStart, bEnd - 1);
    let afterIdx = bEnd;
    while (afterIdx < js.length && /\s/.test(js[afterIdx])) afterIdx++;
    if (afterIdx < js.length && js[afterIdx] === ';') afterIdx++;
    lastIdx = afterIdx;
    classDeclRegex.lastIndex = afterIdx;
    classTransformed += processClass(kind, typeName, rawBody);
  }
  classTransformed += js.slice(lastIdx);
  js = classTransformed;

  // 7. Handle cout chaining: cout << a << b << ...;
  js = js.replace(/\b(?:std::)?cout\s*<<\s*([^;]+);/g, (_, chain) => {
    const parts = [];
    let cur = '', inQuote = false, quoteChar = '';
    for (let i = 0; i < chain.length; i++) {
      const c = chain[i];
      if ((c === '"' || c === "'") && (i === 0 || chain[i - 1] !== '\\')) {
        if (!inQuote) { inQuote = true; quoteChar = c; }
        else if (quoteChar === c) { inQuote = false; }
      }
      if (!inQuote && c === '<' && chain[i + 1] === '<') {
        parts.push(cur.trim());
        cur = '';
        i++; // skip next <
        continue;
      }
      cur += c;
    }
    if (cur.trim()) parts.push(cur.trim());
    return parts.map(p => `__print__(${p});`).join(' ');
  });

  // 8. Handle cin chaining: cin >> a >> b;
  js = js.replace(/\b(?:std::)?cin\s*>>\s*([^;]+);/g, (_, chain) => {
    const vars = chain.split('>>').map(s => s.trim()).filter(Boolean);
    return vars.map(v => `${v} = __parse_val__(__prompt__());`).join(' ');
  });

  // 9. Handle instantiations and assignments of customTypes:
  for (const t of customTypes) {
    const initListRegex = new RegExp(`(?<!class\\s+|struct\\s+)\\b${t}\\s*\\{([^}]*)\\}`, 'g');
    js = js.replace(initListRegex, `new ${t}($1)`);

    const varAssignRegex = new RegExp(`\\b${t}\\s+(\\w+)\\s*=`, 'g');
    js = js.replace(varAssignRegex, `let $1 =`);

    const varInitListRegex = new RegExp(`\\b${t}\\s+(\\w+)\\s*\\{([^}]*)\\}\\s*;`, 'g');
    js = js.replace(varInitListRegex, `let $1 = new ${t}($2);`);

    const varCallRegex = new RegExp(`\\b${t}\\s+(\\w+)\\s*\\(([^)]*)\\)\\s*;`, 'g');
    js = js.replace(varCallRegex, `let $1 = new ${t}($2);`);

    const varDefRegex = new RegExp(`\\b${t}\\s+(\\w+)\\s*;`, 'g');
    js = js.replace(varDefRegex, `let $1 = new ${t}();`);
  }

  // Operator + on customTypes
  js = js.replace(/\b(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)\s*;/g, (m, target, a, b) => {
    return `${target} = (${a} && typeof ${a}.add === 'function' ? ${a}.add(${b}) : (${a} + ${b}));`;
  });

  // 10. Handle reference function calls: doubleVal(x); -> x = doubleVal(x);
  for (const rf of refParamFuncs) {
    const callRegex = new RegExp(`\\b${rf.name}\\s*\\(([^)]+)\\)\\s*;`, 'g');
    js = js.replace(callRegex, (m, argsStr) => {
      const args = argsStr.split(',').map(a => a.trim());
      const assignments = [];
      for (const ref of rf.refIndices) {
        if (args[ref.idx]) {
          assignments.push(`${args[ref.idx]} = ${rf.name}(${argsStr});`);
        }
      }
      return assignments.join(' ') || m;
    });
  }

  // 11. Handle std::vector<T> v = {1, 2, 3}; or vector<int> v;
  js = js.replace(/\b(?:std::)?vector\s*<[^>]+>\s+(\w+)\s*=\s*\{([^}]+)\};/g, 'let $1 = [$2];');
  js = js.replace(/\b(?:std::)?vector\s*<[^>]+>\s+(\w+)\s*;/g, 'let $1 = [];');
  js = js.replace(/\.push_back\s*\(/g, '.push(');
  js = js.replace(/\.size\s*\(\s*\)/g, '.length');

  // 12. Handle std::string: string s = "...";
  js = js.replace(/\b(?:std::)?string\s+(\w+)/g, 'let $1');

  // 13. Handle primitive types: int, double, float, bool, char, long, size_t
  js = js.replace(/\b(?:int|double|float|bool|char|long|size_t)\s+(\w+)\s*(=|;)/g, 'let $1 $2');
  js = js.replace(/\bauto\s+(\w+)\s*=/g, 'let $1 =');

  // 14. Range-based for: for (auto x : vec) or for (int x : arr)
  js = js.replace(/for\s*\(\s*(?:const\s+)?(?:auto|int|double|string|[\w:]+)(?:&)?\s+(\w+)\s*:\s*([^)]+)\)/g, 'for (let $1 of $2)');

  // 15. Handle top-level functions: int multiply(int a, int b) { ... }
  js = js.replace(/\b(?:void|int|double|float|bool|char|string|auto|size_t|long|[A-Z]\w*)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (match, name, args) => {
    if (name === 'main') return 'function main() {';
    if (name === 'if' || name === 'while' || name === 'for' || name === 'switch' || name === 'class') return match;
    const cleanArgs = args.split(',').map(arg => {
      const parts = arg.trim().split(/\s+/);
      return parts[parts.length - 1].replace(/[*&]/g, '');
    }).filter(Boolean).join(', ');
    return `function ${name}(${cleanArgs}) {`;
  });

  // Return mutated ref parameter if function is void and has ref
  for (const rf of refParamFuncs) {
    if (rf.refIndices.length > 0) {
      const pName = rf.refIndices[0].name;
      const fnDefRegex = new RegExp(`function\\s+${rf.name}\\s*\\([^)]*\\)\\s*\\{([\\s\\S]*?)\\}`, 'g');
      js = js.replace(fnDefRegex, (m, body) => {
        if (!body.includes('return ')) {
          return `function ${rf.name}(${pName}) {\n${body}\nreturn ${pName};\n}`;
        }
        return m;
      });
    }
  }

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

    const parseVal = (str) => {
      if (!str) return 0;
      const num = Number(str);
      return isNaN(num) ? str : num;
    };

    const print = (...args) => {
      const str = args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ');
      append(str);
    };

    const println = (...args) => {
      const str = args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ');
      append(str + '\n');
    };

    self.postMessage({ type: 'phase', phase: 'compile' });
    const jsTranspiled = transpileCpp(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });

    const wrappedCode = `
      ${jsTranspiled}

      if (typeof main === 'function') {
        main();
      }
    `;

    const userScope = {
      __println__: println,
      __print__: print,
      __prompt__: fakePrompt,
      __parse_val__: parseVal,
      Math: Math,
      String: String,
      Array: Array,
      Boolean: Boolean,
      Number: Number,
      parseInt: parseInt,
      parseFloat: parseFloat,
      JSON: JSON
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
            const strippedExpr = transpileCpp(test.expression);
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
