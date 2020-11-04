# from flask import request
from flask_restplus import Resource, reqparse

from app.modules.user.dto_user import UserDto
from app.modules.common.decorator import admin_token_required, token_required
from .controller_user import ControllerUser  # create_user, get_list_user, delete_user, update_user, get_list_blocked_user
from flask import request, jsonify, abort

api = UserDto.api
# api = Routing.route_user
_user = UserDto.model

@api.route('/count')
class UserCount(Resource):
    def get(self):
        data = request.args
        controllerUser = ControllerUser()
        cmd = controllerUser.get_query(filters={})
        return controllerUser.count_all(cmd=cmd)

@api.route('')
class UserList(Resource):
    # @admin_token_required
    @api.marshal_list_with(_user)
    def get(self):
        data = request.args
        page = int(data['p']) if ('p' in data and data['p'] != 'undefined') else 0

        controllerUser = ControllerUser()
        cmd = controllerUser.get_query(filters={})
        return controllerUser.get(cmd=cmd, page=page)

    @api.expect(_user, validate=True)
    @api.marshal_with(_user)
    def post(self):
        # data = request.json
        data = api.payload
        controllerUser = ControllerUser()
        return controllerUser.create(data)  # create_user(data)


@api.route('/<int:user_id>')
class User(Resource):
    # @token_required
    @api.marshal_with(_user)
    def get(self, user_id):
        controller = ControllerUser()
        return controller.get_by_id(user_id=user_id)

    # @token_required
    @api.expect(_user, validate=True)
    def put(self, user_id):
        data = api.payload
        controller = ControllerUser()
        return controller.update(object_id=user_id, data=data)

    @admin_token_required
    def delete(self, user_id):
        controller = ControllerUser()
        controller.delete(user_id=user_id)


@api.route('/block')
class BlockList(Resource):
    @admin_token_required
    def get(self):
        controllerUser = ControllerUser()
        return controllerUser.get_list_blocked_user()


parser = reqparse.RequestParser()
parser.add_argument('geo_long', type=float, required=False, help='Geo Longtitude')
parser.add_argument('geo_lat', type=float, required=False, help='Geo Lattitude')
parser.add_argument('country', type=str, required=False, help='The current country of the buyer')
parser.add_argument('city', type=str, required=False, help='The current city of the buyer')
parser.add_argument('street', type=str, required=False, help='The current street of the buyer')
parser.add_argument('max_distance', required=False, help='The max distance to make search')
parser.add_argument('mode', required=False, help='The mode of distance measures')


@api.route('/search')
@api.expect(parser)
class BuyerSearchGeo(Resource):
    # @api.marshal_list_with(_user)
    def get(self):
        args = parser.parse_args()
        controller = ControllerUser()
        return controller.search(args=args)

