"""
Institute Expense Tracker
-------------------------
Records daily operational expenses (stationery, internet, refreshments,
transport, ...) and stores them in expenses.csv so they survive between runs.

Concepts used: file handling (csv), exception handling
(FileNotFoundError, ValueError), sets and comprehensions.
"""

import csv
import os
from datetime import datetime

# Always read/write next to this script, no matter where it is run from.
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.csv")
FIELDS = ["date", "item", "category", "amount"]


def load_expenses():
    """Load saved expenses. Start with an empty list if the file is missing."""
    expenses = []
    try:
        with open(FILE_NAME, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    expenses.append(
                        {
                            "date": row["date"],
                            "item": row["item"],
                            "category": row["category"],
                            "amount": float(row["amount"]),
                        }
                    )
                except (KeyError, ValueError, TypeError):
                    print(f"  ! Skipped a damaged row in {os.path.basename(FILE_NAME)}: {row}")
        print(f"  Loaded {len(expenses)} saved expense(s) from {os.path.basename(FILE_NAME)}.")
    except FileNotFoundError:
        print(f"  No {os.path.basename(FILE_NAME)} found - starting with an empty expense list.")
    return expenses


def save_expense(expense):
    """Append one expense to the CSV file (writes the header the first time)."""
    write_header = not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(expense)


def ask_date():
    """Ask for a date until a valid YYYY-MM-DD value is entered."""
    while True:
        value = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("  Invalid date. Please use the format YYYY-MM-DD (e.g. 2025-03-18).")


def ask_text(prompt):
    """Ask for a non-empty text value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


def ask_amount():
    """Ask for an amount until a valid positive number is entered."""
    while True:
        raw = input("Enter amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                raise ValueError("amount must be positive")
            return amount
        except ValueError:
            print("  Invalid amount. Please enter a valid positive number (e.g. 1500 or 249.50).")


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    expense = {
        "date": ask_date(),
        "item": ask_text("Enter item name: ").title(),
        "category": ask_text("Enter category: ").title(),
        "amount": ask_amount(),
    }
    expenses.append(expense)
    save_expense(expense)
    print(f"  Saved: {expense['item']} ({expense['category']}) - {expense['amount']:.2f}")


def show_all(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("  No expenses recorded yet.")
        return
    print(f"{'No.':<4} {'Date':<12} {'Item':<22} {'Category':<14} {'Amount':>10}")
    print("-" * 66)
    for number, e in enumerate(expenses, start=1):
        print(f"{number:<4} {e['date']:<12} {e['item']:<22} {e['category']:<14} {e['amount']:>10.2f}")
    print("-" * 66)
    print(f"{'Grand total':<54} {sum(e['amount'] for e in expenses):>10.2f}")


def totals_by_category(expenses):
    print("\n--- Total Expenses by Category ---")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    # A set keeps every category only once, however many times it was entered.
    categories = {e["category"] for e in expenses}
    print("Unique categories:", ", ".join(sorted(categories)))
    print()

    # Dictionary comprehension: one total per unique category.
    totals = {
        category: sum(e["amount"] for e in expenses if e["category"] == category)
        for category in categories
    }
    for category in sorted(totals):
        print(f"  {category:<16} {totals[category]:>10.2f}")
    print("  " + "-" * 27)
    print(f"  {'Total':<16} {sum(totals.values()):>10.2f}")


def main():
    print("=" * 40)
    print("   INSTITUTE EXPENSE TRACKER")
    print("=" * 40)
    expenses = load_expenses()

    while True:
        print("\n1. Add New Expense")
        print("2. Show All Expenses")
        print("3. Calculate Total Expenses by Category")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_all(expenses)
        elif choice == "3":
            totals_by_category(expenses)
        elif choice == "4":
            print("Goodbye! Your expenses are saved in expenses.csv.")
            break
        else:
            print("  Invalid option. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
