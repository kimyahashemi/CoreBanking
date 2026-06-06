from Common.DTO.response import Response
from Common.Repositories.iemployee_repository import IEmployeeRepository
from Common.Enums.employee_status import EmployeeStatus
from Common.Entities.employee import Employee

class EmployeeBusiness:
    def __init__(self, employee_repository: IEmployeeRepository):
        self.employee_repository = employee_repository

    def login(self, username, password):
        if len(username) < 3 or len(password) < 6:
            return Response(False, "Invalid data for username or password.", None)

        # 2. Fetch the employee by username only.
        employee = self.employee_repository.get_employee_by_username(username)

        # 3. Check if employee exists AND verify the Bcrypt hash
        if not employee or not employee.check_password(password):
            return Response(False, "Invalid username or password.", None)

        # 4. Handle Statuses
        if employee.status == EmployeeStatus.ACTIVE:
            return Response(True, None, employee)
        elif employee.status == EmployeeStatus.DEACTIVE:
            return Response(False, "Your account is deactivated.", None)
        elif employee.status == EmployeeStatus.PENDING:
            return Response(False, "Your account is in pending status.", None)

    def register(self, first_name, last_name, username, password, email):

        existing_user = self.employee_repository.get_employee_by_username(username)

        if existing_user:
            return Response(False, "Username already exists.")


        new_employee = Employee(
            None, first_name, last_name, username, "", 3, 1, email
        )
        new_employee.set_password(password)

        self.employee_repository.insert_new_employee(new_employee)
        return Response(True, "Registration successful", None)

    def update_password(self, employee_id, hashed_password):
        return self.employee_repository.update_password(employee_id, hashed_password)
