import os
import pymssql
from dotenv import load_dotenv

from Common.Enums.account_types import AccountTypes
from Common.Enums.employee_status import EmployeeStatus
from Common.Enums.transaction_types import TransactionType
from Common.Enums.roles import Roles

def seed_database(server, database_name):
    # Ensure server and database name are provided
    if not server or not database_name:
        print("Database credentials not found. Check your .env file.")
        return

    with pymssql.connect(host=server, database=database_name) as connection:
        cursor = connection.cursor()

        # Dictionary mapping the exact SQL Table name to the Python Enum class
        enum_mappings = {
            "AccountType": AccountTypes,
            "EmployeeStatus": EmployeeStatus,
            "TransactionType": TransactionType,
            "Role": Roles
        }

        for table_name, enum_class in enum_mappings.items():
            print(f"Processing table: {table_name}...")

            for item in enum_class:
                # Check if the record already exists
                cursor.execute(f"SELECT 1 FROM [{table_name}] WHERE Id = %d", (item.value,))
                exists = cursor.fetchone()

                if not exists:
                    # Because Id is an IDENTITY column, we must enable IDENTITY_INSERT
                    cursor.execute(f"""
                        SET IDENTITY_INSERT [{table_name}] ON;
                        INSERT INTO [{table_name}] (Id, Title) VALUES (%d, %s);
                        SET IDENTITY_INSERT [{table_name}] OFF;
                    """, (item.value, item.name))

        connection.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    SERVER_NAME = os.getenv("SQL_SERVER_DATABASE_SERVER")
    DB_NAME = os.getenv("SQL_SERVER_DATABASE_NAME")

    seed_database(SERVER_NAME, DB_NAME)
