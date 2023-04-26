# imports
import gspread
from google.oauth2.service_account import Credentials
import bcrypt

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
#print(account_creds)

budget_info = budget_data.get_all_values()
#print(budget_info)

#Functions
def get_account_details():
    """Gets the account name and pincode from the user and
    saves it to the google sheet named budget_accounts
    """
    print("Welcome")
    account_name = input("Enter your account name: ")
    print(f"Checking your account name'{account_name}'..")
    
    # Check if the account name already exist in the sheet
    account_names = [row[0] for row in account_creds]
    if account_name in account_names:
        print(f"The account name {account_name} was matched against the database. Please continue")
    else:
        print(f"The account name: {account_name} was not found, creating a new Account")
        
        # Append the account name and hashed pincode to the sheet if the user does not already exist
        new_row = [account_name, hashed_pin_str]
        budget_accounts.append_row(new_row)
        print(f"New account '{account_name}' was created successfully")
        
        # Store the password
        account_pin = (input("Enter your pincode(4 numbers): "))
        # Encode the pincode
        account_pin = account_pin.encode("utf-8")
        # Encrypt the stored pincode
        hashed_pin = bcrypt.hashpw(account_pin, bcrypt.gensalt(10))
        hashed_pin_str = hashed_pin.decode("utf-8")
        
        # Checks if the users pincode matches the saved pincode
        
        
    
    print(f"Checking your account name: '{account_name}' with the pincode: '* * * *'.. - test")
    print(f"{hashed_pin} This is the hashed pincode -test")
    print("Matched credentials successfully!")


get_account_details()

# Get the budget amount from the user and validate the input

# Get the type of expense from the user and validate the input

# Get the type of transaction, debit or credit from the user and validate the input

# Get the amount of the expense from the user and validate the input and check if the amount left in the budget is more than 0

