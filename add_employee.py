# add_employee.py
# Function for entering and displaying employee information. 
# Associated with employees.csv

import csv
from dateutil import parser
import datetime

def add_employee():
    """Adds a new employee to the employees.csv file."""

    # Get employee details from user input
    driver_number = input("Enter driver number: ")
    name = input("Enter name: ")
    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")
    license_number = input("Enter driver's license number: ")
    while True:
        date_input = input("Enter license expiry date: ")
        try:
            license_expiry = parser.parse(date_input).date()
            break
        except parser.ParserError:
            print("Invalid date format. Please try again.")
    license_expiry_str = license_expiry.strftime("%Y-%m-%d")
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
    with open("employees.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(employee_data)

    print("\n-----------------------------------------")
    print("   New Employee Added Successfully!")
    print("-----------------------------------------")
    print(f"  Driver Number:       {driver_number}")
    print(f"  Name:                {name}")
    print(f"  Address:             {address}")
    print(f"  Phone Number:        {phone_number}")
    print(f"  License Number:      {license_number}")
    print(f"  License Expiry:      {license_expiry}")
    print(f"  Insurance Company:   {insurance_company}")
    print(f"  Policy Number:       {policy_number}")
    print(f"  Owns Car:            {owns_car}")
    print(f"  Balance Due:         {balance_due}")
    print("-----------------------------------------")

if __name__ == "__main__":
    add_employee()