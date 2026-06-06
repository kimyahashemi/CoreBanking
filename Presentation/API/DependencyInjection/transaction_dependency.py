from BusinessLogic.transaction_business import TransactionBusiness
from DataAccess.SQLServerRepositories.account_repository import SQLServerAccountRepository
from DataAccess.SQLServerRepositories.transaction_repository import SQLServerTransactionRepository
from dotenv import load_dotenv
import os

load_dotenv()

def get_transaction_business():

    sql_server_database_server = os.getenv("SQL_SERVER_DATABASE_SERVER")
    sql_server_database_name = os.getenv("SQL_SERVER_DATABASE_NAME")

    sqlserver_transaction_repository = SQLServerTransactionRepository(sql_server_database_server, sql_server_database_name)
    sqlserver_account_repository = SQLServerAccountRepository(sql_server_database_server,sql_server_database_name)
    
    transaction_business = TransactionBusiness(sqlserver_transaction_repository, sqlserver_account_repository)
    return transaction_business