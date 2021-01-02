from app.app import db
import datetime

# from app.modules.user.user import User
# from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User
from app.modules.user.blacklist import BlacklistToken
from app.modules.user.ip_login_attempts import LoginAttempts
# from app.modules.user.controller_user import ControllerUser

from app.utils.response import error, result
import app.settings.cf as cf


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        return result(message='Successfully logged out.')
    except Exception as e:
        return error(message=e)

def delta_time(date_2, date_1):
    time_delta = (date_2 - date_1)
    total_seconds = time_delta.total_seconds()
    return total_seconds/60

class ControllerAuth:
    @staticmethod
    def login_user(data, ip):
        print('~~~ [login_user] ip', ip)
        try:
            login_attempt = LoginAttempts.query.filter_by(ip=ip).first()
            if login_attempt is not None:
                # print('\t ******* login_attempt', login_attempt, login_attempt.failed_login_attempts)
                time_delt = delta_time(datetime.datetime.now(), login_attempt.failed_login_time)
                if login_attempt.failed_login_attempts == 3 and time_delt < 3:
                    print('\t ******* ERROR', login_attempt, login_attempt.failed_login_attempts)
                    return error(message='You\'ve reached limit tries. Please try again in {} minutes.'.format(round(3-time_delt, 2)))
            

            # user = User.query.filter_by(email=cf.sanitize_data(data.get('email'))).first()
            user = User.query.filter_by(email=data.get('email')).first()
            print("data.get('password')", data.get('password'))
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.user_id)
                if user.blocked:
                    return error(message='User has been blocked')
                if auth_token:
                    return result(message='Successfully logged in', data={'Authorization': auth_token.decode()})
            else:
                # ControllerUser.update()
                if login_attempt is None:
                    # insert login_attempt of this ip
                    ip_login_attempt = LoginAttempts(ip=ip)
                    db.session.add(ip_login_attempt)
                    db.session.commit()
                else:
                    if delta_time(datetime.datetime.now(), login_attempt.failed_login_time) > 3:
                        login_attempt.failed_login_attempts = 1
                    else:
                        login_attempt.failed_login_attempts += 1
                        # print('\t ****** modify! login_attempt.failed_login_attempts', login_attempt.failed_login_attempts)
                    login_attempt.failed_login_time = datetime.datetime.now()
                    db.session.commit()
                return error(message='Email or Password does not match')
        except Exception as e:
            return error(message=e)

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                return error(message=resp)
        else:
            return error(message='Provide a valid auth token')

    @staticmethod
    def get_logged_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            auth_token = auth_token.split(' ')[1]
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(user_id=resp).first()
                print(user)
                res = {
                        'user_id': user.user_id,
                        'email': user.email,
                        'role': user.role,
                        'name': user.name
                        }
                return result(data=res)
            return error(message=resp)
        else:
            return error(message='Provide a valid auth token')