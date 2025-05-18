# Resume Skill Extractor

A web application that extracts and categorizes skills from PDF resumes using Natural Language Processing.

## Project Structure

The project is divided into two main parts:

### Backend (Flask API)

The backend is a Flask application that:
- Accepts PDF uploads
- Extracts text from the PDFs
- Processes the text to identify skills
- Categorizes the skills
- Returns the structured data as JSON

### Frontend (React)

The frontend is a React application that:
- Provides a drag-and-drop interface for PDF uploads
- Communicates with the backend API
- Displays the extracted skills in categorized accordions
- Offers a responsive and user-friendly interface

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

4. Start the backend server:
   ```
   python main.py
   ```
   The server will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The application will open in your browser at http://localhost:3000

## Features

- PDF resume upload (drag-and-drop supported)
- Skill extraction using NLP
- Categorization of skills
- Responsive design
- Error handling
- Loading indicators

## Technologies Used

- **Backend**:
  - Python
  - Flask
  - NLTK for NLP
  - PyPDF for PDF text extraction

- **Frontend**:
  - React
  - Bootstrap for styling
  - Axios for API communication

## API Endpoints

- `GET /api/health`: Health check endpoint
- `POST /api/extract-skills`: Upload and process a PDF resume