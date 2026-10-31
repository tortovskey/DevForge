const fengari = require('../frontend/node_modules/fengari-web');
globalThis.fengari = fengari;

let lastMsg = null;
globalThis.self = {
  postMessage: (msg) => { lastMsg = msg; }
};

require('../frontend/public/workers/lua.js');

async function runTest() {
  const code = `
    local function greet(name)
      return "Hello, " .. name .. "!"
    end
    print(greet("DevForge"))
    x = 10 + 32
  `;

  await globalThis.self.onmessage({
    data: {
      code,
      tests: [
        { id: 't1', expression: 'x', expected: 42 },
        { id: 't2', label: 'stdout test', expected: 'Hello, DevForge!' }
      ]
    }
  });

  console.log('Result:', JSON.stringify(lastMsg, null, 2));
}

runTest().catch(console.error);
