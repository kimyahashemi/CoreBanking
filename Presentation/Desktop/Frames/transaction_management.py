from ttkbootstrap import Frame, Label, Button, Treeview
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Toplevel


class TransactionManagement(Frame):
    def __init__(self, window, view_manager, transaction_business):
        # Apply formal padding
        super().__init__(window, padding=40)
        self.account_id = None
        self.view_manager = view_manager
        self.transaction_business = transaction_business

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(2, weight=1)

        # Formal Header
        self.header_label = Label(self, text="Transaction Management", font=("Helvetica", 20, "bold"),
                                  bootstyle="primary")
        self.header_label.grid(row=0, column=0, columnspan=3, pady=(0, 30), padx=10)

        # Action Buttons
        self.create_transaction_button = Button(self, text="Create", bootstyle="primary",
                                                command=self.create_transaction_button_clicked)
        self.create_transaction_button.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="ew", ipadx=10, ipady=5)

        self.pdf_transaction_button = Button(self, text="PDF", bootstyle="danger",
                                             command=self.pdf_transaction_button_clicked)
        self.pdf_transaction_button.grid(row=1, column=1, pady=(0, 10), padx=10, sticky="ew", ipadx=10, ipady=5)

        self.chart_transaction_button = Button(self, text="Chart", bootstyle="success",
                                               command=self.chart_transaction_button_clicked)
        self.chart_transaction_button.grid(row=1, column=2, pady=(0, 10), padx=10, sticky="ew", ipadx=10, ipady=5)

        # Restyled Treeview (inherits theme, optimized layout)
        self.transaction_treeview = Treeview(self, columns=("amount", "type", "date"), bootstyle="primary")
        self.transaction_treeview.grid(row=2, column=0, columnspan=3, pady=(10, 20), padx=10, sticky="nsew")
        self.transaction_treeview.heading("#0", text="NO")
        self.transaction_treeview.heading("amount", text="Amount")
        self.transaction_treeview.heading("type", text="Transaction Type")
        self.transaction_treeview.heading("date", text="Insert Date")
        self.transaction_treeview.column("#0", width=60, anchor="center")
        self.transaction_treeview.column("amount", anchor="center")
        self.transaction_treeview.column("type", anchor="center")
        self.transaction_treeview.column("date", anchor="center")

        # Pagination controls
        self.previous_button = Button(self, text="Previous", state="disable", bootstyle="info-outline")
        self.previous_button.grid(row=3, column=0, pady=(0, 20), padx=10, sticky="w", ipadx=10)

        self.current_page_number_label = Label(self, text="1", font=("Helvetica", 11, "bold"), bootstyle="info")
        self.current_page_number_label.grid(row=3, column=1, pady=(0, 20), padx=10)

        self.next_button = Button(self, text="Next", bootstyle="info-outline")
        self.next_button.grid(row=3, column=2, pady=(0, 20), padx=10, sticky="e", ipadx=10)

        # Back Button
        self.back_button = Button(self, text="Back", bootstyle="secondary", command=self.back_button_clicked)
        self.back_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew", ipadx=10, ipady=5)

    def load_transactions(self, current_user, account_id):
        self.current_user = current_user
        self.account_id = account_id
        response = self.transaction_business.get_transaction_list(current_user, account_id)
        if response.success:
            self.transaction_treeview.delete(*self.transaction_treeview.get_children())
            # Load data from response to treeview
            for index, transaction in enumerate(response.data):
                self.transaction_treeview.insert("",
                                                 "end",
                                                 iid=transaction.transaction_id,
                                                 text=str(index + 1),
                                                 values=(transaction.amount, transaction.transaction_type.name,
                                                         transaction.insert_date_time))
        else:
            Messagebox.show_error(title="Business Error!", message=response.message)

    def pdf_transaction_button_clicked(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],
                                                 title="Save as Transaction Report",
                                                 initialfile=f"Transaction_Report_{self.account_id}")

        if file_path:
            # Generate PDF
            self.transaction_business.generate_pdf(self.account_id, file_path)

    def create_transaction_button_clicked(self):
        create_transaction_frame = self.view_manager.show_frame("create_transaction")
        create_transaction_frame.set_current_account(self.current_user, self.account_id)

    def chart_transaction_button_clicked(self):

        transactions = []

        for iid in self.transaction_treeview.get_children():
            amount, ttype, date = self.transaction_treeview.item(iid, "values")
            clean_date = date.split(" ")[0]

            transactions.append({
                "amount": float(amount),
                "type": ttype,
                "date": clean_date
            })

        response = self.transaction_business.create_transaction_chart(transactions)

        if not response.success:
            Messagebox.show_info("No Transactions", response.message)
            return

        fig = response.data

        chart_window = Toplevel(self)
        chart_window.title("Transaction Charts")
        chart_window.geometry("1100x800")

        create_pdf_button = Button(
            chart_window,
            text="Create PDF",
            bootstyle="danger",
            command=lambda: self.chart_pdf_button_clicked(transactions)
        )

        create_pdf_button.pack(pady=10, ipadx=10, ipady=5)

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def chart_pdf_button_clicked(self, transactions):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Transaction Charts",
            initialfile=f"Transaction_Charts_{self.account_id}"
        )

        if not file_path:
            return

        response = self.transaction_business.generate_chart_pdf(transactions, file_path)

        if response.success:
            Messagebox.show_info("Success", response.message)
        else:
            Messagebox.show_error("Error", response.message)

    def back_button_clicked(self):
        account_management_frame = self.view_manager.show_frame("account_management")
        account_management_frame.refresh_account_list()
