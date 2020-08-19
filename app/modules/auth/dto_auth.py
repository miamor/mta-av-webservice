from flask_restplus import Namespace, fields
from ..common.dto import Dto


class DtoAuth(Dto):
    name = 'auth'
    api = Namespace(name)
    model = api.model('auth_details', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
    })
