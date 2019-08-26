import logging
from flask import Blueprint, json, Response, current_app

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/new', methods=['GET'])
def new_game():
    print(current_app.wsgi_app.ws.__dict__)
    return Response("OK")