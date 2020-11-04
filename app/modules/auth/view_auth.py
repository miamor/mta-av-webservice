from flask import request
from flask_restplus import Resource

from app.modules.auth.dto_auth import DtoAuth
from .controller_auth import ControllerAuth
from app.modules.user.dto_user import UserDto
# from app.modules.common.decorator import token_required

api = DtoAuth.api
# api = Routing.route_auth
model = DtoAuth.model
_user = UserDto.model


@api.route('/login')
class UserLogin(Resource):
    @api.expect(model, validate=True)
    def post(self):
        post_data = api.payload # request.json
        source_ip = request.remote_addr
        print('[/auth/login] post_data', post_data, 'source_ip', source_ip)
        return ControllerAuth.login_user(data=post_data, ip=source_ip)


@api.route('/logout')
class LogoutAPI(Resource):
    # @token_required
    def post(self):
        auth_header = request.headers.get('Authorization')
        return ControllerAuth.logout_user(data=auth_header)


@api.route('/info')
class UserInfo(Resource):
    # @token_required
    def get(self):
        return ControllerAuth.get_logged_user(request)
