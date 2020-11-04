from flask_restplus import Api
from app.modules import ns_user, ns_auth, ns_capture, ns_history, ns_url, ns_noti


def init_api():
    api = Api(title='mtaSMaD APIs',
              version='1.0',
              description='mtaAV Web API')
    api.add_namespace(ns_user, path='/api/v1/user')
    api.add_namespace(ns_auth, path='/api/v1/auth')
    api.add_namespace(ns_capture, path='/api/v1/capture')
    api.add_namespace(ns_history, path='/api/v1/history')
    api.add_namespace(ns_url, path='/api/v1/url')
    api.add_namespace(ns_noti, path='/api/v1/noti')
    return api
