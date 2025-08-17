
import csv
import datetime

def add_expense():
    """Adds a new expense record to the Expenses.csv file."""

    # Read default values from Defaults.dat
    with open("Defaults.dat", "r") as f:
        lines = f.readlines()
        defaults = {}
        for line in lines:
            key, value = line.strip().split("=")
            defaults[key] = value

    hst_rate = float(defaults["HST_RATE"])

    # Get expense details from user input
    invoice_number = input("Enter invoice number: ")
    invoice_date = input("Enter invoice date (YYYY-MM-DD) or press Enter for today: ")
    if not invoice_date:
        invoice_date = datetime.date.today().strftime("%Y-%m-%d")
    driver_number = input("Enter driver number: ")

    items = []
    while True:
        item_number = input("Enter item number (or press Enter to finish): ")
        if not item_number:
            break
        description = input("Enter description: ")
        cost = float(input("Enter cost: "))
        quantity = int(input("Enter quantity: "))
        item_total = cost * quantity
        items.append([item_number, description, cost, quantity, item_total])

    # Calculate subtotal, HST, and total
    subtotal = sum(item[4] for item in items)
    hst = subtotal * hst_rate
    total = subtotal + hst

    # Prepare the data for writing to the CSV file
    with open("Expenses.csv", "a", newline="") as f:
        writer = csv.writer(f)
        for item in items:
            expense_data = (
                [
                    invoice_number,
                    invoice_date,
                    driver_number,
                ]
                + item
                + [f"{subtotal:.2f}", f"{hst:.2f}", f"{total:.2f}"]
            )
            writer.writerow(expense_data)

    print("Expense recorded successfully!")

if __name__ == "__main__":
    add_expense()
