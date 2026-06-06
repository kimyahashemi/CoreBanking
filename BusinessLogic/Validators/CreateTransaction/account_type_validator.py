from BusinessLogic.Validators.base_handler import BaseHandler
from Common.Enums.account_types import AccountTypes

class AccountTypeValidator(BaseHandler):
    def validate(self, request):

        if request.account_type != AccountTypes.Debit:
            raise ValueError("Invalid account type for create transaction.")

        super().validate(request)