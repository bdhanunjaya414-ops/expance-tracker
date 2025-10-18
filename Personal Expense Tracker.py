import csv
import os
from datetime import datetime

# Folder and file setup
if not os.path.exists('data'):
    os.makedirs('data')

file_path = 'data/expenses.csv'
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Amount', 'Description'])

# Function to add expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD) [default: today]: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    category = input("Enter category (Food, Transport, etc.): ")
    amount = input("Enter amount: ")
    description = input("Enter description: ")

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print("Expense added successfully!\n")

# Function to view all expenses
def view_expenses():
    print("\n--- All Expenses ---")
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        total = 0
        for row in reader:
            print(f"Date: {row[0]}, Category: {row[1]}, Amount: {row[2]}, Description: {row[3]}")
            total += float(row[2])
    print(f"Total Expenses: ${total}\n")

# Function to calculate monthly savings
def monthly_summary():
    month = input("Enter month (YYYY-MM): ")
    total = 0
    print(f"\n--- Expenses for {month} ---")
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if row[0].startswith(month):
                print(f"Date: {row[0]}, Category: {row[1]}, Amount: {row[2]}, Description: {row[3]}")
                total += float(row[2])
    print(f"Total Expenses for {month}: ${total}\n")

# Main menu
def main():
    while True:
        print("=== Personal Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Summary")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            monthly_summary()
        elif choice == '4':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
