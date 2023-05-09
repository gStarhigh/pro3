# imports
import gspread
from google.oauth2.service_account import Credentials
import bcrypt
import datetime
import calendar

# Scope
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


# Functions
def get_account_details():
    """
    Gets the account name and pincode from the user and
    saves it to the google sheet named budget_accounts
    after encrypting the pincode.
    If the account name already exists, the pincode must match
    the saved encrypted pincode.
    If the account is new, the account name and pincode will be
    appended to the google sheet.
    """
    print("Welcome to your Monthly budget application. \n")
    print("If you are a first time user, choose an account name, "
          "it must be unique. \n")
    print("If you are a returning user, please enter your existing " 
          "account name below. \n")
    account_name = input("Enter your account name: \n")
    print(f"Checking your account name '{account_name}'..")
    
    # Check if the account name already exists in the sheet
    account_names = [row[0] for row in account_creds]
    saved_pin = None
    if account_name in account_names:
        print(f"The account name {account_name} was matched against " 
              "the database. Please continue")
        for row in account_creds:
            if row[0] == account_name:
                saved_pin = row[1]
                break
    else:
        print(f"The account name: {account_name} was not found, " 
              "creating a new Account")
        
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
        
        # Append the account name and hashed pincode to the sheet
        # if the user does not already exist
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
                print(f"Checking your account name: '{account_name}' "
                      "with the pincode: '* * * *'..")
                print("Matched credentials successfully!")
                break
            else:
                print("Incorrect pincode. Please try again.")
        else:
            print("The pincode must be 4 numbers, not letters. "
                  "Please try again.")
                
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
    today = datetime.date.today()
    next_month = (today + datetime.timedelta(days=31)).strftime("%B")
    valid_months = [current_month, next_month]
    
    while True:
        print(f"You can only choose from these options: {valid_months}")
        budget_month = input("Enter the month for the budget: \n")
        if budget_month.capitalize() in valid_months:
            print(budget_month.capitalize())
            break
        else:
            print(f"You can only choose from either {current_month} "
                  f" or {next_month}. Please try again.")
        
    while True:
        try:
            total_budget = int(input("Enter your total budget: \n"))
            print(total_budget)
            break
        except ValueError:
            print("You must enter numbers.. Please try again")
    print(f"The month for your budget is: {budget_month.capitalize()},")
    print(f"and your total budget is: {total_budget}$")
    return budget_month, total_budget, valid_months


def get_expenses(account_name, budget_month, total_budget):
    """
    Objective: Get the type, amount and transaction method
    from the user and save them all to the Google sheet. 
    
    Steps:
    1. Get the type of expense from the user.
    2. Get the type of expense amount from the user.
    3. Get the type of transaction method from the user.
    4. Save the entered data to the worksheet: budget_data
    5. Ask the user if they want to add another expense.
    """
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    # Expense types inputs
    print("Loading expense inputs...")
    
    # Using a while loop to ask the user to add expenses until
    # they no longer want to add more.
    while True:
        
        # A list of the different expense categories for
        # the user to choose from.
        expense_categories = [
            "Household",
            "Food",
            "Transportation",
            "Other",
            "Savings"
        ]
        
        # Get the expense type from the user, using a while loop
        # to make sure the input is correct.
        while True:
            print("Select a expense type: ")
            for i, expense_type in enumerate(expense_categories):
                print(f" {i + 1}. {expense_type}")
            value_range = f"[1 - {len(expense_categories)}]"
            selected_expense_type = input(f"Enter a Expense number "
                                          f"between {value_range}: \n")
            if selected_expense_type.isnumeric() and \
            int(selected_expense_type) \
                in range(1, len(expense_categories)+1):
                break
            else:
                print(f"You entered: {selected_expense_type}. "
                      f"Choose a number between 1 and "
                      f"{len(expense_categories)}.")
                
        selected_expense_type = int(selected_expense_type)
        
        # Get the name of the expense from the user.
        expense_name = input("Enter expense name: \n")
        
        # Get the amount of the expense from the user.
        expense_amount = float(input("Enter expense amount: \n"))
        
        # Get the transaction type from the user using a while loop to
        # ensure that the user enters a valid option.
        while True:
            trans_type = input("Enter transaction type "
                               "'debit' or 'credit': \n")
            if trans_type == "debit":
                break
            elif trans_type == "credit":
                break
            else:
                print(f"You must enter the details exactly as follows: "
                      "'debit' or 'credit'. Please try again")
        
        # Prints the entered information for the user to see.
        print(f"You have entered {expense_name.capitalize()} at "
              f"{expense_amount}$, with {trans_type.capitalize()} and "
              f"category {expense_categories[selected_expense_type-1]}")
        
        # Saving the entered data to the worksheet. 
        # Get the number of rows in the worksheet
        row_count = len(budget_data.get_all_values())
        new_row = [account_name, budget_month.capitalize(), total_budget,\
            expense_name.capitalize(), expense_amount, \
            trans_type.capitalize(), today_date]
        budget_data.append_row(new_row, value_input_option="USER_ENTERED")
        
        # Ask the user if they want to add another expense
        add_another = input("Do you want to add another expense? (y/n)\n")
        if add_another.lower() == "n":
            break
    return account_name, budget_month.capitalize(), total_budget,\
            expense_name.capitalize(), expense_amount, \
            trans_type.capitalize(), today_date


