from flask import Blueprint, request, jsonify

from services import user_service
from utils.Exceptions import UserNotFoundError

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
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    users_dict = [user.to_mongo().to_dict() for user in users]
    return jsonify(users_dict)

# @bp.route('/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     return user_service.delete_user(user_id)
