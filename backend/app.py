import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from skill_extractor import extract_skills_from_pdf
import tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills_endpoint():
    """API endpoint to extract skills from an uploaded PDF resume"""
    if 'file' not in request.files:
        logger.error("No file part in the request found")
        return jsonify({'error': 'No file part found'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error("No file selected")
        return jsonify({'error': 'No file selected, select one!'}), 400

    if file and allowed_file(file.filename):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                file.save(temp.name)
                skills = extract_skills_from_pdf(temp.name)
            os.unlink(temp.name)

            return jsonify({
                'success': True,
                'skills': skills
            })
        except Exception as e:
            logger.exception("Error processing file")
            return jsonify({'error': str(e)}), 500
    else:
        logger.error("File type not allowed, upload other type of file please")
        return jsonify({'error': 'File type not allowed. Please upload a PDF file for the assessment.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
