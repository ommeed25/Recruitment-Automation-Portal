from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import SalesSettings


router = APIRouter(
    prefix="/sales/settings",
    tags=["Sales Settings"]
)


@router.get("/")
def get_sales_settings(
    db: Session = Depends(get_db)
):
    settings = db.query(SalesSettings).first()

    if not settings:
        settings = SalesSettings(
            is_enabled=True,
            posting_time="10:00",
            rotation_index=0,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "id": settings.id,
        "is_enabled": settings.is_enabled,
        "posting_time": settings.posting_time,
        "active_image_id": settings.active_image_id,
        "rotation_index": settings.rotation_index,
        "last_rotation_date": settings.last_rotation_date,
    }


@router.put("/")
def update_sales_settings(
    is_enabled: bool,
    posting_time: str,
    db: Session = Depends(get_db)
):
    settings = db.query(SalesSettings).first()

    if not settings:
        settings = SalesSettings(
            is_enabled=is_enabled,
            posting_time=posting_time,
            rotation_index=0,
        )
        db.add(settings)
    else:
        settings.is_enabled = is_enabled
        settings.posting_time = posting_time

    db.commit()
    db.refresh(settings)

    return {
        "message": "Sales settings updated",
        "is_enabled": settings.is_enabled,
        "posting_time": settings.posting_time,
        "active_image_id": settings.active_image_id,
        "rotation_index": settings.rotation_index,
        "last_rotation_date": settings.last_rotation_date,
    }