import traceback
from models.file_model import FileObject

def save_file(filename="", encodedBinFile=None):
    try:
        if FileObject.objects(file_name=filename).first():
            print("File already exist")

        newFile = FileObject(file_name=filename, file=encodedBinFile)
        newFile.save()

        return newFile
    
    except Exception as e:
        print("Failed to save File:", e)
        traceback.print_exc()