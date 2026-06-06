from BusinessLogic.Validators.base_handler import BaseHandler
from Common.Enums.transaction_types import TransactionType

class BalanceValidator(BaseHandler):
    def validate(self, request):
        if request.balance < request.amount and request.transaction_type == TransactionType.Withdraw: 
            raise ValueError(f"Invalid Balance, Your Balance is {request.balance}")
        super().validate(request)