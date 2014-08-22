from __future__ import unicode_literals
import os

from flask import Flask

app = Flask(__name__, '/static')
app.config.from_object('flask_scaffold.default_settings')


def setup_logging():
    """Setup logging configuration

    """
    import logging.config
    import yaml

    log_path = 'logging.yaml'
    if os.path.exists(log_path):
        config = yaml.load(open(log_path, 'rt'))
        logging.config.dictConfig(config)
    else:
        if not app.config['DEBUG']:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)


def load_deps():
    """Load dependencies

    """
    from flask_scaffold.modules.api import api
    app.register_module(api, url_prefix='/api')


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    setup_logging()
    load_deps()
    app.run()