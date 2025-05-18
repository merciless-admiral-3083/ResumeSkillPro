import nltk
import re
import logging
import os
import tempfile
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from skills_data import SKILLS_LIST
from pypdf import PdfReader

# Configure logging
logger = logging.getLogger(__name__)

# Initialize NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PdfReader(file)
            
            # Get the total number of pages
            num_pages = len(pdf_reader.pages)
            
            # Initialize empty text string
            text = ""
            
            # Extract text from each page
            for page_num in range(num_pages):
                # Get the page
                page = pdf_reader.pages[page_num]
                
                # Extract text
                page_text = page.extract_text()
                
                # Add to the total text
                if page_text:
                    text += page_text + "\n"
            
            if not text.strip():
                logger.warning("PDF text extraction yielded empty result")
                
            return text
    except Exception as e:
        logger.exception(f"Error extracting text from PDF: {e}")
        raise

def preprocess_text(text):
    """
    Preprocess the extracted text by removing special characters,
    converting to lowercase, and tokenizing.
    
    Args:
        text (str): Text extracted from PDF
        
    Returns:
        list: List of processed tokens
    """
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens

def identify_skills(tokens, sentences):
    """
    Identify skills from the processed tokens and original sentences.
    
    Args:
        tokens (list): List of processed tokens
        sentences (list): List of sentences from the original text
        
    Returns:
        list: List of identified skills
    """
    identified_skills = set()
    
    # Check for single-word skills
    for token in tokens:
        if token in SKILLS_LIST and len(token) > 1:  # Avoid single-character matches
            identified_skills.add(token)
    
    # Check for multi-word skills
    for skill in SKILLS_LIST:
        if ' ' in skill and skill.lower() in ' '.join(tokens).lower():
            identified_skills.add(skill)
    
    # Check sentences for skills that might contain special characters
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for skill in SKILLS_LIST:
            # Look for skills with word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, sentence_lower):
                identified_skills.add(skill)
    
    return sorted(list(identified_skills))

def categorize_skills(skills):
    """
    Categorize skills into different categories.
    
    Args:
        skills (list): List of identified skills
        
    Returns:
        dict: Dictionary with skills categorized
    """
    # Define categories and their associated keywords
    categories = {
        'Programming Languages': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'typescript', 'go', 'kotlin', 'swift'],
        'Web Development': ['html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'wordpress', 'bootstrap'],
        'Data Science': ['machine learning', 'deep learning', 'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'firebase', 'redis', 'nosql', 'sqlite'],
        'DevOps': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'aws', 'azure', 'gcp', 'terraform', 'ansible'],
        'Other': []
    }
    
    categorized_skills = {category: [] for category in categories}
    
    for skill in skills:
        skill_lower = skill.lower()
        categorized = False
        
        for category, keywords in categories.items():
            if category == 'Other':
                continue
                
            for keyword in keywords:
                if keyword in skill_lower or skill_lower in keyword:
                    categorized_skills[category].append(skill)
                    categorized = True
                    break
            
            if categorized:
                break
        
        if not categorized:
            categorized_skills['Other'].append(skill)
    
    # Remove empty categories
    return {k: v for k, v in categorized_skills.items() if v}

def custom_sentence_tokenize(text):
    """
    A simple custom sentence tokenizer as fallback when NLTK's sent_tokenize fails.
    
    Args:
        text (str): Text to tokenize into sentences
        
    Returns:
        list: List of sentences
    """
    # Basic sentence splitting by common sentence terminators
    # This is a simplified approach and won't handle all cases perfectly
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_skills_from_pdf(pdf_path):
    """
    Main function to extract skills from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary with extracted skills categorized
    """
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if not text.strip():
            # If no text was extracted, return a message
            return {"Error": ["No text could be extracted from the PDF. Please check the file and try again."]}
        
        # Break text into sentences using a try-except block
        try:
            # Try using NLTK's sentence tokenizer
            sentences = sent_tokenize(text)
        except Exception as e:
            logger.warning(f"NLTK sentence tokenization failed: {e}")
            # Fallback to our custom sentence tokenizer
            sentences = custom_sentence_tokenize(text)
        
        # Preprocess the text
        tokens = preprocess_text(text)
        
        # Identify skills
        skills = identify_skills(tokens, sentences)
        
        if not skills:
            # If no skills were identified, return a message
            return {"Notice": ["No skills were identified in this resume. Try a different file or ensure the resume contains relevant skills."]}
        
        # Categorize skills
        categorized_skills = categorize_skills(skills)
        
        return categorized_skills
    except Exception as e:
        logger.exception(f"Error extracting skills from PDF: {e}")
        # Return error message as a categorized skill for better UX
        return {"Error": [f"An error occurred while processing your resume: {str(e)}"]}