from ttkbootstrap import Window, Frame
from ttkbootstrap.constants import *
import json
import os
from Presentation.Mobile.api_client import APIClient
from Presentation.Mobile.UI.login_frame import LoginFrame
from Presentation.Mobile.UI.register_frame import RegisterFrame
from Presentation.Mobile.UI.home_frame import HomeFrame
from Presentation.Mobile.UI.profile_frame import ProfileFrame
from Presentation.Mobile.UI.account_management_frame import AccountManagementFrame
from Presentation.Mobile.UI.transaction_management_frame import TransactionManagementFrame

# Configuration
API_BASE_URL = "http://127.0.0.1:9090"
CONFIG_FILE = "local_storage.json"

# UI Application
class CoreBankingApp(Window):
    def __init__(self):
        super().__init__(themename="litera", title="Core Banking Mobile")
        self.geometry("400x800")
        self.resizable(False, False)

        self.api = APIClient(API_BASE_URL)
        self.frames = {}

        # Container to hold all screens
        self.container = Frame(self)
        self.container.pack(fill=BOTH, expand=True)

        # Initialize screens
        self.frames["Login"] = LoginFrame(self.container, self)
        self.frames["Register"] = RegisterFrame(self.container, self)
        self.frames["Home"] = HomeFrame(self.container, self)
        self.frames["Profile"] = ProfileFrame(self.container, self)
        self.frames["AccountManagementFrame"] = AccountManagementFrame(self.container, self)
        self.frames["TransactionManagementFrame"] = TransactionManagementFrame(self.container, self)


        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Load saved credentials if "Remember Me" was used
        self.load_local_storage()

        self.show_frame("Login")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        # Refresh dynamic content when showing
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def load_local_storage(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                if data.get("remember"):
                    self.frames["Login"].entry_username.insert(0, data.get("username", ""))
                    self.frames["Login"].var_remember.set(True)
            except Exception:
                pass

    def save_local_storage(self, username, remember):
        data = {"remember": remember, "username": username if remember else ""}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)



app = CoreBankingApp()
app.mainloop()