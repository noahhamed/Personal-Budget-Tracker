from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import uuid



# Data Model


@dataclass
class Transaction:
    date: str
    category: str
    amount_cents: int
    ttype: str  # "income" or "expense"
    tid: str = field(default_factory=lambda: uuid.uuid4().hex)



# Validation Helpers


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


def validate_category(category: str) -> str:
    category = category.strip()
    if not category:
        raise ValueError("Category is required.")
    return category


def validate_type(ttype: str) -> str:
    ttype = ttype.strip().lower()
    if ttype not in ("income", "expense"):
        raise ValueError("Type must be income or expense.")
    return ttype



# Core Logic


def add_transaction(
    transactions: list[Transaction],
    date: str,
    category: str,
    amount: str,
    ttype: str = "expense",
) -> None:
    date = validate_date(date)
    category = validate_category(category)
    cents = amount_to_cents(amount)
    ttype = validate_type(ttype)

    transactions.append(
        Transaction(
            date=date,
            category=category,
            amount_cents=cents,
            ttype=ttype,
        )
    )


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
    totals: dict[str, int] = {}

    for t in transactions:
        if t.date[:7] != month:
            continue
        if t.ttype != "expense":
            continue
        totals[t.category] = totals.get(t.category, 0) + t.amount_cents

    return totals



# Data Persistence (JSON)


DATA_FILE = Path("data.json")


def transaction_to_dict(t: Transaction) -> dict:
    return {
        "tid": t.tid,
        "date": t.date,
        "category": t.category,
        "amount_cents": t.amount_cents,
        "ttype": t.ttype,
    }


def dict_to_transaction(d: dict) -> Transaction:
    return Transaction(
        date=d["date"],
        category=d["category"],
        amount_cents=int(d["amount_cents"]),
        ttype=d.get("ttype", "expense"),
        tid=d.get("tid", uuid.uuid4().hex),
    )


def save_transactions(
    transactions: list[Transaction], filepath: Path = DATA_FILE
) -> None:
    data = [transaction_to_dict(t) for t in transactions]
    filepath.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_transactions(filepath: Path = DATA_FILE) -> list[Transaction]:
    if not filepath.exists():
        return []
    raw = json.loads(filepath.read_text(encoding="utf-8"))
    return [dict_to_transaction(item) for item in raw]


def reset_transactions(filepath: Path = DATA_FILE) -> None:
    if filepath.exists():
        filepath.unlink()
