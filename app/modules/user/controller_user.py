from app.app import db, flask_bcrypt
from flask_restplus import marshal
from app.modules.user.user import User
from app.utils.geo import geo_distance

from app.utils.response import error, result
from app.modules.user.dto_user import UserDto
from app.modules.common.controller import Controller


class ControllerUser(Controller):
    """
    Controller to mamage all interaction to user table in database.
    """

    def login(self, data):
        email = data['email']
        password_hash = data['password']
        user = User.query.filter_by(email=email, password_hash=password_hash).first()
        if user is None:
            return None
        return result(data=marshal(user, UserDto.model))  # user

    def create(self, data):
        """
        Tao nguoi dung moi
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            return
        if not 'email' in data and not 'password' in data:
            return
        try:
            exist_user = User.query.filter_by(email=data['email']).first()
            if not exist_user:
                user = self._parse_user(data=data, user=None)
                db.session.add(user)
                db.session.commit()
                return result(message='Create user successfully', data=marshal(user, UserDto.model))  # True, user  # send_result(message='Create user successfully', data=marshal(user, UserDto.model))
            else:
                return error(message='User exists')  # False, None  # send_error(message='User already exists')
        except Exception as e:
            print(e.__str__())
            return error(message='Could not create user. Check again.')  # False, None  # send_error(message=e)

    def get(self):
        """
        Return all users in database
        :return:
        """
        try:
            users = User.query.all()
            # return result(data=marshal(users, UserDto.model))
            return users
        except Exception as e:
            print(e.__str__())
            return error(message='Could not load users.')  # None  # send_error(message=e)

    def get_by_id(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        return result(data=marshal(user, UserDto.model))  # user

    def update(self, object_id, data):
        try:
            user = User.query.filter_by(user_id=object_id).first()
            if not user:
                return error(message='User not found')  # False  # send_error(message='User not found')
            else:
                user = self._parse_user(data=data, user=user)
                db.session.commit()
                return result(message='Update successfully', data=marshal(user, UserDto.model))  # True  # send_result(message='Update user successfully', data=marshal(user, UserDto.model))
        except Exception as e:
            print(e.__str__())
            return error(message='Could not update user')  # False  # send_error(message=e)

    def delete(self, user_id):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                return error(message='User not found')  # False  # send_error(message='User not found')
            else:
                db.session.delete(user)
                db.session.commit()
                return result(message='User was deleted')  # True  # send_result(message='Delete user successfully')
        except Exception as e:
            print(e.__str__())
            return error(message='Could not delete user')  # False  # send_error(message=e)

    def get_list_blocked_user(self):
        try:
            list_blocked_user = User.query.filter_by(isblocked=True).all()
            return result(data=marshal(list_blocked_user, UserDto.model))
        except Exception as e:
            print(e.__str__())
            return error(message='Could not load list blocked users')

    def search(self, args):
        if args is None or not isinstance(args, dict):
            return error(data=None, message='Could not search over your criteria. Please check again.')
        geo_long, geo_lat, country, city, street, max_distance, mode = None, None, None, None, None, None, None
        if 'geo_long' in args:
            geo_long = args['geo_long']
        if 'geo_lat' in args:
            geo_lat = args['geo_lat']
        if 'country' in args:
            country = args['country']
        if 'city' in args:
            city = args['city']
        if 'street' in args:
            street = args['street']
        if 'max_distance' in args:
            max_distance = args['max_distance']
        if 'mode' in args:
            mode = args['mode']
        if geo_long is not None and geo_lat is not None and max_distance is not None:
            users = self._get_by_geo(geo_long=geo_long, geo_lat=geo_lat, max_distance=max_distance, mode=mode)
        else:
            users = self._get_by_address(country=country, city=city, street=street)
        return result(data=marshal(users, UserDto.model))  # users

    # other functions
    def _get_by_geo(self, geo_lat, geo_long, max_distance, mode='km'):
        users = User.query.all()
        ret_users = list()
        for user in users:
            distance = geo_distance((user.home_geo_long, user.home_geo_lat), (geo_long, geo_lat), mode=mode)
            if distance < float(max_distance):
                ret_users.append(user)
        return ret_users

        # users = User.query.filter_by(
        #     geo_distance((User.home_geo_long, User.home_geo_lat), (geo_long, geo_lat), mode=mode) <= max_distance).all()
        # return users

    def _get_by_address(self, country=None, city=None, street=None):
        query = db.session.query(User)
        # users = None
        if country is not None:
            # users = User.query.filter_by(home_country=country).all()
            query = query.filter_by(home_country=country)
        if city is not None:
            # users = users.filter_by(home_city=city).all()
            query = query.filter_by(home_city=city)
        if street is not None:
            # users = users.filter_by(home_street=street).all()
            query = query.filter_by(home_street=street)
        users = query.all()
        return users

    def _parse_user(self, data, user=None):
        name, surname, middlename, fullname, age, birthday, home_address, home_country, home_city, home_street, home_geo_long, home_geo_lat, phone, email, username, passwordHash, blocked, token, facebook, instagram, vkontakte, avatar, isadmin = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        if 'name' in data:
            name = data['name']
        if 'surname' in data:
            surname = data['surname']
        if 'middlename' in data:
            middlename = data['middlename']
        if 'fullname' in data:
            fullname = data['fullname']
        if 'age' in data:
            age = int(data['age'])
        if 'birthday' in data:
            birthday = data['birthday']

        if 'home_address' in data:
            home_address = data['home_address']
        if 'home_country' in data:
            home_country = data['home_country']
        if 'home_city' in data:
            home_city = data['home_city']
        if 'home_street' in data:
            home_street = data['home_street']
        if 'home_geo_long' in data:
            home_geo_long = data['home_geo_long']
        if 'home_geo_lat' in data:
            home_geo_lat = data['home_geo_lat']

        if 'phone' in data:
            phone = data['phone']
        # email bat buoc phai co
        email = data['email']
        if 'username' in data:
            username = data['username']
        # password bat buoc phai co
        password = data['password']
        passwordHash = flask_bcrypt.generate_password_hash(password)
        if 'blocked' in data:
            blocked = bool(data['blocked'])

        if 'token' in data:
            token = data['token']
        if 'facebook' in data:
            facebook = data['facebook']
        if 'instagram' in data:
            instagram = data['instagram']
        if 'vkontakte' in data:
            vkontakte = data['vkontakte']
        if 'avatar' in data:
            avatar = data['avatar']
        # if 'isadmin' in data:
        #     isadmin = bool(data['isadmin'])
        if 'role' in data:
            role = int(data['role'])
        if 'failed_login_attempts' in data:
            failed_login_attempts = int(data['failed_login_attempts'])
        if 'failed_login_time' in data:
            failed_login_time = data['failed_login_time']

        if user is None:
            user = User(name=name, surname=surname, middlename=middlename, fullname=fullname, age=age,
                        birthday=birthday, home_address=home_address, home_country=home_country, home_city=home_city,
                        home_street=home_street, home_geo_long=home_geo_long, home_geo_lat=home_geo_lat, phone=phone,
                        email=email, username=username,
                        password_hash=passwordHash, blocked=blocked, token=token,
                        facebook=facebook, instagram=instagram, vkontakte=vkontakte, avatar=avatar, role=role, failed_login_attempts=failed_login_attempts, failed_login_time=failed_login_time)
        else:
            user.name = name
            user.surname = surname
            user.middlename = middlename
            user.fullname = fullname
            user.age = age
            user.birthday = birthday

            user.home_address = home_address
            user.home_country = home_country
            user.home_city = home_city
            user.home_street = home_street
            user.home_geo_long = home_geo_long
            user.home_geo_lat = home_geo_lat

            user.phone = phone
            user.email = email
            user.username = username
            user.password_hash = passwordHash
            user.blocked = blocked

            user.token = token
            user.facebook = facebook
            user.instagram = instagram
            user.vkontakte = vkontakte
            user.avatar = avatar
            # user.isadmin = isadmin
            user.role = role
            user.failed_login_attempts = failed_login_attempts
            user.failed_login_time = failed_login_time
        return user

# def create_user(data):
#     try:
#         exist_user = User.query.filter_by(email=data['email']).first()
#         if not exist_user:
#             user = User(
#                 name=data['name'],
#                 age=data['age'],
#                 location=data['location'],
#                 phoneNumber=data['phoneNumber'],
#                 email=data['email'],
#                 role=data['role'],
#                 passwordHash=flask_bcrypt.generate_password_hash(data['password']),
#                 status=data['status'],
#                 isBlocked=False
#             )
#             db.session.add(user)
#             db.session.commit()
#             return send_result(message='Create user successfully', data=marshal(user, UserDto.user))
#         else:
#             return send_error(message='User already exists')
#     except Exception as e:
#         return send_error(message=e)
#
#
# def get_list_user():
#     try:
#         list_user = User.query.all()
#         return send_result(data=marshal(list_user, UserDto.user))
#     except Exception as e:
#         return send_error(message=e)
#
#
# def delete_user(data):
#     try:
#         user = User.query.filter_by(userID=data['userID']).first()
#         if not user:
#             return send_error(message='User not found')
#         else:
#             db.session.delete(user)
#             db.session.commit()
#             return send_result(message='Delete user successfully')
#     except Exception as e:
#         return send_error(message=e)
#
#
# def update_user(data):
#     try:
#         user = User.query.filter_by(userID=data['userID']).first()
#         if not user:
#             return send_error(message='User not found')
#         else:
#             user.name = data['name']
#             user.age = data['age']
#             user.location = data['location']
#             user.phoneNumber = data['phoneNumber']
#             user.email = data['email']
#             user.role = data['role']
#             user.status = data['status']
#             user.isBlocked = data['isBlocked']
#             db.session.commit()
#             return send_result(message='Update user successfully', data=marshal(user, UserDto.user))
#     except Exception as e:
#         return send_error(message=e)
#
#
# def get_list_blocked_user():
#     try:
#         list_blocked_user = User.query.filter_by(isBlocked=True).all()
#         return send_result(data=marshal(list_blocked_user, UserDto.user))
#     except Exception as e:
#         return send_error(message=e)
