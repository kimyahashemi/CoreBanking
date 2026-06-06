from ttkbootstrap import Frame, Label, Button, Entry, Combobox
from ttkbootstrap.dialogs import Messagebox
from Common.Entities.account import Account


class CreateAccountFrame(Frame):
    def __init__(self, window, view_manager, account_business, customer_business):
        # Apply padding for the formal "card" aesthetic
        super().__init__(window, padding=40)

        self.view_manager = view_manager
        self.account_business = account_business
        self.customer_business = customer_business

        # Center the content
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Header with formal styling
        self.header_label = Label(self, text="New Account", font=("Helvetica", 20, "bold"), bootstyle="primary")
        self.header_label.grid(row=0, column=1, columnspan=2, pady=(0, 20), sticky="w")

        # Account Number
        self.account_number = Label(self, text="Generated Account Number :", font=("Helvetica", 11, "bold"))
        self.account_number.grid(row=1, column=1, pady=10, padx=(0, 10), sticky="e")

        self.account_number_generated = Entry(self, state="readonly", font=("Helvetica", 11))
        self.account_number_generated.grid(row=1, column=2, pady=10, sticky="ew")
        self.load_account_number()

        # Account Type
        self.account_type = Label(self, text="Account Type :", font=("Helvetica", 11, "bold"))
        self.account_type.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

        self.account_type_combobox = Combobox(self, values=("1-Debit", "2-Credit"), state="readonly",
                                              font=("Helvetica", 11), bootstyle="primary")
        self.account_type_combobox.grid(row=2, column=2, pady=10, sticky="ew")

        # Customer National Code
        self.customer_national_code = Label(self, text="Customer National Code :", font=("Helvetica", 11, "bold"))
        self.customer_national_code.grid(row=3, column=1, pady=10, padx=(0, 10), sticky="e")

        self.customer_national_code_entry = Entry(self, font=("Helvetica", 11))
        self.customer_national_code_entry.grid(row=3, column=2, pady=10, sticky="ew")

        self.search_customer_btn = Button(self, text="Search", bootstyle="primary", command=self.search_customer)
        self.search_customer_btn.grid(row=3, column=3, padx=10, sticky="w")

        # Customer Name Label
        self.customer_name_label = Label(self, text="Customer: Not selected", font=("Helvetica", 10, "italic"),
                                         bootstyle="info")
        self.customer_name_label.grid(row=4, column=2, pady=(0, 10), sticky="w")

        # Action Buttons
        button_frame = Frame(self)
        button_frame.grid(row=5, column=1, columnspan=2, pady=(20, 0), sticky="e")

        self.back_button = Button(button_frame, text="Back", bootstyle="secondary", command=self.back_button_clicked)
        self.back_button.pack(side="left", padx=(0, 10))

        self.create_account_button = Button(button_frame, text="Create", bootstyle="success",
                                            command=self.create_account_button_clicked)
        self.create_account_button.pack(side="left")

    def load_account_number(self):
        account_number = (self.account_business.generate_account_number())

        self.account_number_generated.configure(state="normal")
        self.account_number_generated.delete(0, "end")
        self.account_number_generated.insert(0, account_number)
        self.account_number_generated.configure(state="readonly")

    def search_customer(self):
        national_code = self.customer_national_code_entry.get()
        customer = self.customer_business.find_customer_by_national_code(national_code)

        if customer:
            self.customer_name_label.config(text=f"Customer: {customer.first_name} {customer.last_name}")
            self.selected_customer = customer
        else:
            Messagebox.show_error("Customer not found", "Error")

    def create_account_button_clicked(self):
        if not hasattr(self, "selected_customer"):
            Messagebox.show_error("Please select a customer", "Error")
            return
        if not self.account_type_combobox.get():
            Messagebox.show_error("Please select account type", "Error")
            return

        account_number = self.account_number_generated.get()
        account_type_id = int(self.account_type_combobox.get().split("-")[0])
        customer_id = self.selected_customer.id

        new_account = Account(None, account_number, account_type_id, None,
                              None, None, customer_id)
        response = self.account_business.create_account(new_account)
        if response.success:
            Messagebox.show_info("Account created successfully", "Success")
            self.clear_form()
        else:
            Messagebox.show_error(response.message, "Error")

    def clear_form(self):
        self.customer_national_code_entry.delete(0, "end")
        self.account_type_combobox.set("")
        self.customer_name_label.config(text="Customer: Not selected")
        if hasattr(self, "selected_customer"):
            del self.selected_customer
        self.load_account_number()

    def back_button_clicked(self):
        account_management_frame = self.view_manager.show_frame("account_management")
        account_management_frame.refresh_account_list()
