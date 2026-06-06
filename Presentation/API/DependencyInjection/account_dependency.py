import os
from dotenv import load_dotenv
from BusinessLogic.account_business import AccountBusiness
from DataAccess.SQLServerRepositories.account_repository import SQLServerAccountRepository
load_dotenv()

def account_dependency():

    sql_server_database_server = os.getenv("SQL_SERVER_DATABASE_SERVER")
    sql_server_database_name = os.getenv("SQL_SERVER_DATABASE_NAME")
    sqlserver_account_repository = SQLServerAccountRepository(sql_server_database_server,sql_server_database_name)

    return AccountBusiness(sqlserver_account_repository)