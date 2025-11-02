### Credit Card / Bank Statement PDF Parser

# Overview
This project extracts structured financial data from PDF statements automatically.  
It is designed to support multiple credit card or bank issuers; however, for this submission, only Axis Bank statements were used and tested.  
This was due to the unavailability of verified public datasets for credit card statements from other banks online.  
The structure and code remain fully extensible — new issuer parsers (such as HDFC, SBI, ICICI, and Kotak) can be added easily.


# Objective
To build a robust PDF parser that can extract at least five key data points from credit card or bank statements across multiple issuers.


# Features
Extracts text from real PDFs using pdfplumber
Detects issuer type automatically (Axis, HDFC, ICICI, SBI, Kotak)


# Parses:
Account / Card Last 4 Digits
Statement Period
Opening Balance
Closing / Total Balance
Full Transaction List (date, description, amount, balance)
Outputs results as both JSON and CSV
Easily extendable to support new issuers


# Tech Stack
Python 3.13

# Libraries:
pdfplumber — PDF text extraction
pandas — data handling (optional)
python-dateutil — flexible date parsing
regex — pattern matching


# Project Structure
credit_statement_parser/
├─ statements/                 # input PDFs
├─ outputs/
│  ├─ parsed_json/             # extracted statement data
│  └─ transactions_csv/        # transaction tables
├─ parsers/
│  ├─ axis.py                  # Axis Bank parser logic
│  ├─ hdfc.py                  # (future extension)
│  └─ ...
├─ utils.py                    # helper regex & parsing functions
├─ main.py                     # entry point
├─ requirements.txt
├─ README.md
└─ demo_script.md


# Setup Instructions
1. Clone or open the project
Open the folder in VS Code.
2. Create a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# or
source venv/bin/activate      # macOS / Linux
3. Install dependencies
pip install -r requirements.txt
4. Add statements
Put your real PDF statements in the statements/ folder.
Example:
statements/
 ├─ axis_statement.pdf
 ├─ hdfc_statement.pdf
5. Run the parser
python main.py statements


# Outputs
After running, you’ll find:
outputs/
 ├─ parsed_json/
 │   ├─ axis_statement.json
 └─ transactions_csv/
     ├─ axis_statement_tx.csv

Example JSON
{
  "issuer": "Axis Bank",
  "last4": "3628",
  "billing_cycle": "2023-04-01 to 2023-04-30",
  "opening_balance": 1257703.7,
  "closing_balance": 1653228.37,
  "transactions": [
    {"date": "2023-04-02", "description": "UPI/P2A/309105106390/Paytm/Paytm Pay/ONSPG202", "amount": 9170.0, "balance": 1266873.7}
  ]
}

# How It Works
Text extraction – pdfplumber reads each page’s text.
Issuer detection – keyword matching identifies the bank.
Pattern recognition – regex locates dates, balances, and amounts.
Data normalization – cleaned and structured into consistent fields.
Output generation – saved as both JSON and CSV for analysis.

# Future Improvements
Add OCR fallback using pytesseract for scanned PDFs
Extend support to more issuers (HDFC, ICICI, SBI, Kotak)
Build a simple Streamlit or Flask dashboard
Integrate analytics: monthly spend, income vs expense graphs

# Author
Dwayne Dias
Computer Science & Business Systems Student, NMIMS (MPSTME)
Focused on merging technology, automation, and finance.

Submission Details
Assignment: Credit Card Statement Parser — Sure Financials Internship
Deadline: Sunday, 2nd November (EOD)
