from Presentation.Mobile.UI.base_frame import BaseFrame
from tkinter import font as tkfont
from ttkbootstrap import Frame, Label, Button
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, X, BOTH, BOTTOM, CENTER

class HomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # Define Fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        subtitle_font = tkfont.Font(family="Helvetica", size=10)
        welcome_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        footer_font = tkfont.Font(family="Helvetica", size=9)

        # Main Container (simulating the white box in HTML)
        container = Frame(self, padding=30)
        container.pack(fill=BOTH, expand=True)

        # Logo Section
        Label(container, text="Core Banking", font=title_font, bootstyle=PRIMARY, justify=CENTER).pack(pady=(20, 5))
        Label(container, text="Secure Banking Management System", font=subtitle_font, bootstyle=SECONDARY,
              justify=CENTER).pack(pady=(0, 25))

        # Header / Welcome Label
        self.header_label = Label(container, text="Home Page", font=welcome_font, justify=CENTER, foreground="#0f172a")
        self.header_label.pack(pady=(0, 30))

        # Menu Buttons
        self.profile_btn = Button(container, text="My Profile", bootstyle=PRIMARY, command=self.profile_button_clicked)
        self.profile_btn.pack(fill=X, pady=7, ipady=8)

        self.account_btn = Button(
            container,
            text="Account Management",
            bootstyle=SUCCESS,
            command=self.account_management_button_clicked
        )
        # account_btn is NOT packed initially. It will be shown if the user is a Banker.

        self.logout_btn = Button(
            container,
            text="Logout",
            bootstyle=SECONDARY,
            command=self.logout_button_clicked
        )
        self.logout_btn.pack(fill=X, pady=7, ipady=8)

        # Footer
        Label(container, text="Internal Employee Portal", font=footer_font, bootstyle=SECONDARY, justify=CENTER).pack(
            side=BOTTOM, pady=20)

    def set_current_employee(self, employee):
        if not employee:
            self.controller.show_frame("LoginFrame")
            return

        first_name = employee.get("first_name", "")
        last_name = employee.get("last_name", "")
        role = employee.get("role", "")

        # Update Header
        self.header_label.config(text=f"Welcome {first_name} {last_name}!")

        # Toggle Account Management Button based on role (Case-insensitive check)
        if role.strip().upper() == "BANKER":
            # Pack it before the logout button so it stays in the middle
            self.account_btn.pack(fill=X, pady=7, ipady=8, before=self.logout_btn)
        else:
            # Hide if not a banker
            self.account_btn.pack_forget()

    def profile_button_clicked(self):
        employee_data = self.controller.api.user_data
        self.controller.frames["Profile"].load_profile(employee_data)
        self.controller.show_frame("Profile")

    def account_management_button_clicked(self):
        self.controller.show_frame("AccountManagementFrame")  # Assuming you create this frame next

    def logout_button_clicked(self):
        self.controller.api.token = None
        self.controller.api.user_data = None

        # Optional: Clear the login screen fields
        self.controller.frames["Login"].clear_fields()

        # 2. Navigate back to login using the CORRECT frame name
        self.controller.show_frame("Login")