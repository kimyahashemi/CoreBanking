from Common.Enums.transaction_types import TransactionType


class Transaction():
    def __init__(self, id, amount, transaction_type_id, insert_date_time, account_id):
        self.transaction_id = id
        self.amount = amount
        self.transaction_type = TransactionType(transaction_type_id)
        self.insert_date_time = insert_date_time
        self.account_id = account_id
