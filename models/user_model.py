from mongoengine import Document, StringField, EnumField
from enum import Enum


class UserType(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Document):
    clerk_id = StringField(primary_key=True)
    stripe_id = StringField(unique=True)
    user_type = EnumField(UserType, default=UserType.USER)

    def get_id(self):
        return self.id

    def get_stripe_id(self):
        return self.stripe_id
