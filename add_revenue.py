
import csv
import datetime

def add_revenue():
    """Adds a new revenue record to the Revenues.csv file."""

    # Read default values from Defaults.dat
    with open("Defaults.dat", "r") as f:
        lines = f.readlines()
        defaults = {}
        for line in lines:
            key, value = line.strip().split("=")
            defaults[key] = value

    next_transaction_number = int(defaults["NEXT_TRANSACTION_NUMBER"])
    hst_rate = float(defaults["HST_RATE"])

    # Get revenue details from user input
    transaction_date = input("Enter transaction date (YYYY-MM-DD) or press Enter for today: ")
    if not transaction_date:
        transaction_date = datetime.date.today().strftime("%Y-%m-%d")
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

    # Update the next transaction number in Defaults.dat
    defaults["NEXT_TRANSACTION_NUMBER"] = str(next_transaction_number + 1)
    with open("Defaults.dat", "w") as f:
        for key, value in defaults.items():
            f.write(f"{key}={value}\n")

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
