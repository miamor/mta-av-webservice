from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class UserDto(Dto):
    name = 'user'
    api = Namespace(name)
    model = api.model(name, {
        'user_id': fields.Integer(required=False),
        'name': fields.String(required=False),
        'surname': fields.String(required=False),
        'middlename': fields.String(required=False),
        'fullname': fields.String(required=False),
        'age': fields.Integer(required=False),
        'birthday': fields.Date(required=False),

        'home_address': fields.String(required=False),
        'home_country': fields.String(required=False),
        'home_city': fields.String(required=False),
        'home_street': fields.String(required=False),
        'home_geo_long': fields.Float(required=False),
        'home_geo_lat': fields.Float(required=False),

        'phone': fields.String(required=False),
        'email': fields.String(required=True),
        'username': fields.String(required=False),
        'password': fields.String(required=False),
        'blocked': fields.Boolean(required=False),

        'token': fields.String(required=False),
        'facebook': fields.String(required=False),
        'instagram': fields.String(required=False),
        'vkontakte': fields.String(required=False),
        'avatar': fields.String(required=False),
        # 'isadmin': fields.Boolean(required=False),
        'role': fields.Integer(required=False),
        'failed_login_attempts': fields.Integer(required=False),
        'failed_login_time': fields.String(required=False)
    })
