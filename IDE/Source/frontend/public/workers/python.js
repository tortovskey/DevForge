/* All runtime files are served locally. This worker never sends code to FastAPI. */
let pyodide;
let output = '', errors = '';
function append(value, isError=false) {
  const limit=24000;
  if(isError) { if(errors.length<limit) errors+=value.slice(0,limit-errors.length); }
  else if(output.length<limit) output+=value.slice(0,limit-output.length);
}
function flush(){try{pyodide.runPython("__import__('sys').stdout.flush(); __import__('sys').stderr.flush()");}catch{/* Keep the original execution error. */}}
(async()=>{
  try {
    importScripts('/runtimes/pyodide/pyodide.js');
    pyodide=await loadPyodide({indexURL:'/runtimes/pyodide/'});
    
    await pyodide.loadPackage('sqlite3');
    try {
      const resp = await fetch('/workers/backend_pack.py');
      if (resp.ok) {
        const packCode = await resp.text();
        await pyodide.runPythonAsync(packCode);
      }
    } catch (_) {}
    self.postMessage({type:'ready'});
  } catch(e) {self.postMessage({type:'boot-error',error:String(e)});}
})();
self.onmessage=async({data})=>{
  output='';errors='';
  const outDecoder=new TextDecoder(),errDecoder=new TextDecoder();
  pyodide.setStdout({write:bytes=>{append(outDecoder.decode(bytes,{stream:true}));return bytes.length;}});
  pyodide.setStderr({write:bytes=>{append(errDecoder.decode(bytes,{stream:true}),true);return bytes.length;}});
  // A terminal supplies lines, including an intentional empty line. Exhaustion is EOF.
  const text=String(data.stdin||'').replace(/\r\n/g,'\n');
  const lines=text ? text.split('\n') : [];
  if(text.endsWith('\n')) lines.pop();
  let position=0;
  const shared=typeof SharedArrayBuffer!=='undefined'&&data.inputBuffer instanceof SharedArrayBuffer?data.inputBuffer:null;
  const state=shared?new Int32Array(shared,0,2):null;
  const bytes=shared?new Uint8Array(shared,8):null;
  pyodide.setStdin({stdin:()=>{
    if(position<lines.length)return lines[position++];
    if(!state)return null;
    Atomics.store(state,0,0);
    self.postMessage({type:'input-request',prompt:output.slice(-160)});
    Atomics.wait(state,0,0);
    if(Atomics.load(state,0)!==1)return null;
    const length=Atomics.load(state,1);
    // Browser TextDecoder requires an ordinary ArrayBuffer, not shared memory.
    return new TextDecoder().decode(bytes.slice(0,length));
  },isatty:false});
  const results=[];
  let namespace;
  try {
    // Refresh project modules on every Run; no stale imports after editing a file.
    pyodide.runPython(`
import sys, os, importlib, shutil
for name, module in list(sys.modules.items()):
    if str(getattr(module, '__file__', '')).startswith('/devforge_project/'):
        del sys.modules[name]
if os.path.isdir('/devforge_project'):
    shutil.rmtree('/devforge_project')
os.mkdir('/devforge_project')
if '/devforge_project' not in sys.path:
    sys.path.insert(0, '/devforge_project')
importlib.invalidate_caches()
`);
    for(const file of data.files||[])if(/^[\w-][\w. -]*\.py$/.test(file.name)&&!file.name.includes('..'))pyodide.FS.writeFile('/devforge_project/'+file.name,file.content);
    namespace=pyodide.runPython('dict(__name__="__main__")');
    await pyodide.runPythonAsync(data.code,{globals:namespace,filename:'main.py'});
    flush();
    namespace.set('_stdout',output);
    for(const test of data.tests||[]) {
      try {
        // JSON conversion happens inside Python, preserving lists, dicts, booleans and None.
        const encoded=pyodide.runPython(`__import__('json').dumps(${test.expression}, ensure_ascii=False, allow_nan=False)`,{globals:namespace});
        if(encoded.length>100000) throw new Error('Результат теста слишком большой');
        results.push({id:test.id,actual:JSON.parse(encoded),error:null});
      } catch(e) {results.push({id:test.id,actual:null,error:String(e).slice(0,8000)});}
    }
    self.postMessage({type:'result',result:{stdout:output,stderr:errors,tables:[],results}});
  } catch(e) {
    flush();
    const error=String(e).slice(0,10000);
    self.postMessage({type:'result',result:{stdout:output,stderr:errors,tables:[],results:(data.tests||[]).map(t=>({id:t.id,actual:null,error})),error}});
  } finally {namespace?.destroy();}
};
