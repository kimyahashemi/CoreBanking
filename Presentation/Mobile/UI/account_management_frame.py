from tkinter import messagebox, StringVar, IntVar, VERTICAL, HORIZONTAL, NO, NORMAL, DISABLED
from ttkbootstrap import Frame, Label, Button, Entry, Combobox, Treeview, Scrollbar, Toplevel, Style
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, DANGER, X, CENTER, LEFT, RIGHT, END
from Presentation.Mobile.UI.base_frame import BaseFrame

class AccountManagementFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.all_accounts = []

        self.current_page = 1
        self.total_pages = 1
        self.search_term = ""
        self.active_filters = {"type": "", "min": "", "max": ""}

        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = Frame(self, padding=15)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        # Header
        Label(container, text="Account Management", font=("Helvetica", 18, "bold"),
              bootstyle=PRIMARY, anchor=CENTER).grid(row=0, column=0, pady=(40, 20))

        # Search & Filter
        search_frame = Frame(container)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        search_entry.bind("<Return>", self.on_search)

        Button(search_frame, text="Filter", bootstyle=SUCCESS, command=self.open_filter_modal).pack(side=RIGHT)
        Button(search_frame, text="Search", bootstyle=PRIMARY, command=self.on_search).pack(side=RIGHT, padx=(0, 10))

        # Action Buttons
        btn_frame = Frame(container)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        btn_frame.columnconfigure((0, 1), weight=1)
        Button(btn_frame, text="Create", bootstyle=PRIMARY, command=self.open_create_modal).grid(row=0, column=0,
                                                                                                 sticky="ew",
                                                                                                 padx=(0, 5), pady=2)
        Button(btn_frame, text="Update", bootstyle=SUCCESS, command=self.open_update_modal).grid(row=0, column=1,
                                                                                                 padx=(5, 0), pady=2,
                                                                                                 sticky="ew")
        Button(btn_frame, text="Deactivate", bootstyle=DANGER, command=self.deactivate_account).grid(row=1, column=0,
                                                                                                     sticky="ew",
                                                                                                     padx=(0, 5),
                                                                                                     pady=2)
        Button(btn_frame, text="Transactions", bootstyle=SECONDARY, command=self.transaction_management).grid(row=1,
                                                                                                              column=1,
                                                                                                              padx=(5,
                                                                                                                    0),
                                                                                                              pady=2,
                                                                                                              sticky="ew")

        # Treeview with Horizontal Scrollbar
        tree_frame = Frame(container)
        tree_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        tree_frame.columnconfigure(0, weight=1)  # Allow tree to expand horizontally
        tree_frame.rowconfigure(0, weight=1)  # Allow tree to expand vertically (if needed)

        # Vertical Scrollbar (if needed, though less critical for horizontal spacing)
        scroll_y = Scrollbar(tree_frame, orient= VERTICAL)
        scroll_y.grid(row=0, column=1, sticky="ns")

        # Horizontal Scrollbar
        scroll_x = Scrollbar(tree_frame, orient= HORIZONTAL)
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Style row height for better legibility
        import ttkbootstrap as ttk
        style = Style()
        style.configure("Treeview", rowheight=30)

        self.tree = Treeview(tree_frame, columns=("id", "no", "acc_num", "type", "date", "balance", "cust_id"),
                             show="headings", height=8, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Headings and Columns - Increased widths for better readability
        self.tree.heading("id", text="ID")
        self.tree.heading("no", text="No")
        self.tree.heading("acc_num", text="Account Number")
        self.tree.heading("type", text="Type")
        self.tree.heading("date", text="Opening Date")
        self.tree.heading("balance", text="Balance")
        self.tree.heading("cust_id", text="Customer ID")

        self.tree.column("id", width=0, stretch= NO)
        self.tree.column("no", width=50, anchor=CENTER)
        self.tree.column("acc_num", width=150, anchor=CENTER)  # Increased width
        self.tree.column("type", width=100, anchor=CENTER)  # Increased width
        self.tree.column("date", width=120, anchor=CENTER)  # Increased width
        self.tree.column("balance", width=100, anchor=CENTER)  # Increased width
        self.tree.column("cust_id", width=90, anchor=CENTER)  # Increased width

        # Pagination
        page_frame = Frame(container)
        page_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        self.btn_prev = Button(page_frame, text="←", bootstyle=SECONDARY, command=self.prev_page, width=8)
        self.btn_prev.pack(side=LEFT)
        self.lbl_page = Label(page_frame, text="1 / 1", font=("Helvetica", 10, "bold"))
        self.lbl_page.pack(side=LEFT, expand=True)
        self.btn_next = Button(page_frame, text="→", bootstyle=PRIMARY, command=self.next_page, width=8)
        self.btn_next.pack(side=RIGHT)

        # Bottom
        Button(container, text="Back to Home", bootstyle=SECONDARY, command=self.go_back).grid(row=5, column=0,
                                                                                               sticky="ew")

    def on_show(self):
        self.load_accounts()

    def get_headers(self):
        return {"Authorization": f"Bearer {self.controller.api.token}"}

    def load_accounts(self, page=1):
        self.current_page = page

        url = (
            f"{self.controller.api.api_base_url}/api/accounts"
            f"?term={self.search_term}"
            f"&page_number={self.current_page}"
            f"&page_size=10"
        )

        try:
            response = self.controller.api.session.post(url, headers=self.get_headers())
            if response.status_code == 401:
                if hasattr(self.controller.frames.get("Home"), 'logout_button_clicked'):
                    self.controller.frames["Home"].logout_button_clicked()
                return

            data = response.json()
            if not data.get("success"):
                Messagebox.show_error(data.get("message", "Failed to load accounts"), "Error")
                return

            acc_data = data.get("data", {})
            accounts = acc_data.get("account_list", [])
            total_count = acc_data.get("total_count", 0)

            # Calculate total pages
            self.total_pages = max(1, (total_count + 9) // 10)
            self.lbl_page.config(text=f"{self.current_page} / {self.total_pages}")

            self.btn_prev.config(state= NORMAL if self.current_page > 1 else DISABLED)
            self.btn_next.config(state= NORMAL if self.current_page < self.total_pages else DISABLED)

            self.all_accounts = accounts
            self.populate_tree(accounts)


        except Exception as e:
            print(f"Load accounts error: {e}")

    def populate_tree(self, accounts):
        for item in self.tree.get_children():
            self.tree.delete(item)

        page_size = 10
        start_index = (self.current_page - 1) * page_size + 1

        for i, acc in enumerate(accounts, start=start_index):
            self.tree.insert("", END, values=(
                acc.get("account_id"),
                i,
                acc.get("account_number"),
                acc.get("account_type"),
                acc.get("opening_date"),
                acc.get("balance"),
                acc.get("customer_id")
            ))

    def on_search(self, event=None):
        term = self.search_var.get().strip().lower()
        # 1. If search is cleared, reload from API
        if not term:
            self.load_accounts(1)
            return
        # 2. Filter the cached list locally
        filtered = [
            acc for acc in self.all_accounts
            if term in str(acc.get("account_number", "")).lower()
        ]
        # 3. Populate tree with local results
        self.populate_tree(filtered)
        # 4. Disable pagination while viewing filtered results
        self.lbl_page.config(text=f"Filtered: {len(filtered)}")
        self.btn_prev.config(state=DISABLED)
        self.btn_next.config(state=DISABLED)

    def prev_page(self):
        if self.current_page > 1:
            self.load_accounts(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.load_accounts(self.current_page + 1)

    def get_selected_account(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select an account first.", "Warning")
            return None
        return self.tree.item(selected[0], "values")

    def open_create_modal(self):
        modal = Toplevel(self)
        modal.title("Create Account")
        modal.geometry("350x400")
        modal.grab_set()  # Modal behavior

        Label(modal, text="Create New Account", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Generated Account Number
        Frame1 = Frame(modal)
        Frame1.pack(fill=X, padx=20, pady=5)
        Label(Frame1, text="Account Number:").pack(anchor="w")
        acc_num_var = StringVar()
        Entry(Frame1, textvariable=acc_num_var, state="readonly").pack(fill=X)

        # Fetch generated number
        try:
            res = self.controller.api.session.get(f"{self.controller.api.api_base_url}/api/accounts/generate_number")
            if res.ok:
                acc_num_var.set(res.json().get("account_number", ""))
        except Exception:
            pass

        # Account Type
        Frame2 = Frame(modal)
        Frame2.pack(fill=X, padx=20, pady=5)
        Label(Frame2, text="Account Type:").pack(anchor="w")
        type_var = StringVar()
        cb = Combobox(Frame2, textvariable=type_var, values=["1 (Debit)", "2 (Credit)"], state="readonly")
        cb.pack(fill=X)

        # Customer Search
        Frame3 = Frame(modal)
        Frame3.pack(fill=X, padx=20, pady=5)
        Label(Frame3, text="Customer Nat. Code:").pack(anchor="w")
        nat_code_var = StringVar()
        Entry(Frame3, textvariable=nat_code_var).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        selected_cust_id = IntVar(value=0)
        lbl_cust_name = Label(modal, text="Customer: Not selected", bootstyle=SECONDARY)

        def search_customer():
            code = nat_code_var.get()
            if not code: return
            try:
                res = self.controller.api.session.get(
                    f"{self.controller.api.api_base_url}/api/accounts/get_customer?customer_national_code={code}")
                if res.ok:
                    cust = res.json().get("customer", {})
                    lbl_cust_name.config(
                        text=f"Customer: {cust.get('customer_first_name')} {cust.get('customer_last_name')}",
                        bootstyle=SUCCESS)
                    selected_cust_id.set(cust.get("customer_id"))
                else:
                    lbl_cust_name.config(text="Customer not found", bootstyle=DANGER)
            except Exception:
                pass

        Button(Frame3, text="Search", bootstyle=SUCCESS, command=search_customer).pack(side=RIGHT)
        lbl_cust_name.pack(padx=20, pady=5, anchor="w")

        # Submit
        def submit():
            if not selected_cust_id.get():
                Messagebox.show_error("Select a valid customer", "Error")
                return
            t_val = type_var.get()
            type_id = 1 if "Debit" in t_val else (2 if "Credit" in t_val else 0)
            if not type_id:
                Messagebox.show_error("Select an account type", "Error")
                return

            payload = {
                "account_number": acc_num_var.get(),
                "account_type_id": type_id,
                "customer_id": selected_cust_id.get()
            }
            try:
                res = self.controller.api.session.post(f"{self.controller.api.api_base_url}/api/accounts/create",
                                                       json=payload)
                if res.ok:
                    Messagebox.show_info("Account created successfully.", "Success")
                    modal.destroy()
                    self.load_accounts()
                else:
                    Messagebox.show_error(res.json().get("detail", "Creation failed"), "Error")
            except Exception as e:
                Messagebox.show_error(str(e), "Error")

        Button(modal, text="Create", bootstyle=PRIMARY, command=submit).pack(fill=X, padx=20, pady=20)

    def open_update_modal(self):
        sel = self.get_selected_account()
        if not sel: return

        acc_id, _, acc_num, acc_type, date, bal, cust_id = sel

        modal = Toplevel(self)
        modal.title("Update Account")
        modal.geometry("300x450")
        modal.grab_set()

        # Create a list to hold references to the StringVars so they aren't garbage collected
        modal.string_vars = []

        Label(modal, text="Update Account", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Readonly fields
        for lbl, val in [("Account Number", acc_num), ("Opening Date", date), ("Balance", bal)]:
            f = Frame(modal)
            f.pack(fill=X, padx=20, pady=2)
            Label(f, text=lbl).pack(anchor="w")

            v = StringVar(value=str(val))
            modal.string_vars.append(v)  # <--- Fix: Save the reference here

            Entry(f, textvariable=v, state="readonly").pack(fill=X)

        # Editable Account Type
        f_type = Frame(modal)
        f_type.pack(fill=X, padx=20, pady=2)
        Label(f_type, text="Account Type").pack(anchor="w")
        type_var = StringVar(value="1 (Debit)" if acc_type == "Debit" else "2 (Credit)")
        Combobox(f_type, textvariable=type_var, values=["1 (Debit)", "2 (Credit)"], state="readonly").pack(fill=X)

        # Editable Customer ID
        f_cust = Frame(modal)
        f_cust.pack(fill=X, padx=20, pady=2)
        Label(f_cust, text="Customer ID").pack(anchor="w")
        cust_var = StringVar(value=str(cust_id))
        Entry(f_cust, textvariable=cust_var).pack(fill=X)

        def submit():
            t_val = type_var.get()
            type_id = 1 if "Debit" in t_val else 2
            payload = {"id": int(acc_id), "account_number": acc_num, "account_type_id": type_id, "opening_date": date,
                       "balance": float(bal), "is_active": True, "customer_id": int(cust_var.get())}
            try:
                res = self.controller.api.session.put(f"{self.controller.api.api_base_url}/api/accounts/update",
                                                      json=payload)
                if res.ok:
                    Messagebox.show_info("Account updated.", "Success")
                    modal.destroy()
                    self.load_accounts(self.current_page)
                else:
                    Messagebox.show_error( res.json().get("detail", "Update failed"), "Error")
            except Exception as e:
                Messagebox.show_error(str(e), "Error")

        Button(modal, text="Update", bootstyle=SUCCESS, command=submit).pack(fill=X, padx=20, pady=15)

    def deactivate_account(self):
        sel = self.get_selected_account()
        if not sel: return
        acc_id, _, acc_num, *_ = sel
        if messagebox.askyesno("Confirm", f"Deactivate account {acc_num}?"):
            try:
                res = self.controller.api.session.put(f"{self.controller.api.api_base_url}/api/accounts/deactivate",
                                                      json={"id": int(acc_id)})
                if res.ok:
                    Messagebox.show_info("Account deactivated.","Success")
                    self.load_accounts(self.current_page)
                else:
                    Messagebox.show_error(res.json().get("detail", "Failed to deactivate"), "Error")
            except Exception as e:
                Messagebox.show_error(str(e), "Error")

    def transaction_management(self):
        sel = self.get_selected_account()
        if not sel:
            return

        acc_id = sel[0]
        self.controller.show_frame("TransactionManagementFrame")

        tx_frame = self.controller.frames["TransactionManagementFrame"]
        tx_frame.set_account_id(acc_id)

    def open_filter_modal(self):
        modal = Toplevel(self)
        modal.title("Filter")
        modal.geometry("300x350")
        modal.grab_set()

        Label(modal, text="Filter Accounts", font=("Helvetica", 14, "bold")).pack(pady=10)

        f_type = Frame(modal)
        f_type.pack(fill=X, padx=20, pady=5)
        Label(f_type, text="Account Type").pack(anchor="w")
        type_var = StringVar(value=self.active_filters["type"])
        Combobox(f_type, textvariable=type_var, values=["", "Debit", "Credit"], state="readonly").pack(fill=X)

        f_min = Frame(modal)
        f_min.pack(fill=X, padx=20, pady=5)
        Label(f_min, text="Min Balance").pack(anchor="w")
        min_var = StringVar(value=self.active_filters["min"])
        Entry(f_min, textvariable=min_var).pack(fill=X)

        f_max = Frame(modal)
        f_max.pack(fill=X, padx=20, pady=5)
        Label(f_max, text="Max Balance").pack(anchor="w")
        max_var = StringVar(value=self.active_filters["max"])
        Entry(f_max, textvariable=max_var).pack(fill=X)

        def apply_filters():
            self.active_filters = {
                "type": type_var.get(),
                "min": min_var.get(),
                "max": max_var.get()
            }

            try:
                url = f"{self.controller.api.api_base_url}/api/accounts/filter"
                # Use requests params instead of manually building the URL string
                params = {
                    "type": self.active_filters["type"],
                    "min": self.active_filters["min"],
                    "max": self.active_filters["max"]
                }

                res = self.controller.api.session.get(url, params=params, headers=self.get_headers())
                if res.ok:
                    data = res.json().get("data", {})
                    accounts = data.get("account_list", [])
                    total_count = data.get("total_count", len(accounts))

                    self.populate_tree(accounts)

                    # Since the filter API doesn't support pagination, lock it to page 1
                    self.current_page = 1
                    self.total_pages = 1
                    self.lbl_page.config(text=f"1 / 1 (Filtered: {total_count})")
                    self.btn_prev.config(state=DISABLED)
                    self.btn_next.config(state=DISABLED)

                    modal.destroy()
                else:
                    Messagebox.show_error("Filter failed", "Error")
            except Exception as e:
                Messagebox.show_error(str(e), "Error")

        def clear_filters():
            self.active_filters = {"type": "", "min": "", "max": ""}
            self.search_var.set("")  # Optionally clear the search term as well
            self.search_term = ""
            modal.destroy()
            self.load_accounts(1)  # This will restore normal pagination

        Button(modal, text="Apply", bootstyle=PRIMARY, command=apply_filters).pack(fill=X, padx=20, pady=5)
        Button(modal, text="Clear", bootstyle=DANGER, command=clear_filters).pack(fill=X, padx=20)

    def go_back(self):
        self.controller.show_frame("Home")
