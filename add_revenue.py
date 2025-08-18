# add_revenue.py
# Function for entering and displaying company revenue data for use in financial reports.
# Associated with revenues.csv

import csv
from dateutil import parser
import datetime

def add_revenue():
    """Adds a new revenue record to the Revenues.csv file."""

    # Read default values from Defaults.dat
    defaults = {}
    with open("Defaults.dat", "r") as f:
        for line in f:
            key, value = line.strip().split(':')
            defaults[key] = float(value)
    hst_rate = defaults.get('hst_rate', 0.15)

    # Get the next transaction number from Revenues.csv
    next_transaction_number = 1
    try:
        with open("Revenues.csv", "r") as f:
            reader = csv.reader(f)
            all_lines = list(reader)
            if len(all_lines) > 1:
                last_line = all_lines[-1]
                next_transaction_number = int(last_line[0]) + 1
    except (IOError, IndexError, StopIteration):
        pass

    # Get revenue details from user input
    while True:
        date_input = input("Enter transaction date or press Enter for today: ")
        if not date_input:
            transaction_date = datetime.date.today()
            break
        try:
            transaction_date = parser.parse(date_input).date()
            break
        except parser.ParserError:
            print("Invalid date format. Please try again.")
    transaction_date_str = transaction_date.strftime("%Y-%m-%d")
    description = input("Enter description: ")
    driver_number = input("Enter driver number: ")
    amount = float(input("Enter amount: "))

    # Calculate HST and total
    hst = amount * hst_rate
    total = amount + hst

    # Prepare the data for writing to the CSV file
    revenue_data = [
        next_transaction_number,
        transaction_date,
        description,
        driver_number,
        f"{amount:.2f}",
        f"{hst:.2f}",
        f"{total:.2f}",
    ]

    # Append the new revenue data to the CSV file
    with open("Revenues.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(revenue_data)

    print("\n-----------------------------------------")
    print("   Revenue Recorded Successfully!")
    print("-----------------------------------------")
    print(f"  Transaction Number:  {next_transaction_number}")
    print(f"  Transaction Date:    {transaction_date}")
    print(f"  Driver Number:       {driver_number}")
    print(f"  Description:         {description}")
    print(f"  Amount:              ${amount:.2f}")
    print(f"  HST:                 ${hst:.2f}")
    print(f"  Total:               ${total:.2f}")
    print("-----------------------------------------")

if __name__ == "__main__":
    add_revenue()
