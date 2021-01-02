from flask_restplus import Resource
# from app.modules.common.decorator import token_required, admin_token_required
from .dto_url import DtoUrl
from .controller_url import ControllerUrl
from flask import request, jsonify, abort
import app.settings.cf as cf

import json

api = DtoUrl.api
capture = DtoUrl.model

@api.route('/count')
class UrlCount(Resource):
    def get(self):
        data = request.args
        mode = data['mode'] if 'mode' in data else ''
        controller = ControllerUrl()
        cmd = controller.get_query(mode=mode, filters=data)
        return controller.count_all(cmd=cmd)

@api.route('')
class UrlList(Resource):
    @api.marshal_list_with(capture)
    def get(self):
        data = request.args
        mode = data['mode'] if 'mode' in data else ''
        page = int(data['p']) if ('p' in data and data['p'] != 'undefined') else 0
        controller = ControllerUrl()
        # print('[/url/] GET data', data, 'page', page)
        cmd = controller.get_query(mode=mode, filters=data)
        return controller.get(cmd=cmd, page=page)

    @api.expect(capture)
    @api.marshal_with(capture)
    def post(self):
        # data = api.payload
        # data = request.form.to_dict(flat=True)
        data = request.get_json()
        data['hash'] = data['md5']
        print('[/url] POST', data)
        controller = ControllerUrl()
        return controller.create(data=data)


@api.route('/check')
class UrlCheck(Resource):
    # @api.marshal_with(capture)
    def post(self):
        #print('request.form', request.form)
        post_data = json.loads(request.json)
        print('[/url/checkurl] POST', post_data)

        #urls = post_data['urls'] if urls in post_data else []
        urls = post_data['urls']
        source_ips = post_data['source_ip'] if 'source_ip' in post_data else ''
        # print('[/url/checkurl] is_malicious_urls', is_malicious_urls)
        
        controller = ControllerUrl()
        urls, is_malicious_urls = controller.check(urls, source_ips)
        
        resp = jsonify({
            "status": "success",
            "urls": urls,
            "is_malicious_urls": is_malicious_urls
        })
        resp.status_code = 200
        return resp


@api.route('/<int:cid>')
class Url(Resource):
    @api.marshal_with(capture)
    def get(self, cid):
        controller = ControllerUrl()
        return controller.get_by_id(object_id=cid)

    # @api.expect(capture)
    # def put(self, cid):
    #     data = api.payload
    #     controller = ControllerUrl()
    #     return controller.update(object_id=cid, data=data)

    def delete(self, cid):
        controller = ControllerUrl()
        return controller.delete(object_id=cid)


@api.route('/stat')
class UrlStat(Resource):
    def get(self):
        controller = ControllerUrl()
        # return controller.stat()
        stat_data = controller.stat()
        resp = jsonify({
            "status": "success",
            "stat_data": stat_data
        })
        resp.status_code = 200
        return resp
@api.route('/stat_by_date')
class UrlStatDate(Resource):
    def get(self):
        data = request.args
        split = int(data['split']) if 'split' in data else 10000
        days = int(data['days']) if 'days' in data else 10

        controller = ControllerUrl()

        stat_by_date_data = controller.stat_by_date(days, split)
        resp = jsonify({
            "status": "success",
            "stat_by_date": stat_by_date_data
            # "charts": charts
        })
        resp.status_code = 200
        return resp
