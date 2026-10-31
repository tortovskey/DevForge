import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);

function worker(language,extra={}){
 let result;const self={postMessage:message=>{if(message.type==='result')result=message.result;}};
 const scope={self,console,...extra};vm.createContext(scope);
 vm.runInContext(readFileSync(new URL(`../public/workers/${language}.js`,import.meta.url),'utf8'),scope);
 return async code=>{await self.onmessage({data:{code}});return result;};
}
test('Rust accepts a single-line main function and nested blocks',async()=>{
 const run=worker('rust');
 for(const code of ['fn main(){println!("5");}','fn main(){if true {println!("5");}}']){
  const result=await run(code);assert.equal(result.error,undefined);assert.equal(result.stdout.trim(),'5');
 }
});
test('Lua browser bundle exposes Fengari without CommonJS globals',()=>{
 const scope={self:{},console,TextEncoder,TextDecoder,Uint8Array,Int32Array,ArrayBuffer,setTimeout,clearTimeout};
 vm.createContext(scope);vm.runInContext(readFileSync(new URL('../public/runtimes/fengari/fengari-web.js',import.meta.url),'utf8'),scope);
 assert.equal(typeof scope.self.fengari.lua.lua_gettop,'function');
});
test('Lua executes and reports runtime errors as failures',async()=>{
 const run=worker('lua',{fengari:require('fengari-web')});
 assert.equal((await run('print(5)')).stdout.trim(),'5');
 assert.match((await run('error("broken")')).error,/broken/);
});
