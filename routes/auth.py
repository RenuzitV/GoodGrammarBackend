from flask import Flask, Blueprint, jsonify
from middleware.auth_middleware import token_required
from models.model import User

bp = Blueprint('auth', __name__)


@bp.route('/')
def hello_world():
    """
    Hello world
    :return: Hello World message
    """
    return 'Hello World!!!'


@bp.route('/test_auth')
@token_required
def test_auth(token):
    """
    Test auth
    :param token: returned token from `token_required` decorator
    :return: authorized message and claims from JWT token
    """
    # does not need to check for authorization in this function. if we get here, it means that the token is valid
    print(token['primary_email'])
    return jsonify({
        "message": "Authorized",
        "data": token
    }), 200


@bp.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
