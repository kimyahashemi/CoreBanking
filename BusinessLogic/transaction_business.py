from Common.Enums.roles import Roles
from Common.DTO.response import Response
from Common.Repositories.itransaction_repository import ITransactionRepository
from Common.Repositories.iaccount_repository import IAccountRepository
from Common.Enums.transaction_types import TransactionType
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import matplotlib.pyplot as plt
from BusinessLogic.Validators.CreateTransaction.amount_validator import AmountValidator
from BusinessLogic.Validators.CreateTransaction.account_type_validator import AccountTypeValidator
from BusinessLogic.Validators.CreateTransaction.balance_validator import BalanceValidator
from BusinessLogic.Validators.CreateTransaction.create_transaction_request import CreateTransactionRequest
from BusinessLogic.Validators.CreateTransaction.account_is_active_validator import AccountIsActiveValidator
import os 

class TransactionBusiness:
    def __init__(self, transaction_repository: ITransactionRepository, account_repository: IAccountRepository):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    def get_transaction_list(self, current_employee, account_id):
        if current_employee.role != Roles.Banker:
            return Response(False, "Access Denied!", None)

        try:
            transaction_list = self.transaction_repository.get_transaction_list(account_id)

            return Response(True, None, transaction_list)
        except:
            return Response(False, "Internal Error!", None)
    
    def generate_pdf(self, account_id, file_path):
        transaction_list = self.transaction_repository.get_transaction_list(account_id)

        #Generate PDF
        element_list = []

        pdf_doc = SimpleDocTemplate(file_path, page_size=A4, topMargin=20, leftMargin=40, rightMargin=40)

        styles = getSampleStyleSheet()

        # Add logo
        logo_path = "static/bank-melli-logo.png"  
        logo = Image(logo_path, width=80, height=80, kind='proportional')
        element_list.append(logo)
        element_list.append(Spacer(1, 16))

        header = Paragraph("Transaction Report", styles["Title"])
        element_list.append(header)

        #Account id
        element_list.append(Paragraph(f"Account Id : {account_id}", styles["Normal"]))

        """
        data_table = [("#", "Amount", "Transaction Type", "Transaction Date Time")]
        for index, transaction in enumerate(transaction_list):
            data_table.append((index+1, transaction.amount, transaction.transaction.type.name, transaction.insert_date_time))
        """
        #List Comprehension
        data_table = [("#", "Amount", "Transaction Type", "Transaction Date Time")]+[
            (i+1, t.amount, t.transaction_type.name, t.insert_date_time) for i, t in enumerate(transaction_list)]

        transaction_table = Table(data_table, colWidths=(50,150,150,150))
        transaction_table.setStyle(TableStyle([
        # Header styling
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#b30000")),  # deep red
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 12),
        ("ALIGN", (0,0), (-1,0), "CENTER"),

        # Body styling
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 10),
        ("ALIGN", (0,1), (0,-1), "CENTER"),

        # Alternating row color
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#fff7e6")),

        # Grid lines
        ("GRID", (0,0), (-1,-1), 1, colors.HexColor("#d4af37")),  # gold color

        # Padding
        ("BOTTOMPADDING", (0,0), (-1,0), 12),
        ("TOPPADDING", (0,0), (-1,0), 12),]))
        element_list.append(transaction_table)

        pdf_doc.build(element_list)
        os.startfile(file_path)
        return Response(True, "", None)
    
    def create_transaction(self, amount:float, transaction_type:TransactionType, account_id:int):
        #Validation using Chain of Responsibility
        account = self.account_repository.get_account_by_id(account_id)
        request = CreateTransactionRequest(account.account_type ,amount, account.balance, transaction_type, account.is_active)

        amount_validator = AmountValidator()
        account_type_validator = AccountTypeValidator()
        balance_validator = BalanceValidator()
        account_is_active_validator = AccountIsActiveValidator()

        amount_validator.set_next(account_type_validator)
        account_type_validator.set_next(balance_validator)
        balance_validator.set_next(account_is_active_validator)


        try:
            amount_validator.validate(request)
        except ValueError as error:
            return Response(False, error.args[0], None)
        else:
            self.transaction_repository.create_transaction(request.amount, request.transaction_type.value, account_id)
            return Response(True, None, None)

    def create_transaction_chart(self, transactions):

        if not transactions:
            return Response(False, "No transaction data available.")

        amounts = [t["amount"] for t in transactions]
        types = [t["type"] for t in transactions]
        dates = [t["date"] for t in transactions]

        fig, axes = plt.subplots(3, 1, figsize=(10, 10))

        axes[0].plot(dates, amounts, marker="o")
        axes[0].set_title("Transaction Amount Over Time")
        axes[0].set_ylabel("Amount")
        axes[0].grid(True)

        axes[0].set_xticks(range(len(dates)))
        axes[0].set_xticklabels(dates, rotation=45)
        axes[0].tick_params(axis="x", labelsize=6)

        type_totals = {}
        for amt, t in zip(amounts, types):
            type_totals[t] = type_totals.get(t, 0) + amt

        axes[1].bar(type_totals.keys(), type_totals.values())
        axes[1].set_title("Total Amount per Transaction Type")
        axes[1].set_xlabel("Transaction Type")
        axes[1].set_ylabel("Total Amount")
        axes[1].grid(axis="y")

        axes[2].bar(range(len(amounts)), amounts)
        axes[2].set_title("Transaction Amount Distribution")
        axes[2].set_xlabel("Transaction #")
        axes[2].set_ylabel("Amount")

        fig.subplots_adjust(
            top=0.93,
            bottom=0.10,
            left=0.15,
            right=0.90,
            hspace=0.6
        )

        return Response(True," ", data=fig)

    def generate_chart_pdf(self, transactions, file_path):

        if not transactions:
            return Response(False, "No transaction data available.", None)

        amounts = [t["amount"] for t in transactions]
        types = [t["type"] for t in transactions]
        dates = [t["date"] for t in transactions]

        fig, axes = plt.subplots(3, 1, figsize=(10, 10))

        # Transaction Amount Over Time
        axes[0].plot(dates, amounts, marker="o")
        axes[0].set_title("Transaction Amount Over Time")
        axes[0].set_ylabel("Amount")
        axes[0].grid(True)
        axes[0].set_xticks(range(len(dates)))
        axes[0].set_xticklabels(dates, rotation=45)
        axes[0].tick_params(axis="x", labelsize=6)

        # Total Amount per Transaction Type
        type_totals = {}
        for amt, t in zip(amounts, types):
            type_totals[t] = type_totals.get(t, 0) + amt

        axes[1].bar(type_totals.keys(), type_totals.values())
        axes[1].set_title("Total Amount per Transaction Type")
        axes[1].set_xlabel("Transaction Type")
        axes[1].set_ylabel("Total Amount")
        axes[1].grid(axis="y")

        # Transaction Amount Distribution
        axes[2].bar(range(len(amounts)), amounts)
        axes[2].set_title("Transaction Amount Distribution")
        axes[2].set_xlabel("Transaction #")
        axes[2].set_ylabel("Amount")

        fig.subplots_adjust(
            top=0.93,
            bottom=0.10,
            left=0.15,
            right=0.90,
            hspace=0.6
        )

        try:
            fig.savefig(file_path, dpi=300, bbox_inches="tight")

            os.startfile(file_path)

            return Response(True, "Chart PDF created successfully.", None)

        except Exception as e:
            return Response(False, str(e), None)

