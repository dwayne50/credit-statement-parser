# main.py
import os
import re
import json
import csv
import sys
import pdfplumber
from parsers.axis import parse_axis  # import Axis parser

# ----------- Detect issuer -----------
def detect_issuer(text):
    text_low = text.lower()
    if 'axis' in text_low or 'axis bank' in text_low:
        return 'axis'
    if 'hdfc' in text_low or 'hdfc bank' in text_low:
        return 'hdfc'
    if 'icici' in text_low or 'icici bank' in text_low:
        return 'icici'
    if 'sbi' in text_low or 'state bank' in text_low:
        return 'sbi'
    if 'kotak' in text_low or 'kotak mahindra' in text_low:
        return 'kotak'
    return 'unknown'

# Map each issuer to its parser
PARSER_MAP = {
    'axis': parse_axis,
    # you can later add others here (e.g., 'hdfc': parse_hdfc)
}

# ----------- Core parsing function -----------
def parse_pdf(path):
    print(f"\n📄 Parsing: {os.path.basename(path)}")
    text = ""

    # Extract text from all pages
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # Detect issuer and get its parser
    issuer_key = detect_issuer(text)
    parser = PARSER_MAP.get(issuer_key)

    if parser:
        parsed_data = parser(text)
    else:
        parsed_data = {
            'issuer': issuer_key,
            'message': 'No parser found for this issuer'
        }

    parsed_data['source_file'] = os.path.basename(path)
    return parsed_data

# ----------- Folder runner -----------
def main_folder(folder):
    out_json_folder = 'outputs/parsed_json'
    out_csv_folder = 'outputs/transactions_csv'

    os.makedirs(out_json_folder, exist_ok=True)
    os.makedirs(out_csv_folder, exist_ok=True)

    for fname in os.listdir(folder):
        if not fname.lower().endswith('.pdf'):
            continue

        path = os.path.join(folder, fname)
        parsed = parse_pdf(path)
        base = os.path.splitext(fname)[0]

        # Write parsed JSON
        json_path = os.path.join(out_json_folder, base + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # Write transactions to CSV (if any)
        txs = parsed.get('transactions', [])
        if txs:
            csv_path = os.path.join(out_csv_folder, base + '_tx.csv')
            keys = ['date', 'description', 'amount', 'balance']
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for t in txs:
                    writer.writerow({k: t.get(k) for k in keys})
            print(f"✅ Saved CSV: {csv_path}")
        else:
            print("⚠️ No transactions found for this file.")

# ----------- CLI entry -----------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py statements_folder")
    else:
        folder = sys.argv[1]
        if not os.path.exists(folder):
            print(f"❌ Folder not found: {folder}")
        else:
            main_folder(folder)
