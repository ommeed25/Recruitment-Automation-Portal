from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import SalesPostHistory


router = APIRouter(
    prefix="/sales/history",
    tags=["Sales History"]
)


@router.get("/")
def get_sales_history(
    db: Session = Depends(get_db)
):
    history = (
        db.query(SalesPostHistory)
        .order_by(SalesPostHistory.created_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "sales_linkedin_account_id": item.sales_linkedin_account_id,
            "linkedin_post_id": item.linkedin_post_id,
            "post_status": item.post_status,
            "error_message": item.error_message,
            "posted_at": item.posted_at,
            "created_at": item.created_at,
        }
        for item in history
    ]