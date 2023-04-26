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
    """Gets the account name and pincode from the user and
    saves it to the google sheet named budget_accounts after encrypting the pincode.
    If the account name already exists, the pincode must match the saved encrypted pincode.
    If the account is new, the account name and pincode will be appendet to the google sheet.
    """
    print("Welcome")
    account_name = input("Enter your account name: ")
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
            account_pin = input("Enter your pincode(4 numbers): ")
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
        account_pin = input("Enter your pincode(4 numbers): ")
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
    """ Get the current date and month from datetime.
        Get the budget month from the user and validate it against datetime. 
        Get the budget amount from the user and validate the input. 
        Saves the budget month and the budget amount to google sheets.
    """
    current_month = datetime.date.today().strftime("%B")
    next_month = (datetime.date.today() + datetime.timedelta(days=31)).strftime("%B")
    valid_months = [current_month, next_month]
    print(f"You can only choose from these options: {valid_months}")
    
    while True:
        budget_month = input("Enter the month for the budget: ")
        if budget_month.capitalize() in valid_months:
            print(budget_month.capitalize())
            break
        else:
            print(f"You can only choose from either {current_month} or {next_month}. Please try again.")
        
    while True:
        try:
            total_budget = int(input("Enter your total budget: "))
            print(total_budget)
            break
        except ValueError:
            print("You must enter numbers.. Please try again")
    print(f"The month for your budget is: {budget_month.capitalize()}, and your total budget is: {total_budget}$")
    return budget_month, total_budget    


def main():
    get_account_details()
    get_budget(account_name, saved_pin)
main()


# Get the type of expense from the user and validate the input

# Get the type of transaction, debit or credit from the user and validate the input

# Get the amount of the expense from the user and validate the input and check if the amount left in the budget is more than 0

