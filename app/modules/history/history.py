import datetime

from app.app import db
from app.modules.common.model import Model


class History(Model):
    __tablename__ = "history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('histories', lazy=True))

    description = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    time_created = db.Column(db.Time, nullable=False)

    def __init__(self, user_id, description, date_created=None, time_created=None):
        self.user_id = user_id
        self.description = description
        if date_created is None:
            date_created = datetime.datetime.today().date()
        if time_created is None:
            time_created = datetime.datetime.now().time()
        self.date_created = date_created
        self.time_created = time_created
