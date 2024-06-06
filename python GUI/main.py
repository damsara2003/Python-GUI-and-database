import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class PersonalFinanceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("800x600")

        self.transactions = {}

        self.load_transactions_from_file1("transactions.json")

    def load_transactions_from_file1(self, filename):
        try:
            with open(filename, "r") as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = {}

    def save_transactions_to_file1(self, filename):
        with open(filename, "w") as file:
            json.dump(self.transactions, file)

    def add_transaction1(self, transaction_id, type_, date, amount):
        if transaction_id in [transaction.get('id', '') for transactions in self.transactions.values() for transaction in transactions]:
            return "Transaction ID already exists!"
        else:
            if type_ in self.transactions:
                self.transactions[type_].append({"id": str(transaction_id), "date": date, "amount": amount})
            else:
                self.transactions[type_] = [{"id": str(transaction_id), "date": date, "amount": amount}]
            self.save_transactions_to_file1("transactions.json")
            return "Transaction added successfully!"

    def view_transaction1(self, transaction_id):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    text = f"Type: {type_}\nID: {transaction.get('id', '')}\nDate: {transaction.get('date', '')}\nAmount: {transaction.get('amount', '')}"
                    found = True
                    return text
        if not found:
            return "Transaction not found!"

    def update_transaction1(self, transaction_id, type_, date, amount):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    transaction["date"] = date
                    transaction["amount"] = amount
                    transaction["type"] = type_
                    found = True
                    break
            if found:
                break
        if found:
            self.save_transactions_to_file1("transactions.json")
            return "Transaction updated successfully!"
        else:
            return "Transaction not found!"

    def delete_transaction1(self, transaction_id):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    transactions.remove(transaction)
                    found = True
                    break
            if found:
                break
        if found:
            self.save_transactions_to_file1("transactions.json")
            return "Transaction deleted successfully!"
        else:
            return "Transaction not found!"

    def display_summary1(self):
        summary = {}
        for type_, expenses in self.transactions.items():
            total_amount = sum(expense.get("amount", 0) for expense in expenses)
            summary[type_] = total_amount

        summary_text = "Summary:\n"
        for type_, total_amount in summary.items():
            summary_text += f"{type_}: Total Amount - {total_amount}\n"

        return summary_text

    def read_bulk_transactions_from_file1(self, filename):
        try:
            with open(filename, "r") as file:
                bulk_transactions = json.load(file)
                for type_, transactions in bulk_transactions.items():
                    if type_ in self.transactions:
                        self.transactions[type_].extend(transactions)
                    else:
                        self.transactions[type_] = transactions
            self.save_transactions_to_file1("transactions.json")
            return "Bulk transactions read successfully!"
        except Exception as e:
            return f"Error reading bulk transactions: {e}"

class PersonalFinancialTrackerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("800x600")

        self.transactions = {}

        self.load_transactions_from_file("transactions.json")

        self.create_widgets()

    def load_transactions_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = {}

    def save_transactions_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.transactions, file)

    def add_transaction(self):
        # Function to create a window for adding a transaction
        add_window = tk.Toplevel(self)
        add_window.title("Add Transaction")

        id_label = ttk.Label(add_window, text="Transaction ID:")
        id_label.grid(row=0, column=0)

        id_entry = ttk.Entry(add_window)
        id_entry.grid(row=0, column=1)

        type_label = ttk.Label(add_window, text="Type:")
        type_label.grid(row=1, column=0)

        type_entry = ttk.Entry(add_window)
        type_entry.grid(row=1, column=1)

        date_label = ttk.Label(add_window, text="Date:")
        date_label.grid(row=2, column=0)

        date_entry = ttk.Entry(add_window)
        date_entry.grid(row=2, column=1)

        amount_label = ttk.Label(add_window, text="Amount:")
        amount_label.grid(row=3, column=0)

        amount_entry = ttk.Entry(add_window)
        amount_entry.grid(row=3, column=1)

        add_button = ttk.Button(add_window, text="Add", command=lambda: self.add_transaction_action(add_window, id_entry.get(), date_entry.get(), float(amount_entry.get()), type_entry.get()))
        add_button.grid(row=4, columnspan=2)

    def add_transaction_action(self, window, transaction_id, date, amount, type_):
        if transaction_id in [transaction.get('id', '') for transactions in self.transactions.values() for transaction in transactions]:
            messagebox.showerror("Error", "Transaction ID already exists!")
        else:
            if type_ in self.transactions:
                self.transactions[type_].append({"id": str(transaction_id), "date": date, "amount": amount})
            else:
                self.transactions[type_] = [{"id": str(transaction_id), "date": date, "amount": amount}]
            self.save_transactions_to_file("transactions.json")
            messagebox.showinfo("Success", "Transaction added successfully!")
            window.destroy()

    def view_transaction(self):
        # Function to create a window for viewing a transaction
        view_window = tk.Toplevel(self)
        view_window.title("View Transaction")

        id_label = ttk.Label(view_window, text="Transaction ID:")
        id_label.grid(row=0, column=0)

        id_entry = ttk.Entry(view_window)
        id_entry.grid(row=0, column=1)

        view_button = ttk.Button(view_window, text="View", command=lambda: self.show_transaction(view_window, id_entry.get()))
        view_button.grid(row=1, columnspan=2)

    def show_transaction(self, window, transaction_id):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    text = f"Type: {type_}\nID: {transaction.get('id', '')}\nDate: {transaction.get('date', '')}\nAmount: {transaction.get('amount', '')}"
                    found = True
                    break
            if found:
                break
        if found:
            text_widget = tk.Text(window)
            text_widget.insert(tk.END, text)
            text_widget.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        else:
            messagebox.showerror("Error", "Transaction not found!")

    def update_transaction(self):
        update_window = tk.Toplevel(self)
        update_window.title("Update Transaction")

        id_label = ttk.Label(update_window, text="Transaction ID:")
        id_label.grid(row=0, column=0)

        id_entry = ttk.Entry(update_window)
        id_entry.grid(row=0, column=1)

        search_button = ttk.Button(update_window, text="Search", command=lambda: self.search_transaction(update_window, id_entry.get()))
        search_button.grid(row=0, column=2)

    def search_transaction(self, window, transaction_id):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    type_, date, amount = transaction.get('type', ''), transaction.get('date', ''), transaction.get('amount', '')
                    found = True
                    break
            if found:
                break
        if found:
            self.populate_transaction_details(window, transaction_id, type_, date, amount)
        else:
            messagebox.showerror("Error", "Transaction not found!")

    def populate_transaction_details(self, window, transaction_id, type_, date, amount):
        window.transaction_id = transaction_id  # Store transaction_id as an attribute of the window
        type_label = ttk.Label(window, text="Type:")
        type_label.grid(row=1, column=0)

        type_entry = ttk.Entry(window)
        type_entry.grid(row=1, column=1)
        type_entry.insert(0, type_)

        date_label = ttk.Label(window, text="Date:")
        date_label.grid(row=2, column=0)

        date_entry = ttk.Entry(window)
        date_entry.grid(row=2, column=1)
        date_entry.insert(0, date)

        amount_label = ttk.Label(window, text="Amount:")
        amount_label.grid(row=3, column=0)

        amount_entry = ttk.Entry(window)
        amount_entry.grid(row=3, column=1)
        amount_entry.insert(0, amount)

        update_button = ttk.Button(window, text="Update", command=lambda: self.update_transaction_action(window, date_entry.get(), float(amount_entry.get()), type_entry.get()))
        update_button.grid(row=4, columnspan=2)

    def update_transaction_action(self, window, date, amount, type_):
        transaction_id = window.transaction_id  # Retrieve transaction_id from the window attribute
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    transaction["date"] = date
                    transaction["amount"] = amount
                    transaction["type"] = type_
                    found = True
                    break
            if found:
                break
        if found:
            self.save_transactions_to_file("transactions.json")
            messagebox.showinfo("Success", "Transaction updated successfully!")
        else:
            messagebox.showerror("Error", "Transaction not found!")
        window.destroy()

    def delete_transaction(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Transaction")

        id_label = ttk.Label(delete_window, text="Transaction ID:")
        id_label.grid(row=0, column=0)

        id_entry = ttk.Entry(delete_window)
        id_entry.grid(row=0, column=1)

        delete_button = ttk.Button(delete_window, text="Delete", command=lambda: self.delete_transaction_action(delete_window, id_entry.get()))
        delete_button.grid(row=1, columnspan=2)

    def delete_transaction_action(self, window, transaction_id):
        found = False
        for type_, transactions in self.transactions.items():
            for transaction in transactions:
                if transaction.get("id", '') == transaction_id:
                    transactions.remove(transaction)
                    found = True
                    break
            if found:
                break
        if found:
            self.save_transactions_to_file("transactions.json")
            messagebox.showinfo("Success", "Transaction deleted successfully!")
        else:
            messagebox.showerror("Error", "Transaction not found!")
        window.destroy()

    def display_summary(self):
        # Function to create a window for displaying summary
        summary_window = tk.Toplevel(self)
        summary_window.title("Summary")

        text = tk.Text(summary_window)
        text.pack(expand=True, fill="both")

        summary = {}
        for type_, expenses in self.transactions.items():
            total_amount = sum(expense.get("amount", 0) for expense in expenses)
            summary[type_] = total_amount

        text.insert(tk.END, "Summary:\n")
        for type_, total_amount in summary.items():
            text.insert(tk.END, f"{type_}: Total Amount - {total_amount}\n")

    def read_bulk_transactions_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "r") as file:
                    bulk_transactions = json.load(file)
                    for type_, transactions in bulk_transactions.items():
                        if type_ in self.transactions:
                            self.transactions[type_].extend(transactions)
                        else:
                            self.transactions[type_] = transactions
                self.save_transactions_to_file("transactions.json")
                messagebox.showinfo("Success", "Bulk transactions read successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading bulk transactions: {e}")

    def create_widgets(self):
        # Add buttons for menu options
        add_button = ttk.Button(self, text="Add Transaction", command=self.add_transaction)
        add_button.pack()

        view_button = ttk.Button(self, text="View Transaction", command=self.view_transaction)
        view_button.pack()

        update_button = ttk.Button(self, text="Update Transaction", command=self.update_transaction)
        update_button.pack()

        delete_button = ttk.Button(self, text="Delete Transaction", command=self.delete_transaction)
        delete_button.pack()

        summary_button = ttk.Button(self, text="Display Summary", command=self.display_summary)
        summary_button.pack()

        bulk_button = ttk.Button(self, text="Read Bulk Transactions from File", command=self.read_bulk_transactions_from_file)
        bulk_button.pack()
