import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import random

INVOICE_DIR = os.path.join(os.path.dirname(__file__), "..", "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)

def _make_invoice_pdf(ticket: str, passenger_name: str) -> str:
    """
    Generate a simple PDF invoice for demo. Returns file path.
    """
    invoice_no = f"INV-{random.randint(10000,99999)}"
    date = datetime.utcnow().strftime("%Y-%m-%d")
    airline = "Thai Airways"
    amount = round(random.uniform(1000, 15000), 2)
    gstin = "09ABCDE1234F1Z5"  # sample-looking GSTIN

    fname = f"{ticket}_{invoice_no}.pdf"
    path = os.path.join(INVOICE_DIR, fname)

    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h-80, f"Invoice: {invoice_no}")
    c.setFont("Helvetica", 12)
    c.drawString(40, h-110, f"Ticket Number: {ticket}")
    c.drawString(40, h-130, f"Passenger: {passenger_name}")
    c.drawString(40, h-150, f"Airline: {airline}")
    c.drawString(40, h-170, f"Date: {date}")
    c.drawString(40, h-190, f"Amount: INR {amount}")
    c.drawString(40, h-210, f"GSTIN: {gstin}")
    c.save()

    # return a dict with fields for parser later
    return {
        "file_path": path,
        "invoice_number": invoice_no,
        "invoice_date": date,
        "airline": airline,
        "amount": amount,
        "gstin": gstin,
        "file_name": fname
    }

def download_invoice(ticket: str, passenger_name: str) -> dict:
    """
    Simulate a download: create a PDF invoice and return metadata.
    In a real implementation you'd use Selenium / requests to fetch from portal.
    """
    # For demo we always succeed unless ticket equals NO-PDF
    if ticket.strip().upper() == "NO-PDF":
        return {"success": False, "message": "Invoice not found"}
    meta = _make_invoice_pdf(ticket, passenger_name)
    meta["success"] = True
    return meta
