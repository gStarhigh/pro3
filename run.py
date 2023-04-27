# imports
import gspread
from google.oauth2.service_account import Credentials
import bcrypt
import datetime

#Scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
ACCOUNT_SHEET = GSPREAD_CLIENT.open("budget_accounts")
DATA_SHEET = GSPREAD_CLIENT.open("budget_data")

budget_accounts = ACCOUNT_SHEET.worksheet("tab1")
budget_data = DATA_SHEET.worksheet("tab1")
account_creds = budget_accounts.get_all_values()
budget_info = budget_data.get_all_values()


#Functions
def get_account_details():
    """
    Gets the account name and pincode from the user and
    saves it to the google sheet named budget_accounts after encrypting the pincode.
    If the account name already exists, the pincode must match the saved encrypted pincode.
    If the account is new, the account name and pincode will be appendet to the google sheet.
    """
    print("Welcome to your Monthly budget application. \n")
    print("If you are a first time user, choose an account name, it must be unique. \n")
    print("If you are a returning user, please enter your existing account name below. \n")
    account_name = input("Enter your account name: \n")
    print(f"Checking your account name '{account_name}'..")
    
    # Check if the account name already exists in the sheet
    account_names = [row[0] for row in account_creds]
    saved_pin = None
    if account_name in account_names:
        print(f"The account name {account_name} was matched against the database. Please continue")
        for row in account_creds:
            if row[0] == account_name:
                saved_pin = row[1]
                break
    else:
        print(f"The account name: {account_name} was not found, creating a new Account")
        
        # Asks the user for the pincode and ensure the length is 4 numbers
        while True:
            account_pin = input("Enter your pincode(4 numbers): \n")
            if len(account_pin) == 4 and account_pin.isnumeric():
                break
            else:
                print("The pincode must be 4 numbers. Please try again")
        
        # Encode the pincode
        account_pin = account_pin.encode("utf-8")
        # Encrypt the stored pincode
        hashed_pin = bcrypt.hashpw(account_pin, bcrypt.gensalt(10))
        
        # Append the account name and hashed pincode to the sheet if the user does not already exist
        new_row = [account_name, hashed_pin.decode()]
        budget_accounts.append_row(new_row)
        print(f"New account '{account_name}' was created successfully")
        saved_pin = hashed_pin.decode()
        return account_name, saved_pin
    
    while True:
        # Compare the stored password with the entered password
        account_pin = input("Enter your pincode(4 numbers): \n")
        if len(account_pin) == 4 and account_pin.isnumeric():
            account_pin = account_pin.encode("utf-8")
            if bcrypt.checkpw(account_pin, saved_pin.encode()):
                print(f"Checking your account name: '{account_name}' with the pincode: '* * * *'..")
                print("Matched credentials successfully!")
                break
            else:
                print("Incorrect pincode. Please try again.")
        else:
            print("The pincode must be 4 numbers, not letters. Please try again.")
                
    return account_name, saved_pin

# Get the budget amount from the user and validate the input
def get_budget(account_name, saved_pin):
    """ 
    Get the current date and month from datetime.
    Get the budget month from the user and validate it against datetime. 
    Get the budget amount from the user and validate the input. 
    Saves the budget month and the budget amount to google sheets.
    """
    current_month = datetime.date.today().strftime("%B")
    next_month = (datetime.date.today() + datetime.timedelta(days=31)).strftime("%B")
    valid_months = [current_month, next_month]
    print(f"You can only choose from these options: {valid_months}")
    
    while True:
        budget_month = input("Enter the month for the budget: \n")
        if budget_month.capitalize() in valid_months:
            print(budget_month.capitalize())
            break
        else:
            print(f"You can only choose from either {current_month} or {next_month}. Please try again.")
        
    while True:
        try:
            total_budget = int(input("Enter your total budget: \n"))
            print(total_budget)
            break
        except ValueError:
            print("You must enter numbers.. Please try again")
    print(f"The month for your budget is: {budget_month.capitalize()}, and your total budget is: {total_budget}$")
    #budget_data.append_row([account_name, budget_month.capitalize(), total_budget])
    return budget_month, total_budget    


def get_expenses(account_name, budget_month, total_budget):
    """
    Get the type of expense from the user.
    Get the type of expense amount from the user.
    Get the type of transaction method from the user.
    """
    #Expense types inputs
    print("Loading expense inputs...")
    expense_name = input("Enter expense name: \n")
    expense_amount = float(input("Enter expense amount: \n"))
    while True:
        trans_type = input("Enter transaction type 'debit' or 'credit': \n")
        if trans_type == "debit":
            break
        elif trans_type == "credit":
            break
        else:
            print(f"You must enter the details exactly as follows: 'debit' or 'credit'. Please try again")
    
    # Expense categories
    expense_categories = [
        "Household",
        "Food",
        "Transportation",
        "Other",
        "Savings"
    ]
    
    while True:
        print("Select a expense type: ")
        for i, expense_type in enumerate(expense_categories):
            print(f" {i + 1}. {expense_type}")
        value_range = f"[1 - {len(expense_categories)}]"
        selected_expense_type = input(f"Enter a Expense number between {value_range}: \n")
        if selected_expense_type.isnumeric() and int(selected_expense_type) in range(1, len(expense_categories)+1):
            break
        else:
            print(f"You entered: {selected_expense_type}. Choose a number between 1 and {len(expense_categories)}.")
    selected_expense_type = int(selected_expense_type)
    print(f"You have entered {expense_name.capitalize()} at {expense_amount}$, with {trans_type.capitalize()} and category {expense_categories[selected_expense_type-1]}")
    row_count = len(budget_data.get_all_values()) # get the number of rows in the worksheet
    new_row = [account_name, budget_month.capitalize(), total_budget, expense_name.capitalize(), expense_amount, trans_type]
    budget_data.append_row(new_row, value_input_option="USER_ENTERED")

def main():
    account_name, saved_pin = get_account_details()
    budget_month, total_budget = get_budget(account_name, saved_pin)
    get_expenses(account_name, budget_month, total_budget)
    
main()


# Get the type of expense from the user and validate the input

# Get the type of transaction, debit or credit from the user and validate the input

# Get the amount of the expense from the user and validate the input and check if the amount left in the budget is more than 0

