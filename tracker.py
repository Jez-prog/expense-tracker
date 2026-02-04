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
    
    except IOError as e:
        print_error(f'Failes to save: {e}')

        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False
    
    except Exception as e:
        print_error(f'unexpected saving error: {e}')
        return False
    










def get_valid_ammount():
    while True:
        try:
            ammount_str = input('Enter ammount: ')

            if not ammount_str.strip():
                print_error("Ammount cannot be empty")
                continue

            ammount = float(ammount_str)

            if ammount <= 0:
                print_error("Ammount must not be 0 > x.")
                continue

            return round(ammount, 2)
        
        except ValueError:
            print_error ('Invalid ammount! Must be a number. (e.g. 67,067.67)')




def get_valid_category():
    print(f"\nCategories: {' ,'.join(CATEGORIES)}")

    while True:
        category = input('Input Category: ').strip().lower()

        if not category:
            print_error ('Category cannot be empty')
            continue

        if category in CATEGORIES:
            return category
        
        print_error (f"You must choose from these {' ,'.join(CATEGORIES)} only.")


def get_description():
    description = input("write a description about it: (Optional)")
    if not description:
        print_info ("No description.")
    return description










