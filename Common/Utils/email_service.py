import smtplib
import ssl
import secrets
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def generate_reset_token():
        return secrets.token_urlsafe(16)

    @staticmethod
    def send_reset_email(receiver_email, token):
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        if not sender_email or not sender_password:
            raise ValueError("Email credentials not found in environment variables")

        message = EmailMessage()
        message["Subject"] = "Password Reset Request"
        message["From"] = sender_email
        message["To"] = receiver_email
        message.set_content(
            f"""
            You requested a password reset.

            Your reset code is:

            {token}

            If you did not request this, ignore this email.
            """
        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)