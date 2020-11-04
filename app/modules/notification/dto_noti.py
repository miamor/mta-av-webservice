from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoNoti(Dto):
    name = 'notification'
    api = Namespace(name)
    model = api.model(name, {
        'noti_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=False),
        'message': fields.String(required=False),
        'date_created': fields.String(required=False),
    })
