from app.modules.common.controller import Controller
from .history import History
from app.app import db


class ControllerHistory(Controller):
    def create(self, data):
        history = self._parse(data=data, history=None)
        db.session.add(history)
        db.session.commit()
        return history

    def get(self):
        histories = History.query.all()
        return histories

    def get_by_id(self, object_id):
        history = History.query.filter_by(history_id=object_id).first()
        return history

    def update(self, object_id, data):
        history = History.query.filter_by(history_id=object_id).first()
        history = self._parse(data=data, history=history)
        db.session.commit()
        return history

    def delete(self, object_id):
        history = History.query.filter_by(history_id=object_id).first()
        db.session.delete(history)
        db.session.commit()

    def _parse(self, data, history=None):
        user_id, description, date_created, time_created = None, None, None, None
        if 'user_id' in data:
            user_id = data['user_id']
        if 'description' in data:
            description = data['description']
        if 'date_created' in data:
            date_created = data['date_created']
        if 'time_created' in data:
            time_created = data['time_created']
        if history is None:
            history = History(user_id=user_id, description=description, date_created=date_created,
                              time_created=time_created)
        else:
            history.user_id = user_id
            history.description = description
            history.date_created = date_created
            history.time_created = time_created
        return history
