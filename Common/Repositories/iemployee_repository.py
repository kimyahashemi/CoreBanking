from abc import ABC, abstractmethod

class IEmployeeRepository(ABC):
    @abstractmethod
    def get_employee_by_username(self, username: str):
        pass

    @abstractmethod
    def insert_new_employee(self):
        pass