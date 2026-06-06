from Presentation.Desktop.view_manager import ViewManager
from BusinessLogic.employee_business import EmployeeBusiness
from DataAccess.SQLServerRepositories.employee_repository import SQLServerEmployeeRepository
from BusinessLogic.account_business import AccountBusiness
from DataAccess.SQLServerRepositories.account_repository import SQLServerAccountRepository
from BusinessLogic.transaction_business import TransactionBusiness
from DataAccess.SQLServerRepositories.transaction_repository import SQLServerTransactionRepository
from BusinessLogic.customer_business import CustomerBusiness
from  DataAccess.SQLServerRepositories.customer_repository import SQLServerCustomerRepository
import os
from dotenv import load_dotenv

load_dotenv()
sql_server_database_server = os.getenv("SQL_SERVER_DATABASE_SERVER")
sql_server_database_name = os.getenv("SQL_SERVER_DATABASE_NAME")

sqlserver_employee_repository = SQLServerEmployeeRepository(sql_server_database_server,sql_server_database_name)
employee_business = EmployeeBusiness(sqlserver_employee_repository)

sqlserver_account_repository = SQLServerAccountRepository(sql_server_database_server,sql_server_database_name)
account_business = AccountBusiness(sqlserver_account_repository)

sqlserver_transaction_repository = SQLServerTransactionRepository(sql_server_database_server, sql_server_database_name)
transaction_business = TransactionBusiness(sqlserver_transaction_repository, sqlserver_account_repository)

sqlserver_customer_repository = SQLServerCustomerRepository(sql_server_database_server, sql_server_database_name)
customer_business = CustomerBusiness(sqlserver_customer_repository)

ViewManager(employee_business, account_business, transaction_business, customer_business)
