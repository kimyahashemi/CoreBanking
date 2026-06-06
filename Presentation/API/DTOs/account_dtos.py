from pydantic import BaseModel

class LoginCredentials(BaseModel):
    username: str
    password: str

class CreateAccountRequest(BaseModel):
    account_number: str
    account_type_id: int
    customer_id: int

class UpdateAccountRequest(BaseModel):
    id : int
    account_number : str
    account_type_id : int
    opening_date : str
    balance : float
    is_active : bool
    customer_id : int

class DeactivateAccount(BaseModel):
    id : int
