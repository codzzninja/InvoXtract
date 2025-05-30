# InvoXtract - Invoice Extraction and Verification System

**A Python-based pipeline that extracts structured data from invoice PDFs using OCR (EasyOCR & Tesseract), verifies the extracted data for consistency (like totals and GST), detects signatures, and outputs results in JSON and Excel formats.**

# 🧰 Features
OCR using EasyOCR and Tesseract

Field extraction: invoice number, date, PO number, shipping address, GST

Table extraction with quantity, unit price, and total

Confidence scoring for each field and line item

Verification of subtotal, GST, and final total

Signature detection and cropping

Output in JSON and Excel

Verifiability report generation

# 🚀 How to Run
Follow these steps to set up and run the project:

1. Clone the Repository
   
   git clone https://github.com/codzzninja/InvoXtract.git            
   cd InvoXtract

3. Create and Activate a Virtual Environment

   python -m venv venv
   venv\Scripts\activate

4. Install Dependencies

   pip install -r requirements.txt

5. Run the script

   Streamlit run app.py
   
Also ensure:

Tesseract OCR is installed and added to PATH.

Poppler is installed for pdf2image.

# 📤 Outputs
Generated in output/ folder:

extracted_data.json: structured fields + table

extracted_data.xlsx: item table in spreadsheet

verifiability_report.json: confidence and consistency checks

seal_signature_*.jpg: cropped signature regions (if found)

# 🧪 Tests and Verifiability
Subtotal, GST (18%), and final total are re-computed and checked.

Each table row is validated: quantity × unit_price == total.

Confidence metrics are included per field and row.


# 🛠️ Future Improvements (optional)
GUI or Web UI

Multilingual invoice support

More robust table extraction (deep learning)

Integration with databases or cloud storage


