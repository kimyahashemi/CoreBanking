from ttkbootstrap import Frame, Combobox, Label
from ttkbootstrap.constants import PRIMARY

class Navbar(Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window  # store reference

        # Add padding to the navbar frame to give it breathing room
        self.configure(padding=10)
        self.grid_columnconfigure(1, weight=1)

        # Added a clean label to clarify the dropdown's purpose
        self.theme_label = Label(
            self,
            text="Theme:",
            font=("Helvetica", 10, "bold"),
            bootstyle=PRIMARY
        )
        self.theme_label.grid(row=0, column=0, pady=5, padx=(10, 5), sticky="w")

        self.theme_combobox = Combobox(
            self,
            values=("Light", "Dark"),
            state="readonly",
            bootstyle=PRIMARY,
            width=10
        )
        self.theme_combobox.grid(row=0, column=1, pady=5, padx=(0, 10), sticky="w")
        self.theme_combobox.set("Light")

        # Bind selection change event
        self.theme_combobox.bind("<<ComboboxSelected>>", self.on_theme_change)

    def on_theme_change(self, event):
        selected = self.theme_combobox.get()
        self.window.change_theme(selected)
