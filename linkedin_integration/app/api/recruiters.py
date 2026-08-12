from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.recruiter import RecruiterCreate
from app.db.dependencies import get_db
from app.db.models import Job, LinkedInAccount, LinkedInPost , VendorPostHistory

router = APIRouter(
    prefix="/recruiters",
    tags=["Recruiters"]
)


@router.get("/")
def get_recruiters(
    db: Session = Depends(get_db)
):
    recruiters = []

    created_by_list = (
        db.query(Job.created_by)
        .distinct()
        .all()
    )

    # Recruiters from Jobs table
    for (email,) in created_by_list:

        account = (
            db.query(LinkedInAccount)
            .filter(LinkedInAccount.email == email)
            .first()
        )

        recruiters.append({
            "id": account.id if account else None,
            "employee_id": account.employee_id if account else None,
            "full_name": (
                account.full_name
                if account
                else email.split("@")[0].replace(".", " ").title()
            ),
            "email": email,
            "connected": (
                account is not None
                and account.access_token is not None
            ),
        })

    # Recruiters added manually
    accounts = db.query(LinkedInAccount).all()

    for account in accounts:

        exists = any(
            r["email"] == account.email
            for r in recruiters
        )

        if not exists:
            recruiters.append({
                "id": account.id,
                "employee_id": account.employee_id,
                "full_name": account.full_name,
                "email": account.email,
                "connected": account.access_token is not None,
            })

    return recruiters


@router.post("/")
def create_recruiter(
    recruiter: RecruiterCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(LinkedInAccount)
        .filter(
            LinkedInAccount.email == recruiter.email
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Recruiter already exists"
        )

    account = LinkedInAccount(
        employee_id=recruiter.employee_id,
        full_name=recruiter.full_name,
        email=recruiter.email,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return {
        "message": "Recruiter added successfully"
    }


@router.delete("/{account_id}")
def delete_recruiter(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = (
        db.query(LinkedInAccount)
        .filter(
            LinkedInAccount.id == account_id
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Recruiter not found"
        )

    db.query(LinkedInPost).filter(
        LinkedInPost.linkedin_account_id == account.id
    ).delete(synchronize_session=False)

    db.query(VendorPostHistory).filter(
        VendorPostHistory.linkedin_account_id == account.id
    ).delete(synchronize_session=False)

    db.delete(account)
    db.commit()

    return {
        "message": "Recruiter deleted successfully"
    }
