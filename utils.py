from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_pdf(file_path):
    return extract_text(file_path)

def extract_text_scanned_pdf(file_path):
    images = convert_from_path(file_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_image(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)

def extract_resume_text(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        text = extract_text_pdf(file_path)
        if len(text.strip()) < 100:  # Likely scanned
            return extract_text_scanned_pdf(file_path)
        return text
    elif ext in ['doc', 'docx']:
        return extract_text_docx(file_path)
    elif ext in ['jpg', 'jpeg', 'png']:
        return extract_text_image(file_path)
    else:
        raise ValueError("Unsupported file format")

def get_match_score(jd, resume):
    jd_emb = model.encode(jd, convert_to_tensor=True)
    resume_emb = model.encode(resume, convert_to_tensor=True)
    return util.cos_sim(jd_emb, resume_emb).item()
