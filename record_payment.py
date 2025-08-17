
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
    try:
        with open("Payments.csv", "r") as f:
            last_line = f.readlines()[-1]
            last_payment_id = int(last_line.split(",")[0])
            next_payment_id = last_payment_id + 1
    except (IOError, IndexError):
        next_payment_id = 1

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

    print("Payment recorded successfully!")

if __name__ == "__main__":
    record_payment()
