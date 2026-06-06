import pymssql
from Common.Entities.employee import Employee
from Common.Repositories.iemployee_repository import IEmployeeRepository

class SQLServerEmployeeRepository(IEmployeeRepository):

    def __init__(self, server, database_name):
        self.__server = server
        self.__database_name = database_name

    def create_connection(self):
        return pymssql.connect(host=self.__server, database=self.__database_name)

    def get_employee_by_username(self, username: str):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                Select Id,
                        FirstName,
                        LastName,
                        Username,
                        Password,
                        EmployeeStatusId,
                        RoleId,
                        Email
                From EmployeeTable
                Where Username = %s""", username)
            row = cursor.fetchone()
            if row:
                employee = Employee(*row)
                return employee

    def insert_new_employee(self, new_employee: Employee):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT [EmployeeTable]
                       ([FirstName]
                       ,[LastName]
                       ,[Username]
                       ,[Password]
                       ,[EmployeeStatusId]
                       ,[RoleId]
                       ,[Email])
                VALUES
                       (%s,%s,%s,%s,%s,%s,%s)""",
                           [new_employee.first_name, new_employee.last_name, new_employee.username,
                            new_employee.password, new_employee.status.value, new_employee.role.value, new_employee.email])
            connection.commit()
    def update_password(self, employee_id, hashed_password):
        query = """
            UPDATE EmployeeTable
            SET Password = %s
            WHERE Id = %s
        """
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (hashed_password, employee_id))
            connection.commit()
