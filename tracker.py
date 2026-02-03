import json
import os
import sys
from datetime import datetime

EXPENSE_FILE = 'expense.json'

CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']

class Colors :
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_success(message):
    print(f"{Colors.Green}[SUCCESS]{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED} [ERROR] {Colors.END} {message}")

def print_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {message}")




def load_expenses():
    try:
        if not os.path.exists(EXPENSE_FILE):
            print_info("No such thing exists. Start fresh mfs!")
            return []
    
        with open(EXPENSE_FILE, 'r') as file:
            expenses = json.load(file)
            print_success(f"Loaded: {len(expenses)} expense(s)")
        return expenses 
    
    except json.JSONDecodeError:
        print_error("Expense file is corrupted!")
        choice = input("Do you want to (b)ackup and start fresh or (q)uit?").lower()
    
        if choice == 'b':
            backup_name = f"{EXPENSE_FILE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(EXPENSE_FILE, backup_name)
            print_success(f'Corrupeted file backed up as {backup_name}. Starting fresh.')
        else:
            print_error("Exiting application.")
            sys.exit(1)

    except PermissionError:
        print_error("Permission denied while accessing the expense file.")

    except Exception as e:
        print_error(f'An unexpected error occurred: {e}')
        return []
    
def save_expenses(expenses):
    try: 
        temp_file = f'{EXPENSE_FILE}.tmp'

        with open(temp_file, 'w') as file:
            json.dump(expenses, file, indent=2)

        if os.path.exist(EXPENSE_FILE):
            os.remove(EXPENSE_FILE)
        os.rename(temp_file, EXPENSE_FILE)
         

        return True