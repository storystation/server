import sys

from flask import (current_app as app,
                   json, Response)
import datetime
import jwt
from mongoengine import ValidationError, Q, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash

from Model.User import *


def store(req):
    data = req.get_json()
    error = []
    new_user = None
    try:
        new_user = User(username=data['username'], email=data['email'],
                        password=generate_password_hash(data['password']))
        new_user.created_at = datetime.datetime.utcnow()
        new_user.tokens = []
        new_user.save()
        new_user.tokens.append(encode_auth_token(str(new_user.id)).decode('ascii'))
        new_user.save()
        del new_user.password
    except (KeyError, ValidationError) as e:
        error.append(str(e))
    except (DuplicateKeyError, NotUniqueError) as e:
        email_exists = User.objects(email=data['email']).count()
        if email_exists > 0:
            error.append("Email already exists")
        username_exists = User.objects(username=data['username']).count()
        if username_exists > 0:
            error.append("Username already exists")

    if error.__len__() > 0:
        return Response(json.dumps({"error": "Sent data is invalid", "message": error}), status=400,
                        headers={"content-type": "application/json"})

    return Response(json.dumps(new_user), status=201, headers={"content-type": "application/json"})


def logon(req):
    data = req.get_json()
    error = []
    queried_user = User.objects(Q(username=data['login']) | Q(email=data['login'])).first()
    if queried_user is not None:
        if check_password_hash(queried_user.password, data['password']):
            token = encode_auth_token(str(queried_user.id)).decode('ascii')
            queried_user.tokens.append(token)
            queried_user.save()
            return Response(json.dumps({"token": token}), status=200,
                            headers={"content-type": "application/json"})
        else:
            return Response(json.dumps({"error": "Login or password is incorrect"}), status=403,
                            headers={"content-type": "application/json"})
    else:
        return Response(json.dumps({"error": "Login or password is incorrect"}), status=403,
                        headers={"content-type": "application/json"})


def logout(req):
    return "logout"


def user():
    return "User"


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config['CORE']['secret'],
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
        payload = jwt.decode(auth_token, app.config['CORE']['secret'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
