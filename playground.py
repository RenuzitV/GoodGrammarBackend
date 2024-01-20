from database import db
from models.file_model import FileObject
from models.user_model import User

db.initialize_db()

users = User.objects()

for user in users:
    user.get_history().update
    user.save()
