import re
import pytesseract
from PIL import Image
import logging

# Setup logging
logging.basicConfig(
    filename='ocr_total_extraction.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        logging.info("OCR Text Extracted:\n" + text)
        return text
    except Exception as e:
        logging.error(f"Error in OCR extraction: {e}")
        return ""

def extract_total_amount(ocr_text):
    patterns = [
        r"(Total\s*(Amount)?|Grand\s*Total|Net\s*Payable|Amount\s*Due|Balance\s*Due)[^\d]{0,5}([\$₹]?\s?\d+[.,]?\d{0,2})",
        r"([\$₹]?\s?\d+[.,]?\d{0,2})\s*(Total|Amount\s*Due|Grand\s*Total)"
    ]

    matches = []
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        results = regex.findall(ocr_text)
        for result in results:
            number = result[-1]
            number = re.sub(r'[^\d.]', '', number)
            if number:
                try:
                    matches.append(float(number))
                    logging.debug(f"Match found: {result} → Parsed: {number}")
                except ValueError:
                    logging.warning(f"Invalid float conversion: {number}")

    if matches:
        likely_total = max(matches)
        logging.info(f"Extracted Total Amount: {likely_total}")
        return likely_total
    else:
        logging.warning("No total amount matched.")
        return None
