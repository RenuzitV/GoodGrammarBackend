"""
defines the models for the database
TBD
"""
from enum import Enum


class UserType(Enum):
    USER = 1
    ADMIN = 2


class User:
    def __init__(self, id):
        self.id = id
        self.user_type = UserType.USER

    def get_id(self):
        return self.id