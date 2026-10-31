/* DevForge TypeScript Worker: transforms TypeScript to JavaScript and executes inside disposable Worker */
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

/**
 * Transpiles TypeScript into runnable JavaScript for educational code.
 */
function transpileTypeScript(tsCode) {
  let js = tsCode;

  // 1. Remove interfaces: interface Foo<T> extends Bar { ... }
  js = js.replace(/interface\s+\w+(?:<[^>]+>)?(?:\s+extends\s+[^{]+)?\s*\{[\s\S]*?\}/g, '');

  // 2. Remove type aliases: type Foo = { ... }; or type Foo = string | number;
  js = js.replace(/type\s+\w+(?:<[^>]+>)?\s*=\s*\{[\s\S]*?\};?/g, '');
  js = js.replace(/type\s+\w+(?:<[^>]+>)?\s*=[^;]+;/g, '');

  // 3. Remove generic type arguments on classes: class Foo<T extends ...> {
  js = js.replace(/(\bclass\s+\w+)<[\s\S]*?>(?=\s*\{)/g, '$1');

  // 4. Remove generic type arguments on function declarations: function foo<T>(...)
  js = js.replace(/(\bfunction(?:\s+\w+)?)<[^>]+>/g, '$1');

  // 5. Remove generic type arguments in new expressions: new Foo<Type>(...)
  js = js.replace(/(\bnew\s+\w+)<[^>]+>(?=\s*\()/g, '$1');

  // 6. Remove type assertions: as Type
  js = js.replace(/\s+as\s+[A-Za-z0-9_<>\[\]|&\s]+/g, '');

  // 7. Transform enums: enum OrderStatus { Created, Paid, Shipped }
  js = js.replace(/enum\s+(\w+)\s*\{([^}]+)\}/g, (_, name, body) => {
    const items = body.split(',').map(s => s.trim()).filter(Boolean);
    let lastVal = -1;
    const mappings = [];
    for (const item of items) {
      if (item.includes('=')) {
        const [k, v] = item.split('=').map(s => s.trim());
        const num = Number(v);
        if (!isNaN(num)) {
          lastVal = num;
          mappings.push(`  "${k}": ${num}, ${num}: "${k}"`);
        } else {
          mappings.push(`  "${k}": ${v}`);
        }
      } else {
        lastVal++;
        mappings.push(`  "${item}": ${lastVal}, ${lastVal}: "${item}"`);
      }
    }
    return `const ${name} = {\n${mappings.join(',\n')}\n};`;
  });

  // 8. Remove access modifiers and readonly
  js = js.replace(/\b(public|private|protected|readonly)\s+/g, '');

  // 9. Remove implements clause
  js = js.replace(/(\bclass\s+\w+(?:\s+extends\s+\w+)?)\s+implements\s+[^{\s]+(?:\s*,\s*[^{\s]+)*/g, '$1');

  // 10. Remove return type on functions/methods: ): ReturnType { or ): ReturnType =>
  js = js.replace(/\)\s*:\s*[A-Za-z0-9_<>\[\]|&\s]+\s*(?=[{=])/g, ') ');

  // 11. Remove variable type annotations: let x: number = 5; const y: string[] = [];
  const typeExpr = '(?:[A-Za-z_]\\w*(?:<[^>]+>)?(?:\\[\\])?(?:\\s*[|&]\\s*[A-Za-z_]\\w*(?:<[^>]+>)?(?:\\[\\])?)*)';
  const varRegex = new RegExp('(\\b(?:let|const|var)\\s+\\w+)\\s*:\\s*' + typeExpr + '(?=\\s*(=|;))', 'g');
  js = js.replace(varRegex, '$1');

  // 12. Remove function parameter types: ONLY inside ( ... )
  const paramRegex = new RegExp('(\\b\\w+)\\??\\s*:\\s*' + typeExpr + '(?=\\s*(?:[,)=]|$))', 'g');
  js = js.replace(/\(([^)]*)\)/g, (_, inside) => {
    return `(${inside.replace(paramRegex, '$1')})`;
  });

  // 13. Remove class property type annotations: items: T[] = [];
  const propRegex = new RegExp('^(\\s*\\w+)\\s*:\\s*' + typeExpr + '(?=\\s*[=;])', 'gm');
  js = js.replace(propRegex, '$1');

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

    // Custom console capturing
    const customConsole = {
      log: (...args) => {
        append(args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ') + '\n');
      },
      info: (...args) => customConsole.log(...args),
      warn: (...args) => {
        append(args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ') + '\n', true);
      },
      error: (...args) => {
        append(args.map(a => (typeof a === 'object' && a !== null ? JSON.stringify(a) : String(a))).join(' ') + '\n', true);
      }
    };

    // Prepare scope
    const fileModules = {};
    if (data.files && Array.isArray(data.files)) {
      for (const file of data.files) {
        if ((file.name.endsWith('.ts') || file.name.endsWith('.js')) && file.content && file.name !== (data.filename || 'index.ts')) {
          try {
            const trans = transpileTypeScript(file.content);
            const modFn = new Function('console', 'prompt', 'exports', 'module', trans);
            const modObj = { exports: {} };
            modFn(customConsole, fakePrompt, modObj.exports, modObj);
            fileModules[file.name] = modObj.exports;
          } catch (e) {
            append(`Ошибка в файле ${file.name}: ${e}\n`, true);
          }
        }
      }
    }

    const customRequire = (name) => {
      if (fileModules[name]) return fileModules[name];
      if (fileModules[name + '.ts']) return fileModules[name + '.ts'];
      if (fileModules[name + '.js']) return fileModules[name + '.js'];
      if (fileModules['./' + name]) return fileModules['./' + name];
      if (fileModules['./' + name + '.ts']) return fileModules['./' + name + '.ts'];
      if (fileModules['./' + name + '.js']) return fileModules['./' + name + '.js'];
      throw new Error(`Модуль '${name}' не найден среди файлов проекта`);
    };

    self.postMessage({ type: 'phase', phase: 'compile' });
    const jsTranspiled = transpileTypeScript(data.code || '');

    self.postMessage({ type: 'phase', phase: 'run' });
    const execFn = new Function('console', 'prompt', 'require', jsTranspiled);
    execFn(customConsole, fakePrompt, customRequire);

    // If tests are present
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
            new Function('console', 'prompt', 'require', jsTranspiled)(customConsole, testPrompt, customRequire);
            actualVal = output.trim();
          } else if (test.expression) {
            const strippedExpr = transpileTypeScript(test.expression);
            const testFn = new Function('console', 'prompt', 'require', `${jsTranspiled}\n;return (${strippedExpr});`);
            actualVal = testFn(customConsole, fakePrompt, customRequire);
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
