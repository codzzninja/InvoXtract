import easyocr
import re
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def match_any(text, patterns, group=1):
    for pat in patterns:
        match = re.search(pat, text, re.I)
        if match:
            return match.group(group).strip()
    return ""

def clean_text(text):
    corrections = {
        r'\bIXMOIC\b': 'INVOICE',
        r'\bJata\b': 'Date',
        r'\bIuvoioe\s*K\b': 'Invoice No',
        r'\bsplier\b': 'Supplier',
        r'\bG3t\b': 'GST',
        r'\b3uLl\b': 'Bill',
        r'\bGTT\b': 'GST',
        r'\bmner\b': 'PO Number',
        r'\bsipping\s+MMtrers\b': 'Shipping Address',
        r'\bMurket\b': 'Market',
        r'\bsototal\b': 'Subtotal',
        r'\bretal\b': 'Total',
        r'\bnuthorieed\s+J1\s+natory\b': 'Authorized Signatory',
        r'\(1X\)': 'Tax (18%)'
    }
    for wrong, correct in corrections.items():
        text = re.sub(wrong, correct, text, flags=re.IGNORECASE)
    return text

def extract_fields(image):
    text_list = reader.readtext(np.array(image), detail=0, paragraph=True)
    full_text = clean_text("\n".join(text_list))

    # Debug: print cleaned OCR text for backend verification
    print("=== Cleaned OCR Text ===\n", full_text)

    # Extract fields robustly with multiple regex attempts if needed
    invoice_number = match_any(full_text, [
        r"Invoice\s*(?:No\.?|Number|#|Num|K)?\s*[:\-]?\s*([\w\-\/]+)",
        r"Invoice\s*[:\-]?\s*([\w\-\/]+)"
    ], group=1)

    invoice_date = match_any(full_text, [
        r"(?:Invoice\s*)?(?:Date|Inv\s*Date|Bill\s*Date)\s*[:\-]?\s*([\d]{4}-[\d]{2}-[\d]{2})",
        r"(?:Invoice\s*)?(?:Date|Inv\s*Date|Bill\s*Date)\s*[:\-]?\s*([\d]{1,2}[/-][\d]{1,2}[/-][\d]{2,4})",
        r"Date\s*[:\-]?\s*([\d]{1,2}[/-][\d]{1,2}[/-][\d]{2,4})"
    ], group=1)

    po_number = match_any(full_text, [
        r"(?:P\.?O\.?|Purchase Order|PO)\s*(?:Number|No\.?|#)?\s*[:\-]?\s*([\w\/\-]+)"
    ], group=1)

    shipping_address = match_any(full_text, [
        r"(?:Shipping Address|Ship To|Delivery Address)\s*[:\-]?\s*(.+)"
    ], group=1)

    # GST fallback: find GST numbers (15 uppercase alphanumeric chars)
    gst_matches = re.findall(r'\b[0-9A-Z]{15}\b', full_text)
    supplier_gst_number = gst_matches[0] if len(gst_matches) > 0 else ""
    bill_to_gst_number = gst_matches[1] if len(gst_matches) > 1 else ""

    fields = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "po_number": po_number,
        "shipping_address": shipping_address,
        "supplier_gst_number": supplier_gst_number,
        "bill_to_gst_number": bill_to_gst_number,
    }

    return fields
