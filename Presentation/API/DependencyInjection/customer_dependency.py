import os
from dotenv import load_dotenv
from BusinessLogic.customer_business import CustomerBusiness
from DataAccess.SQLServerRepositories.customer_repository import SQLServerCustomerRepository
load_dotenv()

def customer_dependency():

    sql_server_database_server = os.getenv("SQL_SERVER_DATABASE_SERVER")
    sql_server_database_name = os.getenv("SQL_SERVER_DATABASE_NAME")
    sqlserver_customer_repository = SQLServerCustomerRepository(sql_server_database_server,sql_server_database_name)

    return CustomerBusiness(sqlserver_customer_repository)