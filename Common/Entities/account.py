from Common.Enums.account_types import AccountTypes

class Account:
    def __init__(self, id, account_number, account_type_id, opening_date, balance, is_active, customer_id):
        self.account_id = id
        self.account_number = account_number
        self.account_type = AccountTypes(account_type_id)
        self.opening_date = opening_date
        self.balance = balance
        self.is_active = is_active
        self.customer_id = customer_id

    @classmethod
    def create_with_tuple(cls, data):
        account = cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return account
