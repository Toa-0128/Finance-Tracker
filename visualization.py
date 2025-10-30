import matplotlib.pyplot as plt
import pandas as pd


def plot_monthly_trend(df):
    """
    df: pandas DataFrame
    Columns: Date, Amount
    Display monthly total spending as a line chart
    """
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_totals = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()

    monthly_totals.plot(kind="line", marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.grid(True)
    plt.show()


def plot_spending_by_category(df):
    """
    df: pandas DataFrame
    Display total spending by category as a bar chart
    """
    category_totals = df.groupby("Category")["Amount"].sum()
    category_totals.plot(kind="bar", color="skyblue")
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.show()


def plot_spending_distribution(df):
    """
    df: pandas DataFrame
    Display spending distribution by category as a pie chart
    """
    category_totals = df.groupby("Category")["Amount"].sum()
    category_totals.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Spending Distribution")
    plt.ylabel("")
    plt.show()
