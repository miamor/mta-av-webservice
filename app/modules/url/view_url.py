from flask_restplus import Resource
# from app.modules.common.decorator import token_required, admin_token_required
from .dto_url import DtoUrl
from .controller_url import ControllerUrl
from flask import request, jsonify, abort
import app.settings.cf as cf

import sys
sys.path.insert(1, cf.__URLCHECKER_ROOT__)
import classifier as urlclassifier
import json

api = DtoUrl.api
capture = DtoUrl.model


@api.route('')
class UrlList(Resource):
    @api.marshal_list_with(capture)
    def get(self):
        data = request.args
        controller = ControllerUrl()
        print('[/url] GET', data)
        return controller.get(filters=data)

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
        is_malicious_urls = []
        if len(urls) > 0:
            is_malicious_urls = urlclassifier.classifier(urls).tolist()
        print('[/url/checkurl] is_malicious_urls', is_malicious_urls)
        
        controller = ControllerUrl()
        for i in range(len(urls)):
            if is_malicious_urls[i] == 1:
                data = {
                    'url': urls[i],
                    'is_malicious': is_malicious_urls[i]
                }
                controller.create(data=data)
        
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
class Url(Resource):
    def get(self):
        controller = ControllerUrl()
        return controller.stat()
