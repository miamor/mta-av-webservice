from flask_restplus import Resource
from flask_restplus import Namespace

from .app import init_app, db
from .apis import init_api

ns_hello = Namespace(name='hello')
api = init_api()


@ns_hello.route('')
class HelloWorld(Resource):
    def get(self):
        return {'Hello': 'Hello World!'}


def init_hello():
    """
    This is for testing
    :return:
    """
    api.add_namespace(ns_hello, path='/hello')


def create_app(config):
    """
    Create app.
    :param config:
    :return:
    """
    init_hello()
    app = init_app(config_name=config)
    api.init_app(app)
    return app
