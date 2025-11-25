
import logging
import sys

from pythonjsonlogger import jsonlogger
from flask import Flask

from board import pages

def configure_logging(app):
    root = logging.getLogger()

    root.setLevel(logging.INFO)

    log_format = (
        '[%(asctime)s] %(levelname)s %(module)s %(funcName)s %(lineno)d '
        '%(message)s'
    )

    formatter = jsonlogger.JsonFormatter(
        log_format,
        timestamp=True,
        rename_fields={'levelname': 'level', 'asctime': '@timestamp'}
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    root.addHandler(handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def create_app():
    app = Flask(__name__)

    configure_logging(app)

    app.register_blueprint(pages.bp)
    return app
