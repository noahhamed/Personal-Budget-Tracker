from Budget import add_expense, monthly_totals, category_breakdown, Transaction

transactions: list[Transaction] = []

add_expense(transactions, "2025-12-26", "Food", "12.50")
add_expense(transactions, "2025-12-27", "Food", "7.25")
add_expense(transactions, "2025-12-27", "Transport", "3.25")
add_expense(transactions, "2025-11-10", "Food", "5.00")  # different month

month = "2025-12"
income, expense, net = monthly_totals(transactions, month)
breakdown = category_breakdown(transactions, month)

print("Month:", month)
print("Income:", income / 100)
print("Expense:", expense / 100)
print("Net:", net / 100)
print("Breakdown:", {k: v / 100 for k, v in breakdown.items()})
