from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io
import uvicorn

app = FastAPI()

@app.post("/extract-boq/")
async def extract_boq(file: UploadFile = File(...)):
    """
    Simulates a BOQ extraction endpoint for EthioQS.
    It takes a PDF, finds the largest table on the first page,
    and returns its rows.
    """
    content = await file.read()
    results = []

    with pdfplumber.open(io.BytesIO(content)) as pdf:
        # Focusing on the first page for this PoC
        page = pdf.pages[0]

        # We use 'text' strategy for vertical because construction
        # tables often have implied columns without vertical lines
        table = page.extract_table({
            "vertical_strategy": "text",
            "horizontal_strategy": "lines",
        })

        if table:
            for row in table:
                # Filter out None values and empty strings
                clean_row = [cell for cell in row if cell]
                if clean_row:
                    results.append(clean_row)

    return {
        "filename": file.filename,
        "page_count": len(pdf.pages),
        "extracted_data": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
