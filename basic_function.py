import pandas as pd

import matplotlib.pyplot as plt

transactions = pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type"])

def main_menu():
  while True:
    print("\n=== Personal Finance Tracker ===")
    print("0. Import a CSV file")
    print("1. View all transactions")
    print("2. View Transactions by Date Range")
    print("3. Add a Transaction")
    print("12. Visualize Spending Trends")
    print("13. Visualize Income vs Expense Distribution")
    print("14. Exit")

    option = input("Choose an option: ")
    if option == "0":
      import_csv()
    elif option == "1":
      view_all_transactions()
    elif option == "2":
      view_transactions_by_date()
    elif option == "3":
      add_transaction()
    elif option == "12":
        visualize_spending_trends()
    elif option == "13":
        visualize_income_expense_distribution()
    elif option == "14":
      print("Exiting the program.")
      break
    else:
      print("Invalid option. Try again.")

def import_csv():
    global transactions
    filename = input("Enter CSV file name: ")
    try:
        transactions = pd.read_csv(filename)
        print("File imported successfully!\n")
    except FileNotFoundError:
        print("Error: File not found.\n")
    except Exception as e:
        print(f"Error reading file: {e}\n")

def view_all_transactions():
    if transactions.empty:
        print("No transactions found.\n")
    else:
        print("\n=== All Transactions =====")
        print(transactions, "\n")

def view_transactions_by_date():
    if transactions.empty:
        print("No transactions available.\n")
        return

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-MM): ")

    try:
        transactions["Date"] = pd.to_datetime(transactions["Date"])
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        filtered_transactions = transactions[(transactions["Date"] >= start) & (transactions["Date"] <= end)]

        if filtered_transactions.empty:
            print("No transactions found in this date range.\n")

        else:
              print(f"\n--- Transactions from {start_date} to {end_date} ---")
              print(filtered_transactions, "\n")

    except Exception  as e:
          print(f"Error: {e}\n")

def add_transaction():
    global transactions
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g. Food, Rent): : ")
    description = input("Enter a description: ")

    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Invalid amount. Transaction not added.\n")
        return
    transaction_type = input("Enter transaction type (Income/Expense): ")


    new_data = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount,
        "Type": transaction_type
        }

    transactions = pd.concat([transactions, pd.DataFrame([new_data])], ignore_index=True)
    print("Transaction added successfully!\n")


def visualize_spending_trends():
    if transactions.empty:
        print("No data to visualize.\n")
        return

    transactions["Date"] = pd.to_datetime(transactions["Date"])

    # Ensure that the 'Type' column exists and handle potential missing values
    if 'Type' not in transactions.columns:
        print("Error: 'Type' column not found in transactions.")
        return

    monthly = transactions.groupby(
    [transactions["Date"].dt.to_period("M"), "Type"]
    )["Amount"].sum().unstack(fill_value=0)


    monthly.plot(kind="line", marker="o", title="Monthly Income vs Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    plt.show()

def visualize_spending_vs_budget():
    if transactions.empty:
        print("No transactions available.\n")
        return

    expenses = transactions[transactions["Type"] == "Expense"]
    spending = expenses.groupby("Category")["Amount"].sum()

    # This function requires category_budgets which is not defined.
    # Assuming a dictionary named category_budgets exists with category limits.
    # If not, this function will raise an error.
    # Example: category_budgets = {"Food": 500, "Rent": 1000}
    try:
        combined = pd.DataFrame({
            "Spending": spending,
            "Budget": pd.Series(category_budgets)
        }).fillna(0)

        combined.plot(kind="bar", title="Spending vs Budget by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        plt.show()
    except NameError:
        print("Error: 'category_budgets' is not defined. Cannot visualize spending vs budget.")


def visualize_income_expense_distribution():
    if transactions.empty:
        print("No transactions to visualize.\n")
        return

    summary = transactions.groupby("Type")["Amount"].sum()
    summary.plot(kind="pie", autopct="%1.1f%%", title="Income vs Expense Distribution")
    plt.ylabel("")
    plt.show()

main_menu()
