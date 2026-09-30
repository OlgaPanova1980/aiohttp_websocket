import os
from aiohttp import web

async def index_handler(request):
    with open("index.html", "rb") as fp:
        return web.Response(body=fp.read(), content_type="text/html")

async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    request.app["sockets"].append(ws)
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == "ping":
                    await ws.send_str("pong")
            elif msg.type == web.WSMsgType.ERROR:
                pass
    finally:
        request.app["sockets"].remove(ws)
    return ws

async def news_handler(request):
    if request.method == "POST":
        try:
            data = await request.json()
            text = data.get("text", "")
        except:
            return web.Response(status=400, text="Invalid JSON")
            
        if text:
            for ws in request.app["sockets"]:
                if not ws.closed:
                    await ws.send_str(text)
        return web.Response(status=200, text="OK")

async def on_shutdown(app):
    for ws in app["sockets"]:
        await ws.close()

def init():
    app = web.Application()
    app["sockets"] = []
    app.router.add_get("/", index_handler)
    app.router.add_get("/ws", ws_handler)
    app.router.add_post("/news", news_handler)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    web.run_app(init(), port=8080)


