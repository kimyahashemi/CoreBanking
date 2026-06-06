from ttkbootstrap import Frame, Label, Entry, Button
from ttkbootstrap.constants import SUCCESS, SECONDARY, PRIMARY
from ttkbootstrap.dialogs import Messagebox
from Presentation.Desktop.UIComponents.password_entry import PasswordEntry
from Presentation.Desktop.UIComponents.captcha import CaptchaComponent


class RegisterFrame(Frame):
    def __init__(self, window, employee_business, view_manager):
        # Apply formal padding for card layout
        super().__init__(window, padding=40)

        self.employee_business = employee_business
        self.view_manager = view_manager

        # Center the form
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Formal Header
        self.header_label = Label(self, text="Register", font=("Helvetica", 24, "bold"), bootstyle=PRIMARY)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # First Name
        Label(self, text="First Name", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="e", padx=10,
                                                                            pady=(0, 15))
        self.first_name_entry = Entry(self, width=30)
        self.first_name_entry.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 15))

        # Last Name
        Label(self, text="Last Name", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="e", padx=10,
                                                                           pady=(0, 15))
        self.last_name_entry = Entry(self, width=30)
        self.last_name_entry.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 15))

        # Username
        Label(self, text="Username", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky="e", padx=10,
                                                                          pady=(0, 15))
        self.username_entry = Entry(self, width=30)
        self.username_entry.grid(row=3, column=1, sticky="w", padx=10, pady=(0, 15))

        # Password
        Label(self, text="Password", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky="e", padx=10,
                                                                          pady=(0, 15))
        self.password_component = PasswordEntry(self)
        self.password_component.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 15))

        # Email
        Label(self, text="Email", font=("Helvetica", 10, "bold")).grid(row=5, column=0, sticky="e", padx=10,
                                                                       pady=(0, 15))
        self.email_component = Entry(self, width=30)
        self.email_component.grid(row=5, column=1, sticky="w", padx=10, pady=(0, 15))

        # Captcha (Centered with columnspan=2 to prevent overflow)
        self.captcha_component = CaptchaComponent(self)
        self.captcha_component.grid(row=6, column=0, columnspan=2, pady=20)

        # Action Buttons Container for consistent placement
        self.button_frame = Frame(self)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))

        # Register Button (Primary action -> SUCCESS)
        self.register_button = Button(self.button_frame, text="Register", bootstyle=SUCCESS,
                                      command=self.register_clicked)
        self.register_button.grid(row=0, column=0, padx=10, ipadx=20, ipady=5)

        # Back to login (Secondary action)
        self.back_button = Button(self.button_frame, text="Back to Login", bootstyle=SECONDARY,
                                  command=self.back_to_login)
        self.back_button.grid(row=0, column=1, padx=10, ipadx=20, ipady=5)

    def register_clicked(self):
        if not self.captcha_component.is_valid():
            Messagebox.show_error("Invalid CAPTCHA. Please try again.", "Error")
            self.captcha_component.generate_captcha()
            return

        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_component.get_password_value()
        email = self.email_component.get()

        response = self.employee_business.register(
            first_name,
            last_name,
            username,
            password,
            email
        )

        if not response.success:
            Messagebox.show_error(response.message, "Registration Failed")
        else:
            Messagebox.show_info(response.message, "Success")
            self.back_to_login()

    def clear_fields(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.email_component.delete(0, 'end')
        self.captcha_component.generate_captcha()
        # Note: Depending on PasswordEntry implementation, you may need a clear method there too.

    def back_to_login(self):
        self.clear_fields()
        self.view_manager.show_frame("login")
