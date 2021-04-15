import os
from flask import request, g
from functools import wraps
from jose import jwt

from ..common.responses import auth_error


def encode_jwt(token):
    return jwt.encode(token, os.environ['JWT_SECRET'], algorithm='HS256')


def decode_jwt(token):
    return jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])


def authorize(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info = {}
        auth = request.headers.get('Authorization', None)
        if not auth:
            return auth_error('no authorization token provided.')
        try:
            token = auth.split()
            if len(token) != 2 or token[0].lower() != 'bearer':
                return auth_error('token formatting invalid.')
            user_info = decode_jwt(token[1])
            g.id = user_info['id']
            g.role = user_info['role']
        except Exception as e:
            return auth_error(str(e))
        return f(user_info, *args, **kwargs)
    return decorated
