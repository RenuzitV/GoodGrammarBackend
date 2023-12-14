from flask import Blueprint, jsonify, request
from middleware.auth_middleware import token_required

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    return jsonify({
        "message": """Welcome to the backend! use the link in "test_auth" to test the authentication with JWT token""",
        "test_auth": request.path + "test_auth"
    })


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
