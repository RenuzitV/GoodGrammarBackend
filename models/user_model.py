from mongoengine import Document, StringField, EnumField, ListField
from enum import Enum


class UserType(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Document):
    clerk_id = StringField(primary_key=True)
    stripe_id = StringField(unique=True, required=True)
    user_type = EnumField(UserType, default=UserType.USER)
    user_history = ListField(StringField())
    
    def get_id(self):
        return self.id

    def get_stripe_id(self):
        return self.stripe_id
    
    def get_history(self):
        return self.user_history
