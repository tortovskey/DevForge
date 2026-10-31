/* DevForge Objective-C Worker: transpiles educational Objective-C code to JavaScript and runs in Web Worker */
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

// Polyfill for NSArray .count() -> length
if (!Array.prototype.count) {
  Array.prototype.count = function() { return this.length; };
}

function transpileObjC(mCode) {
  let js = mCode;

  // 1. Remove #import
  js = js.replace(/#import\s+[<"][^>"]+[>"]/g, '');

  // 2. Remove @autoreleasepool { ... }
  js = js.replace(/@autoreleasepool\s*\{/g, '{');

  // 3. Fast Enumeration: for (NSString *name in names) -> for (let name of names)
  js = js.replace(/for\s*\(\s*(?:[\w\s\*]+?)\s*\b(\w+)\s+in\s+([^)]+)\)/g, 'for (let $1 of $2)');

  // 4. Handle @"string" -> "string"
  js = js.replace(/@"([^"]*)"/g, '"$1"');

  // 5. Handle @(123) or @YES -> true, @NO -> false
  js = js.replace(/@YES\b/g, 'true');
  js = js.replace(/@NO\b/g, 'false');
  js = js.replace(/YES\b/g, 'true');
  js = js.replace(/NO\b/g, 'false');
  js = js.replace(/@\((\w+)\)/g, '$1');

  // 6. Handle @[a, b, c] -> [a, b, c]
  js = js.replace(/@\[([^\]]*)\]/g, '[$1]');

  // 7. Handle @{ k: v } -> { k: v }
  js = js.replace(/@\{([^}]*)\}/g, '{$1}');

  // 8. Handle @interface ClassName : SuperClassName ... @end -> strip
  js = js.replace(/@interface\s+(\w+)(?:\s*:\s*(\w+))?[\s\S]*?@end/g, '');

  // 9. Handle @property / @synthesize
  js = js.replace(/@property\s*\([^)]*\)\s*[\w\s\*]+\s+(\w+);/g, '');
  js = js.replace(/@synthesize\s+[\w\s,]+;/g, '');

  // 10. Handle [[Class alloc] initWithParam:arg] or [[Class alloc] init]
  js = js.replace(/\[\[(\w+)\s+alloc\]\s+initWith\w*:\s*([^\]]+)\]/g, 'new $1($2)');
  js = js.replace(/\[\[(\w+)\s+alloc\]\s+init\]/g, 'new $1()');
  js = js.replace(/\[([A-Z]\w*)\s+new\]/g, 'new $1()');

  // Multi-nested bracket calls: do multiple passes
  for (let pass = 0; pass < 3; pass++) {
    // [obj methodName:arg] -> obj.methodName(arg)
    js = js.replace(/\[(\w+(?:\.\w+\([^)]*\))*)\s+(\w+)\s*:\s*([^\]]+)\]/g, '$1.$2($3)');
    // [obj count] -> obj.length
    js = js.replace(/\[(\w+(?:\.\w+\([^)]*\))*)\s+count\]/g, '$1.length');
    // [obj methodName] -> obj.methodName()
    js = js.replace(/\[(\w+(?:\.\w+\([^)]*\))*)\s+(\w+)\]/g, '$1.$2()');
  }

  // Handle .count() or .count -> .length
  js = js.replace(/\.count(?:\(\))?\b/g, '.length');

  // 11. Handle @implementation ClassName ... @end
  js = js.replace(/@implementation\s+(\w+)[\s\S]*?@end/g, (match, className) => {
    let body = match.replace(/@implementation\s+\w+/, '').replace(/@end/, '');
    // Convert - (Type)methodName:(Type)arg1 ... { OR + (Type)classMethod {
    body = body.replace(/([-+])\s*\([^)]*\)\s*(\w+)(?:\s*:\s*\([^)]*\)\s*(\w+))?\s*\{/g, (_, sign, name, arg) => {
      if (name.startsWith('init')) {
        return `constructor(${arg || ''}) {`;
      }
      return `${sign === '+' ? 'static ' : ''}${name}(${arg || ''}) {`;
    });
    // clean self = [super init]; if (self) ... return self;
    body = body.replace(/self\s*=\s*\[super\s+init\];/g, 'super();');
    body = body.replace(/return\s+self;/g, 'return this;');
    body = body.replace(/\bself\b/g, 'this');
    return `class ${className} {\n${body}\n}`;
  });

  // 12. Remove type casts like (unsigned long), (int)
  js = js.replace(/\(\s*(?:unsigned\s+)?(?:long|int|double|float|id|BOOL|NSInteger|NSUInteger)\s*\)/g, '');

  // 13. Handle NSLog(@"Format", arg1, arg2); or NSLog("Format", arg1, arg2);
  js = js.replace(/NSLog\s*\(\s*@?"([^"]*)"(?:\s*,\s*([\s\S]*?))?\s*\);/g, (_, format, argsStr) => {
    if (!argsStr) {
      return `__println__(${JSON.stringify(format)});`;
    }
    const args = argsStr.split(',').map(s => s.trim()).filter(Boolean);
    let argIdx = 0;
    const formatted = format.replace(/%(?:lu|ld|lld|zu|lf|[@dfsi])/g, () => {
      const a = args[argIdx++];
      return a ? `\${${a}}` : '';
    });
    return `__println__(\`${formatted}\`);`;
  });

  // 14. Handle C functions: int square(int n) { ... } -> function square(n) { ... }
  js = js.replace(/\b(?:int|double|float|void|BOOL|NSInteger|NSString\s*\*)\s+(\w+)\s*\(([^)]*)\)\s*\{/g, (match, name, args) => {
    if (name === 'main' || name === 'if' || name === 'while' || name === 'for' || name === 'switch') return match;
    const cleanArgs = args.split(',').map(arg => {
      const parts = arg.trim().split(/\s+/);
      return parts[parts.length - 1].replace(/^\*/, '');
    }).filter(Boolean).join(', ');
    return `function ${name}(${cleanArgs}) {`;
  });

  // 15. Handle variable declarations:
  js = js.replace(/\b(?:int|double|float|BOOL|NSInteger|NSUInteger|NSString|NSNumber|NSArray|NSDictionary|id|[A-Z]\w*)\s*(?:\*\s*)?(\w+)\s*(=|;)/g, (match, vname, rest) => {
    if (vname === 'return' || vname === 'if' || vname === 'while' || vname === 'for' || vname === 'class' || vname === 'function') return match;
    return `let ${vname} ${rest}`;
  });

  // 16. Handle int main(...) { ... }
  js = js.replace(/int\s+main\s*\([^)]*\)\s*\{/g, 'function main() {');

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
    const jsCode = transpileObjC(data.code || '');

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
      Array: Array,
      NSLog: println
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
            const strippedExpr = transpileObjC(test.expression);
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
