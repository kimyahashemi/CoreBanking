from ttkbootstrap import  Frame, Label, Entry, Button, Checkbutton, Labelframe
from ttkbootstrap.style import PRIMARY, SECONDARY, INFO, SUCCESS, WARNING
from ttkbootstrap.dialogs import  Messagebox
from tkinter import BOTH, END, BooleanVar, W, X, LEFT, RIGHT, StringVar
import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
import requests


class ProfileFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        # StringVars to hold dynamic data
        self.var_name = StringVar(value="Loading...")
        self.var_role = StringVar(value="Loading...")
        self.var_status = StringVar(value="Loading...")

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = Frame(self)
        header_frame.pack(fill="x", pady=(10, 20))

        lbl_title = Label(header_frame, text="Profile Page", font=("Helvetica", 24, "bold"), bootstyle="primary")
        lbl_title.pack()

        lbl_subtitle = Label(header_frame, text="Employee Information & Security Settings", font=("Helvetica", 10),
                                 bootstyle="secondary")
        lbl_subtitle.pack()

        # Profile Card
        card_frame = Labelframe(self, text="Details", padding=15, bootstyle="info")
        card_frame.pack(fill="x", pady=10)

        # Name Row
        row_name = Frame(card_frame)
        row_name.pack(fill="x", pady=5)
        Label(row_name, text="Name:", font=("Helvetica", 12, "bold")).pack(side="left")
        Label(row_name, textvariable=self.var_name, font=("Helvetica", 12)).pack(side="right")

        # Role Row
        row_role = ttk.Frame(card_frame)
        row_role.pack(fill="x", pady=5)
        ttk.Label(row_role, text="Role:", font=("Helvetica", 12, "bold")).pack(side="left")
        ttk.Label(row_role, textvariable=self.var_role, font=("Helvetica", 12)).pack(side="right")

        # Status Row
        row_status = Frame(card_frame)
        row_status.pack(fill="x", pady=5)
        Label(row_status, text="Status:", font=("Helvetica", 12, "bold")).pack(side="left")
        Label(row_status, textvariable=self.var_status, font=("Helvetica", 12)).pack(side="right")

        # Buttons
        btn_frame = Frame(self)
        btn_frame.pack(fill="x", pady=20)

        btn_reset = Button(btn_frame, text="Reset Password", bootstyle="success", command=self.reset_password)
        btn_reset.pack(fill="x", pady=5, ipady=5)

        btn_back = Button(btn_frame, text="Back to Home", bootstyle="primary", command=self.go_back)
        btn_back.pack(fill="x", pady=5, ipady=5)

        # Footer
        lbl_footer = Label(self, text="Core Banking Employee Portal", font=("Helvetica", 9), bootstyle="secondary")
        lbl_footer.pack(side="bottom", pady=10)

    def load_profile(self, employee_data):
        if not employee_data:
            return

        first_name = employee_data.get("first_name", "")
        last_name = employee_data.get("last_name", "")
        role = employee_data.get("role", {}).get("name", "N/A") if isinstance(employee_data.get("role"),
                                                                              dict) else employee_data.get("role",
                                                                                                           "N/A")
        status = employee_data.get("status", "Active")  # Default to Active if not provided

        self.var_name.set(f"{first_name} {last_name}".strip())
        self.var_role.set(role)
        self.var_status.set(status)

    def reset_password(self):
        new_password = simpledialog.askstring("Reset Password", "Enter new password:", parent=self, show='*')

        if not new_password:
            return

        try:
            url = f"{self.controller.api.base_url}/employee/reset-password"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.controller.api.token}"  # Assuming you need JWT auth
            }
            payload = {"password": new_password}

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                Messagebox.show_info("Password reset successful", "Success")
            else:
                err_msg = response.json().get("detail", "Error resetting password")
                Messagebox.show_error(err_msg, "Error")

        except requests.exceptions.RequestException as e:
            Messagebox.show_error(f"Network error: {e}", "Error")

    def go_back(self):
        self.controller.show_frame("Home")
