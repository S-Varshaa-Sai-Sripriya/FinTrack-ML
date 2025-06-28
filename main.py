import pandas as pd
import csv
from datetime import datetime
from data_entry import *
import matplotlib.pyplot as plt

class CSV:
    CSV_File = "Finance_data.csv"
    Columns = ["Date", "Amount", "Category", "Description"]
    Format = "%m-%d-%y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_File)
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.Columns)
            df.to_csv(cls.CSV_File, index=False)
            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date" : date,
            "Amount" : amount,
            "Category" : category,
            "Description" : description
        }
        
        with open(cls.CSV_File, "a", newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.Columns)
            writer.writerow(new_entry)
        print("Entry added successfully...!")
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_File)
        df["Date"] = pd.to_datetime(df["Date"], format = CSV.Format)
        start_date = datetime.strptime(start_date, CSV.Format)
        end_date = datetime.strptime(end_date, CSV.Format)
        
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask] 
        
        if filtered_df.empty:
            print("No transactions found in the given date rage!!")
        else:
            print(f"Transaction from {start_date.strftime(CSV.Format)} to {end_date.strftime(CSV.Format)}: ")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x:x.strftime(CSV.Format)}))
            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\n Summary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Saving: ${(total_income-total_expense):.2f}")
            
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction in mm-dd-yy format or enter for today's date: ", allow_default=True) 
    amount = get_amount()
    category = get_category()
    description = get_description()
    print("Adding your entry...")
    CSV.add_entry(date, amount, category, description)  
    
def plot_transactions(df):
    df.set_index("Date", inplace = True)
    income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize = (10,5))
    plt.plot(income_df.index, income_df["Amount"], label = "Income", color = "g")
    plt.plot(expense_df.index, expense_df["Amount"], label = "Income", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Finance Tracker")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n 1. Add a new transaction")
        print("2. View transactions and summary within a range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter your start date in mm-dd-yy format: ")
            end_date = get_date("Enter your end date in mm-dd-yy format: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot [y/n]: ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid entry - Please provide either 1 or 2 or 3 as your choice")
            
if __name__ == "__main__":
    main()