"""
defines the models for the database
TBD
"""

from flask import Flask, jsonify, request
from app import db


class User:
    def signup(self):
        #Create a new user based on the form
        user = {
            "_id": "2",
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        #Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400
        
        #Insert the user to database
        if db.users.insert_one(user):
            return jsonify(user),200

        return jsonify({"error": "Sign up failed"}), 400