# EthioQS Proof-of-Concept (PoC) Guide

This PoC demonstrates how `pdfplumber` can be integrated directly into the `DigitalMehandis` (EthioQS) FastAPI backend as a library dependency.

## Structure
- `poc_ethioqs/backend.py`: A FastAPI server with an `/extract-boq/` endpoint.
- `poc_ethioqs/client_poc.py`: A client script that sends a PDF to the backend and prints the extracted data.

## Prerequisites
Ensure you have the following installed:
```bash
pip install fastapi uvicorn requests python-multipart
pip install -e . # Installs pdfplumber from the local source
```

## Running the PoC

### 1. Start the Backend
In one terminal, run:
```bash
python3 poc_ethioqs/backend.py
```

### 2. Run the Client
In another terminal, run:
```bash
python3 poc_ethioqs/client_poc.py
```

## What this demonstrates
1. **Direct Integration**: The backend imports `pdfplumber` and uses it to process an uploaded file in-memory.
2. **Table Extraction**: It uses `page.extract_table()` with strategies tuned for construction-style documents (where vertical lines are often missing but text is aligned).
3. **Data Mapping**: The PDF data is converted into a clean JSON-serializable list of rows, ready to be saved to a database.
