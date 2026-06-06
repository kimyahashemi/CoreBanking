from tkinter import Frame, Label, Entry, Button
from PIL import ImageTk
from captcha.image import ImageCaptcha
import random
import string
from Common.Decorators.performance_logger import performance_logger_decorator

class CaptchaComponent(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.captcha_text = ""
        self.captcha_photo = None

        # Image label
        self.image_label = Label(self)
        self.image_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Entry
        self.entry = Entry(self)
        self.entry.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        # Refresh button
        self.refresh_button = Button(self, text="Refresh", command=self.generate_captcha)
        self.refresh_button.grid(row=1, column=1, padx=(5, 0), pady=(0, 10))

        self.grid_columnconfigure(0, weight=1)

        self.generate_captcha()
    
    @performance_logger_decorator
    def generate_captcha(self):
        self.captcha_text = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

        image_captcha = ImageCaptcha(width=300, height=90)
        captcha_image = image_captcha.generate_image(self.captcha_text)

        self.captcha_photo = ImageTk.PhotoImage(captcha_image)
        self.image_label.config(image=self.captcha_photo)

        self.entry.delete(0, "end")

    def is_valid(self):
        return self.entry.get() == self.captcha_text

    def clear(self):
        self.entry.delete(0, "end")

