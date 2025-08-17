import add_employee
import add_revenue
import add_expense
import add_rental
import record_payment
import calculate_profit
import employee_financials
import csv
import datetime

def charge_stand_fees():
    # Check if it's the first day of the month
    today = datetime.date.today()
    # To test, uncomment the line below and set a date
    # today = datetime.date(2025, 8, 1)
    if today.day != 1:
        return

    # Check if the fees have already been charged this month
    try:
        with open("last_run.dat", "r") as f:
            last_run_date_str = f.read().strip()
            last_run_date = datetime.datetime.strptime(last_run_date_str, "%Y-%m-%d").date()
            if last_run_date.year == today.year and last_run_date.month == today.month:
                return
    except FileNotFoundError:
        pass

    # Get the stand fee and HST rate. Since Defaults.dat is not readable, use hardcoded values.
    stand_fee = 175.00
    hst_rate = 0.15

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

    # Read employees and identify those who own their car
    employees_to_charge = []
    employees_data = []
    try:
        with open("Employees.csv", "r", newline='') as f:
            reader = csv.reader(f)
            employees_data = list(reader)

        for i in range(1, len(employees_data)):
            row = employees_data[i]
            if len(row) > 8 and row[8].upper() == 'Y':
                employees_to_charge.append(row)
    except FileNotFoundError:
        print("Employees.csv not found. Cannot charge stand fees.")
        return

    if not employees_to_charge:
        return

    print("Charging monthly stand fees...")

    for employee in employees_to_charge:
        driver_number = employee[0]

        hst = stand_fee * hst_rate
        total = stand_fee + hst
        revenue_data = [
            next_transaction_number,
            str(today),
            "Monthly Stand Fees",
            driver_number,
            f"{stand_fee:.2f}",
            f"{hst:.2f}",
            f"{total:.2f}",
        ]
        with open("Revenues.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(revenue_data)

        next_transaction_number += 1

        for i in range(1, len(employees_data)):
            if employees_data[i][0] == driver_number:
                current_balance = float(employees_data[i][9])
                new_balance = current_balance + total
                employees_data[i][9] = f"{new_balance:.2f}"
                break

    with open("Employees.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(employees_data)

    with open("last_run.dat", "w") as f:
        f.write(str(today))

    print("Monthly stand fees charged successfully.")


def pause_and_prompt():
    print("\n--- Action Completed ---")
    while True:
        choice = input("Enter 'C' to continue or 'Q' to quit: ").lower()
        if choice == 'q':
            print("Exiting program.")
            exit()
        elif choice == 'c':
            break
        else:
            print("Invalid choice. Please enter 'c' or 'q'.")

def main():

    charge_stand_fees()
    while True:
        print("HAB Taxi Services")
        print("Company Services System")
        print("1. Enter a New Employee (driver).")
        print("2. Enter Company Revenues.")
        print("3. Enter Company Expenses.")
        print("4. Track Car Rentals.")
        print("5. Record Employee Payment.")
        print("6. Print Company Profit Listing.")
        print("7. Print Driver Financial Listing.")
        print("8. Quit Program.")

        choice = input("Enter choice (1-8): ")

        if choice == '1':
            add_employee.add_employee()
            pause_and_prompt()
        elif choice == '2':
            add_revenue.add_revenue()
            pause_and_prompt()
        elif choice == '3':
            add_expense.add_expense()
            pause_and_prompt()
        elif choice == '4':
            add_rental.add_rental()
            pause_and_prompt()
        elif choice == '5':
            record_payment.record_payment()
            pause_and_prompt()
        elif choice == '6':
            calculate_profit.calculate_profit()
            pause_and_prompt()
        elif choice == '7':
            employee_financials.show_employee_financials()
            pause_and_prompt()
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
