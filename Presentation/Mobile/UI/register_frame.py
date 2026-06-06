from Presentation.Mobile.UI.base_frame import BaseFrame
from ttkbootstrap import  Frame, Label, Entry, Button
from ttkbootstrap.style import PRIMARY, INFO, SUCCESS
from ttkbootstrap.dialogs import  Messagebox
from tkinter import BOTH, END, W, X, LEFT, RIGHT

class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.build_ui()

    def build_ui(self):
        content = Frame(self, padding=30)
        content.pack(fill=BOTH, expand=True)

        Label(content, text="Create Account", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY).pack(pady=(20, 5))

        # Fields
        fields = [
            ("First Name", "first_name"), ("Last Name", "last_name"),
            ("Username", "username"), ("Email", "email")
        ]

        self.entries = {}
        for label, key in fields:
            Label(content, text=label, font=("Helvetica", 10, "bold")).pack(anchor=W)
            ent = Entry(content, font=("Helvetica", 12))
            ent.pack(fill=X, pady=(2, 10))
            self.entries[key] = ent

        Label(content, text="Password", font=("Helvetica", 10, "bold")).pack(anchor=W)
        pass_frame = Frame(content)
        pass_frame.pack(fill=X, pady=(2, 10))
        self.entries["password"] = Entry(pass_frame, font=("Helvetica", 12), show="*")
        self.entries["password"].pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        self.btn_show_pass_reg = Button(pass_frame, text="Show", bootstyle=INFO, command=self.toggle_password)
        self.btn_show_pass_reg.pack(side=RIGHT)

        # Captcha
        self.lbl_captcha = Label(content)
        self.lbl_captcha.pack(pady=5)

        cap_frame = Frame(content)
        cap_frame.pack(fill=X, pady=5)
        self.entries["captcha"] = Entry(cap_frame, font=("Helvetica", 12))
        self.entries["captcha"].pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        Button(cap_frame, text="Refresh", bootstyle=SUCCESS, command=self.refresh_captcha).pack(side=RIGHT)

        # Actions
        Button(content, text="Register", bootstyle=SUCCESS, command=self.handle_register).pack(fill=X, pady=(15, 5),
                                                                                                   ipady=5)
        Button(content, text="Back to Login", bootstyle=PRIMARY,
                   command=lambda: self.controller.show_frame("Login")).pack(fill=X, pady=5, ipady=5)

    def on_show(self):
        self.refresh_captcha()
        for ent in self.entries.values():
            ent.delete(0, END)

    def refresh_captcha(self):
        img = self.controller.api.get_captcha()
        if img:
            self.lbl_captcha.config(image=img)
            self.lbl_captcha.image = img

    def toggle_password(self):
        ent = self.entries["password"]
        if ent.cget("show") == "*":
            ent.config(show="")
            self.btn_show_pass_reg.config(text="Hide")
        else:
            ent.config(show="*")
            self.btn_show_pass_reg.config(text="Show")

    def handle_register(self):
        payload = {k: v.get().strip() for k, v in self.entries.items()}

        if not all(payload.values()):
            Messagebox.show_error("All fields are required.", "Error")
            return

        status, data = self.controller.api.register(payload)

        if status == 200:
            Messagebox.show_info("Registration Successful! Please login.", "Success")
            self.controller.show_frame("Login")
        else:
            Messagebox.show_error(data.get("detail", "Registration Failed"), "Error")
            self.refresh_captcha()