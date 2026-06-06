from abc import ABC, abstractmethod
from Common.Entities.account import Account


class IAccountRepository(ABC):
    @abstractmethod
    def get_account_list(self, term, page_number, page_size):
        pass

    @abstractmethod
    def get_account_by_id(self,account_id: int ):
        pass

    @abstractmethod
    def create_account(self, new_account: Account):
        pass

    @abstractmethod
    def update_account(self, new_account: Account):
        pass

    @abstractmethod
    def deactivate_account(self, account_id):
        pass

    @abstractmethod
    def filter_accounts(self, account_type: str = "", min_balance=None, max_balance=None):
        pass

    @abstractmethod
    def account_count(self, term) -> int:
        pass
