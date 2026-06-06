import pymssql
from Common.Entities.account import Account
from Common.Repositories.iaccount_repository import IAccountRepository


class SQLServerAccountRepository(IAccountRepository):
    def __init__(self, server, database_name):
        self.__server = server
        self.__database_name = database_name

    def create_connection(self):
        return pymssql.connect(host=self.__server, database=self.__database_name)

    def get_account_list(self, term, page_number, page_size):
        account_list = []
        with self.create_connection() as connection:
            cursor = connection.cursor()
            row_skip = page_size * (page_number - 1)
            cursor.execute("""
                Select	Id
                ,		AccountNumber
                ,		AccountTypeId
                ,		OpeningDate
                ,		(
                            Select	ISNULL(SUM(IIF(TransactionTypeId=1,Amount,-Amount)),0)
                            From	[Transaction]
                            Where	[Transaction].AccountId	=	Account.Id
                        )	AS	Balance
                ,		IsActive
                ,       CustomerId
                From	Account
                Where   IsActive = 1
                Order	By	Id	DESC
                Offset	%d	ROWS
                FETCH	NEXT	%d	ROWS	ONLY""", (row_skip, page_size))
            data = cursor.fetchall()
            for row in data:
                account = Account.create_with_tuple(row)
                account_list.append(account)

        return account_list

    def account_count(self, term) -> int:
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
            Select COUNT(*)
            From	Account
            Where   IsActive = 1""")
            count = cursor.fetchone()[0]

            return count

    def get_account_by_id(self,account_id ):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                Select	Top 1 Id
                ,		AccountNumber
                ,		AccountTypeId
                ,		OpeningDate
                ,		(
                            Select	ISNULL(SUM(IIF(TransactionTypeId=1,Amount,-Amount)),0)
                            From	[Transaction]
                            Where	[Transaction].AccountId	=	Account.Id
                        )	AS	Balance
                ,		IsActive
                ,       CustomerId
                From	Account
                Where   IsActive = 1 And Id = %d""", (account_id,))
            row = cursor.fetchone()
            if row:
                account = Account.create_with_tuple(row)
                return account

    def get_next_account_base(self):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("EXEC GetNextAccountBaseNumber")
            row = cursor.fetchone()
            return str(row[0])

    def create_account(self, new_account: Account):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT Account(AccountNumber,AccountTypeId,CustomerId)
            VALUES(%s,%d,%d)""",
            (new_account.account_number, new_account.account_type.value, new_account.customer_id))
            connection.commit()

    def deactivate_account(self, account_id):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Account
                   SET IsActive = 0
                 WHERE Id = %d 
                           """,(account_id,))
            connection.commit()

    def update_account(self, new_account: Account):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE Account
                                           SET AccountTypeId = %d
                                              ,CustomerId = %d
                                         WHERE Id = %d""", (new_account.account_type.value,
                                                            new_account.customer_id, new_account.account_id))
            connection.commit()

    def filter_accounts(self, account_type: str = "", min_balance=None, max_balance=None):
        account_list = []

        query = """
                SELECT A.Id, \
                       A.AccountNumber, \
                       A.AccountTypeId, \
                       A.OpeningDate, \
                       B.Balance, \
                       A.IsActive, \
                       A.CustomerId
                FROM Account A
                    CROSS APPLY (
                SELECT ISNULL(SUM(IIF(TransactionTypeId = 1, Amount, -Amount)),0) AS Balance
                FROM [Transaction]
                WHERE [Transaction].AccountId = A.Id
            ) B
                WHERE A.IsActive = 1 \
                """

        params = []

        if account_type:
            query += " AND A.AccountTypeId = %s"
            params.append(account_type)

        if min_balance is not None:
            query += " AND B.Balance >= %s"
            params.append(min_balance)

        if max_balance is not None:
            query += " AND B.Balance <= %s"
            params.append(max_balance)

        query += " ORDER BY A.Id DESC"

        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()

            for row in data:
                account = Account.create_with_tuple(row)
                account_list.append(account)

        return account_list

