from ttkbootstrap import Frame, Label, Button, Entry, Combobox
from ttkbootstrap.dialogs import Messagebox
from Common.Enums.account_types import AccountTypes
from Common.Entities.account import Account

class UpdateAccount(Frame):
    def __init__(self, window, view_manager, account_business):
        # Apply formal padding
        super().__init__(window, padding=40)

        self.view_manager = view_manager
        self.account_business = account_business
        self.selected_account = None

        # Center the form
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Formal Header
        self.header_label = Label(self, text="Update Account", font=("Helvetica", 20, "bold"), bootstyle="primary")
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Form Elements
        Label(self, text="Account Number", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.account_number_entry = Entry(self, state="readonly", width=30)
        self.account_number_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        Label(self, text="Opening Date", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.opening_date_entry = Entry(self, state="readonly", width=30)
        self.opening_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        Label(self, text="Balance", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.balance_entry = Entry(self, state="readonly", width=30)
        self.balance_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        Label(self, text="Account Type", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.account_type_combobox = Combobox(self, state="readonly", values=("1-Debit", "2-Credit"), width=28)
        self.account_type_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        Label(self, text="Customer ID", font=("Helvetica", 10, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.customer_id_entry = Entry(self, width=30)
        self.customer_id_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Action Buttons Container for consistent placement
        self.button_frame = Frame(self)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=(30, 0))

        self.update_button = Button(self.button_frame, text="Update", bootstyle="success", command=self.update_account_clicked)
        self.update_button.grid(row=0, column=0, padx=10, ipadx=20, ipady=5)

        self.back_button = Button(self.button_frame, text="Back", bootstyle="secondary", command=self.back_button_clicked)
        self.back_button.grid(row=0, column=1, padx=10, ipadx=20, ipady=5)

    def _fill_readonly_field(self, entry_widget, value):
        entry_widget.config(state="normal")
        entry_widget.delete(0, "end")
        entry_widget.insert(0, value)
        entry_widget.config(state="readonly")

    def get_account_data_by_id(self, account_id):
        response = self.account_business.get_account_by_id(account_id)
        if response.success:
            account = response.data
            self.selected_account = account

            self._fill_readonly_field(self.account_number_entry, account.account_number)
            self._fill_readonly_field(self.opening_date_entry, account.opening_date)
            self._fill_readonly_field(self.balance_entry, f"{account.balance:,.2f}")

            type_str = "1-Debit" if account.account_type == AccountTypes.Debit else "2-Credit"
            self.account_type_combobox.set(type_str)

            self.customer_id_entry.delete(0, "end")
            self.customer_id_entry.insert(0, str(account.customer_id))

        else:
            Messagebox.show_error(f"Could not load account: {response.message}", "Error")

    def update_account_clicked(self):
        if self.selected_account is None:
            Messagebox.show_error("No account selected", "Error")
            return

        account_type_id = int(self.account_type_combobox.get().split("-")[0])
        customer_id_text = self.customer_id_entry.get().strip()

        if customer_id_text == "":
            Messagebox.show_error("Customer ID is required", "Validation Error")
            return

        if not customer_id_text.isdigit():
            Messagebox.show_error("Customer ID must be numeric", "Validation Error")
            return

        customer_id = int(customer_id_text)

        edited_account = Account(self.selected_account.account_id, self.selected_account.account_number, account_type_id,
                                 self.selected_account.opening_date, self.selected_account.balance,
                                 self.selected_account.is_active, customer_id)

        confirm = Messagebox.yesno("Are you sure you want to edit this account?", "Confirm")
        if confirm == "Yes":
            response = self.account_business.update_account(edited_account)
            if response.success:
                Messagebox.show_info("Account updated successfully", "Success")
                account_management = self.view_manager.show_frame("account_management")
                account_management.refresh_account_list()
            else:
                Messagebox.show_error(response.message, "Error")

    def back_button_clicked(self):
        account_management = self.view_manager.show_frame("account_management")
        account_management.refresh_account_list()
