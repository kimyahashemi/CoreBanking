import random
from Common.Repositories.iaccount_repository import IAccountRepository
from Common.Enums.roles import Roles
from Common.DTO.response import Response
from Common.Entities.account import Account

class AccountBusiness:
    def __init__(self, account_repository: IAccountRepository):
        self.account_repository = account_repository

    def get_account_list(self, current_employee, term, page_number, page_size):
        if current_employee.role != Roles.Banker:
            return Response(False, "Access Denied!", None)

        try:
            account_list = self.account_repository.get_account_list(term, page_number, page_size)
            total_account = self.account_repository.account_count(term)

        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)
        else:
            return Response(True, "", {
                "account_list": account_list,
                "total_count": total_account
            })

    def get_account_by_id(self, account_id):
        try:
            account = self.account_repository.get_account_by_id(account_id)
        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)
        else:
            return Response(True, "", account)

    def generate_account_number(self):

        base_number = self.account_repository.get_next_account_base()

        check_digit = self.calculate_luhn_check_digit(base_number)

        return base_number + check_digit

    @staticmethod
    def calculate_luhn_check_digit(base_num: str):
        total = 0
        for i, digit in enumerate(reversed(base_num)):
            n = int(digit)
            if i % 2 == 0:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return str((10 - (total % 10)) % 10)

    def create_account(self, new_account: Account):
        try:
            if new_account.customer_id is None:
                return Response(False, "Customer not selected", None)

            if new_account.account_number is None:
                return Response(False, "Account number invalid", None)

            self.account_repository.create_account(new_account)

        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)

        else:
            return Response(True, "Account created", None)

    def update_account(self, new_account: Account):
        try:
            current_account = self.account_repository.get_account_by_id(new_account.account_id)

            if current_account is None:
                return Response(False, "Account not found", None)

            if current_account.balance != 0:
                return Response(False, "Account cannot be edited because it has transaction history", None)

            self.account_repository.update_account(new_account)

        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)

        else:
            return Response(True, "Account updated successfully", None)

    def deactivate_account(self, account_id):
        try:
            self.account_repository.deactivate_account(account_id)

        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)

        else:
            return Response(True, "Account deactivated", None)

    def filter_accounts(self, account_type: str = "", min_balance=None, max_balance=None):

        try:
            account_type = (account_type or "").strip()

            if min_balance is not None:
                min_balance = float(min_balance)
            if max_balance is not None:
                max_balance = float(max_balance)

        except ValueError:
            return Response(False, "Min/Max balance must be numeric", None)

        try:
            account_list = self.account_repository.filter_accounts(account_type=account_type if account_type else None,
                min_balance=min_balance, max_balance=max_balance)

        except Exception as e:
            print("THE REAL ERROR IS:", repr(e))
            return Response(False, "Internal Server Error!", None)

        else:
            return Response(True, "", {
                "account_list": account_list,
                "total_count": len(account_list)})
