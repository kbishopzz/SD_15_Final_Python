
import csv
import datetime

def add_rental():
    """Tracks a new car rental."""

    # Read default values from Defaults.dat
    with open("Defaults.dat", "r") as f:
        lines = f.readlines()
        defaults = {}
        for line in lines:
            key, value = line.strip().split("=")
            defaults[key] = value

    daily_rate = float(defaults["DAILY_RENTAL_FEE"])
    weekly_rate = float(defaults["WEEKLY_RENTAL_FEE"])
    hst_rate = float(defaults["HST_RATE"])
    next_transaction_number = int(defaults["NEXT_TRANSACTION_NUMBER"])

    # Get rental details from user input
    driver_number = input("Enter driver number: ")
    start_date = input("Enter start date (YYYY-MM-DD) or press Enter for today: ")
    if not start_date:
        start_date = datetime.date.today().strftime("%Y-%m-%d")
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
        with open("Rentals.csv", "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                next_rental_id = int(last_row[0]) + 1
    except (IOError, StopIteration):
        pass  # File doesn't exist or is empty

    # 1. Add to Rentals.csv
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
    with open("Rentals.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(rental_data)

    # 2. Add to Revenues.csv
    revenue_data = [
        next_transaction_number,
        start_date,
        f"Car rental - {rental_type_desc}",
        driver_number,
        f"{rental_cost:.2f}",
        f"{hst:.2f}",
        f"{total_cost:.2f}",
    ]
    with open("Revenues.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(revenue_data)

    # 3. Update Employees.csv
    employees = []
    with open("Employees.csv", "r") as f:
        reader = csv.reader(f)
        employees = list(reader)

    for i in range(1, len(employees)):
        if employees[i][0] == driver_number:
            employees[i][9] = f"{float(employees[i][9]) + total_cost:.2f}"
            break

    with open("Employees.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(employees)

    # Update the next transaction number in Defaults.dat
    defaults["NEXT_TRANSACTION_NUMBER"] = str(next_transaction_number + 1)
    with open("Defaults.dat", "w") as f:
        for key, value in defaults.items():
            f.write(f"{key}={value}\n")

    print("Rental recorded successfully!")

if __name__ == "__main__":
    add_rental()
