from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.sales_publish_service import publish_sales_post


router = APIRouter(
    prefix="/sales/posts",
    tags=["Sales Posts"]
)


@router.post("/publish")
def publish_sales_post_api(
    db: Session = Depends(get_db)
):
    return publish_sales_post(db)