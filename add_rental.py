# add_rental.py
# Function for entering rental information of the car fleet.The core function of the company and used in financial and employee reports
# Associated with rentals.csv, revenues.csv, and employees.csv

import csv
from dateutil import parser
import datetime

def add_rental():
    """Tracks a new car rental."""

    # Read default values from Defaults.dat
    defaults = {}
    with open("Defaults.dat", "r") as f:
        for line in f:
            key, value = line.strip().upper().split(':')
            defaults[key] = float(value)
    daily_rate = defaults.get('DAILY_RENTAL_FEE', 20.00)
    weekly_rate = defaults.get('WEEKLY_RENTAL_FEE', 100.00)
    hst_rate = defaults.get('HST_RATE', 0.15)

    # Get the next transaction number from revenues.csv
    next_transaction_number = 1
    try:
        with open("revenues.csv", "r") as f:
            reader = csv.reader(f)
            all_lines = list(reader)
            if len(all_lines) > 1:
                last_line = all_lines[-1]
                next_transaction_number = int(last_line[0]) + 1
    except (IOError, IndexError, StopIteration):
        pass

    # Get rental details from user input
    driver_number = input("Enter driver number: ")
    while True:
        date_input = input("Enter start date or press Enter for today: ")
        if not date_input:
            start_date = datetime.date.today()
            break
        try:
            start_date = parser.parse(date_input).date()
            break
        except parser.ParserError:
            print("Invalid date format. Please try again.")
    start_date_str = start_date.strftime("%Y-%m-%d")
    car_number = input("Enter car number (1-4): ")
    rental_type = input("Enter rental type (D for Day, W for Week): ").upper()

    if rental_type == "D":
        num_days = 1
        rental_cost = daily_rate
        rental_type_desc = "Daily"
    elif rental_type == "W":
        num_days = 7
        rental_cost = weekly_rate
        rental_type_desc = "Weekly"
    else:
        print("Invalid rental type.")
        return

    # Calculate HST and total
    hst = rental_cost * hst_rate
    total_cost = rental_cost + hst

    # Get the next rental ID
    next_rental_id = 1
    try:
        with open("rentals.csv", "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                next_rental_id = int(last_row[0]) + 1
    except (IOError, StopIteration):
        pass  # File doesn't exist or is empty

    # 1. Add to rentals.csv
    rental_data = [
        next_rental_id,
        driver_number,
        start_date,
        car_number,
        rental_type_desc,
        num_days,
        f"{rental_cost:.2f}",
        f"{hst:.2f}",
        f"{total_cost:.2f}",
    ]
    with open("rentals.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(rental_data)

    # 2. Add to revenues.csv
    revenue_data = [
        next_transaction_number,
        start_date,
        f"Car rental - {rental_type_desc}",
        driver_number,
        f"{rental_cost:.2f}",
        f"{hst:.2f}",
        f"{total_cost:.2f}",
    ]
    with open("revenues.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(revenue_data)

    # 3. Update employees.csv
    employees = []
    with open("employees.csv", "r") as f:
        reader = csv.reader(f)
        employees = list(reader)

    for i in range(1, len(employees)):
        if employees[i][0] == driver_number:
            try:
                balance = float(employees[i][9])
            except (ValueError, IndexError):
                balance = 0.0
            employees[i][9] = f"{balance + total_cost:.2f}"
            break

    with open("employees.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(employees)

    print("\n-----------------------------------------")
    print("   Rental Recorded Successfully!")
    print("-----------------------------------------")
    print(f"  Rental ID:          {next_rental_id}")
    print(f"  Driver Number:      {driver_number}")
    print(f"  Start Date:         {start_date}")
    print(f"  Car Number:         {car_number}")
    print(f"  Rental Type:        {rental_type_desc}")
    print(f"  Number of Days:     {num_days}")
    print("-----------------------------------------")
    print(f"  Rental Cost:        ${rental_cost:.2f}")
    print(f"  HST:                ${hst:.2f}")
    print(f"  Total Cost:         ${total_cost:.2f}")
    print("-----------------------------------------")

if __name__ == "__main__":
    add_rental()