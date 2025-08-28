import os
import sqlite3
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "invoices.db")

def _get_conn():
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "invoices"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket TEXT,
        passenger_name TEXT,
        file_name TEXT,
        invoice_number TEXT,
        invoice_date TEXT,
        airline TEXT,
        amount REAL,
        gstin TEXT,
        parse_status TEXT,
        download_status TEXT
    )
    """)
    conn.commit()
    return conn

_conn = init_db()

def insert_invoice_record(record: Dict[str, Any]) -> int:
    cur = _conn.cursor()
    cur.execute("""
    INSERT INTO invoices (ticket, passenger_name, file_name, invoice_number, invoice_date, airline, amount, gstin, parse_status, download_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("ticket"),
        record.get("passenger_name"),
        record.get("file_name"),
        record.get("invoice_number"),
        record.get("invoice_date"),
        record.get("airline"),
        record.get("amount"),
        record.get("gstin"),
        record.get("parse_status", "Pending"),
        record.get("download_status", "Pending")
    ))
    _conn.commit()
    return cur.lastrowid

def update_invoice_by_ticket(ticket: str, updates: Dict[str, Any]):
    cur = _conn.cursor()
    set_clause = ", ".join([f"{k}=?" for k in updates.keys()])
    params = list(updates.values()) + [ticket]
    sql = f"UPDATE invoices SET {set_clause} WHERE ticket=?"
    cur.execute(sql, params)
    _conn.commit()

def find_by_ticket(ticket: str) -> Optional[Dict[str, Any]]:
    cur = _conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE ticket=?", (ticket,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [c[0] for c in cur.description]
    return dict(zip(cols, row))

def all_invoices() -> List[Dict[str, Any]]:
    cur = _conn.cursor()
    cur.execute("SELECT * FROM invoices ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in rows]

def high_value(threshold: float):
    cur = _conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE amount > ?", (threshold,))
    rows = cur.fetchall()
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in rows]

def summary_by_airline():
    cur = _conn.cursor()
    cur.execute("SELECT airline, COUNT(*) as cnt, SUM(amount) as total FROM invoices GROUP BY airline")
    return [{"airline": r[0] or "Unknown", "count": r[1], "total": r[2] or 0} for r in cur.fetchall()]
