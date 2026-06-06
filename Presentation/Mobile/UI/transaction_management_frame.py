from tkinter import messagebox, Toplevel, StringVar
from ttkbootstrap import Frame, Label, Button, Treeview, Scrollbar, Entry, Combobox, Style
from ttkbootstrap.constants import *
import math
from Common.Enums.transaction_types import TransactionType


class TransactionManagementFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.account_id = None
        self.transactions_data = []
        self.current_page = 1
        self.rows_per_page = 10

        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main Container
        container = Frame(self, padding=15)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        # Header
        Label(container, text="Transaction Management", font=("Helvetica", 18, "bold"),
              bootstyle=PRIMARY, anchor=CENTER).grid(row=0, column=0, pady=(40, 20))

        # Action Buttons
        btn_frame = Frame(container)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        btn_frame.columnconfigure(0, weight=1)
        Button(btn_frame, text="Create", bootstyle=SUCCESS, command=self.open_create_modal).grid(row=0, column=0,
                                                                                                 sticky="ew", pady=2)

        # Table (Treeview)
        tree_frame = Frame(container)
        tree_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Vertical and Horizontal Scrollbars
        scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Style row height for better legibility
        style = Style()
        style.configure("Treeview", rowheight=30)

        cols = ("No", "Amount", "Type", "Date")

        # ADD xscrollcommand HERE
        self.tree = Treeview(
            tree_frame,
            columns=cols,
            show="headings",
            height=8,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Headings and Columns
        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.column("No", width=50, anchor=CENTER)
        self.tree.column("Amount", width=120, anchor=CENTER)
        self.tree.column("Type", width=100, anchor=CENTER)
        self.tree.column("Date", width=150, anchor=CENTER)

        # Pagination
        page_frame = Frame(container)
        page_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        self.btn_prev = Button(page_frame, text="←", bootstyle=SECONDARY, command=self.prev_page, width=8)
        self.btn_prev.pack(side=LEFT)

        self.lbl_page = Label(page_frame, text="1 / 1", font=("Helvetica", 10, "bold"))
        self.lbl_page.pack(side=LEFT, expand=True)

        self.btn_next = Button(page_frame, text="→", bootstyle=PRIMARY, command=self.next_page, width=8)
        self.btn_next.pack(side=RIGHT)

        # Bottom / Back Button
        Button(container, text="Back", bootstyle=SECONDARY, command=self.go_back).grid(row=4, column=0, sticky="ew")

    def set_account_id(self, acc_id):
        self.account_id = acc_id
        self.current_page = 1
        self.load_transactions()

    def load_transactions(self):
        if not self.account_id:
            return

        try:
            url = f"{self.controller.api.api_base_url}/api/transaction_management"

            # Add Authorization header
            headers = {"Authorization": f"Bearer {self.controller.api.token}"}

            res = self.controller.api.session.get(
                url,
                params={"account_id": self.account_id},
                headers=headers  # Pass headers here
            )

            if res.ok:
                data = res.json()
                self.transactions_data = data.get("data", [])
                self.current_page = 1
                self.render_table()
            else:
                # Fallback error message handling
                err_msg = res.json().get("detail", "Failed to fetch transactions.")
                messagebox.showerror("Error", f"Status {res.status_code}: {err_msg}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    def render_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Use rows_per_page instead of items_per_page
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = start_idx + self.rows_per_page

        # Use transactions_data instead of transactions
        page_data = self.transactions_data[start_idx:end_idx]

        for idx, tx in enumerate(page_data, start=start_idx + 1):
            amount = tx.get("amount", "")
            tx_type = tx.get("transaction_type", "")
            raw_date = tx.get("insert_date_time", "")

            # Format the date to remove the time portion
            formatted_date = raw_date.split("T")[0] if "T" in raw_date else raw_date

            self.tree.insert("", "end", values=(idx, amount, tx_type, formatted_date))

        # Update pagination controls using transactions_data and rows_per_page
        total_pages = max(1, (len(self.transactions_data) + self.rows_per_page - 1) // self.rows_per_page)
        self.lbl_page.config(text=f"Page {self.current_page} of {total_pages}")

        self.btn_prev.config(state="normal" if self.current_page > 1 else "disabled")
        self.btn_next.config(state="normal" if self.current_page < total_pages else "disabled")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_table()

    def next_page(self):
        total_pages = math.ceil(len(self.transactions_data) / self.rows_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.render_table()

    def open_create_modal(self):
        modal = Toplevel(self)
        modal.title("Create Transaction")
        modal.geometry("300x300")
        modal.grab_set()

        Label(modal, text="Create Transaction", font=("Helvetica", 14, "bold")).pack(pady=10)

        f_amt = Frame(modal)
        f_amt.pack(fill=X, padx=20, pady=5)
        Label(f_amt, text="Amount").pack(anchor="w")
        amt_var = StringVar()
        Entry(f_amt, textvariable=amt_var).pack(fill=X)

        f_type = Frame(modal)
        f_type.pack(fill=X, padx=20, pady=5)
        Label(f_type, text="Transaction Type").pack(anchor="w")
        type_var = StringVar(value="Deposit")
        Combobox(f_type, textvariable=type_var, values=["Deposit", "Withdraw"], state="readonly").pack(fill=X)

        def submit():
            try:
                amt = float(amt_var.get())
                if amt <= 0: raise ValueError
            except:
                messagebox.showerror("Error", "Enter a valid positive amount.")
                return

            t_val = type_var.get()
            try:
                t_type = TransactionType[t_val].value
            except KeyError:
                messagebox.showerror("Error", "Invalid transaction type selected.")
                return

            payload = {
                "amount": amt,
                "transaction_type": t_type,
                "account_id": int(self.account_id)
            }

            try:
                url = f"{self.controller.api.api_base_url}/api/create_transaction"

                # Add Authorization header
                headers = {"Authorization": f"Bearer {self.controller.api.token}"}

                res = self.controller.api.session.post(
                    url,
                    json=payload,
                    headers=headers  # Pass headers here
                )

                if res.ok:
                    messagebox.showinfo("Success", "Transaction created successfully.")
                    modal.destroy()
                    self.load_transactions()
                else:
                    err_msg = res.json().get("detail", "Creation failed.")
                    messagebox.showerror("Error", f"Status {res.status_code}: {err_msg}")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {e}")

        btn_f = Frame(modal)
        btn_f.pack(fill=X, padx=20, pady=20)
        Button(btn_f, text="Submit", bootstyle=SUCCESS, command=submit).pack(side=LEFT, expand=True, fill=X, padx=2)
        Button(btn_f, text="Cancel", bootstyle=SECONDARY, command=modal.destroy).pack(side=RIGHT, expand=True, fill=X,
                                                                                      padx=2)

    def generate_pdf(self):
        messagebox.showinfo("PDF", "PDF Generation not implemented yet.")

    def show_chart(self):
        messagebox.showinfo("Chart", "Chart not implemented yet.")

    def go_back(self):
        self.controller.show_frame("AccountManagementFrame")
