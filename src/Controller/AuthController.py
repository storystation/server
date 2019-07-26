import sys

from flask import (current_app as app,
                   json, Response)
from datetime import datetime
import jwt
from mongoengine import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from Model.User import *


def store(req):
    data = req.get_json()
    error = []
    email_exists = User.objects(email=data['email'])
    if email_exists.count() > 0:
        error.append("Email already exists")
    username_exists = User.objects(username=data['username'])
    if username_exists.count() > 0:
        error.append("Username already exists")
    try:
        new_user = User(username=data['username'], email=data['email'],
                        password=generate_password_hash(data['password']))
        new_user.created_at = datetime.utcnow()
        new_user.save()
        del new_user.password
        return Response(json.dumps(new_user), status=201, headers={"content-type": "application/json"})
    except (KeyError, ValidationError) as e:
        print(e, file=sys.stderr)
        error.append("You must provide all required data")

    if error.__len__() > 0:
        return Response(json.dumps({"error": "Sent data is invalid", "message": error}), status=400,
                        headers={"content-type": "application/json"})


def logon(req):
    return "logon"


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
            app.config['core']['secret'],
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
        payload = jwt.decode(auth_token, app.config['core']['secret'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
