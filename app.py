import os
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from skill_extractor import extract_skills_from_pdf
import tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills():
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logger.error("No file selected")
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                file.save(temp.name)
                temp_path = temp.name  

            skills = extract_skills_from_pdf(temp_path)

            os.unlink(temp_path)

            return jsonify({
                'success': True,
                'skills': skills
            })
        except Exception as e:
            logger.exception("Error processing file")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
