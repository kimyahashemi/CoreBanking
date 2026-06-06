from Common.Repositories.icustomer_repository import ICustomerRepository

class CustomerBusiness:
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def find_customer_by_national_code(self, national_code):
        return self.customer_repository.find_customer_by_national_code(national_code)