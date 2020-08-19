from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoHistory(Dto):
    name = 'history'
    api = Namespace(name)
    model = api.model(name, {
        'history_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=True),
        'description': fields.String(required=True),
        'date_created': fields.Date(required=False),
        'time_created': fields.DateTime(required=False)
    })
