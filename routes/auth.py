from flask import Flask, Blueprint, jsonify
from middleware.auth_middleware import token_required
# from models.user_model import User

bp = Blueprint('auth', __name__)

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


# @bp.route('/user/create_user', methods=['POST'])
# def create_user():
#     return User().create_user()
#
#
# @bp.route('/user/get_user/<user_id>', methods=['GET'])
# def get_user(user_id):
#     return User().get_user(user_id)
#
#
# @bp.route('/user/delete_user/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     return User().delete_user(user_id)