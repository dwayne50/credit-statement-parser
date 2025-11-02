import re
from dateutil import parser as dateparser
from decimal import Decimal

def clean_amount(s):
    if not s: return None
    s = s.replace('₹','').replace('$','').replace(',','').strip()
    try:
        return float(Decimal(s))
    except:
        return None

def parse_date(s):
    try:
        d = dateparser.parse(s, fuzzy=True)
        return d.date().isoformat()
    except:
        return None


def find_first_regex(text, patterns):
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m
    return None

def extract_last4(text):
    m = find_first_regex(text, [
        r'ending\s+(\d{4})',
        r'XX+\d{4}',
        r'\d{4}\b'
    ])
    return m.group(1) if m else None

def extract_due_date(text):
    m = find_first_regex(text, [
        r'Payment\s+Due\s+Date[:\s]*([A-Za-z0-9, \-/]+)',
        r'Due\s+Date[:\s]*([A-Za-z0-9, \-/]+)'
    ])
    if m:
        return parse_date(m.group(1))
    return None

def extract_total_balance(text):
    m = find_first_regex(text, [
        r'Total\s+Amount\s+Due[:\s]*([\₹,\d\.\sCRDR-]+)',
        r'Outstanding\s+Balance[:\s]*([\₹,\d\.\sCRDR-]+)',
        r'New\s+Balance[:\s]*([\₹,\d\.\sCRDR-]+)'
    ])
    if m:
        return clean_amount(m.group(1))
    return None

def extract_transactions_from_text(text):
    lines = text.splitlines()
    txs = []
    date_re = re.compile(r'\b(\d{1,2}[-/][A-Za-z]{3,9}[-/]\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4})')
    amt_re = re.compile(r'(-?₹?\s?[\d,]+\.\d{2})')
    for line in lines:
        if date_re.search(line) and amt_re.search(line):
            date_str = date_re.search(line).group(0)
            amt_str = amt_re.search(line).group(0)
            desc = line.split(date_str)[-1].split(amt_str)[0].strip()
            txs.append({
                'date': parse_date(date_str),
                'description': desc,
                'amount': clean_amount(amt_str)
            })
    return txs
