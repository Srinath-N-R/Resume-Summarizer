import os
import fitz  # PyMuPDF
from docx import Document
from werkzeug.utils import secure_filename

def handle_file_upload(file, upload_folder):
    """Save the uploaded file and return its filename and full file path."""
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filename, filepath

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "".join([page.get_text() for page in doc])
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX using python-docx."""
    doc = Document(docx_path)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)
