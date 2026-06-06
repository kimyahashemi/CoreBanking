from BusinessLogic.Validators.base_handler import BaseHandler

class AccountIsActiveValidator(BaseHandler):
    def validate(self, request):
        if request.is_active != True:
            raise ValueError("Account is not Active.")
        super().validate(request)