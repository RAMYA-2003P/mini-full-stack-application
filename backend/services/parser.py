# Since our PDF generation put the fields in plain text at known locations,
# a simple parser can just read the text from PDF using PyPDF2.
import PyPDF2

def parse_invoice(pdf_path: str) -> dict:
    """
    Try to extract invoice data from a PDF. Returns dict of parsed fields.
    """
    out = {}
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for p in reader.pages:
                ptxt = p.extract_text()
                if ptxt:
                    text += ptxt + "\n"
        # naive regex-free extraction based on labelled lines
        for line in text.splitlines():
            if line.startswith("Invoice:"):
                out["invoice_number"] = line.split("Invoice:")[1].strip()
            elif line.startswith("Ticket Number:"):
                out["ticket"] = line.split("Ticket Number:")[1].strip()
            elif line.startswith("Passenger:"):
                out["passenger_name"] = line.split("Passenger:")[1].strip()
            elif line.startswith("Airline:"):
                out["airline"] = line.split("Airline:")[1].strip()
            elif line.startswith("Date:"):
                out["invoice_date"] = line.split("Date:")[1].strip()
            elif line.startswith("Amount:"):
                token = line.split("Amount:")[-1].strip()
                token = token.replace("INR", "").replace(",", "").strip()
                try:
                    out["amount"] = float(token)
                except:
                    out["amount"] = None
            elif line.startswith("GSTIN:"):
                out["gstin"] = line.split("GSTIN:")[1].strip()
        return out
    except Exception as e:
        return {"error": str(e)}
