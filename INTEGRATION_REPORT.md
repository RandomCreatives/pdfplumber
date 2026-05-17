# Project Explanation: pdfplumber

`pdfplumber` is a Python library designed for deep inspection and data extraction from PDF files. Unlike many PDF libraries that focus on text alone, `pdfplumber` provides granular access to every element on a page, including characters, lines, rectangles, and curves, along with their precise coordinates and formatting attributes.

### Key Capabilities:
- **Granular Extraction**: Access the exact (x, y) coordinates of every character and shape.
- **Table Extraction**: A robust, customizable engine for finding and extracting tables, even those without visible borders.
- **Visual Debugging**: Tools to generate images of PDF pages with detected objects (like table cells or words) highlighted for verification.
- **Cropping & Filtering**: Ability to focus on specific regions of a page or filter objects based on properties.

---

# Integration with DigitalMehandis_V5.0

`DigitalMehandis_V5.0` (EthioQS) is a tool for quantity surveying, Bill of Quantities (BOQ), and Bar Bending Schedules (BBS). Integrating `pdfplumber` can transform it from a manual entry tool into an automated data extraction powerhouse.

### Architectural Choice: Library Dependency vs. Microservice
When integrating `pdfplumber` with `DigitalMehandis`, the recommended approach is to **use `pdfplumber` as a library dependency** within the `DigitalMehandis` backend.

- **Why not recreate it?** `pdfplumber` is the result of years of development and handles complex PDF edge cases (encoding, rotation, coordinate mapping). Re-creating its features would be an immense and unnecessary undertaking.
- **Why library dependency?**
    - **Performance**: Direct in-process access to the PDF data avoids the latency and overhead of network calls between two separate repositories.
    - **Simplicity**: You manage one backend codebase. You simply add `pdfplumber` to your `requirements.txt`.
    - **Tight Integration**: You can directly map `pdfplumber` objects to your SQLAlchemy models or Pydantic schemas without intermediate serialization layers.

Only choose a separate "OCR/Extraction Microservice" if you expect extremely high load that requires scaling the extraction logic independently from the rest of the application.

### 1. Automated BOQ and BBS Extraction
Construction professionals often receive existing BOQs or BBSs in PDF format. `pdfplumber` can be used in the `backend` (FastAPI) to automatically parse these tables and populate the database.

**Integration Point**: A new API endpoint in `backend/app/api/v1/extract.py`.

### 2. Drawing "Take-off" Assistance
In quantity surveying, "take-off" is the process of measuring dimensions from drawings. `pdfplumber` can extract vector graphics (lines and rects) from machine-generated architectural PDFs.
- **Automated Measuring**: Calculate the length of walls or the area of rooms by analyzing the geometry of the PDF.
- **Object Counting**: Identify symbols or recurring shapes to count items like windows or doors.

### 3. Visual Verification in Frontend
You can use `pdfplumber` to generate a "mapped" image of the PDF. The frontend (Next.js/Fabric.js) can then overlay these detected elements, allowing users to confirm or adjust measurements.

---

### Sample FastAPI Implementation

Here is how you might implement a BOQ extraction endpoint in the `DigitalMehandis` backend:

```python
from fastapi import APIRouter, UploadFile, File
import pdfplumber
import io

router = APIRouter()

@router.post("/extract-boq/")
async def extract_boq(file: UploadFile = File(...)):
    content = await file.read()
    results = []

    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            # Extract tables using settings tuned for MoUDC formats
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "snap_tolerance": 3,
            })
            for table in tables:
                # Process rows into BOQ line items
                for row in table:
                    # Example mapping: [Item No, Description, Unit, Quantity, Rate, Amount]
                    results.append({
                        "description": row[1],
                        "quantity": row[3],
                        "unit": row[2]
                    })

    return {"items": results}
```

### Integration Steps for EthioQS:
1.  **Add Dependency**: Add `pdfplumber` to `backend/requirements.txt`.
2.  **Service Layer**: Create a `backend/app/services/pdf_service.py` to handle the logic of interpreting construction drawings.
3.  **Frontend Update**: Modify the drawing viewer in `frontend/` to request "object maps" from the backend, allowing users to click on a wall to automatically get its length extracted by `pdfplumber`.
