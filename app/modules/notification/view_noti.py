from flask_restplus import Resource
# from app.modules.common.decorator import token_required, admin_token_required
from .dto_noti import DtoNoti
# from .controller_noti import ControllerNoti
from flask import request, jsonify, abort
import app.settings.cf as cf
import json

api = DtoNoti.api
noti = DtoNoti.model

@api.route('/count')
class NotiCount(Resource):
    def get(self):
        data = request.args
        # controller = ControllerNoti()
        cmd = cf.controllerNoti.get_query(filters=data)
        return cf.controllerNoti.count_all(cmd=cmd)

@api.route('')
class NotiList(Resource):
    @api.marshal_list_with(noti)
    def get(self):
        data = request.args
        page = int(data['p']) if ('p' in data and data['p'] != 'undefined') else 0
        # controller = ControllerNoti()
        cmd = cf.controllerNoti.get_query(filters=data)
        return cf.controllerNoti.get(cmd=cmd, page=page)

    @api.expect(noti)
    @api.marshal_with(noti)
    def post(self):
        # data = api.payload
        # data = request.form.to_dict(flat=True)
        data = request.get_json()
        # controller = ControllerNoti()
        return cf.controllerNoti.create(data=data)


@api.route('/<int:cid>')
class Noti(Resource):
    @api.marshal_with(noti)
    def get(self, cid):
        # controller = ControllerNoti()
        return cf.controllerNoti.get_by_id(object_id=cid)

    # @api.expect(noti)
    # def put(self, cid):
    #     data = api.payload
    #     # controller = ControllerNoti()
    #     return cf.controllerNoti.update(object_id=cid, data=data)

    def delete(self, cid):
        # controller = ControllerNoti()
        return cf.controllerNoti.delete(object_id=cid)

