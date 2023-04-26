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


