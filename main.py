import logging
import os

import sqlalchemy as db
from aiohttp import web
from aiohttp.web_app import Application
from sqlalchemy import inspect

from hndlrs.hndlrs import Handler


def get_db_engine():
    engine = db.create_engine(
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER', 'postgres')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB', 'client_db')}", )
    insp = inspect(engine)
    print(insp.get_enums())
    return engine


def make_app() -> Application:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    _app = web.Application()
    _app.engine = get_db_engine()

    connection = _app.engine.connect()
    metadata = db.MetaData()
    _app.logger = logger
    _handler = Handler(app=_app)
    _app.router.add_get('/', _handler.handle_greeting)
    _app.router.add_post('/run', _handler.handle_running)
    return _app


if __name__ == '__main__':
    app = make_app()
    web.run_app(app)
