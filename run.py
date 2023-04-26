# imports
import gspread
from google.oauth2.service_account import Credentials

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
print(account_creds)

budget_info = budget_data.get_all_values()
print(budget_info)


# Get account name and pincode from the user and validate the input

# Get the budget amount from the user and validate the input

# Get the type of expense from the user and validate the input

# Get the type of transaction, debit or credit from the user and validate the input

# Get the amount of the expense from the user and validate the input and check if the amount left in the budget is more than 0

