/* DevForge JavaScript Worker: runs safely inside this disposable Web Worker */
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
        if (file.name.endsWith('.js') && file.content && file.name !== (data.filename || 'index.js')) {
          try {
            const modFn = new Function('console', 'prompt', 'exports', 'module', file.content);
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
      if (fileModules[name + '.js']) return fileModules[name + '.js'];
      if (fileModules['./' + name]) return fileModules['./' + name];
      if (fileModules['./' + name + '.js']) return fileModules['./' + name + '.js'];
      throw new Error(`Модуль '${name}' не найден среди файлов проекта`);
    };

    self.postMessage({ type: 'phase', phase: 'run' });

    // Execute user code
    const codeToRun = data.code || '';
    const execFn = new Function('console', 'prompt', 'require', codeToRun);
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
            new Function('console', 'prompt', 'require', codeToRun)(customConsole, testPrompt, customRequire);
            actualVal = output.trim();
          } else if (test.expression) {
            const testFn = new Function('console', 'prompt', 'require', `${codeToRun}\n;return (${test.expression});`);
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
