from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from Presentation.API.DTOs.authentication_dtos import LoginRequest, RegisterRequest
from Presentation.API.DependencyInjection.employee_dependency import employee_dependency
from BusinessLogic.employee_business import EmployeeBusiness
from captcha.image import ImageCaptcha
from Presentation.API.Endpoints.security import create_access_token
from io import BytesIO
import random
import string
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/captcha")
def generate_captcha(request: Request):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    request.session["captcha"] = captcha_text

    # Generate image
    image = ImageCaptcha()
    data = image.generate(captcha_text)
    image_bytes = BytesIO(data.read())
    return Response(content=image_bytes.getvalue(), media_type="image/png")

@auth_router.post("/login")
def login(request: Request, credentials: LoginRequest,
    employee_business: EmployeeBusiness = Depends(employee_dependency)):

    stored_captcha = request.session.get("captcha")

    if not stored_captcha:
        raise HTTPException(status_code=400, detail="CAPTCHA expired. Please refresh and try again.")

    if credentials.captcha.upper() != stored_captcha.upper():
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    result = employee_business.login(credentials.username, credentials.password)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    employee = result.data

    token_data = {"sub": employee.username, "role": employee.role.name}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer", "message": "Login successful",
            "employee": {"id": employee.id, "username": employee.username, "first_name": employee.first_name,
            "last_name": employee.last_name, "role": employee.role.name, "status": employee.status.name, "email" : employee.email}}
@auth_router.post("/register")
def register(request: Request, credentials: RegisterRequest,
             employee_business: EmployeeBusiness = Depends(employee_dependency)):
    stored_captcha = request.session.get("captcha")

    if not stored_captcha:
        raise HTTPException(status_code=400, detail="CAPTCHA expired. Please refresh and try again.")

    if credentials.captcha.upper() != stored_captcha.upper():
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    result = employee_business.register(credentials.first_name,credentials.last_name,
        credentials.username, credentials.password, credentials.email)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return {"message": result.message}
