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




def getValidMaxIndex(max_index):
    while True:
        try:
            index_str = input(f"Enter exepense number 1-{max_index}")

            if not index_str.strip():
                print_error ("Must enter a number")

            index = int(index_str)

            if 1 <= index <= max_index:
                return index -1
            
            print_error(f"Number must be within 1-{max_index}")

        except ValueError:
            print_error("Ivalid input. Please input correct value.")


def add_expenses(expenses):
    print(f"\n{Colors.BLUE}{"="*50}{Colors.END}")
    print(f"{Colors.BLUE}ADD NEW EXPENSES{Colors.END}")
    print(f"{Colors.BLUE}{"="}{Colors.END}")

    ammount = get_valid_ammount()
    category = get_valid_category()
    description = get_valid_ammount()

    expense = {
        "id": len(expenses) + 1,
        "ammount": ammount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses.append(expense)

    if save_expenses(expense):
        print_success(f"Expense added: ${ammount} for {category}. Saved succesfully!")

    else:
        expenses.pop()
        print_error("Something went wrong!")







def view_all_expenses(expenses):
    if not expenses:
        print_info("No expenses recorded yet!")
        return
    

    print(f"\n{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BLUE}ALL EXPENSES{Colors.END}")
    print(f"\n{Colors.BLUE}{'='*80}{Colors.END}")

    total = sum(exp['ammount'] for exp in expenses)

    for i, exp in enumerate(expenses, 1):
        print(f"[{exp['category'].upper()}] ${exp['ammount']:.2f} - {exp['description']}") 
        print(f"       Date: {exp['date']}\n")

    print(f"{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.GREEN}TOTAL: ${total:.2f}{Colors.END}")
    print(f"{Colors.BLUE}{'='*80}{Colors.END}")



def view_by_category(expenses):
    if not expenses:
        print_info("No category recorded yet!")
        return
    
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.GREEN}EXPENSES BY CATEGORY{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    
    by_category = {}
    if exp in expenses:
        cat = exp['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(exp)

        grand_total = 0
        for category in sorted(by_category.keys()):
            cat_expenses = by_category[category]
            cat_total = sum(exp['amount'] for exp in cat_expenses)
            grand_total += cat_total
        
            print(f"{Colors.YELLOW}{category.upper()}{Colors.END}")
            print(f"  Count: {len(cat_expenses)}")
            print(f"  Total: ₱{cat_total:.2f}")
        
            for exp in cat_expenses:
                print(f"    - ₱{exp['amount']:.2f}: {exp['description']}")
            print()
    
        print(f"{Colors.GREEN}GRAND TOTAL: ₱{grand_total:.2f}{Colors.END}\n")

