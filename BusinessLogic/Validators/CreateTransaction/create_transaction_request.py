from dataclasses import dataclass
from Common.Enums.account_types import AccountTypes
from Common.Enums.transaction_types import TransactionType

@dataclass
class CreateTransactionRequest: 
    account_type : AccountTypes
    amount: float
    balance : float
    transaction_type : TransactionType
    is_active : bool
    