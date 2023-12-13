# """
# defines the models for the database
# TBD
# """
#
# from flask import Flask, jsonify, request
# from app import db
# import uuid
# from datetime import datetime
#
# class User:
#     def create_user(self):
#         #Create a new user based on the form
#         user = {
#             "_id": uuid.uuid4().hex, # change later for clerk
#             "email": request.form.get("email"),
#             "date_created": datetime.utcnow(),
#             "subscription": False,
#             "is_user": True
#         }
#
#         #Check for existing email address
#         if db.users.find_one({"email": user['email']}):
#             return jsonify({"error": "Email address already in use"}), 400
#
#         #Insert the user to database
#         if db.users.insert_one(user):
#             return jsonify(user),200
#
#         return jsonify({"error": "Sign up failed"}), 400
#
#     def get_user(self, id):
#         #Create a new user based on the form
#         user_result = db.users.find_one({"_id": id})
#         if user_result:
#             print(user_result.get("email"))
#             print(user_result.get("date_created"))
#             print(user_result.get("is_user"))
#             print(user_result.get("password"))
#             print(user_result.get("subscription"))
#             return jsonify(user_result),200
#         else:
#             return jsonify({"error": "User not found"}), 400
#
#     def delete_user(self, id):
#         #Create a new user based on the form
#         user_result = db.users.find_one({"_ids": id})
#         if user_result:
#             try:
#                 db.users.delete_one({"_id": id})
#             except:
#                 return jsonify({"error": f"Cannot delete the user with id {id} "}), 400
#             return jsonify(f"User with id {id} deleted"),200
#         else:
#             return jsonify({"error": "User not found"}), 400