def launch_gui():
    app = PersonalFinancialTrackerUI()
    app.mainloop()
def menu1(app):
    print("\n+------Personal Finance Tracker------+")
    print("1. Add Transaction")
    print("2. View Transaction")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. Display Summary")
    print("6. Read Bulk Transactions from File")
    print("7. Open UI")
    print("8. Exit")
    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        transaction_id = input("Enter Transaction ID: ")
        type_ = input("Enter Type: ")
        date = input("Enter Date: ")
        amount = float(input("Enter Amount: "))
        result = app.add_transaction1(transaction_id, type_, date, amount)
        print(result)
    elif choice == '2':
        transaction_id = input("Enter Transaction ID: ")
        print(app.view_transaction1(transaction_id))
    elif choice == '3':
        transaction_id = input("Enter Transaction ID: ")
        type_ = input("Enter Type: ")
        date = input("Enter Date: ")
        amount = float(input("Enter Amount: "))
        print(app.update_transaction1(transaction_id, type_, date, amount))
    elif choice == '4':
        transaction_id = input("Enter Transaction ID: ")
        print(app.delete_transaction1(transaction_id))
    elif choice == '5':
        print(app.display_summary1())
    elif choice == '6':
        filename = input("Enter file name: ")
        print(app.read_bulk_transactions_from_file1(filename))
    elif choice == '7':
        launch_gui()
    elif choice == '8':
        exit()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    app = PersonalFinanceTrackerApp()
    while True:
        menu1(app)
