import os
from dotenv import load_dotenv
from BusinessLogic.employee_business import EmployeeBusiness
from DataAccess.SQLServerRepositories.employee_repository import SQLServerEmployeeRepository
load_dotenv()

def employee_dependency():

    sql_server_database_server = os.getenv("SQL_SERVER_DATABASE_SERVER")
    sql_server_database_name = os.getenv("SQL_SERVER_DATABASE_NAME")
    sqlserver_employee_repository = SQLServerEmployeeRepository(sql_server_database_server,sql_server_database_name)

    return EmployeeBusiness(sqlserver_employee_repository)