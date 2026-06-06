from Presentation.Mobile.UI.base_frame import BaseFrame
from ttkbootstrap import  Frame, Label, Entry, Button, Checkbutton
from ttkbootstrap.style import PRIMARY, SECONDARY, INFO, SUCCESS, WARNING
from ttkbootstrap.dialogs import  Messagebox
from tkinter import BOTH, END, BooleanVar, W, X, LEFT, RIGHT

class LoginFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.build_ui()

    def build_ui(self):
        content = Frame(self, padding=30)
        content.pack(fill=BOTH, expand=True)

        Label(content, text="Core Banking System", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY).pack(
            pady=(40, 5))
        Label(content, text="Employee Secure Login", font=("Helvetica", 10), bootstyle=SECONDARY).pack(pady=(0, 30))

        # Form
        Label(content, text="Username", font=("Helvetica", 10, "bold")).pack(anchor=W)
        self.entry_username = Entry(content, font=("Helvetica", 12))
        self.entry_username.pack(fill=X, pady=(5, 15))

        Label(content, text="Password", font=("Helvetica", 10, "bold")).pack(anchor=W)
        pass_frame = Frame(content)
        pass_frame.pack(fill=X, pady=(5, 10))

        self.entry_password = Entry(pass_frame, font=("Helvetica", 12), show="*")
        self.entry_password.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        self.btn_show_pass = Button(pass_frame, text="Show", bootstyle=INFO, command=self.toggle_password)
        self.btn_show_pass.pack(side=RIGHT)

        self.var_remember = BooleanVar()
        Checkbutton(content, text="Remember me", variable=self.var_remember, bootstyle="primary-round-toggle").pack(
            anchor=W, pady=(0, 15))

        # Captcha
        self.lbl_captcha = Label(content)
        self.lbl_captcha.pack(pady=5)

        self.entry_captcha = Entry(content, font=("Helvetica", 12))
        self.entry_captcha.pack(fill=X, pady=5)

        Button(content, text="Refresh CAPTCHA", bootstyle=SUCCESS, command=self.refresh_captcha).pack(fill=X,
                                                                                                          pady=(0, 20))

        # Actions
        Button(content, text="Login", bootstyle=PRIMARY, command=self.handle_login).pack(fill=X, pady=5, ipady=5)
        Button(content, text="Register", bootstyle=SECONDARY,
                   command=lambda: self.controller.show_frame("Register")).pack(fill=X, pady=5, ipady=5)

    def on_show(self):
        self.refresh_captcha()
        self.entry_password.delete(0, END)
        self.entry_captcha.delete(0, END)

    def refresh_captcha(self):
        img = self.controller.api.get_captcha()
        if img:
            self.lbl_captcha.config(image=img)
            self.lbl_captcha.image = img  # Keep a reference to avoid garbage collection

    def toggle_password(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.config(show="")
            self.btn_show_pass.config(text="Hide")
        else:
            self.entry_password.config(show="*")
            self.btn_show_pass.config(text="Show")

    def handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        captcha = self.entry_captcha.get().strip()

        if not username or not password or not captcha:
            Messagebox.show_error("Please fill all fields.", "Error")
            return

        status, data = self.controller.api.login(username, password, captcha)

        if status == 200:
            self.controller.api.token = data.get("access_token")
            employee_data = data.get("employee")
            self.controller.api.user_data = employee_data

            self.controller.save_local_storage(username, self.var_remember.get())
            self.controller.frames["Home"].set_current_employee(employee_data)

            self.controller.show_frame("Home")
        else:
            Messagebox.show_error(data.get("detail", "Login Failed"), "Login Failed")
            self.refresh_captcha()

    def clear_fields(self):
        self.entry_password.delete(0, 'end')
