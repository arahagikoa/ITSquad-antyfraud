import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
import os
from langdetect import detect

# Language mapping for Tesseract
LANG_MAPPING = {
    "af": "afr", "ar": "ara", "bg": "bul", "bn": "ben", "ca": "cat", "cs": "ces", "cy": "cym", "da": "dan",
    "de": "deu", "el": "ell", "en": "eng", "es": "spa", "et": "est", "fa": "fas", "fi": "fin", "fr": "fra",
    "gu": "guj", "he": "heb", "hi": "hin", "hr": "hrv", "hu": "hun", "id": "ind", "it": "ita", "ja": "jpn",
    "kn": "kan", "ko": "kor", "lt": "lit", "lv": "lav", "mk": "mkd", "ml": "mal", "mr": "mar", "ne": "nep",
    "nl": "nld", "no": "nor", "pa": "pan", "pl": "pol", "pt": "por", "ro": "ron", "ru": "rus", "sk": "slk",
    "sl": "slv", "sq": "sqi", "sv": "swe", "sw": "swa", "ta": "tam", "te": "tel", "th": "tha",
    "tl": "tgl", "tr": "tur", "uk": "ukr", "ur": "urd", "vi": "vie", "zh-cn": "chi_sim", "zh-tw": "chi_tra"
}

def detect_language(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        detected_lang = detect(text)
        tesseract_lang = LANG_MAPPING.get(detected_lang, "eng")  # Default to English if not found
        return tesseract_lang
    except Exception as e:
        print(f"Error detecting language: {e}")
        return 'eng'  # Fallback to English

def resize_image(image):
    if image.size[0] < 1000 and image.size[1] < 640:
        return image.resize((int(image.size[0] * 3), int(image.size[1] * 3)), Image.LANCZOS)
    else:
        return image

def preprocess_image_for_ocr(image_path, output_path):
    image = Image.open(image_path)

    # Resize the image
    image = resize_image(image)
    
    # Convert the resized image to a format suitable for OpenCV
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction using Non-Local Means Denoising
    gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    
    # Adaptive thresholding
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Morphological operations
    kernel = np.ones((2, 2), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    # Image sharpening
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    gray = cv2.filter2D(gray, -1, sharpen_kernel)

    # Contrast enhancement
    pil_image = Image.fromarray(gray)
    enhancer = ImageEnhance.Contrast(pil_image)
    gray = np.array(enhancer.enhance(2))
    print(output_path)
    # Save the preprocessed image
    #Image.fromarray(gray).save(output_path)
    cv2.imwrite(output_path, gray)

def perform_ocr_on_preprocessed_images(preprocessed_dir, lang='eng'):
    preprocessed_images = [f for f in os.listdir(preprocessed_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', 'webp'))]
    all_text = []
    for image_name in preprocessed_images:
        image_path = os.path.join(preprocessed_dir, image_name)
        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
        print(f"OCR result for {image_name}:")
        print(text)
        print("-" * 50)
        all_text.append(
            {image_name:text}
        )
    
    return all_text

# Set directories
#image_dir = r'E:\Projekty\for_work\text-extraction\text_extraction\extracted_info'
#preprocessed_dir = r'E:\Projekty\for_work\text-extraction\text_extraction\preprocessed'

# Create preprocessed directory if it doesn't exist
#os.makedirs(preprocessed_dir, exist_ok=True)

# Preprocess images and save them to the preprocessed directory
#image_paths = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', 'webp'))]

#for image_path in image_paths:
#    full_path = os.path.join(image_dir, image_path)
#    preprocessed_image_path = os.path.join(preprocessed_dir, f'preprocessed_{image_path}')
#    preprocess_image_for_ocr(full_path, preprocessed_image_path)

# Perform OCR on preprocessed images
#perform_ocr_on_preprocessed_images(preprocessed_dir, lang='pol')