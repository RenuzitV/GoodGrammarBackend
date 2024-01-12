from mongoengine import Document, StringField, BinaryField

class FileObject(Document):
    file_name = StringField(required=True)
    file = BinaryField()

    def get_file_name(self):
        return self.file_name
    
    def get_file(self):
        return self.file

