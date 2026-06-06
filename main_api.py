from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from Presentation.API.Endpoints.transaction_apis import transaction_router
from Presentation.API.Endpoints.authentication_api import auth_router
from Presentation.API.Endpoints.account_api import account_router
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Baam Core Banking API")
app.add_middleware(CORSMiddleware, allow_methods = ["*"], allow_headers = ["*"],allow_credentials=True)
app.add_middleware(SessionMiddleware,secret_key= os.getenv("SECRET_KEY"))

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)

@app.get("/")
def root():
    return RedirectResponse(url="/auth/login")
@app.get("/auth/login")
def login_page():
    return FileResponse("Presentation/API/FrontEnd/login.html")
@app.get("/auth/register")
def register_page():
    return FileResponse("Presentation/API/FrontEnd/register.html")
@app.get("/home")
def home_page():
    return FileResponse("Presentation/API/FrontEnd/home.html")
@app.get("/profile")
def profile():
    return FileResponse("Presentation/API/FrontEnd/profile.html")
@app.get("/api/account_management")
def account_management_page():
    return FileResponse("Presentation/API/FrontEnd/account_management.html")

@app.get("/transaction_management")
def transaction_management_page():
    return FileResponse("Presentation/API/FrontEnd/transaction_management.html")
