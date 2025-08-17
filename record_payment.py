
import csv
import datetime

def record_payment():
    """Records a payment from a driver."""

    # Get payment details from user input
    driver_number = input("Enter driver number: ")
    payment_date = input("Enter payment date (YYYY-MM-DD) or press Enter for today: ")
    if not payment_date:
        payment_date = datetime.date.today().strftime("%Y-%m-%d")
    payment_amount = float(input("Enter payment amount: "))
    reason = input("Enter reason for payment: ")
    payment_method = input("Enter payment method (Cash, Debit, Visa): ")

    # Get the next payment ID
    next_payment_id = 1
    try:
        with open("Payments.csv", "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                next_payment_id = int(last_row[0]) + 1
    except (IOError, StopIteration):
        pass  # File doesn't exist or is empty

    # 1. Add to Payments.csv
    payment_data = [
        next_payment_id,
        driver_number,
        payment_date,
        f"{payment_amount:.2f}",
        reason,
        payment_method,
    ]
    with open("Payments.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(payment_data)

    # 2. Update Employees.csv
    employees = []
    with open("Employees.csv", "r") as f:
        reader = csv.reader(f)
        employees = list(reader)

    for i in range(1, len(employees)):
        if employees[i][0] == driver_number:
            employees[i][9] = f"{float(employees[i][9]) - payment_amount:.2f}"
            break

    with open("Employees.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(employees)

    print("\n-----------------------------------------")
    print("   Payment Recorded Successfully!")
    print("-----------------------------------------")
    print(f"  Payment ID:         {next_payment_id}")
    print(f"  Driver Number:      {driver_number}")
    print(f"  Payment Date:       {payment_date}")
    print(f"  Payment Amount:     ${payment_amount:.2f}")
    print(f"  Reason:             {reason}")
    print(f"  Payment Method:     {payment_method}")
    print("-----------------------------------------")

if __name__ == "__main__":
    record_payment()
