import requests
import os
import sys

def run_poc():
    # We'll use an example PDF from the pdfplumber repo
    pdf_path = "examples/pdfs/background-checks.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    print(f"--- EthioQS PoC: Sending {pdf_path} to backend ---")

    url = "http://localhost:8000/extract-boq/"

    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()

            print("\nExtracted Data Summary:")
            print(f"Filename: {data['filename']}")
            print(f"Total Pages: {data['page_count']}")
            print(f"Rows Extracted from Page 1: {len(data['extracted_data'])}")

            print("\nFirst 5 rows of data:")
            for row in data['extracted_data'][:5]:
                print(f"  {row}")

        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the PoC backend. Is it running?")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_poc()
