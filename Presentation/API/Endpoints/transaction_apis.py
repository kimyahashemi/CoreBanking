from fastapi import APIRouter, Depends, HTTPException, Response, Query
from BusinessLogic.transaction_business import TransactionBusiness
from BusinessLogic.employee_business import EmployeeBusiness
from Presentation.API.DependencyInjection.transaction_dependency import get_transaction_business
from Presentation.API.DTOs.transaction_dtos import CreateTransactionRequest
from Presentation.API.DependencyInjection.auth_dependency import get_current_employee
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import tempfile
import os

transaction_router = APIRouter(prefix="/api", tags=["Transactions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
@transaction_router.get("/transaction_management")
def get_transaction_list(current_employee = Depends(get_current_employee),
                        transaction: TransactionBusiness=Depends(get_transaction_business),
                         account_id : int = Query()):

    transaction_response = transaction.get_transaction_list(current_employee = current_employee, account_id=account_id)
    if not transaction_response.success:
        status_code = 403 if transaction_response.message == "Access Denied!" else 400
        raise HTTPException(status_code=status_code, detail=transaction_response.message)
    return {"success": True,"message": "",
        "data": [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "transaction_type": t.transaction_type.name,
                "insert_date_time": t.insert_date_time,
                "account_id": t.account_id
            }
            for t in transaction_response.data
        ]
    }

@transaction_router.post("/create_transaction")
def create_transactions(request : CreateTransactionRequest, transaction_business: TransactionBusiness=Depends(get_transaction_business)):
    response = transaction_business.create_transaction(request.amount, request.transaction_type, request.account_id)
    if response.success:
        return {"success": True, "message": "Transaction created successfully"}
    else:
        raise HTTPException(status_code=400, detail= response.message)