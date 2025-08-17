import csv

def add_employee():
    """Adds a new employee to the Employees.csv file."""

    # Get employee details from user input
    driver_number = input("Enter driver number: ")
    name = input("Enter name: ")
    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")
    license_number = input("Enter driver's license number: ")
    license_expiry = input("Enter license expiry date (YYYY-MM-DD): ")
    insurance_company = input("Enter insurance company: ")
    policy_number = input("Enter insurance policy number: ")
    owns_car = input("Does the driver have their own car? (Y/N): ").upper()
    balance_due = input("Enter balance due: ")

    # Prepare the data for writing to the CSV file
    employee_data = [
        driver_number,
        name,
        address,
        phone_number,
        license_number,
        license_expiry,
        insurance_company,
        policy_number,
        owns_car,
        balance_due,
    ]

    # Append the new employee data to the CSV file
    with open("Employees.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(employee_data)

    print("Employee added successfully!")

if __name__ == "__main__":
    add_employee()
