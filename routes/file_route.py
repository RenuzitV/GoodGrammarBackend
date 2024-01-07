from flask import Blueprint, request, jsonify

import docx

bp = Blueprint('file', __name__)

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'doc', 'docx'}

API_URL = "https://polite-horribly-cub.ngrok-free.app/generate_code"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/get_content', methods=['POST'])
def get_file_content():
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')

        return jsonify({'error': 'No file attached'}), 500
    
    # Get the file
    file = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        print('No selected file')

        return jsonify({'respone': 'No selected file'}), 500
    
    # If file valid and is allowed
    if file and allowed_file(file.filename):
        doc = docx.Document(file)

        fulltext = []

        for para in doc.paragraphs:
            fulltext.append(para.text)
            
        return jsonify({'respone': '\n'.join(fulltext)})