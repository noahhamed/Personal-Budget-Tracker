from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    date: str
    category: str
    amount_cents: int
    ttype: str
def amount_to_cents(amount_str: str) -> int:
    amount_str = amount_str.strip()
    if not amount_str:
        raise ValueError("Amount is required.")
    try:
        value = float(amount_str)
    except ValueError:
        raise ValueError("Amount must be a number.")
    if value <= 0:
        raise ValueError("Amount must be greater than 0.")
    return int(round(value * 100))


def validate_date(date_str: str) -> str:
    datetime.strptime(date_str, "%Y-%m-%d")
    return date_str

def validate_type(ttype: str) -> str:
    ttype = ttype.strip().lower()
    if ttype not in ("income", "expense"):
        raise ValueError("Type must be income or expense.")
    return ttype


def validate_category(category: str) -> str:
    category = category.strip()
    if not category:
        raise ValueError("Category is required.")
    return category


def add_transaction(transactions: list[Transaction], date: str, category: str, amount: str, ttype: str = "expense") -> None:
    date = validate_date(date)
    category = validate_category(category)
    cents = amount_to_cents(amount)
    ttype = validate_type(ttype)

    transactions.append(Transaction(date=date, category=category, amount_cents=cents, ttype=ttype))


def monthly_totals(transactions: list[Transaction], month: str) -> tuple[int, int, int]:
    income = 0
    expense = 0

    for t in transactions:
        if t.date[:7] != month:
            continue
        if t.ttype == "income":
            income += t.amount_cents
        else:
            expense += t.amount_cents

    return income, expense, income - expense


def category_breakdown(transactions: list[Transaction], month: str) -> dict[str, int]:
    totals = {}
    for t in transactions:
        if t.date[:7] != month:
            continue
        if t.ttype != "expense":
            continue
        totals[t.category] = totals.get(t.category, 0) + t.amount_cents
    return totals
