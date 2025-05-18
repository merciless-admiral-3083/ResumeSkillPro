import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from skill_extractor import extract_skills_from_pdf
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Configure upload settings
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills():
    """API endpoint to extract skills from an uploaded PDF resume"""
    # Check if the post request has the file part
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submits an empty part without filename
    if file.filename == '':
        logger.error("No file selected")
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create a temporary file to store the uploaded PDF
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                file.save(temp.name)
                # Extract skills from the PDF
                skills = extract_skills_from_pdf(temp.name)
                
                # Remove the temporary file
                os.unlink(temp.name)
                
                # Return the extracted skills
                return jsonify({
                    'success': True,
                    'skills': skills
                })
        except Exception as e:
            logger.exception("Error processing file")
            return jsonify({'error': str(e)}), 500
    else:
        logger.error("File type not allowed")
        return jsonify({'error': 'File type not allowed. Please upload a PDF file.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)