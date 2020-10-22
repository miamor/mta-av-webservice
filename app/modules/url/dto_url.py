from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoUrl(Dto):
    name = 'capture'
    api = Namespace(name)
    model = api.model(name, {
        'capture_id': fields.Integer(required=False),

        'file_name': fields.String(required=True, help='The name of file'),
        'file_size': fields.String(required=False, help='The size of file '),
        'file_extension': fields.String(required=False),
        'file_path': fields.String(required=False),
        
        'hash': fields.String(required=False),
        'md5': fields.String(required=False),
        'sha1': fields.String(required=False),
        'sha256': fields.String(required=False),
        'sha512': fields.String(required=False),
        'ssdeep': fields.String(required=False),
        'report_path': fields.String(required=False),
        'report_id': fields.Integer(required=False),

        'date_created': fields.Date(required=False),
        'date_modified': fields.Date(required=False),

        'date_sent': fields.Date(required=False),
        'time_sent': fields.DateTime(required=False),
        'date_received': fields.Date(required=False),
        'time_received': fields.String(required=False),

        'collection_date': fields.String(required=False),
        'collection_type': fields.String(required=False),
        'source_ip': fields.String(required=False),
        'destination_ip': fields.String(required=False),

        'source_mac': fields.String(required=False),
        'destination_mac': fields.String(required=False),

        'source_url': fields.String(required=False),
        'destination_url': fields.String(required=False),
        'hostname': fields.String(required=False),
        'protocol': fields.String(required=False),

        'source_email': fields.String(required=False),
        'destination_email': fields.String(required=False),
        'source_country': fields.String(required=False),
        'destination_country': fields.String(required=False),

        'malware_type': fields.String(required=False),
        'source_dns': fields.String(required=False),
        'destination_dns': fields.String(required=False),
        'entropy': fields.Float(required=False),

        'description': fields.String(required=False),
        'detected_by': fields.String(required=False),
        'detector_output': fields.String(required=False),
        'scan_time': fields.Float(required=False),
        'warning_level': fields.Integer(required=False),
    })
