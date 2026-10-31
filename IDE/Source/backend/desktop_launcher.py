"""Native Windows window with system WebView2; no Python/Node installation required."""
import os
from pathlib import Path
import socket
import sys
import threading
import time

def main():
    from native_shell import claim_instance
    if not claim_instance('Desktop'):return
    data=Path(os.environ.get('DEVFORGE_DATA_DIR') or Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'DevForge'/'data')
    data.mkdir(parents=True,exist_ok=True);os.environ['DEVFORGE_DATA_DIR']=str(data)
    os.environ['DEVFORGE_DESKTOP']='1'
    if sys.stdout is None:sys.stdout=open(data/'desktop.log','a',encoding='utf-8',buffering=1)
    if sys.stderr is None:sys.stderr=sys.stdout
    import uvicorn
    import webview
    from app.main import app
    sock=socket.socket()
    try:sock.bind(('127.0.0.1',0 if os.environ.get('DEVFORGE_TEST_HIDDEN') else 8766))
    except OSError:
        # Keep the origin stable so browser draft recovery survives restarts.
        import ctypes
        ctypes.windll.user32.MessageBoxW(0,'DevForge Desktop уже открыт или порт 8766 занят. Закройте предыдущее окно.','DevForge 1.0.0',64)
        return
    port=sock.getsockname()[1]
    server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,log_level='warning',access_log=False))
    thread=threading.Thread(target=lambda:server.run(sockets=[sock]),daemon=True);thread.start()
    for _ in range(300):
        if server.started:break
        time.sleep(.1)
    if not server.started:raise RuntimeError('Local server did not start')
    url=f'http://127.0.0.1:{port}'
    webview.settings['ALLOW_DOWNLOADS']=True
    webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER']=True
    window=webview.create_window('DevForge IDE 1.0.0',url,width=1440,height=960,min_size=(760,600),background_color='#111318',text_select=True,hidden=bool(os.environ.get('DEVFORGE_TEST_HIDDEN')))
    def close():server.should_exit=True
    window.events.closed+=close
    # Test entry accepts no external code: it checks the bundled Python worker.
    def smoke():
        report=os.environ.get('DEVFORGE_SMOKE_REPORT')
        if not report:return
        import json
        for _ in range(100):
            if window.evaluate_js("!!document.querySelector('.auth-card')"):break
            time.sleep(.2)
        window.evaluate_js("""
        window.__smokeResult=null;
        if(!crossOriginIsolated){window.__smokeResult={error:'Shared memory unavailable'};}
        else {
          const buffer=new SharedArrayBuffer(4104),state=new Int32Array(buffer,0,2);
          const worker=new Worker('/workers/python.js');
          worker.onerror=e=>{window.__smokeResult={error:e.message};worker.terminate();};
          worker.onmessage=e=>{
            if(e.data.type==='ready')worker.postMessage({code:'print(int(input())+1)',inputBuffer:buffer});
            if(e.data.type==='input-request'){
              new Uint8Array(buffer,8).set(new TextEncoder().encode('41'));
              Atomics.store(state,1,2);Atomics.store(state,0,1);Atomics.notify(state,0);
            }
            if(e.data.type==='result'||e.data.type==='boot-error'){
              window.__smokeResult=e.data.result||{error:e.data.error};worker.terminate();
            }
          };
        }
        """)
        for _ in range(300):
            if window.evaluate_js('window.__smokeResult!==null'):break
            time.sleep(.2)
        state=window.evaluate_js("JSON.stringify({title:document.title,login:!!document.querySelector('.auth-card'),isolated:crossOriginIsolated,python:window.__smokeResult,url:location.origin,body:document.body.innerText.slice(0,1000)})")
        Path(report).write_text(state,encoding='utf-8');window.destroy()
    try:
        from app.database import ROOT
        webview.start(smoke,gui='edgechromium',debug=False,private_mode=False,storage_path=str(data.parent/'webview'),icon=str(ROOT/'assets'/'forge.ico'))
    finally:server.should_exit=True;thread.join(timeout=5);sock.close()

if __name__=='__main__':
    try:main()
    except Exception as error:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0,'Не удалось открыть DevForge.\n'+str(error)+'\nПроверьте наличие Microsoft Edge WebView2 Runtime.','DevForge 1.0.0',16)
        raise
