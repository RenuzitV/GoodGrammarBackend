from flask import jsonify, request

from models.user_model import User
from utils.Exceptions import UserAlreadyExistsError, InternalServerError, UserNotFoundError, InvalidRequestError


def create_user_by_id(user_id):
    if User.objects(clerk_id=user_id).first():
        raise UserAlreadyExistsError("User already exists")

    try:
        created_user = User(clerk_id=user_id)
        created_user.save()
        return created_user
    except Exception as e:
        print("Failed to create user:", e)
        raise InternalServerError("Internal Server Error")


def create_user():
    # Create a new user based on the form
    if not request.is_json:
        raise InvalidRequestError("Request is not JSON")

    clerk_id = request.json.get("clerk_id", None)
    if not clerk_id:
        raise InvalidRequestError("clerk_id is required")

    if User.objects(clerk_id=clerk_id).first():
        raise UserAlreadyExistsError("User already exists")

    try:
        created_user = User(clerk_id=clerk_id)
        created_user.save()
        return created_user
    except Exception as e:
        print("Failed to create user:", e)
        raise InternalServerError("Internal Server Error")


def get_user(user_id):
    # Create a new user based on the form
    user = User.objects(clerk_id=user_id).first()
    if user:
        return user
    else:
        raise UserNotFoundError("User not found")


def delete_user(user_id):
    # Create a new user based on the form
    if not user_id:
        raise InvalidRequestError("user_id is required")

    deleted_user = User.objects(clerk_id=user_id).first()
    if deleted_user:
        deleted_user.delete()
        return deleted_user
    else:
        raise UserNotFoundError("User not found")


def update_user(user_id):
    # Create a new user based on the form
    if not request.is_json:
        raise InvalidRequestError("Request is not JSON")

    user = User.objects(clerk_id=user_id).first()
    if user:
        print("received update request on an existing user, but this function is not implemented yet.")
        return user
    else:
        raise UserNotFoundError("User not found")