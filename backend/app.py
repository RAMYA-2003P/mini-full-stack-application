import os
import csv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List
from services.downloader import download_invoice, INVOICE_DIR
from services.parser import parse_invoice
from services import storage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CSV = os.path.join(BASE_DIR, "data.csv")

app = FastAPI(title="Invoice Downloader Demo")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load passengers from CSV at startup
# def load_passengers():
#     rows = []
#     if not os.path.exists(DATA_CSV):
#         return rows
#     with open(DATA_CSV, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for r in reader:
#             # normalize keys
#             rows.append({
#                 "ticket": r.get("Ticket Number") or r.get("ticket") or r.get("ticket_no") or "",
#                 "first_name": r.get("First Name") or r.get("first_name") or "",
#                 "last_name": r.get("Last Name") or r.get("last_name") or ""
#             })
#     return rows

def load_passengers():
    rows = []
    if not os.path.exists(DATA_CSV):
        return rows
    with open(DATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "ticket": r.get("Ticket Number") or r.get("ticket") or r.get("ticket_no") or "",
                "first_name": r.get("First Name") or r.get("first_name") or "",
                "last_name": r.get("Last Name") or r.get("last_name") or ""
            })
    return rows



PASSENGERS = load_passengers()


@app.get("/api/passengers")
def get_passengers():
    # Return passenger list with current statuses (look up DB)
    out = []
    for p in PASSENGERS:
        rec = storage.find_by_ticket(p["ticket"])
        
        out.append({
            "ticket": p["ticket"],
            "name": f"{p['first_name']} {p['last_name']}".strip(),
            "download_status": rec["download_status"] if rec else "Pending",
            "parse_status": rec["parse_status"] if rec else "Pending",
            "invoice_id": rec["id"] if rec else None
        })
    return out

@app.post("/api/download/{ticket}")
def api_download(ticket: str):
    # find passenger
    p = next((pp for pp in PASSENGERS if pp["ticket"] == ticket), None)
    if not p:
        raise HTTPException(status_code=404, detail="Passenger not found")
    passenger_name = f"{p['first_name']} {p['last_name']}".strip()
    result = download_invoice(ticket, passenger_name)
    if not result.get("success"):
        # store record with Not Found
        storage.insert_invoice_record({
            "ticket": ticket,
            "passenger_name": passenger_name,
            "file_name": "",
            "download_status": "Not Found",
            "parse_status": "Pending",
            "invoice_number": None,
            "invoice_date": None,
            "airline": None,
            "amount": None,
            "gstin": None
        })
        return {"status": "NotFound", "message": result.get("message", "Not found")}
    # success -> insert record (or update)
    file_name = result["file_name"]
    rec = storage.find_by_ticket(ticket)
    if rec:
        storage.update_invoice_by_ticket(ticket, {"file_name": file_name, "download_status": "Success"})
    else:
        storage.insert_invoice_record({
            "ticket": ticket,
            "passenger_name": passenger_name,
            "file_name": file_name,
            "download_status": "Success",
            "parse_status": "Pending",
            "invoice_number": result["invoice_number"],
            "invoice_date": result["invoice_date"],
            "airline": result["airline"],
            "amount": result["amount"],
            "gstin": result["gstin"]
        })
    return {"status": "Success", "file_name": file_name}

@app.post("/api/parse/{ticket}")
def api_parse(ticket: str):
    rec = storage.find_by_ticket(ticket)
    if not rec or not rec.get("file_name"):
        raise HTTPException(status_code=400, detail="No downloaded PDF found. Download first.")
    pdf_path = os.path.join(os.path.dirname(__file__), "invoices", rec["file_name"])
    parsed = parse_invoice(pdf_path)
    if parsed.get("error"):
        storage.update_invoice_by_ticket(ticket, {"parse_status": "Error"})
        raise HTTPException(status_code=500, detail=parsed["error"])
    # update DB with parsed details
    updates = {
        "invoice_number": parsed.get("invoice_number"),
        "invoice_date": parsed.get("invoice_date"),
        "airline": parsed.get("airline"),
        "amount": parsed.get("amount"),
        "gstin": parsed.get("gstin"),
        "parse_status": "Success"
    }
    storage.update_invoice_by_ticket(ticket, updates)
    return {"status": "Success", "parsed": updates}

@app.get("/api/invoices")
def api_invoices():
    return storage.all_invoices()

@app.get("/api/summary")
def api_summary():
    return storage.summary_by_airline()

@app.get("/api/high-value/{threshold}")
def api_high_value(threshold: float):
    return storage.high_value(threshold)

@app.get("/api/download-file/{ticket}")
def api_download_file(ticket: str):
    rec = storage.find_by_ticket(ticket)
    if not rec or not rec.get("file_name"):
        raise HTTPException(404, "File not found")
    path = os.path.join(os.path.dirname(__file__), "invoices", rec["file_name"])
    if not os.path.exists(path):
        raise HTTPException(404, "File not found on disk")
    return FileResponse(path, filename=rec["file_name"], media_type="application/pdf")
