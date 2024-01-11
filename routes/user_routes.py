from flask import Blueprint, request, jsonify, abort

from middleware.clerk_middleware import token_required
from services import user_service
from utils.exceptions import UserNotFoundError
from utils.token_utils import get_user_id

bp = Blueprint('user', __name__)


# @bp.route('/', methods=['POST'])
# def create_user():
#     return user_service.create_user()

@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_service.get_user(user_id)
        return user.to_json()
    except UserNotFoundError as e:
        print("could not get user", user_id)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    users_dict = [user.to_mongo().to_dict() for user in users]
    return jsonify(users_dict)


# @bp.route('/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     return user_service.delete_user(user_id)
