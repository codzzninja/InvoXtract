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


