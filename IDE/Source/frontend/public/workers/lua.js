/* DevForge Lua Worker: runs Lua 5.3 in Web Worker using Fengari */
let output = '', errors = '', bootError = null;

function append(val, isError = false) {
  const limit = 32000;
  const str = String(val);
  if (isError) {
    if (errors.length < limit) errors += str.slice(0, limit - errors.length);
  } else {
    if (output.length < limit) output += str.slice(0, limit - output.length);
  }
}

// In worker or node environment, import fengari
try {
  if (typeof importScripts === 'function') {
    importScripts('/runtimes/fengari/fengari-web.js');
  } else if (typeof require === 'function') {
    globalThis.fengari = require('fengari-web');
  }
} catch (e) {
  bootError='Ошибка загрузки среды Lua (Fengari): ' + e.message;
}

if (typeof self !== 'undefined' && self.postMessage) {
  self.postMessage(bootError?{type:'boot-error',error:bootError}:{type:'ready'});
}

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

    const fengariObj = typeof fengari !== 'undefined' ? fengari : (typeof window !== 'undefined' ? window.fengari : null);
    if (!fengariObj) {
      throw new Error('Модуль Fengari Lua 5.3 недоступен в воркере');
    }

    const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengariObj;
    const L = lauxlib.luaL_newstate();
    lualib.luaL_openlibs(L);

    // Override print
    lua.lua_register(L, to_luastring('print'), (state) => {
      const n = lua.lua_gettop(state);
      const parts = [];
      for (let i = 1; i <= n; i++) {
        if (lua.lua_isnil(state, i)) {
          parts.push('nil');
        } else if (lua.lua_isboolean(state, i)) {
          parts.push(lua.lua_toboolean(state, i) ? 'true' : 'false');
        } else if (lua.lua_isstring(state, i)) {
          parts.push(to_jsstring(lua.lua_tolstring(state, i)));
        } else {
          parts.push(`[${to_jsstring(lua.luaL_typename(state, i))}]`);
        }
      }
      append(parts.join('\t') + '\n');
      return 0;
    });

    // Custom io.read and io.write
    const setupIoShim = `
      io.read = function()
        return __js_read_line()
      end
      io.write = function(...)
        local args = {...}
        for _, v in ipairs(args) do
          __js_write_raw(tostring(v))
        end
      end
    `;

    lua.lua_register(L, to_luastring('__js_read_line'), (state) => {
      const line = fakePrompt();
      lua.lua_pushstring(state, to_luastring(line));
      return 1;
    });

    lua.lua_register(L, to_luastring('__js_write_raw'), (state) => {
      if (lua.lua_isstring(state, 1)) {
        append(to_jsstring(lua.lua_tolstring(state, 1)));
      }
      return 0;
    });

    lauxlib.luaL_dostring(L, to_luastring(setupIoShim));

    // Multi-file modules support: package.preload
    if (data.files && Array.isArray(data.files)) {
      for (const file of data.files) {
        if (file.name.endsWith('.lua') && file.content && file.name !== (data.filename || 'main.lua')) {
          const modName = file.name.replace(/\.lua$/, '');
          const modLoaderCode = `
            package.preload['${modName}'] = function()
              ${file.content}
            end
          `;
          lauxlib.luaL_dostring(L, to_luastring(modLoaderCode));
        }
      }
    }

    // Run main code
    const mainCode = data.code || '';
    const status = lauxlib.luaL_dostring(L, to_luastring(mainCode));
    if (status !== lua.LUA_OK) {
      const errMsg = to_jsstring(lua.lua_tolstring(L, -1));
      throw new Error('Ошибка Lua: ' + errMsg);
    }

    // Process unit tests
    if (data.tests && Array.isArray(data.tests)) {
      for (const test of data.tests) {
        try {
          if (test.expression) {
            // Evaluate expression in Lua
            const testCode = `return (${test.expression})`;
            const evalStatus = lauxlib.luaL_dostring(L, to_luastring(testCode));
            if (evalStatus === lua.LUA_OK) {
              let actual = null;
              if (lua.lua_isboolean(L, -1)) {
                actual = lua.lua_toboolean(L, -1);
              } else if (lua.lua_isnumber(L, -1)) {
                actual = lua.lua_tonumber(L, -1);
              } else if (lua.lua_isstring(L, -1)) {
                actual = to_jsstring(lua.lua_tolstring(L, -1));
              } else if (lua.lua_isnil(L, -1)) {
                actual = null;
              } else if (lua.lua_istable(L, -1)) {
                // Read small table to array/object
                const obj = {};
                const arr = [];
                let isArr = true;
                lua.lua_pushnil(L);
                while (lua.lua_next(L, -2) !== 0) {
                  let k = lua.lua_isnumber(L, -2) ? lua.lua_tonumber(L, -2) : to_jsstring(lua.lua_tolstring(L, -2));
                  let v = lua.lua_isnumber(L, -1) ? lua.lua_tonumber(L, -1) : (lua.lua_isstring(L, -1) ? to_jsstring(lua.lua_tolstring(L, -1)) : (lua.lua_isboolean(L, -1) ? lua.lua_toboolean(L, -1) : null));
                  if (typeof k === 'number') {
                    arr[k - 1] = v;
                  } else {
                    isArr = false;
                  }
                  obj[k] = v;
                  lua.lua_pop(L, 1);
                }
                actual = isArr && arr.length > 0 ? arr : obj;
              }
              lua.lua_pop(L, 1);

              results.push({
                id: test.id,
                actual: actual,
                error: null
              });
            } else {
              const err = to_jsstring(lua.lua_tolstring(L, -1));
              results.push({
                id: test.id,
                actual: null,
                error: err
              });
            }
          } else {
            // Stdout comparison test
            const normalizedOut = output.trim();
            const expectedStr = typeof test.expected === 'string' ? test.expected.trim() : String(test.expected);
            results.push({
              id: test.id,
              actual: normalizedOut,
              error: null
            });
          }
        } catch (testErr) {
          results.push({
            id: test.id,
            actual: null,
            error: testErr.message
          });
        }
      }
    }

    lua.lua_close(L);
  } catch (err) {
    append('Критическая ошибка выполнения: ' + (err.message || String(err)) + '\n', true);
  }

  const resultPayload = {
    stdout: output,
    stderr: errors,
    tables: [],
    results,
    error: errors || undefined
  };

  self.postMessage({
    type: 'result',
    result: resultPayload
  });
};
