from Model.User import *
from flask import json


class UsersController:
    @classmethod
    def show(cls):
        user = User.objects.first()
        return json.jsonify(user)

    @classmethod
    def store(cls, req):
        data = req.get_json()
        user = User(username=data['username'], email=data['email'], password=data['password'])
        user.save()
        return json.jsonify(user)
