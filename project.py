import argparse
import sqlite3
from datetime import date, timedelta
import json
import matplotlib.pyplot as plt

DB_PATH = "expenses.db"

def initialize_db(db_path: str = DB_PATH) -> None:
    """Create the expenses table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def add_expense(
    amount: float,
    category: str,
    on_date: str | None = None,
    db_path: str = DB_PATH,
) -> dict:
    """
    Insert a new expense into the database.
    on_date should be 'YYYY-MM-DD'; if None, uses today.
    Returns the dict of the added entry.
    """
    if on_date is None:
        on_date = date.today().isoformat()
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, on_date),
    )
    conn.commit()
    conn.close()
    return {"amount": amount, "category": category, "date": on_date}

def get_all_expenses(db_path: str = DB_PATH) -> list[dict]:
    """
    Fetch all expenses from the database as a list of dicts:
    [{"amount":…, "category":…, "date":…}, …]
    """
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, date FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"amount": r[0], "category": r[1], "date": r[2]}
        for r in rows
    ]

def get_total_by_category(db_path: str = DB_PATH) -> dict[str, float]:
    """Return a dict mapping category → sum of amounts."""
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def generate_report(
    period: str = "monthly", db_path: str = DB_PATH
) -> dict:
    """
    Produce a report dict with keys:
      - period (daily, weekly, monthly, all)
      - total: sum of all amounts in that period
      - by_category: dict of category sums
      - first_date / last_date of an expense in that slice
    """
    initialize_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, date FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    # Build list of dicts
    expenses = [{"amount": r[0], "category": r[1], "date": r[2]} for r in rows]

    if period != "all":
        today = date.today()
        cutoff_map = {
            "daily": today,
            "weekly": today - timedelta(days=7),
            "monthly": today - timedelta(days=30),
        }
        cutoff = cutoff_map[period]
        expenses = [e for e in expenses if date.fromisoformat(e["date"]) >= cutoff]

    total = sum(e["amount"] for e in expenses)
    by_cat: dict[str, float] = {}
    dates: list[date] = []

    for e in expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
        dates.append(date.fromisoformat(e["date"]))

    return {
        "period": period,
        "total": total,
        "by_category": by_cat,
        "first_date": min(dates).isoformat() if dates else None,
        "last_date": max(dates).isoformat() if dates else None,
    }

def plot_expenses(period: str = "monthly", db_path: str = DB_PATH) -> None:
    """
    Plot a bar chart of expenses-by-category for the given period
    and save it as PNG.
    """
    report = generate_report(period, db_path)
    data = report["by_category"]
    if not data:
        print("No data to plot.")
        return

    cats = list(data.keys())
    vals = list(data.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(cats, vals, color="skyblue")
    plt.title(f"Expenses by Category ({period})")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45, ha="right")

    for bar in bars:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, y + 0.5, f"{y:.2f}", ha="center")

    plt.tight_layout()
    fname = f"expenses_{period}.png"
    plt.savefig(fname)
    print(f"Saved plot to {fname}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Personal Expense Tracker")
    subs = parser.add_subparsers(dest="cmd")

    p_add = subs.add_parser("add", help="Add a new expense")
    p_add.add_argument("--amount", type=float, required=True)
    p_add.add_argument("--category", type=str, required=True)
    p_add.add_argument("--date", type=str)

    p_report = subs.add_parser("report", help="Show textual report")
    p_report.add_argument(
        "--period",
        choices=["daily", "weekly", "monthly", "all"],
        default="monthly",
    )

    p_plot = subs.add_parser("plot", help="Generate bar chart")
    p_plot.add_argument(
        "--period",
        choices=["daily", "weekly", "monthly", "all"],
        default="monthly",
    )

    args = parser.parse_args()

    if args.cmd == "add":
        entry = add_expense(args.amount, args.category, args.date)
        print(f"Added: {entry}")
    elif args.cmd == "report":
        rpt = generate_report(args.period)
        print(json.dumps(rpt, ensure_ascii=False, indent=2))
    elif args.cmd == "plot":
        plot_expenses(args.period)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
