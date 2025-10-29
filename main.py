import pandas as pd
from visualization import (
    plot_monthly_trend,
    plot_spending_by_category,
    plot_spending_distribution,
)
from file_operations import save_to_csv

# Sample data
df = pd.DataFrame(
    [
        {
            "Date": "2024-10-01",
            "Category": "Food",
            "Description": "Grocery",
            "Amount": 50.75,
        },
        {
            "Date": "2024-10-02",
            "Category": "Rent",
            "Description": "Monthly Rent",
            "Amount": 1200.00,
        },
        {
            "Date": "2024-10-03",
            "Category": "Food",
            "Description": "Dinner",
            "Amount": 30.00,
        },
    ]
)


def show_menu():
    print("\n=== Personal Finance Tracker ===")
    print("1. Visualize Monthly Spending Trend")
    print("2. Visualize Spending by Category")
    print("3. Visualize Spending Distribution")
    print("4. Save Transactions to CSV")
    print("5. Exit")
    choice = input("Choose an option (1-5): ")
    return choice


def main():
    while True:
        choice = show_menu()
        if choice == "1":
            plot_monthly_trend(df)
        elif choice == "2":
            plot_spending_by_category(df)
        elif choice == "3":
            plot_spending_distribution(df)
        elif choice == "4":
            filename = input("Enter file name to save (e.g., 'transactions.csv'): ")
            save_to_csv(df, filename)
        elif choice == "5":
            print("Exiting the Personal Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
