from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import os

# Load the sentence transformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_pdf(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_scanned_pdf(file_path):
    try:
        images = convert_from_path(file_path)
        return ''.join([pytesseract.image_to_string(img) for img in images])
    except Exception as e:
        print(f"Error extracting text from scanned PDF: {e}")
        return ""

def extract_text_docx(file_path):
    try:
        doc = Document(file_path)
        return '\n'.join(para.text for para in doc.paragraphs)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_image(file_path):
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def extract_resume_text(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        text = extract_text_pdf(file_path)
        if len(text.strip()) < 100:
            return extract_text_scanned_pdf(file_path)
        return text
    elif ext in ['doc', 'docx']:
        return extract_text_docx(file_path)
    elif ext in ['jpg', 'jpeg', 'png']:
        return extract_text_image(file_path)
    else:
        raise ValueError("Unsupported file format: " + ext)

def get_match_score(jd, resume):
    if not jd.strip() or not resume.strip():
        return 0.0
    jd_emb = model.encode(jd, convert_to_tensor=True)
    resume_emb = model.encode(resume, convert_to_tensor=True)
    return util.cos_sim(jd_emb, resume_emb).item() * 100  # Return as percentage
