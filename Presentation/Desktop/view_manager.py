from Presentation.Desktop.window import Window
from Presentation.Desktop.Frames.login import LoginFrame
from Presentation.Desktop.Frames.register import RegisterFrame
from Presentation.Desktop.Frames.home import HomeFrame
from Presentation.Desktop.Frames.profile import ProfileFrame
from Presentation.Desktop.Frames.account_management import AccountManagement
from Presentation.Desktop.Frames.create_account import CreateAccountFrame
from Presentation.Desktop.Frames.transaction_management import TransactionManagement
from Presentation.Desktop.Frames.create_transaction import CreateTransactionFrame
from Presentation.Desktop.Frames.update_account import UpdateAccount
from Presentation.Desktop.Frames.Shared.navbar import Navbar
from BusinessLogic.employee_business import EmployeeBusiness
from BusinessLogic.account_business import AccountBusiness
from BusinessLogic.transaction_business import TransactionBusiness
from BusinessLogic.customer_business import CustomerBusiness


class ViewManager:
    def __init__(self, employee_business: EmployeeBusiness,
                 account_business: AccountBusiness,
                 transaction_business: TransactionBusiness,
                 customer_business: CustomerBusiness):
        self.frames = {}
        self.employee_business = employee_business
        self.account_business = account_business
        self.transaction_business = transaction_business
        self.app_window = Window("Core Banking Application")

        self.current_employee = None
        self.navbar = Navbar(self.app_window)
        self.navbar.grid(row=0, column=0, sticky="ew")

        # Increased dimensions to prevent UI elements from overflowing
        self.add_frame("update_account", UpdateAccount(self.app_window, self, account_business), 700, 650)
        self.add_frame("create_account", CreateAccountFrame(self.app_window, self, account_business, customer_business),
                       700, 650)
        self.add_frame("create_transaction", CreateTransactionFrame(self.app_window, self, transaction_business), 700,
                       650)
        self.add_frame("transaction_management", TransactionManagement(self.app_window, self, transaction_business),
                       800, 600)
        self.add_frame("account_management", AccountManagement(self.app_window, self, account_business), 800, 600)
        self.add_frame("profile", ProfileFrame(self.app_window, self), 500, 650)
        self.add_frame("home", HomeFrame(self.app_window, self), 500, 500)
        self.add_frame("register", RegisterFrame(self.app_window, employee_business, self), 500, 650)
        self.add_frame("login", LoginFrame(self.app_window, employee_business, self), 500, 650)

        # Set initial window size to match the login frame
        self.app_window.window_resize(f"500x650")
        self.app_window.show()

    def add_frame(self, frame_name, frame, width, height):
        self.frames[frame_name] = {
            "frame": frame,
            "size": f"{width}x{height}"
        }
        frame.grid(row=1, column=0, sticky="ewns")

    def show_frame(self, frame_name):
        frame_data = self.frames[frame_name]
        frame = frame_data["frame"]
        frame_size = frame_data["size"]

        frame.tkraise()
        self.app_window.window_resize(frame_size)

        return frame
