/* Clang 8 / WASI: compilation and execution stay inside this disposable Worker. */
importScripts('/runtimes/clang/shared.js');
const base='/runtimes/clang/';
const buffers=new Map(),modules=new Map();
let output='';
const clean=s=>s.replace(/\x1b\[[0-9;]*m/g,'');
async function readBuffer(url){if(!buffers.has(url)){const r=await fetch(url);if(!r.ok)throw new Error(`Runtime ${r.status}: ${url}`);buffers.set(url,await r.arrayBuffer());}return buffers.get(url);}
async function compileStreaming(url){if(!modules.has(url))modules.set(url,await WebAssembly.compile(await readBuffer(url)));return modules.get(url);}
function create(){
 const api=new API({readBuffer,compileStreaming,hostWrite:s=>{output=(output+clean(s)).slice(0,24000);},clang:base+'clang',lld:base+'lld',memfs:base+'memfs',sysroot:base+'sysroot.tar'});
 api.hostLog=()=>{};api.hostLogAsync=async(_,promise)=>await promise;
 return api;
}
(async()=>{try{await Promise.all(['clang','lld','memfs'].map(f=>compileStreaming(base+f)));await readBuffer(base+'sysroot.tar');self.postMessage({type:'ready'});}catch(e){self.postMessage({type:'boot-error',error:String(e)});}})();
self.onmessage=async({data})=>{
 output='';let warnings='',results=[];
 try{
  self.postMessage({type:'phase',phase:'compile'});
  const api=create();await api.ready;output='';
  const filename=data.filename&&/^[\w-][\w. -]*\.(c|h)$/.test(data.filename)&&!data.filename.includes('..')?data.filename:'main.c';
  const files=(data.files||[]).filter(f=>/^[\w-][\w. -]*\.(c|h)$/.test(f.name)&&!f.name.includes('..'));
  const sources=files.filter(f=>f.name!==filename);sources.push({name:filename,content:data.code});
  for(const file of sources)api.memfs.addFile(file.name,new TextEncoder().encode(file.content));
  const clang=await compileStreaming(base+'clang'),lld=await compileStreaming(base+'lld');
  const objects=[];
  for(const file of sources.filter(f=>f.name.endsWith('.c'))){const obj=file.name+'.o';await api.run(clang,'clang','-cc1','-emit-obj',...api.clangCommonArgs,'-std=c11','-Wall','-Wextra','-O0','-o',obj,'-x','c',file.name);objects.push(obj);}
  await api.run(lld,'wasm-ld','--no-threads','-z','stack-size=1048576','-Llib/wasm32-wasi','lib/wasm32-wasi/crt1.o',...objects,'-lc','-o','program.wasm');
  warnings=output.trim();
  const compiled=await WebAssembly.compile(api.memfs.getFileContents('program.wasm'));
  const execute=async(stdin)=>{
   output='';
   // MemFS consumes binary strings, so encode input as UTF-8 explicitly.
   api.memfs.setStdinStr(Array.from(new TextEncoder().encode(stdin||''),b=>String.fromCharCode(b)).join(''));
   self.postMessage({type:'phase',phase:'run'});
   await api.run(compiled,'program.wasm');
   return output.endsWith('\n')?output.slice(0,-1):output;
  };
  let stdout='';
  if(data.check&&(data.tests||[]).length){
   for(const t of data.tests){try{const text=await execute(t.stdin??data.stdin);if(!stdout)stdout=text;results.push({id:t.id,actual:text.trim(),error:null});}catch(e){results.push({id:t.id,actual:null,error:String(e)});}}
  }else stdout=await execute(data.stdin);
  self.postMessage({type:'result',result:{stdout,stderr:warnings,tables:[],results}});
 }catch(e){const error=(output+'\n'+String(e)).slice(0,10000);self.postMessage({type:'result',result:{stdout:'',stderr:warnings,tables:[],results,error}});}
};
