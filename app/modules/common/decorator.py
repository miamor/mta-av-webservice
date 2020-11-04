from functools import wraps

from flask import request

from app.modules.auth.controller_auth import ControllerAuth
from app.utils.response import error


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = ControllerAuth.get_logged_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('[admin_token_required] request', request)
        data, status = ControllerAuth.get_logged_user(request)
        token = data.get('data')

        if not token:
            return data, status

        role = token.get('role')
        if role != 3:
            return error('Admin token required')

        return f(*args, **kwargs)

    return decorated
