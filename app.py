import streamlit as st
import os
from extractor import process_invoice
import json

st.title("📄 Invoice Data Extractor & Verifier")

# Ensure directory setup
os.makedirs("current_directory/input", exist_ok=True)
os.makedirs("current_directory/output", exist_ok=True)

uploaded_file = st.file_uploader("Upload scanned invoice PDF", type="pdf")

if uploaded_file:
    input_path = os.path.join("current_directory/input", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processing invoice..."):
        json_path, excel_path, verif_path = process_invoice(input_path)

    st.success("Extraction complete!")

    with open(json_path, "r") as f:
        data_json = json.load(f)

    st.subheader("Extracted JSON Data")
    st.json(data_json)

    st.download_button("Download JSON", json.dumps(data_json, indent=2), file_name="extracted_data.json")

    with open(excel_path, "rb") as ef:
        excel_bytes = ef.read()
    st.download_button("Download Excel", excel_bytes, file_name="extracted_data.xlsx")

    with open(verif_path, "r") as f:
        verif_report = json.load(f)

    st.subheader("Verifiability Report")
    st.json(verif_report)

    st.download_button("Download Verifiability Report", json.dumps(verif_report, indent=2), file_name="verifiability_report.json")
