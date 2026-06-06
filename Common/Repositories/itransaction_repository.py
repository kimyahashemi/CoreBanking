from abc import ABC, abstractmethod


class ITransactionRepository(ABC):
    @abstractmethod
    def get_transaction_list(self, account_id):
        pass

    @abstractmethod
    def create_transaction(self, amount: float, transaction_type_id: int, account_id: int):
        pass
