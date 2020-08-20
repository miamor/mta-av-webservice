from app.app import db, flask_bcrypt
import datetime
import jwt

from app.settings.config import key
from .blacklist import BlacklistToken
from ..common.model import Model


class User(Model):
    """
    user_id
    name
    surname
    middlename
    fullname
    age
    birthday
    home_address
    home_country
    home_city
    home_street
    home_geo_long
    home_geo_lat
    phone
    email
    username
    password_hash
    blocked
    token
    facebook
    instagram
    vkontakte
    avatar
    isadmin
    """
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    middlename = db.Column(db.String(80))
    fullname = db.Column(db.String(80))

    age = db.Column(db.Integer, nullable=True)
    birthday = db.Column(db.Date)

    home_address = db.Column(db.String(255))
    home_country = db.Column(db.String(80))
    home_city = db.Column(db.String(80))
    home_street = db.Column(db.String(80))
    home_geo_long = db.Column(db.Float)
    home_geo_lat = db.Column(db.Float)

    phone = db.Column(db.String(45))
    email = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45))
    password_hash = db.Column(db.String(255))
    blocked = db.Column(db.Boolean, default=False)

    token = db.Column(db.String(255))
    facebook = db.Column(db.String(80))
    instagram = db.Column(db.String(80))
    vkontakte = db.Column(db.String(80))
    avatar = db.Column(db.String(80))  # path to avatar image

    isadmin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password_hash, name=None, surname=None, middlename=None, fullname=None, age=None,
                 birthday=None, home_address=None, home_country=None, home_city=None, home_street=None,
                 home_geo_long=None, home_geo_lat=None, phone=None, username=None, blocked=None,
                 token=None, facebook=None, instagram=None, vkontakte=None, avatar=None, isadmin=None):
        self.name = name
        self.surname = surname
        self.middlename = middlename
        self.fullname = fullname
        self.age = age
        self.birthday = birthday

        self.home_address = home_address
        self.home_country = home_country
        self.home_city = home_city
        self.home_street = home_street
        self.home_geo_long = home_geo_long
        self.home_geo_lat = home_geo_lat

        self.phone = phone
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.blocked = blocked

        self.token = token
        self.facebook = facebook
        self.instagram = instagram
        self.vkontakte = vkontakte
        self.avatar = avatar
        self.isadmin = isadmin

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(userID):
        """
        Generate the Auth token
        :param userID:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': userID
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklist_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklist_token:
                return None  # 'Token blacklisted. Please login again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return None  # 'Signature expired. Please login again.'
        except jwt.InvalidTokenError:
            return None  # 'Invalid token. Please login again.'
