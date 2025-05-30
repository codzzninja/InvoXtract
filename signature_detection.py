import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)
KEYWORDS = ['sign', 'signature', 'authorised', 'authorized', 'seal', 'verified']

def detect_signature(pil_img):
    image_np = np.array(pil_img)
    results = reader.readtext(image_np)

    cropped_regions = []

    for bbox, text, confidence in results:
        if any(keyword in text.lower() for keyword in KEYWORDS):
            x_min = max(int(min(pt[0] for pt in bbox)) - 10, 0)
            y_min = max(int(min(pt[1] for pt in bbox)) - 10, 0)
            x_max = min(int(max(pt[0] for pt in bbox)) + 10, pil_img.width)
            y_max = min(int(max(pt[1] for pt in bbox)) + 10, pil_img.height)

            cropped = pil_img.crop((x_min, y_min, x_max, y_max))

            # Filter out empty or too-small crops
            if cropped.size[0] > 30 and cropped.size[1] > 15:
                cropped_regions.append(cropped)

    # Detected is True only if at least one valid cropped image exists
    detected = len(cropped_regions) > 0
    return detected, cropped_regions