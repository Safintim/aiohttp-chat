import os.path
import sys
import logging
from os.path import dirname

from aiohttp import web

sys.path.append(os.path.join(dirname(__file__), '..'))

from chat.settings import config
from chat.routes import setup_routes
from chat.middlewares import setup_middlewares
from chat.db import close_pg, init_pg


async def web_app():
    app = web.Application()
    app['config'] = config
    app['websockets_channels'] = {}

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    disabled_loggers = ['urllib3.connectionpool', 'urllib3.util.retry']
    for logger_name in disabled_loggers:
        logger = logging.getLogger(logger_name)
        logger.disabled = True
    app = web_app()
    web.run_app(app)
