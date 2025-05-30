import os
from utils import pdf_to_images, preprocess_image
from field_parsers import extract_fields  # corrected import (was field_parsers)
from table_extractor import extract_table
from signature_detection import detect_signature
from verifiability import generate_verification_report
import json
import pandas as pd

def process_invoice(pdf_path):
    output_dir = "current_directory/output"
    os.makedirs(output_dir, exist_ok=True)

    images = pdf_to_images(pdf_path)
    fields = {}
    table_data = []
    all_confidences = []

    for img in images:
        processed_img = preprocess_image(img)
        new_fields = extract_fields(processed_img)
        # Update fields without overwriting keys with empty strings:
        for k, v in new_fields.items():
            if v:  # Only update if non-empty
                fields[k] = v

        table_rows, confidences = extract_table(processed_img)
        table_data.extend(table_rows)
        all_confidences.extend(confidences)

    seal_present, seal_imgs = detect_signature(images[0])
    if seal_present:
        for idx, cropped in enumerate(seal_imgs):
            cropped.save(os.path.join(output_dir, f"seal_signature_{idx+1}.jpg"))
    fields["seal_and_sign_present"] = seal_present

    df = pd.DataFrame(table_data)
    fields["no_items"] = len(df)

    json_output = os.path.join(output_dir, "extracted_data.json")
    excel_output = os.path.join(output_dir, "extracted_data.xlsx")
    verif_output = os.path.join(output_dir, "verifiability_report.json")

    with open(json_output, "w") as jf:
        json.dump({"fields": fields, "table": table_data}, jf, indent=2)

    df.to_excel(excel_output, index=False, engine='openpyxl')

    report = generate_verification_report(fields, table_data, all_confidences)
    with open(verif_output, "w") as vf:
        json.dump(report, vf, indent=2)

    return json_output, excel_output, verif_output
