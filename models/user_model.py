"""
defines the models for the database
TBD
"""
import uuid
from datetime import datetime

class User:
    def __init__(self, email):
        self.id = uuid.uuid4().hex
        self.email = email
        self.date_created = datetime.utcnow()
        self.subscription = False
        self.is_user = True