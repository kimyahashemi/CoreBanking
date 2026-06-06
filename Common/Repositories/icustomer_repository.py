from abc import  ABC, abstractmethod

class ICustomerRepository(ABC):
    @abstractmethod
    def find_customer_by_national_code(self, national_code):
        pass
    @abstractmethod
    def create_customer(self):
        pass
    @abstractmethod
    def update_customer(self):
        pass
    @abstractmethod
    def delete_customer(self):
        pass

