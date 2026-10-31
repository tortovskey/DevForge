"""HTTP and worker boundaries for the local application."""
import asyncio
import re
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import JSONResponse

MAX_BODY = 7_000_000
ORIGINS = [f'http://{host}:{port}' for host in ('127.0.0.1', 'localhost') for port in (5173, 5174, 8000, 8765, 8766, 8767)]
HOST = re.compile(r'(?:127\.0\.0\.1|localhost|testserver)(?::([0-9]{1,5}))?\Z', re.ASCII)


class LocalSecurityMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        headers = Headers(scope=scope)
        host = headers.get('host', '')
        match = HOST.fullmatch(host)
        error = None
        if not match or (match.group(1) and not 1 <= int(match.group(1)) <= 65535):
            error = (403, 'Local hosts only')
        # Reject Windows drive/UNC syntax before StaticFiles touches the filesystem.
        path = scope['path']
        if '\\' in path or ':' in path or '\x00' in path or path.startswith('//'):
            error = (400, 'Invalid path')
        origin = f"{scope['scheme']}://{host}"
        if scope['method'] not in {'GET', 'HEAD', 'OPTIONS'}:
            if headers.get('origin') and headers['origin'] not in [*ORIGINS, origin]:
                error = (403, 'Untrusted origin')
            if headers.get('sec-fetch-site') == 'cross-site':
                error = (403, 'Cross-site write blocked')
        length = headers.get('content-length')
        if length is not None and (not re.fullmatch(r'[0-9]{1,10}', length) or int(length) > MAX_BODY):
            error = (413, 'Request too large')

        async def secured_send(message):
            if message['type'] == 'http.response.start':
                out = MutableHeaders(scope=message)
                out['X-Content-Type-Options'] = 'nosniff'
                out['Referrer-Policy'] = 'no-referrer'
                out['Cross-Origin-Opener-Policy'] = 'same-origin'
                out['Cross-Origin-Embedder-Policy'] = 'require-corp'
                out['X-Frame-Options'] = 'DENY'
                if path.startswith('/api/'):
                    out['Cache-Control'] = 'no-store'
                if path.startswith(('/workers/', '/runtimes/')):
                    # Worker code is untrusted. Only bundled runtime files may be fetched.
                    runtime = origin + '/runtimes/'
                    worker = origin + '/workers/backend_pack.py'
                    out['Content-Security-Policy'] = (
                        f"default-src 'none'; script-src {runtime} blob: 'unsafe-eval'; "
                        f"connect-src {runtime} {worker}; worker-src {runtime} blob:; "
                        "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
                    )
                else:
                    out['Content-Security-Policy'] = (
                        "default-src 'self'; script-src 'self' 'unsafe-eval'; "
                        "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
                        "font-src 'self' data:; connect-src 'self'; worker-src 'self' blob:; "
                        "frame-src 'self' blob:; object-src 'none'; base-uri 'none'; "
                        "form-action 'self'; frame-ancestors 'none'"
                    )
            await send(message)

        if error:
            return await JSONResponse({'detail': error[1]}, status_code=error[0])(scope, receive, secured_send)

        # Enforce the limit on actual bytes, including chunked requests with no Content-Length.
        chunks, size = [], 0
        try:
            async with asyncio.timeout(15):
                while True:
                    message = await receive()
                    if message['type'] == 'http.disconnect':
                        return
                    chunk = message.get('body', b'')
                    size += len(chunk)
                    if size > MAX_BODY:
                        return await JSONResponse({'detail': 'Request too large'}, status_code=413)(scope, receive, secured_send)
                    chunks.append(chunk)
                    if not message.get('more_body', False):
                        break
        except TimeoutError:
            return await JSONResponse({'detail': 'Request body timed out'}, status_code=408)(scope, receive, secured_send)
        if length is not None and int(length) != size:
            return await JSONResponse({'detail': 'Invalid Content-Length'}, status_code=400)(scope, receive, secured_send)
        delivered = False

        async def buffered_receive():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {'type': 'http.request', 'body': b''.join(chunks), 'more_body': False}
            return await receive()

        await self.app(scope, buffered_receive, secured_send)
