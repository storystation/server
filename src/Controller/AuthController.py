import datetime

from flask import json, Response
from mongoengine import ValidationError, Q, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash

from DTO.UserDTO import UserDTO
from Middleware.Auth import auth, encode_auth_token
from Model.User import User


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
    except ValidationError as e:
        error.append(str(e))
    except KeyError as e:
        error.append("Missing key in request body : {}".format(e))
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

    user_response = UserDTO(new_user).__dict__
    user_response['tokens'] = new_user.tokens
    return Response(json.dumps(user_response), status=201, headers={"content-type": "application/json"})


def logon(req):
    data = req.get_json()
    try:
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
    except KeyError as e:
        return Response(json.dumps({"error": "{} field is required".format(e)}), status=400,
                        headers={"content-type": "application/json"})

@auth
def logout(req, **kwargs):
    current_user = kwargs['request_user']
    User.objects(id=current_user.id).update_one(pull__tokens=current_user.tokens[0])
    return Response("", status=204)


@auth
def user(req, **kwargs):
    user_response = UserDTO(kwargs['request_user']).__dict__
    return Response(json.dumps(user_response), status=200,
                    headers={"content-type": "application/json"})
