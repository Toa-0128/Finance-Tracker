import pandas as pd
import matplotlib.pyplot as plt

# Global variables
transactions = pd.DataFrame(
    columns=["Date", "Category", "Description", "Amount", "Type"]
)
monthly_income = 0.0
category_budgets = {}


# ------------------ Main Menu ------------------
def main_menu():
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("0. Import a CSV file")
        print("1. View all transactions")
        print("2. View Transactions by Date Range")
        print("3. Add a Transaction")
        print("4. Edit a Transaction")
        print("5. Delete a Transaction")
        print("6. Analyze Spending by Category")
        print("7. Calculate Average Monthly Spending")
        print("8. Show Top Spending Category")
        print("9. Set Monthly Income")
        print("10. Set Category Budget")
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
        elif option == "4":
            edit_transaction()
        elif option == "5":
            delete_transaction()
        elif option == "6":
            analyze_spending_by_category()
        elif option == "7":
            calculate_average_monthly_spending()
        elif option == "8":
            show_top_spending_category()
        elif option == "9":
            set_monthly_income()
        elif option == "10":
            set_category_budget()
        elif option == "12":
            visualize_spending_trends()
        elif option == "13":
            visualize_income_expense_distribution()
        elif option == "14":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Try again.")


# ------------------ File Operations ------------------
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


def save_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"Transactions saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")


# ------------------ Transaction Management ------------------
def view_all_transactions():
    if transactions.empty:
        print("No transactions found.\n")
    else:
        print("\n=== All Transactions ===")
        print(transactions, "\n")


def view_transactions_by_date():
    if transactions.empty:
        print("No transactions available.\n")
        return

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        transactions["Date"] = pd.to_datetime(transactions["Date"])
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        filtered_transactions = transactions[
            (transactions["Date"] >= start) & (transactions["Date"] <= end)
        ]

        if filtered_transactions.empty:
            print("No transactions found in this date range.\n")
        else:
            print(f"\n--- Transactions from {start_date} to {end_date} ---")
            print(filtered_transactions, "\n")
    except Exception as e:
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
        "Type": transaction_type,
    }

    transactions = pd.concat(
        [transactions, pd.DataFrame([new_data])], ignore_index=True
    )
    print("Transaction added successfully!\n")


def edit_transaction():
    global transactions
    if transactions.empty:
        print("No transactions to edit.\n")
        return

    print(transactions)
    try:
        index = int(input("Enter the index of the transaction to edit: "))
        if index < 0 or index >= len(transactions):
            print("Invalid index.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    print("Current Transaction Details:")
    print(transactions.loc[index])

    date = input("Enter new date (YYYY-MM-DD) or press Enter to keep current: ")
    category = input("Enter new category or press Enter to keep current: ")
    description = input("Enter new description or press Enter to keep current: ")
    amount = input("Enter new amount or press Enter to keep current: ")
    transaction_type = input(
        "Enter new transaction type (Income/Expense) or press Enter to keep current: "
    )

    if date:
        transactions.at[index, "Date"] = date
    if category:
        transactions.at[index, "Category"] = category
    if description:
        transactions.at[index, "Description"] = description
    if amount:
        try:
            transactions.at[index, "Amount"] = float(amount)
        except ValueError:
            print("Invalid amount. Value not changed.")
    if transaction_type:
        transactions.at[index, "Type"] = transaction_type

    print("Transaction updated successfully!\n")


def delete_transaction():
    global transactions
    if transactions.empty:
        print("No transactions to delete.\n")
        return

    print(transactions)
    try:
        index = int(input("Enter the index of the transaction to delete: "))
        if index < 0 or index >= len(transactions):
            print("Invalid index.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    confirm = input(
        f"Are you sure you want to delete transaction {index}? (y/n): "
    ).lower()
    if confirm == "y":
        transactions = transactions.drop(index).reset_index(drop=True)
        print("Transaction deleted successfully!\n")
    else:
        print("Delete cancelled.\n")


# ------------------ Budget Management ------------------
def set_monthly_income():
    global monthly_income
    try:
        income = float(input("Enter your total monthly income: "))
        if income < 0:
            print("Income cannot be negative.\n")
            return
        monthly_income = income
        print(f"Monthly income set to ${monthly_income:.2f}\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")


def set_category_budget():
    global category_budgets
    category = input("Enter the category name to set a budget for: ").capitalize()
    try:
        budget = float(input(f"Enter the budget amount for {category}: "))
        if budget < 0:
            print("Budget cannot be negative.\n")
            return
        category_budgets[category] = budget
        print(f"Budget for '{category}' set to ${budget:.2f}\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")


# ------------------ Spending Analysis ------------------
def analyze_spending_by_category():
    """
    Display total spending by category.
    Only considers transactions with Type == 'Expense'
    """
    if transactions.empty:
        print("No transactions to analyze.\n")
        return

    expenses = transactions[transactions["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("No expense transactions found.\n")
        return

    category_totals = (
        expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    )
    print("\n=== Spending by Category ===")
    print(category_totals)
    print("\nTotal Spending: $", category_totals.sum())
    print("-" * 40)


def calculate_average_monthly_spending():
    """
    Calculate and display average monthly spending.
    """
    if transactions.empty:
        print("No transactions to analyze.\n")
        return

    expenses = transactions[transactions["Type"].str.lower() == "expense"].copy()
    if expenses.empty:
        print("No expense transactions found.\n")
        return

    expenses["Date"] = pd.to_datetime(expenses["Date"])
    monthly_totals = expenses.groupby(expenses["Date"].dt.to_period("M"))[
        "Amount"
    ].sum()

    avg_spending = monthly_totals.mean()
    print("\n=== Average Monthly Spending ===")
    print(f"Average monthly spending: ${avg_spending:.2f}\n")


def show_top_spending_category():
    """
    Identify and display the category with the highest spending.
    """
    if transactions.empty:
        print("No transactions to analyze.\n")
        return

    expenses = transactions[transactions["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("No expense transactions found.\n")
        return

    category_totals = expenses.groupby("Category")["Amount"].sum()

    top_category = category_totals.idxmax()
    top_amount = category_totals.max()

    print("\n=== Top Spending Category ===")
    print(f"Category: {top_category}")
    print(f"Total Spending: ${top_amount:.2f}\n")


# ------------------ Visualization ------------------
def visualize_spending_trends():
    if transactions.empty:
        print("No data to visualize.\n")
        return

    transactions["Date"] = pd.to_datetime(transactions["Date"])

    if "Type" not in transactions.columns:
        print("Error: 'Type' column not found in transactions.")
        return

    monthly = (
        transactions.groupby([transactions["Date"].dt.to_period("M"), "Type"])["Amount"]
        .sum()
        .unstack(fill_value=0)
    )

    monthly.plot(kind="line", marker="o", title="Monthly Income vs Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    plt.show()


def visualize_income_expense_distribution():
    if transactions.empty:
        print("No transactions to visualize.\n")
        return

    summary = transactions.groupby("Type")["Amount"].sum()
    summary.plot(kind="pie", autopct="%1.1f%%", title="Income vs Expense Distribution")
    plt.ylabel("")
    plt.show()


# ------------------ Run Program ------------------
if __name__ == "__main__":
    main_menu()
