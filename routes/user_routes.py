import os

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, abort

from middleware.clerk_middleware import token_required
from services import user_service, stripe_service
from utils.exceptions import UserNotFoundError, NoActiveSubscriptionError
from utils.token_utils import get_user_id

bp = Blueprint('user', __name__)

load_dotenv()


# @bp.route('/', methods=['POST'])
# def create_user():
#     return user_service.create_user()

@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_service.get_user(user_id)
        return user.to_json(), 200
    except UserNotFoundError as e:
        print("could not get user", user_id)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('', methods=['GET'])
def get_all_users():
    if os.getenv("ENVIRONMENT") == "production":
        print("Cannot get all users in production")
        abort(403, "Forbidden")

    users = user_service.get_all_users()
    users_dict = [user.to_mongo().to_dict() for user in users]
    return jsonify(users_dict), 200


@bp.route('get_subscription_tier', methods=['GET'])
@token_required
def get_user_subscription_tier(token):

    user_id = get_user_id(token)

    try:
        tier = stripe_service.get_subscription_details(user_id)

        return jsonify(tier), 200

    except UserNotFoundError as e:
        print("could not get user", user_id)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('history', methods=['POST'])
@token_required
def add_file(token):
    userId = ""
    data = request.get_json()
    fileId = data.get("fileId")
    try:
        userId = get_user_id(token)
        user_service.add_file_to_history(userId, fileId)
        return jsonify({
            "status": "ok",
            "fileId": fileId,
        }), 200
    except UserNotFoundError as e:
        print("could not get user", userId)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('history', methods=['GET'])
@token_required
def get_files(token):
    try:
        userId = get_user_id(token)
        history = user_service.get_history(userId)
        return history, 200
    except UserNotFoundError as e:
        print("could not get user", userId)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('history/<file_id>', methods=['DELETE'])
@token_required
def delete_file(token, file_id):
    try:
        userId = get_user_id(token)
        user_service.delete_file_from_history(userId, file_id)
        return jsonify({
            "status":"ok",
            "fileId":file_id,
        }), 200
    except UserNotFoundError as e:
        print("could not get user", userId)
        print("Error: ", e)
        abort(404, "User not found")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")
