# imports
import gspread
from google.oauth2.service_account import Credentials
import bcrypt
import datetime
import calendar
import pyfiglet
from colorama import Fore, Back, Style

# Colorama colors
# Red background color
red_back = Back.RED
# Green background color
green_back = Back.GREEN
# Red text color
red_text = Fore.RED
# Green text color
green_text = Fore.GREEN
# Blue text color
blue_text = Fore.BLUE
# Reset all inputs
reset_all = Style.RESET_ALL

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



# Main budget class
class budget_app:
    def __init__(self):
        self.budget_accounts = ACCOUNT_SHEET.worksheet("tab1")
        self.budget_data = DATA_SHEET.worksheet("tab1")
        self.account_creds = self.budget_accounts.get_all_values()
        self.budget_info = self.budget_data.get_all_values()
        self.valid_months = None
        self.account_name = None


    # Functions
    def get_valid_months(self):
        """
        Get the current month current day and the next month to be able
        to calculate data in the budget.
        """    
        self.current_month = datetime.date.today().strftime("%B")
        self.today = datetime.date.today()
        self.next_month = (self.today + datetime.timedelta(days=31)).strftime("%B")
        self.valid_months = [current_month, next_month]
        return self.valid_months, self.today
        

    def get_account_details(self):
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
        self.account_name = input("Enter your account name: \n")
        print(f"Checking your account name '{self.account_name}'..")

        # Check if the account name already exists in the sheet
        account_names = [row[0] for row in self.account_creds]
        self.saved_pin = None
        if self.account_name in account_names:
            print(f"✅ The account name {self.account_name} was matched against "
                "the database.\n")
            for row in self.account_creds:
                if row[0] == self.account_name:
                    self.saved_pin = row[1]
                    while True:
                        wrong_account = input(("Did you enter the"
                                        " wrong account name?"
                                        " Type: 'restart' to start over or type:"
                                        " continue to proceed \n"))
                        if wrong_account.lower() == "restart":
                            restart_budget()
                        elif wrong_account.lower() == "continue":
                            break
        else:
            print(f"The account name: {self.account_name} was not found, "
                "creating a new Account")

            # Asks the user for the pincode and ensure the length is 4 numbers
            while True:
                account_pin = input("Enter your pincode(4 numbers): \n")
                if len(account_pin) == 4 and account_pin.isnumeric():
                    break
                elif account_pin.isnumeric() and len(account_pin) != 4:
                    print("❗The pincode must be 4 letters in length")
                else:
                    print("❗The pincode must be 4 numbers, not letters. "
                    "Please try again.")

            # Encode the pincode
            account_pin = account_pin.encode("utf-8")
            # Encrypt the stored pincode
            hashed_pin = bcrypt.hashpw(account_pin, bcrypt.gensalt(10))

            # Append the account name and hashed pincode to the sheet
            # if the user does not already exist
            new_row = [self.account_name, hashed_pin.decode()]
            self.budget_accounts.append_row(new_row)
            print(f"✅ New account '{self.account_name}' was created successfully")
            self.saved_pin = hashed_pin.decode()
            return self.account_name, self.saved_pin

        while True:
            # Compare the stored password with the entered password, 
            # and ensures that the pincode is 4 numbers in length.
            # The user has 3 tries, after that the program exits.
            tries_left = 3
            for i in range(3):
                account_pin = input("Enter your pincode(4 numbers):\n")
                tries_left -= 1
                if len(account_pin) == 4 and account_pin.isnumeric():
                    account_pin = account_pin.encode("utf-8")
                    if bcrypt.checkpw(account_pin, self.saved_pin.encode()):
                        print(f"Checking your account name: '{self.account_name}' "
                            "with the pincode: '* * * *'..")
                        print("✅ Matched credentials successfully!")
                        break
                    else:
                        if i != 2:
                            print("❗Incorrect pincode. Please try again.")
                            print(f"You have {Style.BRIGHT}{red_text}{tries_left}"
                                f"{reset_all} tries left.\n")
                # If the pincode is numbers but not 4 numbers in length:
                elif len(account_pin) != 4 and account_pin.isnumeric():
                    print("❗ The pincode must be 4 numbers in length."
                        " Try again.")
                # If the pincode does not only contain numbers:
                else:
                    print("❗ The pincode must be 4 numbers, not letters. "
                        "Please try again.")
                if tries_left == 1:
                    print(Style.BRIGHT + red_back + f"This is you last try!"
                        f"\n" + reset_all )
            if i == 2:
                print(Style.BRIGHT + red_text + "Maximum of tries exceeded."
                    " Program shuts down.." + reset_all)
                exit()
            break

        return self.account_name, self.saved_pin


    def options(self, account_name):
        """
        Give the user the option to either see the existing data
        or to delete data without entering any new data.
        """    
        user_option = input(f"{self.account_name}, Do you want to display or"
                            f" delete data? Please answer 'yes' or 'no'\n")
        if user_option == "yes":
            delete_option = input("Do you want to 'display' or 'delete' data? \n")
            if delete_option.lower() == "display":
                self.get_expenses(account_name, budget_month, total_budget)
            elif delete_option.lower() == "delete":
                self.delete_data(budget_data, account_name, valid_months)
        elif user_option == "no":
            return

    def get_budget(self, valid_months):
        """
        Get the current date and month from valid_months.
        Get the budget month from the user and validate it against valid_months.
        Get the budget amount from the user and validate the input.
        Saves the budget month and the budget amount to google sheets.
        """

        while True:
            print(f"You can only choose from these options: {self.valid_months}")
            self.budget_month = input("Enter the month for the budget: \n")
            if self.budget_month.capitalize() in self.valid_months:
                print(self.budget_month.capitalize())
                break
            else:
                print(f"❗You can only choose from either {self.current_month} "
                    f" or {self.next_month}. Please try again.")

        while True:
            try:
                self.total_budget = int(input("📈 Enter your total budget: \n"))
                print(self.total_budget)
                break
            except ValueError:
                print("❗You must enter numbers.. Please try again")
        print(f"The month for your budget is: {self.budget_month.capitalize()},")
        print(f"and your total budget is: {self.total_budget}$")
        return self.budget_month, self.total_budget, self.valid_months


    def get_expenses(self, account_name, budget_month, total_budget):
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
                "🏡 Household",
                "🍔 Food",
                "🚘 Transportation",
                "🎉 Other",
                "💰 Savings"
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
                    print(f"❗You entered: {selected_expense_type}. "
                        f"Choose a number between 1 and "
                        f"{len(expense_categories)}.")

            selected_expense_type = int(selected_expense_type)

            # Get the name of the expense from the user.
            expense_name = input("Enter expense name: \n")

            # Get the amount of the expense from the user.
            # And ensure that the input are numbers.
            while True:
                expense_amount_str = input("Enter expense amount: \n")
                if expense_amount_str.isnumeric():
                    expense_amount = float(expense_amount_str)
                    break
                else:
                    print(f"❗ You can only use numbers, please try again.")

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
                    print(f"❗You must enter the details exactly as follows: "
                        "'debit' or 'credit'. Please try again")

            # Prints the entered information for the user to see.
            print(f"You have entered {expense_name.capitalize()} at "
                f"{expense_amount}$, with {trans_type.capitalize()} and "
                f"category {expense_categories[selected_expense_type-1]}")

            # Saving the entered data to the worksheet.
            # Get the number of rows in the worksheet
            row_count = len(budget_data.get_all_values())
            new_row = [account_name, budget_month.capitalize(), total_budget,
                expense_name.capitalize(), expense_amount,
                trans_type.capitalize(), today_date, selected_expense_type]
            budget_data.append_row(new_row, value_input_option="USER_ENTERED")

            # Ask the user if they want to add another expense
            # and ensure that the input is either "y" or "n"
            while True:
                add_another = input("Do you want to add another expense? (y/n)\n")
                if add_another.lower() == "n":
                    return
                elif add_another.lower() == "y":
                    break
                else:
                    print("Invalidn input, try again.")
        return account_name, budget_month.capitalize(), total_budget,\
                expense_name.capitalize(), expense_amount, \
                trans_type.capitalize(), today_date, selected_expense_type


    def calculate_budget(self, account_name, valid_months, budget_month):
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
            display_month = input("Enter the month you want to see"
                                " or enter 'q' to exit: \n")
            if display_month == "q":
                print("Exiting program...")
                return
            elif display_month.capitalize() in valid_months:
                budget_rows = budget_data.get_all_values()
                valid_budget_rows = [row for row in budget_rows
                    if row[0] == account_name and
                        row[1] == display_month.capitalize()]
                if not valid_budget_rows:
                    print(f"❗Sorry, there is no data for {account_name} "
                        f"in {display_month}")
                else:
                    break
            else:
                print(f"❗That month does not exist. Make sure"
                    f" you choose between {valid_months}")
                continue

        # Set the total debit and Credit
        total_debit = 0
        total_credit = 0
        total_budget = 0
        left_per_day = 0

        # Loop through the valid_budget_rows and get the total budget.
        for row in reversed(valid_budget_rows):
            if row[2]:
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

        # create a dictionary of expenses grouped by expense_type
        expenses_dict = {}
        for row in valid_budget_rows:
            expense = row[3]
            amount = row[4]
            trans_type = row[5]
            expense_type = row[7]
            if expense_type not in expenses_dict:
                expenses_dict[expense_type] = []
            expenses_dict[expense_type].append((expense, amount, trans_type))

        # Print the information to the user:
        print(f"✅ Your Total Budget is: {total_budget:.2f}$.\n")
        print(f"📃 Your different expenses for {display_month} are: \n")

        # Adding the emoji to the corresponding expense type.
        for expense_type, expenses in expenses_dict.items():
            if expense_type == "1":
                expense_char = "🏡"
            elif expense_type == "2":
                expense_char = "🍔"
            elif expense_type == "3":
                expense_char = "🚘"
            elif expense_type == "4":
                expense_char = "🎉"
            elif expense_type == "5":
                expense_char = "💰"
            else:
                expense_char = ""
            # Print out the different expenses grouped by expense_type
            print(f"{expense_char} Expenses:")
            for expense, amount, trans_type in expenses:
                print(f"{expense}: - {amount}$ - {trans_type}")
            print("")

        print(f"💵 Total Debit: {total_debit:.2f}$.\n")
        print(f"💳 Total Credit: {total_credit:.2f}$.\n")

        # Check if the user has less left than the credit bill
        # then print custom message.
        if total_left < total_credit and total_credit != 0:
            print(f"🔴 You don't have enough left to pay your credit:"
                f"{total_left}$. You should adjust your\n expenses to make"
                f" sure to have more money left\n to afford the"
                f" credit bill of 💳 {total_credit}$.\n")

        # Checks if the user has less than 0 left if so, prints a custom message.
        if total_left < 0:
            print(f"🔴 With these expenses you have exceeded your budget with:"
                f" {total_left}$. You should change your expenses"
                f" to make sure you don't zero out your balance.\n")


        print(f"💶 You have a total of {total_left:.2f}$ left this month.\n")
        print(f"📉 You have {left_per_day:.2f}$ to spend per day"
            f" this month calulating that you need to\nsave"
            f" 💳 {total_credit:.2f}$ to afford the credit\n")


    def delete_data(self, budget_data, account_name, valid_months):
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
            print(f"✅ {deleted_rows} rows have been successfully deleted.")
            print("Program terminated❗")
            

    def restart_budget(self,):
        """
        Let the user choose between restarting and exiting the program.
        """
        restart = input("Do you want to restart or exit type: "
                        "'restart' or 'exit' \n")
        if restart.lower() == "restart":
            print("Restarting...")
            get_account_details()
            
        elif restart.lower() == "exit":
            print ("Good bye!")
            exit()
        
        elif restart.lower() != "restart" or "exit":
            print("Please enter a valid option")
            restart_budget()


def main():
    """
    A main function to call all functions of the program.
    """
    # Create an instance of the budget_app class
    app = budget_app()
    
    # Welcome print with Pyfiglet
    welcome_text = "Your budget app!"
    ascii_text = pyfiglet.figlet_format(welcome_text)
    print(Style.BRIGHT + green_text + ascii_text + reset_all)
    
    # Functions
    app.get_valid_months()
    account_name, saved_pin = app.get_account_details()
    options(account_name)
    budget_month, total_budget, valid_months = app.get_budget()
    app.get_expenses(account_name, budget_month, total_budget)
    app.calculate_budget(account_name, valid_months, budget_month)
    app.delete_data()


# Run the main function
if __name__ == "__main__":
    main()


# New idea: Before the expenses, make the user choose to either enter
# an expense, or see the budget. Maybe they only want to see earlier data and
# not add new data.
