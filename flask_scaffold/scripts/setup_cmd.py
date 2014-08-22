from __future__ import unicode_literals

from distutils.core import Command

class RunServerCommand(Command):
    description = "run server"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from flask_scaffold.core import load_deps, app, setup_logging
        setup_logging()
        load_deps()

        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(
            address=app.config['SERVER_HOSTNAME'],
            port=app.config['SERVER_PORT'])
        IOLoop.instance().start()

