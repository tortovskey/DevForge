// Match function bodies by brace depth, independently of line breaks.
function replaceRustFunctions(source, replace) {
  const signature = /\bfn\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*[A-Za-z0-9_<>&\[\]\s]+)?\s*\{/g;
  let output = '', start = 0, match;
  while ((match = signature.exec(source))) {
    let index = signature.lastIndex, depth = 1, quote = '', escaped = false;
    for (; index < source.length && depth; index++) {
      const char = source[index];
      if (quote) { if (escaped) escaped=false; else if (char==='\\') escaped=true; else if (char===quote) quote=''; continue; }
      if (char==='"'||char==="'"||char==='`') { quote=char; continue; }
      if (char==='/'&&source[index+1]==='/') { const end=source.indexOf('\n',index); index=end<0?source.length:end; continue; }
      if (char==='/'&&source[index+1]==='*') { const end=source.indexOf('*/',index+2); index=end<0?source.length:end+1; continue; }
      if (char==='{') depth++; else if (char==='}') depth--;
    }
    if(depth) throw new SyntaxError('Незакрытое тело функции Rust');
    output += source.slice(start,match.index)+replace(source.slice(match.index,index),match[1],match[2],source.slice(signature.lastIndex,index-1));
    start=index; signature.lastIndex=index;
  }
  return output+source.slice(start);
}

/* DevForge Rust Worker: transpiles educational Rust code to JavaScript and runs in Web Worker */
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

