import os

from flask import jsonify, request
from app import stripe
from models.user_model import User
from utils.Exceptions import UserAlreadyExistsError, InternalServerError, UserNotFoundError, InvalidRequestError
import requests


def create_user_by_id_and_email(user_id, user_email):
    if User.objects(clerk_id=user_id).first():
        raise UserAlreadyExistsError("User already exists")

    try:
        created_user = User(clerk_id=user_id)
        created_user.save()
        stripe.Customer.create(
            id=user_id,
            email=user_email
        )
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


def get_user_email(user_primary_email_id):
    response = requests.get("https://api.clerk.dev/v1/email_addresses/" + user_primary_email_id,
                            headers={os.getenv("CLERK_API_KEY")}
                            )
    if response.status_code == 200:
        return response.json()["email_address"]
    else:
        raise InternalServerError("Internal Server Error")
