from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.dependencies import get_db
from app.db.models import SalesLinkedInAccount


router = APIRouter(
    prefix="/sales/accounts",
    tags=["Sales Accounts"]
)


class SalesAccountCreate(BaseModel):
    full_name: str
    email: str
    employee_id: int | None = None

@router.get("/")
def get_sales_accounts(
    db: Session = Depends(get_db)
):
    accounts = db.query(SalesLinkedInAccount).all()

    return [
        {
            "id": account.id,
            "employee_id": account.employee_id,
            "linkedin_sub": account.linkedin_sub,
            "full_name": account.full_name,
            "email": account.email,
            "token_type": account.token_type,
            "expires_in": account.expires_in,
            "created_at": account.created_at,
            "updated_at": account.updated_at,
            "connected": account.access_token is not None,
        }
        for account in accounts
    ]

@router.post("/")
def create_sales_account(
    payload: SalesAccountCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(SalesLinkedInAccount)
        .filter(SalesLinkedInAccount.email == payload.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Sales account with this email already exists",
        )

    account = SalesLinkedInAccount(
        full_name=payload.full_name,
        email=payload.email,
        employee_id=payload.employee_id,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return {
        "id": account.id,
        "employee_id": account.employee_id,
        "full_name": account.full_name,
        "email": account.email,
        "connected": False,
    }

@router.delete("/{account_id}")
def delete_sales_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = (
        db.query(SalesLinkedInAccount)
        .filter(
            SalesLinkedInAccount.id == account_id
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Sales LinkedIn account not found"
        )

    db.delete(account)
    db.commit()

    return {
        "message": "Sales LinkedIn account deleted successfully"
    }