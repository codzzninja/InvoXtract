# table_extractor.py
import pytesseract
from pytesseract import Output
import re

def extract_table(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    rows, confidences, current_line, line_data = [], [], -1, []

    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if not text:
            continue

        line_num = data['line_num'][i]
        conf = int(data['conf'][i]) / 100.0 if data['conf'][i] != '-1' else 0.0

        if line_num != current_line:
            if line_data:
                row = parse_table_line(line_data)
                if row:
                    rows.append(row[0])
                    confidences.append(row[1])
            line_data = []
            current_line = line_num

        line_data.append((text, conf))

    if line_data:
        row = parse_table_line(line_data)
        if row:
            rows.append(row[0])
            confidences.append(row[1])

    return rows, confidences

def avg_confidence(line_data):
    return round(sum(conf for _, conf in line_data) / len(line_data), 2) if line_data else 0.0

def parse_table_line(line_data):
    words = [word for word, _ in line_data]
    numbers = [float(num) for num in re.findall(r"\d+(?:\.\d+)?", ' '.join(words))]

    # We expect at least quantity, unit_price, total
    if len(numbers) >= 3:
        try:
            quantity = numbers[-3]
            unit_price = numbers[-2]
            total_amount = numbers[-1]
            description_words = []

            for word, _ in line_data:
                if re.fullmatch(r"\d+(\.\d+)?", word):
                    continue
                description_words.append(word)

            description = ' '.join(description_words)

            # Validate extracted total
            expected_total = round(quantity * unit_price, 2)
            if abs(expected_total - total_amount) > 1:  # allow small OCR drift
                return None

            confidence_data = {
                "description_confidence": avg_confidence(line_data),
                "quantity_confidence": 0.95,
                "unit_price_confidence": 0.95,
                "total_amount_confidence": 0.95,
                "serial_number_confidence": 0.90
            }

            return ({
                "description": description.strip(),
                "hsn_sac": "",
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "serial_number": ""
            }, confidence_data)
        except:
            return None
    return None
