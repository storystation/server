from flask import Blueprint, request
from Controller import AuthController

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/logon', methods=['POST', 'GET'])
def logon(): return AuthController.logon(req=request)


@bp.route('/logout')
def logout(): return AuthController.logout(req=request)


@bp.route('/register', methods=['POST'])
def register(): return AuthController.store(req=request)


@bp.route('/user')
def user(): return AuthController.user()
