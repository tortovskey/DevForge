import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import ts from 'typescript';

const source = ts.transpileModule(readFileSync(new URL('../src/runners/runner.ts', import.meta.url), 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022}
}).outputText;

function harness() {
  let clock = 1, sequence = 0;
  const timers = new Map(), workers = [];
  class Worker {
    terminated = false;
    messages = [];
    constructor() { workers.push(this); }
    ready() { this.onmessage({data: {type: 'ready'}}); }
    result(stdout = 'ok') { this.onmessage({data: {type: 'result', result: {stdout, stderr: '', results: [], tables: []}}}); }
    postMessage(request) { this.messages.push(request); }
    terminate() { this.terminated = true; }
  }
  const exports = {};
  vm.runInNewContext(source, {
    exports, Worker, performance: {now: () => clock}, TextEncoder, Uint8Array, Int32Array,
    setTimeout: (fn, ms) => {const id = ++sequence; timers.set(id, {fn, time: clock + ms}); return id;},
    clearTimeout: id => timers.delete(id)
  });
  return {Runner: exports.BrowserRunner, workers, timers,
    advance(ms) {clock += ms; for(const [id, timer] of [...timers]) if(timer.time <= clock) {timers.delete(id); timer.fn();}}
  };
}

test('completed run clears its timer and reports elapsed execution time', async () => {
  const h = harness(), runner = new h.Runner('javascript', () => {}, 100);
  const first = runner.run({code: 'console.log(1)'});
  h.workers[0].ready(); await Promise.resolve();
  h.advance(20); h.workers[0].result('1');
  assert.equal((await first).duration, 20);
  assert.equal(h.timers.size, 0);
  const second = runner.run({code: 'console.log(2)'}); await Promise.resolve();
  h.advance(90);
  assert.equal(h.workers[0].terminated, false);
  h.workers[0].result('2'); assert.equal((await second).stdout, '2');
  assert.equal(h.timers.size, 0);
});

test('timeout terminates worker and the next run creates a fresh runtime', async () => {
  const h = harness(), runner = new h.Runner('javascript', () => {}, 100);
  const first = runner.run({code: 'while(true){}'});
  h.workers[0].ready(); await Promise.resolve(); h.advance(101);
  assert.match((await first).error, /Timeout/);
  assert.equal(h.workers[0].terminated, true);
  const next = runner.run({code: 'console.log(42)'});
  h.workers[1].ready(); await Promise.resolve(); h.workers[1].result('42');
  assert.equal((await next).stdout, '42');
});

test('stop during boot cannot post the cancelled program into another run', async () => {
  const h = harness(), runner = new h.Runner('javascript');
  const cancelled = runner.run({code: 'cancelled'}); runner.stop();
  const next = runner.run({code: 'next'});
  h.workers[1].ready(); await Promise.resolve(); await Promise.resolve();
  assert.equal(h.workers[1].messages.length, 1);
  assert.equal(h.workers[1].messages[0].code, 'next');
  h.workers[1].result();
  assert.match((await cancelled).error, /остановлено/);
  assert.equal((await next).stdout, 'ok');
});

test('waiting for input pauses execution timeout', async () => {
  const h = harness(), runner = new h.Runner('javascript', () => {}, 100);
  const result = runner.run({code: ''}); h.workers[0].ready(); await Promise.resolve();
  h.advance(20); h.workers[0].onmessage({data: {type: 'phase', phase: 'input'}});
  h.advance(1000); assert.equal(h.workers[0].terminated, false);
  h.workers[0].onmessage({data: {type: 'phase', phase: 'run'}});
  h.advance(20); h.workers[0].result();
  assert.equal((await result).duration, 40);
});
