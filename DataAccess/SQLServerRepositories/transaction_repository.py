import pymssql
from Common.Entities.transaction import Transaction
from Common.Repositories.itransaction_repository import ITransactionRepository

class SQLServerTransactionRepository(ITransactionRepository):
    def __init__(self, server, database_name):
        self.__server = server
        self.__database_name = database_name

    def create_connection(self):
        return pymssql.connect(host=self.__server, database=self.__database_name)
    
    def get_transaction_list(self, account_id):
        transaction_list = []
        with self.create_connection() as connection:
            cursor = connection.cursor(as_dict=True)
            cursor.execute("""
                SELECT Id
                    ,Amount
                    ,TransactionTypeId
                    ,InsertDateTime
                    ,AccountId
                FROM [Transaction]
                WHERE AccountId = %d
                ORDER BY Id ASC""", (account_id))
            data = cursor.fetchall()
            for row in data:
                transaction = Transaction(row["Id"], row["Amount"], row["TransactionTypeId"], row["InsertDateTime"], row["AccountId"])
                transaction_list.append(transaction)
        return transaction_list


    def create_transaction(self, amount: float, transaction_type_id: int, account_id: int):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT [Transaction]([Amount],[TransactionTypeId],[AccountId])
            VALUES (%d,%d,%d)""", [amount, transaction_type_id, account_id])
            
            connection.commit()