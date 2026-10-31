import {cp,mkdir,readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('..',import.meta.url)));
await mkdir('public/runtimes/pyodide',{recursive:true});
await cp('node_modules/pyodide','public/runtimes/pyodide',{recursive:true});
await mkdir('public/runtimes/sql',{recursive:true});
for(const file of ['sql-wasm.js','sql-wasm.wasm']) await cp(`node_modules/sql.js/dist/${file}`,`public/runtimes/sql/${file}`);
console.log('Local Python and SQLite runtimes ready.');
await mkdir('public/runtimes/pglite',{recursive:true});
await cp('node_modules/@electric-sql/pglite/dist','public/runtimes/pglite',{recursive:true,filter:source=>!source.endsWith('.map')&&!source.endsWith('.ts')&&!source.endsWith('.cts')&&!source.endsWith('.cjs')});
console.log('Local PostgreSQL / PGlite runtime ready.');
await mkdir('public/runtimes/fengari',{recursive:true});
// The package's bundle is CommonJS. Give it a local module, then expose its API in the Worker.
const fengariBundle=await readFile('node_modules/fengari-web/dist/fengari-web.bundle.js','utf8');
await writeFile('public/runtimes/fengari/fengari-web.js',`(function(module){${fengariBundle}\nself.fengari=module.exports;})({exports:{}});`);
console.log('Local Lua / Fengari runtime ready.');
