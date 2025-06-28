from datetime import datetime

date_format = "%m-%d-%y"
def get_date(prompt, allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Date format!!")
        print("Enter date in mm-dd-yyyy format")
        return get_date(prompt, allow_default)
    
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative and non-zero value...")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
categories = {'I': "Income", 'E': "Expense"}
def get_category():
    category = input("Enter the category ('I' for Income/ 'E' for Expense): ").upper()
    if category in categories:
        return categories[category]
    print("Invalid category!! \n Please enter 'I' for income and 'E' for expense")
    
def get_description():
    return input("Enter your description for this entry {Optional}: ")