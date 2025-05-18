import fitz  # PyMuPDF
import nltk
import re
import logging
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from skills_data import SKILLS_LIST

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
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
            
        doc.close()
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
        
        # Break text into sentences
        sentences = sent_tokenize(text)
        
        # Preprocess the text
        tokens = preprocess_text(text)
        
        # Identify skills
        skills = identify_skills(tokens, sentences)
        
        # Categorize skills
        categorized_skills = categorize_skills(skills)
        
        return categorized_skills
    except Exception as e:
        logger.exception(f"Error extracting skills from PDF: {e}")
        raise
