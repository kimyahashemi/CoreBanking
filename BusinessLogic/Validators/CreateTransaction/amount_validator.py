from BusinessLogic.Validators.base_handler import BaseHandler


class AmountValidator(BaseHandler):
    def validate(self, request):
        if request.amount <= 0:
            raise ValueError("Invalid amount, amount can not be zero!")

        super().validate(request)
