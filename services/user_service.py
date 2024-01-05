import uuid

from flask import Flask, jsonify, request
from models.user_model import User
from database.db import db
from utils.Exceptions import UserAlreadyExistsError, InternalServerError


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
    user = User(uuid.UUID.hex)

    # Check for existing email address
    if db.users.find_one({"id": user.get_id()}):
        return jsonify({"error": "id address already in use"}), 400

    # Insert the user to database
    if db.users.insert_one(user):
        return jsonify(user), 200

    return jsonify({"error": "Sign up failed"}), 400


def get_user(user_id):
    # Create a new user based on the form
    user_result = db.users.find_one({"_id": user_id})
    if user_result:
        return jsonify(user_result), 200
    else:
        return jsonify({"error": "User not found"}), 400


def delete_user(user_id):
    # Create a new user based on the form
    user_result = db.users.find_one({"_ids": user_id})
    if user_result:
        try:
            db.users.delete_one({"_id": user_id})
        except Exception as e:
            return jsonify({"error": f"Cannot delete the user with id {user_id} "}), 400
        return jsonify(f"User with id {user_id} deleted"), 200
    else:
        return jsonify({"error": "User not found"}), 400
