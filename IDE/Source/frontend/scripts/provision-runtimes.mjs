import {mkdir,readFile,writeFile,rename,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve,join} from 'node:path';

const root=fileURLToPath(new URL('..',import.meta.url));
const destination=process.env.DEVFORGE_RUNTIME_DIR?resolve(process.env.DEVFORGE_RUNTIME_DIR):join(root,'public/runtimes');
const provenance=JSON.parse(await readFile(join(root,'../licenses/wasm-clang-PROVENANCE.json'),'utf8'));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
async function acquire(url,path,expected){
  try{if(sha(await readFile(path))===expected)return;}catch(e){if(e.code!=='ENOENT')throw e;}
  await mkdir(resolve(path,'..'),{recursive:true});
  const response=await fetch(url,{signal:AbortSignal.timeout(180000)});
  if(!response.ok)throw new Error(`Runtime download failed (${response.status}): ${url}`);
  const bytes=new Uint8Array(await response.arrayBuffer());
  if(sha(bytes)!==expected)throw new Error(`SHA-256 mismatch: ${url}`);
  const temporary=path+'.download';
  try{await writeFile(temporary,bytes);await rename(temporary,path);}finally{await rm(temporary,{force:true});}
}
for(const [name,expected] of Object.entries(provenance.sha256)){
  if(!/^[\w.-]+$/.test(name))throw new Error('Invalid provenance path');
  await acquire(`https://raw.githubusercontent.com/binji/wasm-clang/${provenance.commit}/${name}`,join(destination,'clang',name),expected);
}
await writeFile(join(destination,'clang/PROVENANCE.json'),JSON.stringify(provenance,null,2)+'\n');
const pyodide=JSON.parse(await readFile(join(root,'node_modules/pyodide/package.json'),'utf8'));
const lock=JSON.parse(await readFile(join(root,'node_modules/pyodide/pyodide-lock.json'),'utf8'));
const sqlite=lock.packages.sqlite3;
if(!/^sqlite3-[\w.-]+\.whl$/.test(sqlite.file_name))throw new Error('Invalid sqlite package filename');
await acquire(`https://cdn.jsdelivr.net/pyodide/v${pyodide.version}/full/${sqlite.file_name}`,join(destination,'pyodide',sqlite.file_name),sqlite.sha256);
console.log('Pinned Clang toolchain and Python SQLite package ready; SHA-256 verified.');
