import pdfplumber, pytesseract
from PIL import Image
import whisper

def extract_text_and_metadata(file_path):
    if file_path.lower().endswith('.pdf'):
        return process_pdf(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return process_image(file_path)
    elif file_path.endswith((".mp3", ".wav", ".m4a")):
        return process_audio(file_path) 
    else:
        return "", {"error": "Unsupported file type"}
    
def process_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return clean_text(text), {"file_type": "pdf"}
    
def process_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return clean_text(text), {"file_type": "image"}

def process_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return clean_text(result["text"]), {"file_type": "audio"}

def clean_text(text):
    return " ".join(text.split())