
import csv

def calculate_profit():
    """Calculates and displays the company's profit."""

    # Calculate total revenue
    total_revenue = 0
    with open("Revenues.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            total_revenue += float(row[4])

    # Calculate total expenses
    total_expenses = 0
    with open("Expenses.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            total_expenses += float(row[7])

    # Calculate profit
    profit = total_revenue - total_expenses

    # Display the results
    print("Company Profitability Report")
    print("============================")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Expenses: ${total_expenses:,.2f}")
    print("----------------------------")
    print(f"Profit: ${profit:,.2f}")

if __name__ == "__main__":
    calculate_profit()
