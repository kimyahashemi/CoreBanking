from ttkbootstrap import Frame, Label, Button
from ttkbootstrap.constants import PRIMARY, SUCCESS, OUTLINE
from tkinter import simpledialog, messagebox
from Common.Utils.email_service import EmailService


class ProfileFrame(Frame):
    def __init__(self, window, view_manager):
        super().__init__(window)

        self.view_manager = view_manager

        # Center the profile card in the middle of the screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create an inner frame to act as a "Card"
        self.card_frame = Frame(self, padding=40)
        self.card_frame.grid(row=0, column=0)
        self.card_frame.grid_columnconfigure(1, weight=1)

        # Header (Blue/Primary styling, larger formal font)
        self.header_label = Label(
            self.card_frame,
            text="Profile Page",
            font=("Helvetica", 20, "bold"),
            bootstyle=PRIMARY
        )
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")

        # Labels (Bold for keys)
        label_font = ("Helvetica", 10, "bold")

        self.employee_name_label = Label(self.card_frame, text="Name:", font=label_font)
        self.employee_name_label.grid(row=1, column=0, pady=10, padx=(0, 15), sticky="w")

        self.employee_role_label = Label(self.card_frame, text="Role:", font=label_font)
        self.employee_role_label.grid(row=2, column=0, pady=10, padx=(0, 15), sticky="w")

        self.employee_status_label = Label(self.card_frame, text="Status:", font=label_font)
        self.employee_status_label.grid(row=3, column=0, pady=10, padx=(0, 15), sticky="w")

        # Action Buttons (Success/Green for primary action, Outline Blue for secondary)
        self.reset_password_button = Button(
            self.card_frame,
            text="Reset Password",
            command=self.reset_password,
            bootstyle=SUCCESS
        )
        self.reset_password_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="ew")

        self.back_button = Button(
            self.card_frame,
            text="Back",
            command=self.back_button_clicked,
            bootstyle=(PRIMARY, OUTLINE)
        )
        self.back_button.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def back_button_clicked(self):
        self.view_manager.show_frame("home")

    def get_employee_info(self):
        employee = self.view_manager.current_employee
        value_font = ("Helvetica", 10)

        # Placed dynamically inside the card_frame to align with the labels
        self.employee_name = Label(self.card_frame, text=f"{employee.get_fullname()}", font=value_font)
        self.employee_name.grid(row=1, column=1, pady=10, padx=(0, 10), sticky="e")

        self.employee_role = Label(self.card_frame, text=f"{employee.role.name}", font=value_font)
        self.employee_role.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

        self.employee_status = Label(self.card_frame, text=f"{employee.status.name}", font=value_font)
        self.employee_status.grid(row=3, column=1, pady=10, padx=(0, 10), sticky="e")

    def reset_password(self):
        employee = self.view_manager.current_employee

        # Generate token
        token = EmailService.generate_reset_token()
        employee.set_reset_token(token)

        # Send email
        try:
            EmailService.send_reset_email(employee.email, token)
            messagebox.showinfo("Success", "Reset code sent to your email.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email:\n{e}")
            return

        # Ask user for code
        entered_token = simpledialog.askstring("Reset Password", "Enter the code sent to your email:")

        if not employee.verify_reset_token(entered_token):
            messagebox.showerror("Error", "Invalid reset code.")
            return

        # 4️⃣ Ask for new password
        new_password = simpledialog.askstring("New Password", "Enter new password:", show="*")

        if new_password:
            employee.set_password(new_password)
            self.view_manager.employee_business.update_password(
                employee.id,
                employee.password
            )
            employee.reset_token = None
            messagebox.showinfo("Success", "Password reset successfully!")
