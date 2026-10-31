"""Native Windows window for DevForge IDE; opens directly into the standalone IDE."""
import os
from pathlib import Path
import socket
import sys
import threading
import time

def main():
    from native_shell import claim_instance
    if not claim_instance('IDE'):return
    data = Path(os.environ.get('DEVFORGE_DATA_DIR') or Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'DevForgeIDE' / 'data')
    data.mkdir(parents=True, exist_ok=True)
    os.environ['DEVFORGE_DATA_DIR'] = str(data)
    os.environ['DEVFORGE_DESKTOP'] = '1'
    os.environ['DEVFORGE_MODE'] = 'ide'
    if sys.stdout is None:
        sys.stdout = open(data / 'ide_desktop.log', 'a', encoding='utf-8', buffering=1)
    if sys.stderr is None:
        sys.stderr = sys.stdout
    import uvicorn
    import webview
    from app.main import app

    sock = socket.socket()
    try:
        sock.bind(('127.0.0.1', 0 if os.environ.get('DEVFORGE_TEST_HIDDEN') else 8767))
    except OSError:
        raise RuntimeError('Порт 8767 занят. Закройте другое окно DevForge IDE и повторите запуск.')

    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host='127.0.0.1', port=port, log_level='warning', access_log=False))
    thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
    thread.start()
    for _ in range(300):
        if server.started:
            break
        time.sleep(.1)
    if not server.started:
        raise RuntimeError('Local IDE server did not start')

    url = f'http://127.0.0.1:{port}/ide'
    webview.settings['ALLOW_DOWNLOADS'] = True
    webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = True
    window = webview.create_window(
        'DevForge IDE 1.0.0',
        url,
        width=1500,
        height=980,
        min_size=(800, 600),
        background_color='#111318',
        text_select=True,
        hidden=bool(os.environ.get('DEVFORGE_TEST_HIDDEN'))
    )

    def close():
        server.should_exit = True

    window.events.closed += close

    def smoke():
        report = os.environ.get('DEVFORGE_SMOKE_REPORT')
        if not report:
            return
        import json
        for _ in range(150):
            if window.evaluate_js("!!document.querySelector('.monaco-editor')"):
                break
            time.sleep(.2)
        state = window.evaluate_js("JSON.stringify({title:document.title,url:location.href,ready:!!document.querySelector('.monaco-editor'),icon:[...document.images].some(i=>i.src.endsWith('/forge.svg')&&i.naturalWidth>0),isolated:crossOriginIsolated})")
        Path(report).write_text(state or '{"ready": false}', encoding='utf-8')
        window.destroy()

    try:
        from app.database import ROOT
        webview.start(smoke, gui='edgechromium', debug=False, private_mode=False, storage_path=str(data.parent / 'webview_ide'),icon=str(ROOT/'assets'/'forge.ico'))
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        sock.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, f'Не удалось открыть DevForge IDE.\n{error}\nПроверьте наличие Microsoft Edge WebView2 Runtime.', 'DevForge IDE 1.0.0', 16)
        raise
