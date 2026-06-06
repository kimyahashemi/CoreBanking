import math
from ttkbootstrap import Frame, Label, Entry, Button, Treeview
from ttkbootstrap.dialogs import Messagebox
from Presentation.Desktop.UIComponents.account_filter import FilterDialog
from Common.Entities.employee import Employee

class AccountManagement(Frame):
    def __init__(self, window, view_manager, account_business):
        # Apply padding to the main frame to maintain the spacious layout
        super().__init__(window, padding=30)

        self.view_manager = view_manager
        self.account_business = account_business

        self.active_filters = {"account_type": None,"min_balance": None,"max_balance": None}
        self.active_search_term = ""

        columns = (0, 1, 2, 3)
        for index in columns:
            self.grid_columnconfigure(index, weight=1)

        self.grid_rowconfigure(3, weight=1)

        # Header with primary style and larger Helvetica font
        self.header_label = Label(self, text="Account Management", font=("Helvetica", 20, "bold"), bootstyle="primary", anchor="center")
        self.header_label.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="ew")

        # Search Entry
        self.search_entry = Entry(self, font=("Helvetica", 11))
        self.search_entry.grid(row=1, column=0, columnspan=3, pady=10, padx=(0, 10), sticky="ew")

        button_frame = Frame(self)
        button_frame.grid(row=1, column=3, pady=10, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.search_button = Button(button_frame, text="Search", bootstyle="primary", command=self.search_button_clicked)
        self.search_button.grid(row=1, column=0, sticky="ew", padx=(0,10))

        self.filter_button = Button(button_frame, text="Filter", bootstyle="outline-primary", command=self.filter_button_clicked)
        self.filter_button.grid(row=1, column=1, sticky="ew")

        # Action Buttons styling (Success for create, Info for update, Danger for deactivate)
        self.create_account_button = Button(self, text="Create New Account", bootstyle="success", command=self.create_account_button_clicked)
        self.create_account_button.grid(row=2, column=0, pady=(10, 20), padx=(0, 10), sticky="ew")

        self.update_account_button = Button(self, text="Update Account", bootstyle="info", command=self.update_account_button_clicked)
        self.update_account_button.grid(row=2, column=1, pady=(10, 20), padx=(0, 10), sticky="ew")

        self.deactivate_account_button = Button(self, text="Deactivate Account", bootstyle="danger", command=self.deactivate_account_button_clicked)
        self.deactivate_account_button.grid(row=2, column=2, pady=(10, 20), padx=(0, 10), sticky="ew")

        self.transaction_management_button = Button(self, text="Transaction Management", bootstyle="primary", command=self.transaction_management_button_clicked)
        self.transaction_management_button.grid(row=2, column=3, pady=(10, 20), sticky="ew")

        # Treeview styling
        self.account_treeview = Treeview(self, bootstyle="primary", columns=("account_number", "account_type",
                                                        "opening_date", "balance", "customer_id"))
        self.account_treeview.grid(row=3, column=0, columnspan=4, pady=(0, 20), sticky="nsew")
        self.account_treeview.heading("#0", text="NO")
        self.account_treeview.heading("account_number", text="Account Number")
        self.account_treeview.heading("account_type", text="Account Type")
        self.account_treeview.heading("opening_date", text="Opening Date")
        self.account_treeview.heading("balance", text="Balance")
        self.account_treeview.heading("customer_id", text="Customer Id")
        self.account_treeview.column("#0", width=60)

        # Pagination controls
        self.current_page = 1
        self.total_pages = 1

        self.previous_button = Button(self, text="Previous", bootstyle="outline-primary",
                                      state="disable", command=self.previous_button_clicked)

        self.previous_button.grid(row=4, column=0, pady=(0, 10), sticky="w")

        self.current_page_number_label = Label(self, text="1", font=("Helvetica", 11, "bold"), bootstyle="info", anchor="center")
        self.current_page_number_label.grid(row=4, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        self.next_button = Button(self, text="Next", bootstyle="outline-primary", command=self.next_button_clicked)
        self.next_button.grid(row=4, column=3, pady=(0, 10), sticky="e")

        # Back Button
        self.back_button = Button(self, text="Back", bootstyle="secondary", command=self.back_button_clicked)
        self.back_button.grid(row=5, column=0, pady=(10, 0), sticky="w")

    def set_current_employee(self, current_employee: Employee):
        self.current_employee = current_employee
        self.current_page = 1
        self.load_current_page()

    def previous_button_clicked(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_current_page()

    def next_button_clicked(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_current_page()

    def load_current_page(self):
        # Fetch data for the current page
        response = self.account_business.get_account_list(self.current_employee, self.active_search_term,
                                                          self.current_page, 10)

        if not response.success:
            Messagebox.show_error(title="Operation Failed!", message=response.message)
            return

        # Clear existing treeview
        for row in self.account_treeview.get_children():
            self.account_treeview.delete(row)

        # Update page tracking
        self.total_pages = math.ceil(response.data["total_count"] / 10)
        if self.total_pages == 0:
            self.total_pages = 1

        self.current_page_number_label.config(text=f"{self.current_page} / {self.total_pages}")

        # Populate treeview
        account_list = response.data["account_list"]
        row_number = (self.current_page - 1) * 10 + 1
        for account in account_list:
            self.account_treeview.insert(
                "",
                "end",
                iid=account.account_id,
                text=row_number,
                values=(account.account_number,
                        account.account_type.name,
                        account.opening_date,
                        account.balance,
                        account.customer_id)
            )
            row_number += 1

        # Update button states
        self.previous_button.config(state="normal" if self.current_page > 1 else "disable")
        self.next_button.config(state="normal" if self.current_page < self.total_pages else "disable")

    def refresh_account_list(self):
        for row in self.account_treeview.get_children():
            self.account_treeview.delete(row)
        if hasattr(self, 'current_employee'):
            self.set_current_employee(self.current_employee)

    def create_account_button_clicked(self):
        self.view_manager.show_frame("create_account")

    def update_account_button_clicked(self):
        if not self.account_treeview.selection():
            Messagebox.show_error("Please select an account", "Error")
            return
        account_id = int(self.account_treeview.selection()[0])
        update_frame = self.view_manager.show_frame("update_account")
        update_frame.get_account_data_by_id(account_id)

    def deactivate_account_button_clicked(self):
        if not self.account_treeview.selection():
            Messagebox.show_error("Please select an account", "Error")
            return

        account_id = int(self.account_treeview.selection()[0])

        confirm = Messagebox.yesno("Are you sure you want to deactivate this account?","Confirm")
        if confirm != "Yes":
            return

        response = self.account_business.deactivate_account(account_id)

        if response.success:
            Messagebox.show_info("Account deactivated", "Success")
            self.refresh_account_list()
        else:
            Messagebox.show_error(response.message, "Error")

    def transaction_management_button_clicked(self):
        selected_items = self.account_treeview.selection()

        if not selected_items:
            Messagebox.show_error("Please select an account", "Error")
            return

        account_id = int(selected_items[0])
        transaction_frame = self.view_manager.show_frame("transaction_management")
        transaction_frame.load_transactions(self.current_employee, account_id)

    def filter_button_clicked(self):
        dialog = FilterDialog(self)
        self.wait_window(dialog)

        if dialog.result is None:
            return

        account_type = dialog.result["account_type"] or None
        min_balance = dialog.result["min_balance"]
        max_balance = dialog.result["max_balance"]

        min_balance = float(min_balance) if min_balance else None
        max_balance = float(max_balance) if max_balance else None

        # Store filters
        self.active_filters = {
            "account_type": account_type,
            "min_balance": min_balance,
            "max_balance": max_balance
        }

        self.apply_filters_and_search()

    def search_button_clicked(self):
        term = self.search_entry.get().strip()
        self.active_search_term = term
        self.apply_filters_and_search()

    def apply_filters_and_search(self):
        f = self.active_filters

        # Step 1: filter on backend
        response = self.account_business.filter_accounts(account_type=f["account_type"],min_balance=f["min_balance"],
            max_balance=f["max_balance"])

        if not response.success:
            Messagebox.show_error(response.message, "Error")
            return

        account_list = response.data["account_list"]

        # Step 2: apply search (local filtering)
        term = self.active_search_term.lower().strip()

        if term:
            account_list = [
                acc for acc in account_list
                if term in str(acc.account_number).lower()
                   or term in str(acc.account_type.name).lower()
                   or term in str(acc.opening_date).lower()
                   or term in str(acc.balance).lower()]

        # Step 3: update TreeView
        for row in self.account_treeview.get_children():
            self.account_treeview.delete(row)

        row_num = 1
        for account in account_list:
            self.account_treeview.insert(
                "",
                "end",
                iid=account.account_id,
                text=row_num,
                values=(
                    account.account_number,
                    account.account_type.name,
                    account.opening_date,
                    account.balance,
                    account.customer_id
                )
            )
            row_num += 1

    def back_button_clicked(self):
        self.view_manager.show_frame("home")
