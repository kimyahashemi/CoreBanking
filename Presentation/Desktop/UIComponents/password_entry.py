from tkinter import Frame, Entry, Button

class PasswordEntry(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.password_entry = Entry(self, show="*")
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.status_button =Button(self, text="Show", command= self.status_button_clicked)
        self.status_button.grid(row=0, column=1, sticky="w")

    def status_button_clicked(self):
        current_status = self.status_button.cget("text")
        if current_status=="Show":
            self.status_button.config(text="Hide")
            self.password_entry.config(show="")
        else:
            self.status_button.config(text="Show")
            self.password_entry.config(show="*")

    def get_password_value(self):
        password = self.password_entry.get()
        return password