
import csv

def show_employee_financials():
    """Displays a financial report for each employee."""

    # Read employee data
    employees = {}
    with open("Employees.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            employees[row[0]] = {"name": row[1], "balance": float(row[9])}

    # Calculate total revenue per driver
    revenues = {}
    with open("Revenues.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            driver_number = row[3]
            amount = float(row[4])
            if driver_number in revenues:
                revenues[driver_number] += amount
            else:
                revenues[driver_number] = amount

    # Calculate total payments per driver
    payments = {}
    with open("Payments.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            driver_number = row[1]
            amount = float(row[3])
            if driver_number in payments:
                payments[driver_number] += amount
            else:
                payments[driver_number] = amount

    # Display the report
    print("Employee Financial Report")
    print("=========================")

    for driver_number, details in employees.items():
        print(f"Driver: {details['name']} (#{driver_number})")
        print(f"  Current Balance Due: ${details['balance']:,.2f}")
        print(f"  Total Revenue Generated: ${revenues.get(driver_number, 0):,.2f}")
        print(f"  Total Payments Made: ${payments.get(driver_number, 0):,.2f}")
        print("-------------------------")

if __name__ == "__main__":
    show_employee_financials()
