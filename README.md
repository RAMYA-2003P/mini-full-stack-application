# Mini Full-Stack Invoice Dashboard

## Overview
This project is a **mini full-stack application** that simulates a real-world workflow of downloading airline invoices, parsing them, and displaying them in a dashboard. It demonstrates full-stack development skills using **FastAPI** for the backend and **React** for the frontend.

---

## Features
- Load passenger data from CSV
- Download invoice PDFs for passengers (simulated)
- Parse invoice PDFs to extract details (invoice number, date, airline, amount, GSTIN)
- Display passenger list and invoice data in a React dashboard
- Show invoice summary and high-value invoices

---

## Tech Stack
- **Backend:** Python, FastAPI, Uvicorn, Pandas, ReportLab, PyPDF2  
- **Frontend:** React, JavaScript, HTML, CSS  
- **Tools:** Git, VS Code, Node.js, npm  

---

## Project Structure
aaa/
├── backend/
│ ├── app.py # FastAPI app
│ ├── services/ # Downloader, parser, storage
│ ├── models.py # Pydantic models
│ ├── data.csv # Passenger input file
│ └── invoices/ # Folder for generated PDFs
├── frontend/
│ ├── src/
│ │ ├── components/ # React components
│ │ ├── pages/ # Dashboard pages
│ │ └── App.jsx # Main React app
│ └── package.json
├── requirements.txt # Backend dependencies
└── README.md




---

## Installation

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload

f#rontend
cd frontend
npm install
npm start
Frontend
