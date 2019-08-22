import datetime

import jwt
from flask import (current_app as app, Response)

from Model.User import User


def auth(method):
    def decorator(req):
        token = req.headers.get('Authorization')
        connected_user = User.objects(tokens=token).first()
        if connected_user is not None:
            del connected_user.password
            del connected_user.tokens
            connected_user.tokens = [req.headers.get('Authorization')]
            return method(req, request_user=connected_user)

        return Response("Unauthenticated", status=401)
        
    return decorator


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
