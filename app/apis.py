from flask_restplus import Api
from app.modules import ns_user, ns_auth, ns_capture, ns_history, ns_stat


def init_api():
    api = Api(title='mtaAV APIs',
              version='1.0',
              description='mtaAV Web API')
    api.add_namespace(ns_user, path='/api/v1/user')
    api.add_namespace(ns_auth, path='/api/v1/auth')
    api.add_namespace(ns_capture, path='/api/v1/capture')
    api.add_namespace(ns_stat, path='/api/v1/stat')
    api.add_namespace(ns_history, path='/api/v1/history')
    return api
