from database import db
from models.file_model import FileObject

db.initialize_db()

print(FileObject.objects().first().deleted)

FileObject.objects(deleted__exists=False).update(set__deleted=False)
