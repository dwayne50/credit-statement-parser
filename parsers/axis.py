# parsers/axis.py
import re
from utils import clean_amount, parse_date

def parse_axis(text):
    # --- Account number ---
    acc_match = re.search(r'Account\s*No\s*[:\-]?\s*(\d+)', text, re.IGNORECASE)
    last4 = acc_match.group(1)[-4:] if acc_match else None

    # --- Statement period ---
    period_match = re.search(r'period\s*\(From\s*[:\-]?\s*([\d\-\/]+)\s*To\s*[:\-]?\s*([\d\-\/]+)\)', text, re.IGNORECASE)
    billing_cycle = None
    if period_match:
        start = parse_date(period_match.group(1))
        end = parse_date(period_match.group(2))
        billing_cycle = f"{start} to {end}"

    # --- Opening and closing balances ---
    open_match = re.search(r'OPENING\s+BALANCE\s+([\d,]+\.\d{2})', text, re.IGNORECASE)
    close_match = re.search(r'CLOSING\s+BALANCE\s+([\d,]+\.\d{2})', text, re.IGNORECASE)
    opening_balance = clean_amount(open_match.group(1)) if open_match else None
    closing_balance = clean_amount(close_match.group(1)) if close_match else None

    # --- Transactions ---
    txs = []
    # Pattern fits lines like: 02-04-2023 ... 9170.00 1266873.70
    line_pattern = re.compile(
        r'(\d{2}-\d{2}-\d{4})\s+(.*?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})',
        re.DOTALL
    )

    for m in line_pattern.finditer(text):
        date_str = m.group(1)
        desc = " ".join(m.group(2).split())
        amount = clean_amount(m.group(3))
        balance = clean_amount(m.group(4))
        txs.append({
            'date': parse_date(date_str),
            'description': desc,
            'amount': amount,
            'balance': balance
        })

    return {
        'issuer': 'Axis Bank',
        'last4': last4,
        'billing_cycle': billing_cycle,
        'opening_balance': opening_balance,
        'closing_balance': closing_balance,
        'transactions': txs
    }
