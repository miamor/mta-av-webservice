from app.app import db
import datetime
# from app.modules.common.entity import Entity
from ..common.model import Model



class BlacklistToken(Model):
    """
    Token model for storing JWT tokens
    """
    __tablename__ = 'blacklist_token'

    blacklist_token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.date_created = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
