from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
TEMP_DIR = os.path.join(app.root_path, 'tmp')
os.makedirs(TEMP_DIR, exist_ok=True)

file_code_map = {}

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'fileToUpload' not in request.files:
        return 'No file part', 400
    file = request.files['fileToUpload']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())  # Generate a unique code
        temp_file_path = os.path.join(TEMP_DIR, file_id)
        file.save(temp_file_path)
        file_code_map[file_id] = filename
        return jsonify({'code': file_id}), 200  # Return the code in JSON format

@app.route('/download/<code>', methods=['GET'])
def download(code):
    if code in file_code_map:
        original_filename = file_code_map[code]
        file_path = os.path.join(TEMP_DIR, code)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=original_filename)
        else:
            return "File not found on server", 404
    else:
        return "Invalid download code", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8300, debug=True)