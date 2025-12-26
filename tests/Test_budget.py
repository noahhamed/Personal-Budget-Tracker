import pytest
from budget import amount_to_cents, add_transaction, monthly_totals, category_breakdown, Transaction


def test_amount_to_cents():
    assert amount_to_cents("10") == 1000
    assert amount_to_cents("10.50") == 1050
    with pytest.raises(ValueError):
        amount_to_cents("")
    with pytest.raises(ValueError):
        amount_to_cents("-2")

def test_add_expense_appends_transaction():
    tx: list[Transaction] = []
    add_transaction(tx, "2025-12-26", "Food", "12.50")
    assert len(tx) == 1
    assert tx[0].category == "Food"
    assert tx[0].amount_cents == 1250

def test_monthly_totals_filters_by_month():
    tx = []
    add_transaction(tx, "2025-12-01", "Food", "5.00")
    add_transaction(tx, "2025-12-02", "Transport", "3.00")
    add_transaction(tx, "2025-11-30", "Food", "100.00")  # other month

    income, expense, net = monthly_totals(tx, "2025-12")
    assert income == 0
    assert expense == 800  # 5.00 + 3.00
    assert net == -800

def test_category_breakdown_sums_categories():
    tx = []
    add_transaction(tx, "2025-12-01", "Food", "5.00")
    add_transaction(tx, "2025-12-02", "Food", "2.50")
    add_transaction(tx, "2025-12-02", "Transport", "3.00")

    breakdown = category_breakdown(tx, "2025-12")
    assert breakdown["Food"] == 750
    assert breakdown["Transport"] == 300
def test_monthly_totals_income_and_expense():
    tx = []
    add_transaction(tx, "2025-12-01", "Pay", "1000.00", "income")
    add_transaction(tx, "2025-12-02", "Food", "10.00", "expense")

    income, expense, net = monthly_totals(tx, "2025-12")
    assert income == 100000
    assert expense == 1000
    assert net == 99000
