from flask import Flask, render_template, request, send_file
import os
import random
import string
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta

app = Flask(__name__)
TEMP_DIR = os.path.join(app.root_path, 'tmp')
os.makedirs(TEMP_DIR, exist_ok=True)

file_code_map = {}

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def generate_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def delete_file(code):
    file_path = os.path.join(TEMP_DIR, code)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    if code in file_code_map:
        del file_code_map[code]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    response_html = ""
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            response_html += "<p>No selected file</p>"
            continue
        if file:
            filename = secure_filename(file.filename)
            file_code = generate_code()
            while file_code in file_code_map:  # Ensure uniqueness
                file_code = generate_code()
            temp_file_path = os.path.join(TEMP_DIR, file_code)
            file.save(temp_file_path)
            file_code_map[file_code] = filename
            response_html += f"File uploaded.<br>Download code: {file_code}<br>5 hours till deletion"

            # Schedule file deletion after 5 hours
            scheduler.add_job(delete_file, trigger=IntervalTrigger(hours=5), args=[file_code])
    return response_html if response_html else "<p>Failed to upload files</p>", 200

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

if __name__ == "__main__":
    app.run()
