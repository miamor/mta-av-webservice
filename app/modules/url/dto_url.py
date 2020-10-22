from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoUrl(Dto):
    name = 'capture_url'
    api = Namespace(name)
    model = api.model(name, {
        'url_capture_id': fields.Integer(required=False),

        'url': fields.String(required=False),
        
        'date_requested': fields.Date(required=False),
        'time_requested': fields.String(required=False),

        'source_ip': fields.String(required=False),

        'protocol': fields.String(required=False),

        'is_malicious': fields.String(required=False),
        'score': fields.String(required=False),
    })
