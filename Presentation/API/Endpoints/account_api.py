from fastapi import APIRouter, Depends, HTTPException, status, Query
from Presentation.API.DependencyInjection.account_dependency import account_dependency
from BusinessLogic.account_business import AccountBusiness
from BusinessLogic.customer_business import CustomerBusiness
from Presentation.API.DependencyInjection.auth_dependency import get_current_employee
from Presentation.API.DependencyInjection.customer_dependency import customer_dependency
from Presentation.API.DTOs.account_dtos import CreateAccountRequest, UpdateAccountRequest, DeactivateAccount
from Common.Entities.account import Account
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

account_router = APIRouter(prefix="/api", tags=["Account Management"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
@account_router.post("/accounts")
def get_account_list(account: AccountBusiness = Depends(account_dependency),
                     current_employee = Depends(get_current_employee),
                    term: str = "", page_number: int = 1, page_size: int = 10):


    account_response = account.get_account_list(current_employee=current_employee,
        term=term, page_number=page_number, page_size=page_size)

    if not account_response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=account_response.message
        )

    return {
        "success": True,
        "message": "",
        "data": {
            "account_list": [
                {
                    "account_id": acc.account_id,
                    "account_number": acc.account_number,
                    "account_type": acc.account_type.name,
                    "opening_date": str(acc.opening_date),
                    "balance": acc.balance,
                    "customer_id": acc.customer_id
                }
                for acc in account_response.data["account_list"]
            ],
            "total_count": account_response.data["total_count"]}}

@account_router.get("/accounts/get_customer")
def find_customer_by_national_code(customer_national_code: str = Query(), customer_business : CustomerBusiness = Depends(customer_dependency)):
    customer  = customer_business.find_customer_by_national_code(customer_national_code)
    if not customer :
        raise HTTPException(status_code=404, detail="Customer not found with the provided national code.")

    return {"customer": {"customer_id": customer.id, "customer_first_name": customer.first_name,
                         "customer_last_name": customer.last_name, "customer_phone": customer.phone}}

@account_router.get("/accounts/generate_number")
def generate_new_account_number(account_business: AccountBusiness = Depends(account_dependency)):
    account_number = account_business.generate_account_number()
    return {"account_number": account_number}

@account_router.post("/accounts/create", status_code=status.HTTP_201_CREATED)
def create_account(request_data : CreateAccountRequest, account_business: AccountBusiness = Depends(account_dependency)):
    new_account = Account(
        id=None,
        account_number=request_data.account_number,
        account_type_id=request_data.account_type_id,
        opening_date=None,
        balance=0,
        is_active=True,
        customer_id=request_data.customer_id)

    response = account_business.create_account(new_account)
    if not response.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.message)

    return {"message": "Account created successfully!"}

@account_router.put("/accounts/update", status_code=status.HTTP_202_ACCEPTED)
def update_account(request_data : UpdateAccountRequest, account_business: AccountBusiness = Depends(account_dependency)):
    updated_account = Account(request_data.id, request_data.account_number, request_data.account_type_id,
                              request_data.opening_date, request_data.balance, request_data.is_active,
                              request_data.customer_id)
    response = account_business.update_account(updated_account)
    if not response.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.message)
    return {"message": "Account updated successfully!"}

@account_router.put("/accounts/deactivate", status_code=status.HTTP_202_ACCEPTED)
def deactivate_account(request_data : DeactivateAccount, account_business: AccountBusiness = Depends(account_dependency)):
    response = account_business.deactivate_account(request_data.id)
    if not response.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.message)
    return {"message": "Account deactivated successfully!"}

@account_router.get("/accounts/filter")
def filter_accounts(
        type: str = Query("", description="Account type, e.g., Debit or Credit"),
        min: Optional[str] = Query(None, description="Minimum balance"),
        max: Optional[str] = Query(None, description="Maximum balance"),
        account_business: AccountBusiness = Depends(account_dependency)):
    type_mapping = {"Debit": "1","Credit": "2",}
    mapped_type = ""
    if type and type.strip() != "":
        mapped_type = type_mapping.get(type.capitalize(), "")

    safe_min = None
    if min and min.strip() != "":
        try:
            safe_min = float(min)
        except ValueError:
            pass

    safe_max = None
    if max and max.strip() != "":
        try:
            safe_max = float(max)
        except ValueError:
            pass


    result = account_business.filter_accounts(account_type=mapped_type,min_balance=safe_min,max_balance=safe_max)

    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.message
        )

    return {"success": True, "message": "",
        "data": {
            "account_list": [
                {
                    "account_id": acc.account_id,
                    "account_number": acc.account_number,
                    "account_type": acc.account_type.name,
                    "opening_date": str(acc.opening_date),
                    "balance": acc.balance,
                    "customer_id": acc.customer_id
                }
                for acc in result.data["account_list"]
            ],
            "total_count": result.data["total_count"]
        }
    }