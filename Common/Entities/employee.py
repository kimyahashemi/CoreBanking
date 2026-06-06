import bcrypt
from Common.Enums.roles import Roles
from Common.Enums.employee_status import EmployeeStatus
class Employee:
    def __init__(self, employee_id, first_name, last_name, username, password, status_id, role_id, email):
        self.id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.status = EmployeeStatus(status_id)
        self.role = Roles(role_id)
        self.email = email

        #email reset token
        self.reset_token = None

    def set_password(self, raw_password):
        hashed_bytes = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())
        self.password = hashed_bytes.decode()  # ✅ convert to string

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode(),
            self.password.encode()
        )

    def set_reset_token(self, token):
        self.reset_token = token

    def verify_reset_token(self, token):
        return self.reset_token == token

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
