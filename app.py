from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

# keep your current file name (capital B)
from budget import (
    add_transaction,
    monthly_totals,
    category_breakdown,
    Transaction,
    load_transactions,
    save_transactions,
    reset_transactions
)


app = Flask(__name__)
app.secret_key = "dev"  # ok for a student project

# simple in-memory storage (we can add database later)
transactions: list[Transaction] = load_transactions()


@app.route("/")
def index():
    month = request.args.get("month") or datetime.now().strftime("%Y-%m")
    available_months = sorted({t.date[:7] for t in transactions}, reverse=True)

    # If user typed a month that doesn't exist, default to newest available month
    if available_months and month not in available_months:
        month = available_months[0]

    txns = [t for t in transactions if t.date[:7] == month]
    txns.sort(key=lambda t: t.date, reverse=True)

    income, expense, net = monthly_totals(transactions, month)
    breakdown = category_breakdown(transactions, month)

    # show 10 most recent
    recent = list(reversed(transactions))[:10]

    return render_template(
        "index.html",
        month=month,
        income=income,
        expense=expense,
        net=net,
        available_months=available_months,
        breakdown=breakdown,
        recent=recent,
        txns=txns
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form.get("date", "")
        category = request.form.get("category", "")
        amount = request.form.get("amount", "")
        ttype = request.form.get("type", "expense")

        try:
            add_transaction(transactions, date, category, amount, ttype)
            save_transactions(transactions)
            flash("Expense added!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("add.html")
@app.route("/reset", methods=["POST"])
def reset():
    transactions.clear()
    reset_transactions()
    flash("All data has been reset.", "warning")
    return redirect(url_for("index"))
@app.route("/delete/<tid>", methods=["POST"])
def delete(tid: str):
    month = request.args.get("month")  # preserve the current month view

    # remove matching transaction
    for i, t in enumerate(transactions):
        if t.tid == tid:
            transactions.pop(i)
            save_transactions(transactions)
            flash("Transaction deleted.", "secondary")
            break

    if month:
        return redirect(url_for("index", month=month))
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)
