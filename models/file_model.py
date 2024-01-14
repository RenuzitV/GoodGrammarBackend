import datetime
from mongoengine import Document, StringField, BinaryField, DateTimeField

class FileObject(Document):
    file_name = StringField(required=True)
    file = BinaryField()
    created_at = DateTimeField(required=True, default=datetime.datetime.now)

    def get_file_name(self):
        return self.file_name
    
    def get_file(self):
        return self.file

    def get_create_at(self):
        return self.created_at
