import requests
from io import BytesIO
from PIL import Image, ImageTk

class APIClient:
    def __init__(self, api_base_url):
        # Using a Session to retain the session cookie for the CAPTCHA
        self.session = requests.Session()
        self.token = None
        self.user_data = None
        self.api_base_url = api_base_url

    def get_captcha(self):
        try:
            response = self.session.get(f"{self.api_base_url}/auth/captcha")
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((220, 70), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Captcha Error: {e}")
            return None

    def login(self, username, password, captcha):
        url = f"{self.api_base_url}/auth/login"
        payload = {"username": username, "password": password, "captcha": captcha}
        try:
            response = self.session.post(url, json=payload)
            return response.status_code, response.json()
        except requests.exceptions.RequestException as e:
            return 500, {"detail": str(e)}

    def register(self, payload):
        url = f"{self.api_base_url}/auth/register"
        try:
            response = self.session.post(url, json=payload)
            return response.status_code, response.json()
        except requests.exceptions.RequestException as e:
            return 500, {"detail": str(e)}