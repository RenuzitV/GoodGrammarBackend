from flask import Blueprint, request, jsonify, send_file

import docx
import requests
import io
from bson.binary import Binary
from werkzeug.utils import secure_filename
from services.file_service import save_file
from models.file_model import FileObject

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

        return jsonify({'error': 'No selected file'}), 500

    # If file valid and is allowed
    if file and allowed_file(file.filename):
        doc = docx.Document(file)

        fulltext = []

        for para in doc.paragraphs:
            fulltext.append(para.text)

        return jsonify({'response': '\n'.join(fulltext)})
    
@bp.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')

            return jsonify({'error': 'No file attached'})
        
        file = request.files['file']

        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            print('No selected file')

            return jsonify({'error': 'No selected file'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            resultDoc = docx.Document(file)

            paragraphs = resultDoc.paragraphs

            # Ieterate through each paragraph
            for i in range(0, len(paragraphs)):
                para = paragraphs[i]

                # Skip the reference
                if is_heading(para) and para.text.lower() == "references":
                    print("Found")
                    break

                # If the current paragraph is not heading and not a blank
                if not is_heading(para) and para.text != "":
                    # Iterate through each run of the paragraph
                    for row in para.runs:
                        # Store the content of the run
                        content = row.text 

                        # Removing all its content.
                        # Run-level formatting, such as style, is preserved.
                        row.clear()

                        # Split the whole paragraph tosentences
                        if content.find(".") != -1:
                            sentences = splitKeepDelimiter(content, ".")

                            # Store small paragraphs have maximum 128 words
                            splitted_paragraphs = []

                            # Store the current paragraph for splitting
                            cur_para = ""

                            # Iterate through each sentences int the paragraph
                            for sentence in sentences:
                                if (sentence == ""):
                                    continue

                                # Check if the length after adding sentence to paragraph is grater than 128 words or not
                                if (len(cur_para.split()) + len(sentence.split()) ) > 128:
                                    # If larger add current paragraph to list
                                    splitted_paragraphs.append(cur_para)

                                    # Reset the current paragraph to the current sentence
                                    cur_para = sentence

                                else:
                                    cur_para += sentence
                        
                            # Finish iteration and the current paragraph is not empty
                            if cur_para:
                                # Add the current paragrpah to the list
                                splitted_paragraphs.append(cur_para)

                            for splitted_para in splitted_paragraphs:
                                # call_API(splitted_para)

                                row.text = ''.join(splitted_para)
                        
                        else:
                            row.text = content

            # Save the edited document to mongodb
            binaryStream1 = io.BytesIO()

            resultDoc.save(binaryStream1)

            binaryStream1.seek(0)

            encoded = Binary(binaryStream1.read())

            myDoc = save_file(filename=filename.split(".")[0] + "(edited).docx", encodedBinFile=encoded)

    return jsonify(
        {
            'edited_file_id': str(myDoc.id)
        }
    )

@bp.route('/get_file_info', methods=['GET'])
def get_file_info():
    fileId = request.args.get('file_id')

    result = FileObject.objects(pk=fileId).first()

    gotFile = result["file"]

    binaryStream2 = io.BytesIO(gotFile)

    myDocument = docx.Document(binaryStream2)

    fulltext = []

    for para in myDocument.paragraphs:
        fulltext.append(para.text)

    return jsonify(
        {
            'file_name': str(result["file_name"]),
            'create_at': str(result["created_at"]),
            'content': '\n'.join(fulltext)
        }
    )


@bp.route('/get_file', methods=['GET'])
def get_file():
    fileId = request.args.get('file_id')

    result = FileObject.objects(pk=fileId).first()

    gotFile = result["file"]

    binaryStream2 = io.BytesIO(gotFile)

    myDocument = docx.Document(binaryStream2)

    f = io.BytesIO()
    myDocument.save(f)
    f.seek(0)

    filename = str(result["file_name"])

    return send_file(
        f, 
        as_attachment=True,
        download_name=filename,
        )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def call_API(text):
    print(str(len(text.split())) + "Before: " + text)

    prompts = []

    result = ""

    # for sentence in splitKeepDelimiter(text, "."):
    #     prompts.append("Correct English: " + sentence + "Here is the corrected version")

    prompts.append("Correct English and do not additional text: " + text + "Here is the corrected version:")

    param = []

    param += [("max_length", 128)]

    param += [("prompts", prompt) for prompt in prompts]

    response = requests.get(API_URL, params=param)

    # print(param)

    if response.status_code == 200:
        generated_code_list = response.json()
        for i, code in enumerate(generated_code_list):

            print("After: " + transform_result(text, code) + "\n\n")
            # result += code

            # return jsonify({'respone': response.json()})
    else:
        print("Failed to retrieve code. Status code:", response.status_code)

def transform_result(s1, s2):
    result_str = ""

    if s1[0] == ' ':
        result_str = ' '

        if s1[1].islower():
            result_str += s2[0].lower() + s2[1:]
        
        else:
            result_str += s2[0].upper() + s2[1:]
    
    else:
        if s1[0].islower():
            result_str = s2[0].lower() + s2[1:]
        
        else:
            result_str = s2[0].upper() + s2[1:]

    if s1.endswith(' ') and s2.endswith('.') :
        result_str = result_str.rstrip('.')
        result_str += ' '

    return result_str

def is_heading(paragraph):
    """Checks if a paragraph is a heading.

    :param paragraph:
    :return:
    """
    if paragraph.style.name.startswith('Heading'):
        return True
    
def splitKeepDelimiter(s, delimiter):
    split = s.split(delimiter)

    return [substr + delimiter for substr in split[:-1]] + [split[-1]]