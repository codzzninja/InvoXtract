def verify_fields(data):
    """
    Verifies required fields in the extracted invoice data.
    Returns a dictionary with pass/fail flags for each field.
    """
    report = {}

    # Required fields
    required_fields = ["invoice_total", "signature_detected"]

    for field in required_fields:
        if field not in data:
            report[field] = "Missing"
        else:
            value = data[field]
            if field == "invoice_total":
                report[field] = "Valid" if isinstance(value, (int, float)) and value > 0 else "Invalid or Zero"
            elif field == "signature_detected":
                report[field] = "Valid" if isinstance(value, bool) else "Invalid Type"

    report["status"] = "Passed" if all(v == "Valid" for v in report.values() if v != "Missing") else "Check Issues"
    return report
