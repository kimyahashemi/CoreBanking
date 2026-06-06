from ttkbootstrap import Frame, Label, Button
from Common.Entities.employee import Employee
from Common.Enums.roles import Roles
from Common.Decorators.performance_logger import performance_logger_decorator

class HomeFrame(Frame):
    def __init__(self, window, view_manager):
        # Apply padding for the formal "card" aesthetic
        super().__init__(window, padding=40)

        self.view_manager = view_manager

        # Center the content
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Header with formal styling
        self.header_label = Label(self, text="Home Page", font=("Helvetica", 20, "bold"), bootstyle="primary")
        self.header_label.grid(row=0, column=1, pady=(0, 30), padx=10)

        # Action Buttons styled consistently
        self.profile_button = Button(self, text="My Profile", bootstyle="primary", command=self.profile_button_clicked)
        self.profile_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew", ipadx=10, ipady=5)

        self.account_management_button = Button(self, text="Account Management", bootstyle="success", command=self.account_management_button_clicked)

        self.logout_button = Button(self, text="Logout", bootstyle="danger", command=self.logout_button_clicked)
        self.logout_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew", ipadx=10, ipady=5)

    @performance_logger_decorator
    def set_current_employee(self, employee: Employee):
        self.current_employee = employee
        self.header_label.config(text=f"Welcome {self.current_employee.get_fullname()}!")

        # Role-based rendering mapping updated to column 1 to preserve centering
        match employee.role:
            case Roles.Banker:
                self.account_management_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew", ipadx=10, ipady=5)
            case Roles.Admin:
                self.account_management_button.grid_forget()

    def profile_button_clicked(self):
        profile_frame = self.view_manager.show_frame("profile")
        profile_frame.get_employee_info()

    def logout_button_clicked(self):
        self.view_manager.show_frame("login")

    def account_management_button_clicked(self):
        frame = self.view_manager.show_frame("account_management")
        frame.set_current_employee(self.current_employee)
