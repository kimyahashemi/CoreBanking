from ttkbootstrap import Combobox, Label, Entry, Toplevel, Button
from ttkbootstrap.dialogs import Messagebox

class FilterDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Filter Accounts")
        self.geometry("300x200")
        self.resizable(False, False)
        self.grab_set()

        self.account_type = Label(self, text="Account Type:")
        self.account_type.grid(row=0, column=0, pady=(0, 10), padx=5, sticky="w")

        self.account_type_combobox = Combobox(self, values=("1-Debit", "2-Credit"), state="readonly")
        self.account_type_combobox.grid(row=0, column=1, pady=(0, 10), padx=5, sticky="e")

        self.min_balance = Label(self, text="Min Balance:")
        self.min_balance.grid(row=1, column=0, pady=(0, 10), padx=5, sticky="w")

        self.min_balance_entry = Entry(self)
        self.min_balance_entry.grid(row=1, column=1, pady=(0, 10), padx=5, sticky="e")

        self.max_balance = Label(self, text="Max Balance:")
        self.max_balance.grid(row=2, column=0, pady=(0, 10), padx=5, sticky="w")

        self.max_balance_entry = Entry(self)
        self.max_balance_entry.grid(row=2, column=1, pady=(0, 10), padx=5, sticky="e")

        self.apply_filter = Button(self, text="Apply Filter", command=self.apply)
        self.apply_filter.grid(row=3, column=0, pady=(0, 10), padx=5, sticky="w")

        self.result = None

    def apply(self):
        self.result = {
            "account_type": self.account_type_combobox.get().split("-")[0],
            "min_balance": self.min_balance_entry.get().strip(),
            "max_balance": self.max_balance_entry.get().strip(),
        }
        self.destroy()