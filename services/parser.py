import pdfplumber
import pytesseract
from PIL import Image
import io
import os
import shutil

# Cross-platform Tesseract path (Linux deployment vs Windows local)
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ''
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text and page_text.strip():
                text += page_text + '\n'
            else:
                page_image = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(page_image)
                text += ocr_text + '\n'
    return clean_text(text)

def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return clean_text(text)

def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if len(line) > 3:
            cleaned.append(line)
    return '\n'.join(cleaned)

def parse_uploaded_file(file_bytes: bytes, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_bytes)
    elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
        return extract_text_from_image(file_bytes)
    elif ext == '.txt':
        return clean_text(file_bytes.decode('utf-8'))
    else:
        raise ValueError(f'Unsupported file type: {ext}')
