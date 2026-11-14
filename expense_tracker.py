"""Institute Expense Tracker.

Records daily operational expenses in expenses.csv
(columns: date,item,category,amount).
"""

import csv
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDS = ["date", "item", "category", "amount"]


def load_expenses(filename=FILE_NAME):
    """Load saved expenses. Return an empty list if the file does not exist."""
    expenses = []
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    row["amount"] = float(row["amount"])
                    expenses.append(row)
                except (ValueError, TypeError, KeyError):
                    print(f"Skipped a corrupted row in {filename}: {row}")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty expense list.")
    return expenses


def save_expense(expense, filename=FILE_NAME):
    """Append one expense to the CSV file (writes the header for a new file)."""
    try:
        with open(filename, "r", encoding="utf-8"):
            needs_header = False
    except FileNotFoundError:
        needs_header = True

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(expense)


def ask_text(prompt):
    """Ask until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def ask_date():
    """Ask for a date in YYYY-MM-DD format until it is valid."""
    while True:
        value = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD, e.g. 2025-03-15.")


def ask_amount():
    """Ask for a positive number until a valid amount is entered."""
    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            return amount
        except ValueError:
            print("Invalid amount. Please enter a positive number, e.g. 1250.50")


def add_expense(expenses):
    expense = {
        "date": ask_date(),
        "item": ask_text("Item name: "),
        "category": ask_text("Category: ").title(),
        "amount": ask_amount(),
    }
    expenses.append(expense)
    save_expense(expense)
    print("Expense saved.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'Date':<12}{'Item':<22}{'Category':<16}{'Amount':>10}")
    print("-" * 60)
    for e in expenses:
        print(f"{e['date']:<12}{e['item']:<22}{e['category']:<16}{e['amount']:>10.2f}")

    unique_categories = {e["category"] for e in expenses}  # set
    print("\nUnique categories:", ", ".join(sorted(unique_categories)))


def show_category_totals(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    categories = {e["category"] for e in expenses}  # set of unique categories
    totals = {
        c: sum(e["amount"] for e in expenses if e["category"] == c)
        for c in sorted(categories)
    }

    print(f"\n{'Category':<20}{'Total':>12}")
    print("-" * 32)
    for category, total in totals.items():
        print(f"{category:<20}{total:>12.2f}")
    print("-" * 32)
    print(f"{'Grand Total':<20}{sum(totals.values()):>12.2f}")


def main():
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} saved expense(s).")

    while True:
        print("\n=== Institute Expense Tracker ===")
        print("1. Add New Expense")
        print("2. Show All Expenses")
        print("3. Calculate Total Expenses by Category")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_category_totals(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
