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
# Red text color
red_text = Fore.RED
# Green text color
green_text = Fore.GREEN
# Blue text color
blue_text = Fore.BLUE
# Yellow text color
yellow_text = Fore.YELLOW
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
class BudgetApp:
    """ The budget application class.
    This class represents the budget application and provides
    methods for managing the budget accounts and data.

    Methods:
    __init__(self): Placeholder and data holding attributes.
    get_valid_months: Gets the valid months for the user
    get_account_details: Gets the account name and pincode from the user.
    options: Presents the user with different options, like add och display.
    add_option_method: Tells the program what methods to run after a
        user has chosen "add" in the options.
    get_budget: Gets the budget from the user.
    get_expenses: Gets the different type of expenses from the user.
    calculate_budget: Calculates the budget from the inputs of the user.
    delete_data: Deletes the users chosen data from the worksheet.
    restart_budget: Restarts the application from the beginning.
    final_question: Asks the user if they want to see the options or exit.

    """
    def __init__(self):
        """
        Gets worksheet data and placeholder attributes.
        """
        self.budget_accounts = ACCOUNT_SHEET.worksheet("tab1")
        self.budget_data = DATA_SHEET.worksheet("tab1")
        self.account_creds = self.budget_accounts.get_all_values()
        self.budget_info = self.budget_data.get_all_values()
        self.valid_months = None
        self.account_name = None
        self.budget_month = None
        self.total_budget = None

    def get_valid_months(self):
        """
        Get the current month current day and the next month to be able
        to calculate data in the budget.
        """
        self.current_month = datetime.date.today().strftime("%B")
        self.today = datetime.date.today()
        self.next_month = (self.today +
                           datetime.timedelta(days=31)).strftime("%B")
        self.valid_months = [self.current_month, self.next_month]
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
            print(f"✅ The account name {self.account_name} "
                  f"was matched against the database.\n")
            for row in self.account_creds:
                if row[0] == self.account_name:
                    self.saved_pin = row[1]
                    while True:
                        wrong_account = input(("Did you enter the"
                                               " correct account name?\n"
                                               f"Type:{Style.BRIGHT}{red_text}"
                                               f" no{reset_all} to start "
                                               "over or type:"
                                               f" {Style.BRIGHT}{green_text}"
                                               f"yes{reset_all}"
                                               " to proceed\n"))
                        if wrong_account.lower() == "no":
                            self.restart_budget()
                        elif wrong_account.lower() == "yes":
                            break
                        else:
                            print(f"{yellow_text}Invalid input. "
                                  f"Please try again{reset_all}.")
        else:
            print(f"The account name:{blue_text}{self.account_name}"
                  f"{reset_all} was not found, "
                  "creating a new Account")

            # Asks the user for the pincode and ensure the length is 4 numbers
            while True:
                account_pin = input("Enter your pincode(4 numbers): \n")
                if len(account_pin) == 4 and account_pin.isnumeric():
                    break
                elif account_pin.isnumeric() and len(account_pin) != 4:
                    print(f"❗The pincode must be"
                          f"{Style.BRIGHT}{red_text} 4 {reset_all}"
                          f"letters in length")
                else:
                    print(f"❗{yellow_text} The pincode must be 4 numbers,"
                          f"not letters. Please try again.{reset_all}")

            # Encode the pincode
            account_pin = account_pin.encode("utf-8")
            # Encrypt the stored pincode
            hashed_pin = bcrypt.hashpw(account_pin, bcrypt.gensalt(10))

            # Append the account name and hashed pincode to the sheet
            # if the user does not already exist
            new_row = [self.account_name, hashed_pin.decode()]
            self.budget_accounts.append_row(new_row)
            print(f"✅ New account '{Style.BRIGHT}{green_text}"
                  f"{self.account_name}'{reset_all} "
                  f"was created successfully")
            self.saved_pin = hashed_pin.decode()
            return self.account_name, self.saved_pin

        while True:
            # Compare the stored password with the entered password,
            # and ensures that the pincode is 4 numbers in length.
            # The user has 3 tries, after that the program exits.
            tries_left = 3
            correct = False
            for i in range(3):
                account_pin = input("Enter your pincode(4 numbers):\n")
                tries_left -= 1
                if len(account_pin) == 4 and account_pin.isnumeric():
                    account_pin = account_pin.encode("utf-8")
                    if bcrypt.checkpw(account_pin, self.saved_pin.encode()):
                        print(f"Checking your account name: "
                              f"{Style.BRIGHT}{green_text}"
                              f"{self.account_name} {reset_all}"
                              f"with the pincode: '* * * *'..")
                        print("✅ Matched credentials successfully!")
                        correct = True
                        break
                    else:
                        if i != 2:
                            print(f"{yellow_text}Incorrect pincode."
                                  f"Please try again. {reset_all}")
                            print(f"You have {Style.BRIGHT}{red_text}"
                                  f"{tries_left}{reset_all} tries left.\n")
                # If the pincode is numbers but not 4 numbers in length:
                elif len(account_pin) != 4 and account_pin.isnumeric():
                    print("❗ The pincode must be 4 numbers in length."
                          " Try again.")
                # If the pincode does not only contain numbers:
                else:
                    print(f"You have {Style.BRIGHT}{red_text}"
                          f"{tries_left}{reset_all} tries left.\n")
                    print(f"{yellow_text}The pincode must be 4 numbers,"
                          f"not letters. Please try again.{reset_all}")
                if tries_left == 1:
                    print(red_back + f"This is you last try!" + reset_all)
            if i == 2 and correct is not True:
                print(Style.BRIGHT + red_text + "Maximum of tries exceeded."
                                                " Program shuts down.."
                                                + reset_all)
                exit()
            break

        return self.account_name, self.saved_pin

    def options(self, account_name):
        """
        Give the user the option to either see the existing data
        or to delete data without entering any new data.
        """
        while True:
            user_option = input(f"{self.account_name}, Do you want to"
                                f" add, display, delete or exit?\n"
                                f"Please answer:"
                                f"{Style.BRIGHT}{green_text} add {reset_all}"
                                f", "
                                f"{Style.BRIGHT}{yellow_text}"
                                f"display{reset_all}"
                                f", "
                                f"{Style.BRIGHT}{red_text}"
                                f"delete {reset_all}"
                                f"or: "
                                f"{Style.BRIGHT}{blue_text}"
                                f"exit{reset_all}\n")
            if user_option.lower() == "add":
                self.add_option()
            elif user_option.lower() == "display":
                self.calculate_budget(self.account_name, self.valid_months,
                                      self.budget_month)
            elif user_option.lower() == "delete":
                self.delete_data(self.budget_data, self.account_name,
                                 self.valid_months)
            elif user_option.lower() == "exit":
                print("Good bye!")
                exit()
            else:
                print(f"{yellow_text}Invalid option. "
                      f"Please try again.{reset_all}")

    def add_option(self):
        """
        Methods to be run after the user chooses add in options.
        """
        budget_month, total_budget, valid_months \
            = self.get_budget(self.valid_months)
        self.get_expenses(self.account_name, budget_month, total_budget)
        self.calculate_budget(self.account_name, valid_months, budget_month)
        self.final_question()

    def get_budget(self, valid_months):
        """
        Get the current date and month from valid_months.
        Get the budget month from the user and validates
        it against valid_months.
        Get the budget amount from the user and validate the input.
        Saves the budget month and the budget amount to google sheets.
        """
        while True:
            self.budget_month = input(f"Enter the month for the budget, "
                                      f"Choose between: {self.valid_months}\n")
            if self.budget_month.capitalize() in self.valid_months:
                break
            else:
                print("You can only choose from either"
                      f" {blue_text}{self.current_month}{reset_all}"
                      f" or {blue_text}{self.next_month}{reset_all}."
                      " Please try again.")

        while True:
            try:
                self.total_budget = int(input("📈 Enter your total budget:\n"))
                break
            except ValueError:
                print(f"{yellow_text}You must enter numbers... "
                      f"Please try again {reset_all}")

        print(f"The month for your budget is: "
              f"{Style.BRIGHT}{blue_text}{self.budget_month.capitalize()},"
              f"{reset_all}")
        print(f"and your total budget is:"
              f"{Style.BRIGHT}{green_text} {self.total_budget}$ {reset_all}\n")
        print()
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
        self.today_date = datetime.date.today().strftime("%Y-%m-%d")
        # Expense types inputs
        print("Loading expense inputs...\n")

        # Using a while loop to ask the user to add expenses until
        # they no longer want to add more.
        while True:

            # A list of the different expense categories for
            # the user to choose from.
            self.expense_categories = [
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
                for i, self.expense_type in enumerate(self.expense_categories):
                    print(f" {i + 1}. {self.expense_type}")
                value_range = f"[1 - {len(self.expense_categories)}]"
                self.selected_expense_type = input(f"Enter a Expense number "
                                                   f"between {value_range}:\n")
                if self.selected_expense_type.isnumeric() and \
                    int(self.selected_expense_type) \
                        in range(1, len(self.expense_categories)+1):
                    break
                else:
                    print(f"❗You entered: {self.selected_expense_type}. "
                          f"Choose a number between 1 and "
                          f"{len(self.expense_categories)}.")

            self.selected_expense_type = int(self.selected_expense_type)

            # Get the name of the expense from the user.
            self.expense_name = input("Enter expense name: \n")

            # Get the amount of the expense from the user.
            # And ensure that the input are numbers.
            while True:
                expense_amount_str = input("Enter expense amount: \n")
                if expense_amount_str.isnumeric():
                    self.expense_amount = float(expense_amount_str)
                    break
                else:
                    print(f"{yellow_text}You can only use numbers, "
                          f"please try again.{reset_all}")

            # Get the transaction type from the user using a while loop to
            # ensure that the user enters a valid option.
            while True:
                self.trans_type = input("Enter transaction type "
                                        "'debit' or 'credit': \n")
                if self.trans_type in ["debit", "credit"]:
                    break
                else:
                    print(f"❗You must enter the details exactly as follows: "
                          "'debit' or 'credit'. Please try again")

            # Prints the entered information for the user to see.
            print(f"You have added: "
                  f"{Style.BRIGHT}{blue_text}"
                  f"{self.expense_name.capitalize()}{reset_all}"
                  f" at "
                  f"{Style.BRIGHT}{green_text}{self.expense_amount}{reset_all}"
                  f"$, paid with "
                  f"{yellow_text}{self.trans_type.capitalize()}{reset_all}"
                  f" and \nin the Category:"
                  f" {self.expense_categories[self.selected_expense_type-1]}")

            # Saving the entered data to the worksheet.
            # Get the number of rows in the worksheet
            row_count = len(self.budget_data.get_all_values())
            new_row = [self.account_name, self.budget_month.capitalize(),
                       self.total_budget,
                       self.expense_name.capitalize(), self.expense_amount,
                       self.trans_type.capitalize(), self.today_date,
                       self.selected_expense_type]
            self.budget_data.append_row(new_row,
                                        value_input_option="USER_ENTERED")

            # Ask the user if they want to add another expense
            # and ensure that the input is either "y" or "n"
            while True:
                add_another = input("Do you want to add "
                                    "another expense? (y/n)\n")
                if add_another.lower() == "n":
                    return
                elif add_another.lower() == "y":
                    break
                else:
                    print(f"{yellow_text}Invalid input, try again.{reset_all}")
        return self.account_name, self.budget_month.capitalize(),\
            self.total_budget, self.expense_name.capitalize(), \
            self.expense_amount, self.trans_type.capitalize(), \
            self.today_date, self.selected_expense_type

    def calculate_budget(self, account_name, valid_months, budget_month):
        """
        Objective: Calculate the remaining budget for the user.

        Steps:
        1. Match the users data to the month and date
        2. Calculate the remaining budget
        3. Display budget left in total, per day and how much
        credit is left to pay.

        Get the user to choose a month to view their budget for.
        Check so that the account name has data in the month that the user
        chooses to see, if not, loops until the user
        chooses a month with data or the user quits the program.
        """
        print()
        print(f"All done{Style.BRIGHT}{green_text} {self.account_name}"
              f"{reset_all}, "
              f"You can now display your budget!\n")
        print(f"Choose the month you want to display your budget for:")
        print(f"You can choose between: {self.valid_months}\n")
        while True:
            self.display_month = input(f"Enter the month you want to see"
                                       " or type "
                                       f"{red_text}q{reset_all} to exit: \n")
            if self.display_month.lower() == "q":
                print("Exiting program...")
                exit()
            elif self.display_month.capitalize() in self.valid_months:
                budget_rows = self.budget_data.get_all_values()
                self.valid_budget_rows = [row for row in budget_rows
                                          if row[0] == self.account_name and
                                          row[1] ==
                                          self.display_month.capitalize()]
                if not self.valid_budget_rows:
                    print(f"❗Sorry, there is no data for "
                          f"{green_text}{self.account_name}{reset_all}"
                          f" in {blue_text}{self.display_month}{reset_all}")
                else:
                    break
            else:
                print(f"❗That month does not exist. Make sure you choose "
                      f"between {blue_text}{self.valid_months}{reset_all}")
                continue

        # Set the total debit and Credit
        self.total_debit = 0
        self.total_credit = 0
        self.total_budget = 0
        self.left_per_day = 0

        # Loop through the valid_budget_rows and get the total budget.
        for row in reversed(self.valid_budget_rows):
            if row[2]:
                self.total_budget += float(row[2])
                break

        # Loop through the valid_budget_rows and
        # sum up all debit expense amounts.
        for row in self.valid_budget_rows:
            if row[5] == "Debit":
                self.total_debit += float(row[4])

        # Loop through the valid_budget_rows and
        # sum up all credit expense amounts.
        for row in self.valid_budget_rows:
            if row[5] == "Credit":
                self.total_credit += float(row[4])

        # Calculate how much the user has left
        self.total_left = self.total_budget - self.total_debit

        # Get the number of days left in the month
        self.today_date = datetime.date.today()
        self.days_in_month = calendar.monthrange(self.today_date.year,
                                                 self.today_date.month)[1]

        self.remaining_days = self.days_in_month - self.today_date.day

        # Calculate how much the user has each day
        self.left_per_day = self.total_left / self.remaining_days

        # create a dictionary of expenses grouped by expense_type
        self.expenses_dict = {}
        for row in self.valid_budget_rows:
            self.expense = row[3]
            self.amount = row[4]
            self.trans_type = row[5]
            self.expense_type = row[7]
            if self.expense_type not in self.expenses_dict:
                self.expenses_dict[self.expense_type] = []
            self.expenses_dict[self.expense_type].append((self.expense,
                                                          self.amount,
                                                          self.trans_type))

        # Print the information to the user:
        print(f"✅  Your Total Budget is: {self.total_budget:.2f}$.\n")
        print(f"📃  Your different expenses for {self.display_month} are: \n")

        # Adding the emoji to the corresponding expense type.
        for self.expense_type, self.expenses in self.expenses_dict.items():
            if self.expense_type == "1":
                self.expense_char = "🏡"
            elif self.expense_type == "2":
                self.expense_char = "🍔"
            elif self.expense_type == "3":
                self.expense_char = "🚘"
            elif self.expense_type == "4":
                self.expense_char = "🎉"
            elif self.expense_type == "5":
                self.expense_char = "💰"
            else:
                self.expense_char = ""
            # Print out the different expenses grouped by expense_type
            print(f"{self.expense_char}  Expenses:")
            for self.expense, self.amount, self.trans_type in self.expenses:
                print(f"{self.expense}: - {self.amount}$ - {self.trans_type}")
            print("")

        print(f"💵  Total Debit: {self.total_debit:.2f}$.\n")
        print(f"💳  Total Credit: {self.total_credit:.2f}$.\n")

        # Check if the user has less left than the credit bill
        # then print custom message.
        if self.total_left < self.total_credit and self.total_credit != 0:
            print(f"🔴 You don't have enough left to pay your credit:"
                  f"{Style.BRIGHT}{red_text}{self.total_left}{reset_all}"
                  f"$.\n You should adjust your expenses to make"
                  f" sure to have more money left\n to afford the"
                  f" credit bill of 💳 "
                  f"{yellow_text}{self.total_credit}{reset_all}$.\n")

        # Checks if the user has less than 0 left if so,
        # prints a custom message.
        elif self.total_left < 0:
            print(f"🔴 With these expenses you have exceeded your budget with:"
                  f" {Style.BRIGHT}{red_text}{self.total_left}{reset_all}$."
                  f" \nYou should change your expenses"
                  f" to make sure you don't\nzero out your balance.\n")
        else:
            print(f"💶 You have a total of "
                f"{Style.BRIGHT}{green_text}{self.total_left:.2f}{reset_all}$ "
                f"left this month.\n")
            print(f"📉 You have {blue_text}{self.left_per_day:.2f}{reset_all}"
                f"$ to spend per day this month calulating"
                f" that you need to\nsave"
                f" 💳 {yellow_text}{self.total_credit:.2f}{reset_all}"
                f"$ to afford the credit\n")

    def delete_data(self, budget_data, account_name, valid_months):
        """
        Asks the user if they want to delete any saved data.
        The user is presented with the months from the valid months variable.
        If the user chooses a month to delete, it will loop through the google
        sheet and delete the matching rows.
        """
        while True:
            delete_confirmation = input("Do you want to delete any saved data"
                                        " or your account? "
                                        "\nPlease answer 'Data'"
                                        " 'Account' or 'No'.\n")
            if delete_confirmation.capitalize() == "No":
                return None
            elif delete_confirmation.capitalize() == "Data":
                while True:
                    chosen_month = input(f"Which month's data do you"
                                         f" want do delete, You must choose"
                                         f" from {self.valid_months}.\n")
                    if chosen_month.capitalize() in self.valid_months:
                        break
                    else:
                        print(f"You chose {chosen_month}, please choose"
                              f" from {self.valid_months}.")
                deleted_rows = 0
                for i, row in enumerate(self.budget_data.get_all_values()):
                    if row[0] == self.account_name and \
                            row[1] == chosen_month.capitalize():

                        budget_data.delete_rows(i + 1 - deleted_rows)
                        deleted_rows += 1
                if deleted_rows == 0:
                    print(f"{chosen_month.capitalize()} does not contain"
                          " any data.\nNo data has been deleted.")
                else:
                    print(f"✅ {deleted_rows} rows have been successfully"
                          " deleted.")
                self.options(self.account_name)
            # If the user Chooses account, validate the answer one more time
            # Then delete all data and call the delete account method.
            elif delete_confirmation.capitalize() == "Account":
                while True:
                    true_confirmation = input(f"{red_back}"
                                              "Are you sure you want "
                                              "to delete your account? \nThis "
                                              "action cannot be reversed! "
                                              "Answer 'Yes' or 'No'."
                                              f"{reset_all}\n")
                    if true_confirmation.capitalize() == "Yes":
                        deleted_rows = 0
                        for i, row in\
                                enumerate(self.budget_data.get_all_values()):
                            if row[0] == self.account_name:
                                budget_data.delete_rows(i + 1 - deleted_rows)
                                deleted_rows += 1
                        self.delete_account(self.budget_accounts, account_name)
                    elif true_confirmation.capitalize() == "No":
                        self.options(self.account_name)
                    else:
                        print("Invalid input, try again.")
            else:
                print("Invalid input, try again.")

    def delete_account(self, budget_accounts, account_name):
        """
        If the user in delete_data chooses to delete the account, this
        method will delete the account data from the budget_accounts sheet.
        """
        deleted_rows = 0
        data = self.budget_accounts.get_all_values()
        for i, row in enumerate(data):
            if row[0] == account_name:
                self.budget_accounts.delete_rows(i + 1 - deleted_rows)
                deleted_rows += 1
        print(f"✅ Your account {account_name} and all your data "
              f"has been deleted. \nYou are welcome to return anytime!")
        self.restart_budget()

    def restart_budget(self):
        """
        Let the user choose between restarting and exiting the program.
        """
        restart = input("Do you want to restart or exit type: "
                        f"{Style.BRIGHT}{green_text}restart{reset_all} or "
                        f"{Style.BRIGHT}{red_text}exit{reset_all} \n")
        if restart.lower() == "restart":
            print(f"{Style.BRIGHT}{green_text}Restarting...{reset_all}")
            self.account_name = None
            self.saved_pin = None
            main()

        elif restart.lower() == "exit":
            print(f"{Style.BRIGHT}{green_text}Good bye!{reset_all}")
            exit()

        elif restart.lower() != "restart" or "exit":
            print(f"{yellow_text}Please enter a valid option{reset_all}")
            self.restart_budget()

    def final_question(self):
        """
        Final question of the program that asks if the user wants to display
        all options again, or to exit the program.
        """
        while True:
            option_question = input("Do you want to see your options or exit? "
                                    "Enter: 'yes' or 'exit'\n")
            if option_question.lower() == "yes":
                self.options(self.account_name)
                break
            elif option_question.lower() == "exit":
                exit()
            else:
                print("Invalid input. Please try again")


def main():
    """
    A main method to call all methods of the program.
    """
    # Create an instance of the BudgetApp class
    app = BudgetApp()

    # Welcome print with Pyfiglet
    welcome_text = "Your budget app!"
    ascii_text = pyfiglet.figlet_format(welcome_text)
    print(Style.BRIGHT + green_text + ascii_text + reset_all)

    # Methods
    app.get_valid_months()
    account_name, saved_pin = app.get_account_details()
    app.options(account_name)
    budget_month, total_budget, valid_months = app.get_budget(app.valid_months)
    app.get_expenses(account_name, budget_month, total_budget)
    app.calculate_budget(account_name, valid_months, budget_month)
    app.final_question()


# Run the main Method
if __name__ == "__main__":
    main()
