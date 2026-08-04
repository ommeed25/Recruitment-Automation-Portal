from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import Job, LinkedInAccount

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

    for (email,) in created_by_list:

        account = (
            db.query(LinkedInAccount)
            .filter(LinkedInAccount.email == email)
            .first()
        )

        recruiters.append({
            "employee_id": account.employee_id if account else None,
            "full_name": account.full_name if account else email.split("@")[0].replace(".", " ").title(),
            "email": email,
            "connected": account is not None,
        })

        accounts = db.query(LinkedInAccount).all()

    for account in accounts:
        exists = any(r["email"] == account.email for r in recruiters)

        if not exists:
            recruiters.append({
                "employee_id": account.employee_id,
                "full_name": account.full_name,
                "email": account.email,
                "connected": True,
            })

    return recruiters