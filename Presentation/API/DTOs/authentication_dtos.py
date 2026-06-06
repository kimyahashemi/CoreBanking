from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    captcha: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    captcha: str

class AuthResponse(BaseModel):
    success: bool
    message: str | None