function transpileRust(rsCode) {
  let js = rsCode;

  // 1. Array polyfill: scores.len() -> scores.length
  js = js.replace(/\.len\s*\(\s*\)/g, '.length');

  // 2. Enum double colons: Direction::North -> Direction.North
  js = js.replace(/([A-Z]\w*)::([A-Za-z0-9_]+)/g, '$1.$2');

  // 3. String::from("...") -> "..."
  js = js.replace(/String\.from\s*\(\s*"([^"]*)"\s*\)/g, '"$1"');
  js = js.replace(/\.to_string\s*\(\s*\)/g, '');

  // 4. Handle vec![1, 2, 3] -> [1, 2, 3]
  js = js.replace(/vec!\s*\[([^\]]*)\]/g, '[$1]');

  // 5. Tuple declarations: let point = (10, 20); -> let point = [10, 20];
  js = js.replace(/(=\s*)\(([^)]+)\);/g, '$1[$2];');
  // Tuple access: point.0 -> point[0], point.1 -> point[1]
  js = js.replace(/(\w+)\.([0-9]+)\b/g, '$1[$2]');

  // 6. Handle mutable references:
  const mutRefMap = {};
  js = js.replace(/let\s+(?:mut\s+)?(\w+)\s*=\s*&mut\s+(\w+);/g, (_, refName, origName) => {
    mutRefMap[refName] = origName;
    return `let ${refName} = ${origName};`;
  });
  for (const [refName, origName] of Object.entries(mutRefMap)) {
    const starRef = new RegExp(`\\*${refName}\\b`, 'g');
    js = js.replace(starRef, origName);
  }
  js = js.replace(/=\s*&([a-zA-Z0-9_]+)/g, '= $1');

  // 7. Enums: enum Direction { North, South, East, West }
  js = js.replace(/enum\s+(\w+)\s*\{([^}]+)\}/g, (_, ename, variants) => {
    const vars = variants.split(',').map(v => v.trim()).filter(Boolean);
    const obj = vars.map(v => `${v}: "${v}"`).join(', ');
    return `const ${ename} = { ${obj} };`;
  });

  // 8. Structs: struct Player { name: String, score: i32 }
  const structNames = [];
  js = js.replace(/struct\s+(\w+)\s*\{([^}]+)\}/g, (_, sname, fieldsStr) => {
    structNames.push(sname);
    const fields = fieldsStr.split(',').map(f => f.trim().split(':')[0].trim()).filter(Boolean);
    const ctorParams = fields.join(', ');
    const ctorBody = fields.map(f => `this.${f} = ${f};`).join('\n    ');
    return `class ${sname} {\n  constructor(${ctorParams}) {\n    ${ctorBody}\n  }\n}`;
  });

  // 9. Struct impl blocks
  js = js.replace(/impl\s+(\w+)\s*\{([\s\S]*?)\n\}/g, (_, sname, body) => {
    let methods = body;
    methods = methods.replace(/fn\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*[A-Za-z0-9_<>&\[\]\s]+)?\s*\{([\s\S]*?)\n\s*\}/g, (m, mname, args, mbody) => {
      const cleanArgs = args.split(',').map(a => a.trim()).filter(a => a !== '&self' && a !== '&mut self' && a !== 'self').map(a => a.split(':')[0].trim()).join(', ');
      let transformedBody = mbody.replace(/\bself\./g, 'this.').trim();
      const lines = transformedBody.split('\n');
      const lastLine = lines[lines.length - 1].trim();
      if (lastLine && !lastLine.endsWith(';') && !lastLine.endsWith('}') && !lastLine.startsWith('return ')) {
        lines[lines.length - 1] = `return ${lastLine};`;
        transformedBody = lines.join('\n');
      }
      return `${sname}.prototype.${mname} = function(${cleanArgs}) {\n${transformedBody}\n};`;
    });
    return methods;
  });

  // 10. Struct instantiation: Player { name: ..., score: ... } -> new Player(...)
  for (const sname of structNames) {
    const instRegex = new RegExp(`(?<!class\\s+)\\b${sname}\\s*\\{([^}]+)\\}`, 'g');
    js = js.replace(instRegex, (_, props) => {
      const vals = props.split(',').map(p => {
        const parts = p.split(':');
        return parts.length > 1 ? parts[1].trim() : parts[0].trim();
      }).filter(Boolean).join(', ');
      return `new ${sname}(${vals})`;
    });
  }

  // 11. Control flow: if cond { -> if (cond) {, while cond { -> while (cond) {
  js = js.replace(/\bif\s+([^({]+)\{/g, 'if ($1) {');
  js = js.replace(/\bwhile\s+([^({]+)\{/g, 'while ($1) {');

  // 12. For loops: for i in 0..10 or for x in arr
  js = js.replace(/for\s+(\w+)\s+in\s+(\d+)\.\.(\d+)\s*\{/g, 'for (let $1 = $2; $1 < $3; $1++) {');
  js = js.replace(/for\s+(\w+)\s+in\s+([^\{]+)\{/g, (_, item, coll) => {
    const cleanColl = coll.trim().replace(/\.iter\(\)/g, '').replace(/&/g, '');
    return `for (let ${item} of ${cleanColl}) {`;
  });

  // 13. Match expressions -> switch
  js = js.replace(/match\s+([^\{]+)\s*\{([\s\S]*?)\}/g, (_, expr, arms) => {
    const lines = arms.split(',').map(s => s.trim()).filter(Boolean);
    let switchCode = `switch (${expr.trim()}) {\n`;
    for (const arm of lines) {
      if (!arm.includes('=>')) continue;
      const [pat, body] = arm.split('=>').map(s => s.trim());
      if (pat === '_') {
        switchCode += `  default: ${body}; break;\n`;
      } else {
        switchCode += `  case ${pat}: ${body}; break;\n`;
      }
    }
    switchCode += '}';
    return switchCode;
  });

  // 14. Variable declarations: let [mut] x [: type] = val;
  js = js.replace(/let\s+(?:mut\s+)?(\w+)(?:\s*:\s*[A-Za-z0-9_<>&\[\]\s]+)?\s*=\s*/g, 'let $1 = ');
  js = js.replace(/let\s+(?:mut\s+)?(\w+)(?:\s*:\s*[A-Za-z0-9_<>&\[\]\s]+)?\s*;/g, 'let $1;');

  // 15. println! and print!
  js = js.replace(/println!\s*\(\s*"([^"]*)"(?:\s*,\s*([\s\S]*?))?\s*\);/g, (_, format, argsStr) => {
    if (!argsStr) {
      return `__println__(${JSON.stringify(format)});`;
    }
    const args = argsStr.split(',').map(s => s.trim()).filter(Boolean);
    let argIdx = 0;
    const formatted = format.replace(/\{(?::\?)?\}/g, () => {
      const a = args[argIdx++];
      return a ? `\${typeof ${a} === 'object' && ${a} !== null ? JSON.stringify(${a}) : ${a}}` : '';
    });
    return `__println__(\`${formatted}\`);`;
  });

  js = js.replace(/print!\s*\(\s*"([^"]*)"(?:\s*,\s*([\s\S]*?))?\s*\);/g, (_, format, argsStr) => {
    if (!argsStr) {
      return `__print__(${JSON.stringify(format)});`;
    }
    const args = argsStr.split(',').map(s => s.trim()).filter(Boolean);
    let argIdx = 0;
    const formatted = format.replace(/\{(?::\?)?\}/g, () => {
      const a = args[argIdx++];
      return a ? `\${typeof ${a} === 'object' && ${a} !== null ? JSON.stringify(${a}) : ${a}}` : '';
    });
    return `__print__(\`${formatted}\`);`;
  });

  // 16. Functions: fn name(...) [-> ret] { ... }
  js = replaceRustFunctions(js, (m, name, args, body) => {
    const cleanArgs = args.split(',').map(a => a.trim().split(':')[0].trim()).filter(Boolean).join(', ');
    let transformedBody = body.trim();
    const lines = transformedBody.split('\n');
    const lastLine = lines[lines.length - 1].trim();
    if (lastLine && !lastLine.endsWith(';') && !lastLine.endsWith('}') && !lastLine.startsWith('return ') && name !== 'main') {
      lines[lines.length - 1] = `return ${lastLine};`;
      transformedBody = lines.join('\n');
    }
    return `function ${name}(${cleanArgs}) {\n${transformedBody}\n}`;
  });

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
    const jsCode = transpileRust(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });

    const wrappedCode = `
      ${jsCode}

      if (typeof main === 'function') {
        main();
      }
    `;

    const userScope = {
      __print__: print,
      __println__: println,
      __prompt__: fakePrompt,
      Math: Math,
      String: String,
      Array: Array
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
            const strippedExpr = transpileRust(test.expression);
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
