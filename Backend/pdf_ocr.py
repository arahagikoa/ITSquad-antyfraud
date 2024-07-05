import pytesseract
from PIL import Image
import os
from langdetect import detect

# Mapping of langdetect language codes to Tesseract language codes
LANG_MAPPING = {
    "af": "afr", "ar": "ara", "bg": "bul", "bn": "ben", "ca": "cat", "cs": "ces", "cy": "cym", "da": "dan",
    "de": "deu", "el": "ell", "en": "eng", "es": "spa", "et": "est", "fa": "fas", "fi": "fin", "fr": "fra",
    "gu": "guj", "he": "heb", "hi": "hin", "hr": "hrv", "hu": "hun", "id": "ind", "it": "ita", "ja": "jpn",
    "kn": "kan", "ko": "kor", "lt": "lit", "lv": "lav", "mk": "mkd", "ml": "mal", "mr": "mar", "ne": "nep",
    "nl": "nld", "no": "nor", "pa": "pan", "pl": "pol", "pt": "por", "ro": "ron", "ru": "rus", "sk": "slk",
    "sl": "slv", "so": "som", "sq": "sqi", "sv": "swe", "sw": "swa", "ta": "tam", "te": "tel", "th": "tha",
    "tl": "tgl", "tr": "tur", "uk": "ukr", "ur": "urd", "vi": "vie", "zh-cn": "chi_sim", "zh-tw": "chi_tra"
}

def detect_language(images):
    for image in images:
        text = pytesseract.image_to_string(image)
        try:
            detected_lang = detect(text)
            tesseract_lang = LANG_MAPPING.get(detected_lang, "eng")  # Default to English if not found
            return tesseract_lang
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'eng'  # Fallback to English

def extract_text_from_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    language = detect_language(images)
    extracted_text = []
    
    for image in images:
        try:
            text = pytesseract.image_to_string(image, lang=language)
            extracted_text.append(text)
        except pytesseract.TesseractError as e:
            print(f"TesseractError: {e}. Falling back to English.")
            try:
                text = pytesseract.image_to_string(image, lang="eng")
                extracted_text.append(text)
            except pytesseract.TesseractError as fallback_e:
                print(f"Failed to process image even with fallback language: {fallback_e}")
                extracted_text.append('')  # Add an empty string for failed OCR attempts

    return extracted_text

input_dir = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\CNN\dataset\train\paszportObcy"

if os.path.exists(input_dir):
    image_paths = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir)]
else:
    print("Provided path is incorrect")
    image_paths = []

texts = []

for image_path in image_paths:
    text = extract_text_from_images([image_path])  # Pass as a list
    if isinstance(text, list):
        text = "\n".join(text)
    texts.append(text)

print(texts)

with open("file.txt", "w", encoding='UTF-8') as file:
    to_write = "\n".join(texts)
    file.write(to_write)
