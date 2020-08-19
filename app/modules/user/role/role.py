from app.modules.common.model import Model
from app.app import db


class Role(Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String, nullable=False)
    role_description = db.Column(db.String)

    def __init__(self, role_name, role_description):
        self.role_name = role_name
        self.role_description = role_description