def calculate_budget(account_name, valid_months, budget_month):
    """
    Objective: Calculate the remaining budget for the user.
    
    Steps:
    1. Match the users data to the month and date
    2. Calculate the remaining budget
    3. Display budget left in total, per day and how much
    credit is left to pay.
    """
    
    # Get the user to choose a month to view their budget for.
    # Check so that the account name has data in the month that the user
    # chooses to see, if not, loops until the user chooses a month with data
    # or the user quits the program.   
    print(f"All done {account_name}, You can now display your budget!\n")
    print(f"Choose the month you want to display your budget for:")
    print(f"You can choose between: {valid_months}\n")
    while True:
        display_month = input("Enter the month you want to see "
                            " or enter 'q' to exit: \n")
        if display_month == "q":
            print("Exiting program...")
            return
        elif display_month.capitalize() in valid_months:
            budget_rows = budget_data.get_all_values()
            valid_budget_rows = [row for row in budget_rows \
                if row[0] == account_name and \
                    row[1] == display_month.capitalize()]
            if not valid_budget_rows:
                print(f"Sorry, there is no data for {account_name} "
                      f"in the month:{display_month}")
            else:
                break
        else:
            print(f"That month does not exist. Make sure you choose between "
                f"{valid_months}")
            return
    
    # Set the total debit and Credit
    total_debit = 0
    total_credit = 0
    total_budget = 0
    left_per_day = 0
    
    # Loop through the valid_budget_rows and get the total budget.
    for row in valid_budget_rows:
            total_budget += float(row[2])
            break
    
    # Loop through the valid_budget_rows and sum up all debit expense amounts.
    for row in valid_budget_rows:
        if row[5] == "Debit":
            total_debit += float(row[4])
    
    # Loop through the valid_budget_rows and sum up all credit expense amounts.
    for row in valid_budget_rows:
        if row[5] == "Credit":
            total_credit += float(row[4])    
    
    # Calculate how much the user has left
    total_left = total_budget - total_debit
    
    # Get the number of days left in the month
    today_date = datetime.date.today()
    days_in_month = calendar.monthrange(today_date.year, today_date.month)[1]
    remaining_days = days_in_month - today_date.day
    
    # Calculate how much the user has each day
    left_per_day = total_left / remaining_days
    
    # Print the information to the user:
    print(f"Your Total Budget is: {total_budget}$.\n")
    print(f"You have a total of {total_left}$ left this month.\n")
    print(f"Total Debit: {total_debit}$.\n")
    print(f"Total Credit: {total_credit}$.\n")
    print(f"You have {left_per_day}$ to spend per day this month calulating "
          f"that you \n need to save {total_credit}$ to afford the credit\n")
    

def delete_data(budget_data, account_name, valid_months):
    """
    Asks the user if they want to delete any saved data. The user is presented
    with the months from the valid months variable.
    If the user chooses a month to delete, it will loop through the google
    sheet and delete the matching rows.
    """
    delete_confirmation = input("Do you want to delete any saved data?"
                                " Please answer 'Yes or No'\n")
    if delete_confirmation.capitalize() == "No":
        return None
    elif delete_confirmation.capitalize() == "Yes":
        while True:
            chosen_month = input(f"Which month's data do you want do delete,"
                                 f"You must choose from {valid_months}.\n")
            if chosen_month.capitalize() in valid_months:
                break
            else:
                print(f"You chose {chosen_month}, please choose"
                      f" from {valid_months}.")
        deleted_rows = 0
        for i, row in enumerate(budget_data.get_all_values()):
            if row[0] == account_name and row[1] == chosen_month.capitalize():
                budget_data.delete_rows(i + 1 - deleted_rows)
                deleted_rows += 1
        print(f"{deleted_rows} rows have been successfully deleted.")

    
def main():
    """
    A main function to call all functions of the program.
    """
    account_name, saved_pin = get_account_details()
    budget_month, total_budget, valid_months = get_budget(account_name, saved_pin)
    get_expenses(account_name, budget_month, total_budget)
    calculate_budget(account_name, valid_months, budget_month)
    delete_data(budget_data, account_name, valid_months)
    
# Run the main function
main()

# New idea: Before the expenses, make the user choose to either enter
# an expense, or see the budget. Maybe they only want to see earlier data and
# not add new data. 