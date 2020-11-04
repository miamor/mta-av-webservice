from app.app import db
import datetime
# from app.modules.common.entity import Entity
from ..common.model import Model



class LoginAttempts(Model):
    __tablename__ = 'ip_login_attempts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100), unique=True, nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=True)
    failed_login_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, ip, failed_login_attempts=1):
        self.ip = ip
        self.failed_login_attempts = failed_login_attempts
        self.failed_login_time = datetime.datetime.now()

    # @staticmethod
    # def check_blacklist(auth_token):
    #     res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    #     if res:
    #         return True
    #     else:
    #         return False
