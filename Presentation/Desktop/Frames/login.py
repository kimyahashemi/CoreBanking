from ttkbootstrap import Frame, Label, Entry, Button, Checkbutton
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import PRIMARY, SUCCESS, OUTLINE
from Presentation.Desktop.UIComponents.password_entry import PasswordEntry
from Presentation.Desktop.UIComponents.captcha import CaptchaComponent
from BusinessLogic.employee_business import EmployeeBusiness
from tkinter import BooleanVar
import json
import os


class LoginFrame(Frame):
    def __init__(self, window, employee_business: EmployeeBusiness, view_manager):
        super().__init__(window)

        self.view_manager = view_manager
        self.employee_business = employee_business

        # Center the login card in the middle of the screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create an inner frame to act as a "Card" for the login form
        self.card_frame = Frame(self, padding=40)
        self.card_frame.grid(row=0, column=0)
        self.card_frame.grid_columnconfigure(1, weight=1)

        # Header
        self.header_label = Label(
            self.card_frame,
            text="Core Banking Login",
            font=("Helvetica", 20, "bold"),
            bootstyle=PRIMARY
        )
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")

        # Username
        self.user_label = Label(self.card_frame, text="Username", font=("Helvetica", 10))
        self.user_label.grid(row=1, column=0, padx=(0, 15), pady=(0, 15), sticky="e")

        self.user_entry = Entry(self.card_frame, font=("Helvetica", 10))
        self.user_entry.grid(row=1, column=1, pady=(0, 15), sticky="ew")

        # Password
        self.password_label = Label(self.card_frame, text="Password", font=("Helvetica", 10))
        self.password_label.grid(row=2, column=0, padx=(0, 15), pady=(0, 15), sticky="e")

        self.password_entry = Entry(self.card_frame)  # Kept to preserve your original code

        self.password_component = PasswordEntry(self.card_frame)
        self.password_component.grid(row=2, column=1, pady=(0, 15), sticky="ew")

        # Remember Me
        self.remember_var = BooleanVar()
        self.remember_me = Checkbutton(
            self.card_frame,
            text="Remember me",
            variable=self.remember_var,
            bootstyle="success-round-toggle"
        )
        self.remember_me.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="w")
        self.load_remembered_user()

        # Captcha - Changed to columnspan=2 to prevent overflowing the right side
        self.captcha_component = CaptchaComponent(self.card_frame)
        self.captcha_component.grid(row=4, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        # Login Button - Changed to columnspan=2
        self.login_button = Button(
            self.card_frame,
            text="Login",
            command=self.login_button_clicked,
            bootstyle=SUCCESS,
            width=20
        )
        self.login_button.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Register Button - Changed to columnspan=2
        self.register_button = Button(
            self.card_frame,
            text="Register a new account",
            command=self.register_button_clicked,
            bootstyle=(PRIMARY, OUTLINE)
        )
        self.register_button.grid(row=6, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def login_button_clicked(self):
        if not self.captcha_component.is_valid():
            Messagebox.show_error("Invalid CAPTCHA", "Error")
            self.captcha_component.generate_captcha()
            return

        username = self.user_entry.get()
        password = self.password_component.get_password_value()

        response = self.employee_business.login(username, password)

        if not response.success:
            Messagebox.show_error(response.message, "Login Failed!")
        elif response.success:
            if self.remember_var.get():
                with open("remember_me.json", "w") as file:
                    json.dump({
                        "remember": True,
                        "username": username
                    }, file)
            else:
                if os.path.exists("remember_me.json"):
                    os.remove("remember_me.json")

            home_frame = self.view_manager.show_frame("home")
            self.view_manager.current_employee = response.data
            home_frame.set_current_employee(response.data)

    def register_button_clicked(self):
        self.view_manager.show_frame("register")

    def load_remembered_user(self):
        if os.path.exists("remember_me.json"):
            with open("remember_me.json", "r") as file:
                data = json.load(file)
                if data.get("remember"):
                    self.user_entry.insert(0, data.get("username"))
                    self.remember_var.set(True)
