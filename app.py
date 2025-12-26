from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

# keep your current file name (capital B)
from budget import add_transaction, monthly_totals, category_breakdown, Transaction

app = Flask(__name__)
app.secret_key = "dev"  # ok for a student project

# simple in-memory storage (we can add database later)
transactions: list[Transaction] = []


@app.route("/")
def index():
    month = request.args.get("month") or datetime.now().strftime("%Y-%m")

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
        breakdown=breakdown,
        recent=recent
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

            flash("Expense added!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
