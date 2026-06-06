from pydantic import BaseModel 
from Common.Enums.transaction_types import TransactionType

class CreateTransactionRequest(BaseModel):
    amount : float
    transaction_type : TransactionType
    account_id : int


