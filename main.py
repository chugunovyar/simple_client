import logging

from aiohttp import web
from aiohttp.web_app import Application

from hndlrs.hndlrs import Handler


def make_app() -> Application:
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    app = web.Application()
    app.logger = logger
    _handler = Handler(app=app)
    app.router.add_get('/', _handler.handle_greeting)
    app.router.add_post('/run', _handler.handle_running)
    return app


if __name__ == '__main__':
    web.run_app(make_app())
