from flask_restplus import Resource
from .dto_history import DtoHistory
from .controller_history import ControllerHistory

api = DtoHistory.api
history = DtoHistory.model


@api.route('')
class HistoryList(Resource):
    @api.marshal_list_with(history)
    def get(self):
        controller = ControllerHistory()
        return controller.get()

    @api.expect(history)
    @api.marshal_with(history)
    def post(self):
        data = api.payload
        controller = ControllerHistory()
        return controller.create(data=data)


@api.route('/<int:history_id>')
class History(Resource):
    @api.marshal_with(history)
    def get(self, history_id):
        controller = ControllerHistory()

    @api.marshal_with(history)
    @api.expect(history)
    def put(self, history_id):
        data = api.payload
        controller = ControllerHistory()
        return controller.update(object_id=history_id, data=data)

    def delete(self, history_id):
        controller = ControllerHistory()
        return controller.delete(object_id=history_id)
