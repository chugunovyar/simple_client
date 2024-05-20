import asyncio

from aiohttp import web
from aiohttp.web_app import Application

from tools.tools import generate_articles


class Handler:
    def __init__(self, app: Application):
        self.log = app.logger

    async def handle_greeting(self, request):
        name = request.match_info.get('name', "Anonymous")
        txt = "Hello, {}".format(name)
        return web.Response(text=txt)

    async def handle_running(self, request):
        data = await request.json()
        self.log.debug(f"{data}")
        asyncio.create_task(generate_articles(data['num']))
        return web.json_response(data={}, status=200)
