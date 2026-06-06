from ttkbootstrap import Frame, Label, Button, Entry, Combobox
from ttkbootstrap.constants import SUCCESS, SECONDARY, PRIMARY
from ttkbootstrap.dialogs import Messagebox
from Common.Enums.transaction_types import TransactionType


class CreateTransactionFrame(Frame):
    def __init__(self, window, view_manager, transaction_business):
        # Apply formal padding
        super().__init__(window, padding=40)

        self.account_id = None
        self.transaction_business = transaction_business
        self.view_manager = view_manager

        # Center the form
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Formal Header
        self.header_label = Label(self, text="New Transaction", font=("Helvetica", 20, "bold"), bootstyle=PRIMARY)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Form Elements
        self.amount_label = Label(self, text="Amount", font=("Helvetica", 10, "bold"))
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.amount_entry = Entry(self, width=30)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.transaction_type_label = Label(self, text="Transaction Type", font=("Helvetica", 10, "bold"))
        self.transaction_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.transaction_type_combobox = Combobox(self, values=("1-Deposit", "2-Withdraw"), state="readonly", width=28)
        self.transaction_type_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Action Buttons Container for consistent placement
        self.button_frame = Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=(30, 0))

        self.create_transaction_button = Button(self.button_frame, text="Create", bootstyle=SUCCESS,
                                                command=self.create_transaction_button_clicked)
        self.create_transaction_button.grid(row=0, column=0, padx=10, ipadx=20, ipady=5)

        self.cancel_button = Button(self.button_frame, text="Cancel", bootstyle=SECONDARY,
                                    command=self.cancel_button_clicked)
        self.cancel_button.grid(row=0, column=1, padx=10, ipadx=20, ipady=5)

    def set_current_account(self, current_user, account_id):
        self.current_user = current_user
        self.account_id = account_id

    def create_transaction_button_clicked(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            Messagebox.show_error("Please enter a valid numeric amount.", "Validation Error")
            return

        type_selection = self.transaction_type_combobox.get()
        if not type_selection:
            Messagebox.show_error("Please select a transaction type.", "Validation Error")
            return

        transaction_type_id = int(type_selection.split("-")[0])
        transaction_type = TransactionType(transaction_type_id)

        response = self.transaction_business.create_transaction(amount, transaction_type, self.account_id)

        if response.success:
            self.clear_fields()
            transaction_management_frame = self.view_manager.show_frame("transaction_management")
            transaction_management_frame.load_transactions(self.current_user, self.account_id)
        else:
            Messagebox.show_error(response.message, "Transaction Failed!")

    def clear_fields(self):
        self.amount_entry.delete(0, "end")
        self.transaction_type_combobox.set("")

    def cancel_button_clicked(self):
        self.clear_fields()
        self.view_manager.show_frame("transaction_management")
