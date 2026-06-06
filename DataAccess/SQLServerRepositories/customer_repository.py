import pymssql
from Common.Entities.customer import Customer
from Common.Repositories.icustomer_repository import ICustomerRepository

class SQLServerCustomerRepository(ICustomerRepository):
    def __init__(self, server, database_name):
        self.__server = server
        self.__database_name = database_name

    def create_connection(self):
        return pymssql.connect(host=self.__server, database=self.__database_name)

    def find_customer_by_national_code(self, national_code):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Id
                      ,FirstName
                      ,LastName
                      ,Phone
                      ,NationalCode
                FROM Customer
                Where NationalCode = %s""", national_code)
            row = cursor.fetchone()
            if row:
                customer = Customer.create_with_tuple(row)
                return customer
            else:
                return None


    def create_customer(self):
        pass

    def update_customer(self):
        pass

    def delete_customer(self):
        pass
