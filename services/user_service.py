import os
import traceback

from flask import jsonify, request
import stripe
from models.user_model import User
from models.file_model import FileObject
from utils.exceptions import UserAlreadyExistsError, InternalServerError, UserNotFoundError, InvalidRequestError
import requests


def create_user(user_id=None, user_email="", user_name=""):
    if not user_id:
        raise InvalidRequestError("clerk_id is required")

    try:
        if User.objects(clerk_id=user_id).first():
            print("User already exists in MongoDB")
            raise UserAlreadyExistsError("User already exists")

        customer = stripe.Customer.create(
            email=user_email,
            name=user_name
        )

        created_user = User(clerk_id=user_id, stripe_id=customer.id)
        created_user.save()

        return created_user
    except UserAlreadyExistsError:
        raise UserAlreadyExistsError("User already exists")
    except Exception as e:
        print("Failed to create user:", e)
        traceback.print_exc()
        raise InternalServerError("Internal Server Error")


def get_user(user_id):
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
        try:
            stripe.Customer.delete(deleted_user.stripe_id)
        except Exception as e:
            print("Failed to delete user from Stripe:", e)
            raise InternalServerError("Internal Server Error")

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
    response = requests.get("https://api.clerk.com/v1/email_addresses/" + user_primary_email_id,
                            headers={
                                "Authorization": "Bearer " + os.getenv("CLERK_API_KEY")
                            }
                            )
    if response.status_code == 200:
        return response.json()["email_address"]
    elif response.status_code == 404:
        raise UserNotFoundError("User not found")
    else:
        print(response.status_code)
        print(response.json())
        raise InternalServerError("Internal Server Error")


def get_all_users():
    return User.objects()


def add_file_to_history(user_id, file_id):
    user = User.objects(clerk_id=user_id).first()
    if user:
        user.user_history.append(file_id)
        user.save()
        return user
    else:
        raise UserNotFoundError("User not found")


def get_history(user_id):
    user = User.objects(clerk_id=user_id).first()

    if user:
        detailed_history = []
        fileId_history = user.get_history()
        for fileId in fileId_history:
            result = FileObject.objects(pk=fileId).first()
            detailed_history.append({
                'file_id': fileId,
                'file_name': str(result["file_name"]),
                'create_at': str(result["created_at"]),
            })

        return detailed_history
    else:
        raise UserNotFoundError("User not found")


def delete_file_from_history(user_id, file_id):
    user = User.objects(clerk_id=user_id).first()
    if user:
        user.user_history.remove(file_id)
        user.save()
        return user
    else:
        raise UserNotFoundError("User not found")


# def create_user():
#     # Create a new user based on the form
#     if not request.is_json:
#         raise InvalidRequestError("Request is not JSON")
#
#     clerk_id = request.json.get("clerk_id", None)
#     if not clerk_id:
#         raise InvalidRequestError("clerk_id is required")
#
#     if User.objects(clerk_id=clerk_id).first():
#         raise UserAlreadyExistsError("User already exists")
#
#     try:
#         created_user = User(clerk_id=clerk_id)
#         created_user.save()
#         return created_user
#     except Exception as e:
#         print("Failed to create user:", e)
#         raise InternalServerError("Internal Server Error")
def get_user_by_stripe_id(customer_id):
    user = User.objects(stripe_id=customer_id).first()
    if user:
        return user
    else:
        raise UserNotFoundError("User not found")
