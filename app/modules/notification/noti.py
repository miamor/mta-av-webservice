from app.modules.common.model import Model
from app.app import db


class Noti(Model):
    __tablename__ = "notification"
    noti_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String)
    date_created = db.Column(db.String)

    def __init__(self, user_id=None, message=None, date_created=None):
        self.user_id = user_id
        self.date_created = date_created
        self.message = message
