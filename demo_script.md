# Demo Script – Credit Card / Bank Statement PDF Parser

1. Introduction
Hello, my name is Dwayne Dias.  
This is my submission for the Sure Financials internship assignment — a PDF Statement Parser that automatically extracts structured financial data from real statements.


2. What the project does
The parser reads a real Axis Bank statement PDF, detects the issuer, and extracts key information such as:

- Account or card last four digits  
- Statement period  
- Opening and closing balances  
- A full list of transactions with date, description, amount, and balance  

For this project, Axis Bank statements were used as the primary dataset, since authentic credit card statements from other issuers were not publicly available online.  
However, the system is built so that additional issuers (HDFC, ICICI, SBI, Kotak) can be supported easily by adding new parser modules.
The program exports all parsed information in both JSON and CSV formats.


3. Demonstration
Run the command:
```bash
python main.py statements
The program processes each PDF in the statements folder and prints progress messages such as:
Parsing: axis_statement.pdf
Saved JSON: outputs/parsed_json/axis_statement.json
Saved CSV: outputs/transactions_csv/axis_statement_tx.csv
Then open the generated files:
In parsed_json, show the structured JSON output with the key fields.
In transactions_csv, open the CSV file and point out the extracted transaction table.

4. How it works
pdfplumber extracts text from the PDF pages.
The program detects which bank issued the statement using keyword matching.
Each bank has its own parser that uses regular expressions to identify statement fields and transaction details.
The data is normalized and exported as JSON and CSV.

5. Challenges and learning
Each bank uses different layouts and formats for their statements.
Some PDFs are scanned images with no selectable text.
To handle such cases, an OCR fallback using pytesseract can be added in the future.
Finding real credit card statements from multiple issuers was also a challenge, so the Axis Bank dataset was used to demonstrate the working prototype.

6. Future improvements
Add support for additional banks such as HDFC, ICICI, SBI, and Kotak.
Include OCR for image-based PDFs.
Build a simple dashboard using Streamlit to visualize spending and balances.
Add analytics such as monthly income and expense tracking.

7. Conclusion
This project demonstrates how unstructured financial documents can be transformed into clean, machine-readable data.
It combines text extraction, data parsing, and automation — providing a strong foundation for intelligent financial tools.