import cv2
import pytesseract
import re

# Load and preprocess the image
def __preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    return denoised

# OCR processing function
def __ocr_process(image):
    # custom_config = r'--oem 3 --psm 6'
    custom_config = ''
    text = pytesseract.image_to_string(image, config=custom_config, lang='eng+pol')
    return text

# Function to clean and standardize OCR output
def __clean_ocr_text(text):
    text = re.sub(r'[~:"]', '', text)
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'[^a-zA-Z0-9\s./]', '', text)  # Remove unwanted characters
    text = re.sub(r':', '', text) # remove colons
    text = re.sub(r'([a-zA-Z])\.', r'\1', text) # remove dots after letters
    text = re.sub(r'\s+(\.+)\s+', ' ', text) # remove single dots
    text = re.sub(r'/', '', text) # clean slashes
    text = re.sub(r'\s+[a-z]{1,2}\s+', ' ', text) # clean single or double letters
    return text

# Function to extract key fields from the text
def __extract_fields(text):
    fields = {}
    
    patterns = {
        'SURNAME': r'SURNAME\s*\w{1}?\s*([A-Z]{2,})',
        'GIVEN_NAMES': r'GIVEN \b\w+\b\s*([A-Z]+)',
        'NATIONALITY': r'.*(POLSKIE)',
        'DATE_OF_BIRTH': r'DATE OF BIRTH\s*|POLSKIE\s*(\d{1,2}\.\d{1,2}\.\d{4})',
        'IDENTITY_CARD_NUMBER': r'CARD NUMBER\s*([A-Z]{3}\s\d{6})',
        'SEX': r'.*\s+([KM]{1})\s+',
        'EXPIRY_DATE': r'EXPIRY DATE\s*(\d{1,2}\.\d{1,2}\.\d{4})'
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[field] = match.group(1)
    
    return fields

# Function to process all images in a given folder and save results
def get_data_from_document(filenames):
    results = []
    for filename in filenames:
        if 'document' in filename.lower() and filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            img = cv2.imread(filename)
            preprocessed_image = __preprocess_image(img)
            ocr_output = __ocr_process(preprocessed_image)
            cleaned_text = __clean_ocr_text(ocr_output)
            fields = __extract_fields(cleaned_text)
            fields['FILENAME'] = filename
            results.append(fields)
    return results

def get_data_from_image(image):
    preprocessed_image = __preprocess_image(image)
    ocr_output = __ocr_process(preprocessed_image)
    cleaned_text = __clean_ocr_text(ocr_output)
    fields = __extract_fields(cleaned_text)
    return fields