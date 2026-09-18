from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import SalesHashtag
from app.schemas.vendor import VendorHashtagBulkCreate


router = APIRouter(
    prefix="/sales/hashtags",
    tags=["Sales Hashtags"]
)


@router.get("/")
def get_sales_hashtags(
    db: Session = Depends(get_db)
):
    hashtags = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.is_active.is_(True))
        .order_by(SalesHashtag.id.asc())
        .all()
    )

    return [
        {
            "id": hashtag.id,
            "hashtag": hashtag.hashtag,
            "is_active": hashtag.is_active,
        }
        for hashtag in hashtags
    ]


@router.post("/")
def add_sales_hashtag(
    hashtag: str,
    db: Session = Depends(get_db)
):
    hashtag = hashtag.strip()

    if not hashtag:
        raise HTTPException(
            status_code=400,
            detail="Hashtag cannot be empty"
        )

    if not hashtag.startswith("#"):
        hashtag = f"#{hashtag}"

    existing = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.hashtag.ilike(hashtag))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Hashtag already exists"
        )

    active_count = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.is_active.is_(True))
        .count()
    )

    if active_count >= 30:
        raise HTTPException(
            status_code=400,
            detail="Maximum 30 hashtags allowed"
        )

    new_hashtag = SalesHashtag(
        hashtag=hashtag,
        is_active=True
    )

    db.add(new_hashtag)
    db.commit()
    db.refresh(new_hashtag)

    return {
        "id": new_hashtag.id,
        "hashtag": new_hashtag.hashtag,
        "is_active": new_hashtag.is_active,
    }


@router.post("/bulk")
def add_sales_hashtags(
    data: VendorHashtagBulkCreate,
    db: Session = Depends(get_db)
):
    if not data.hashtags:
        raise HTTPException(
            status_code=400,
            detail="No hashtags provided"
        )

    active_hashtags = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.is_active.is_(True))
        .all()
    )

    existing = {
        h.hashtag.lower()
        for h in active_hashtags
    }

    new_values = []

    for value in data.hashtags:
        value = value.strip()

        if not value:
            continue

        if not value.startswith("#"):
            value = f"#{value}"

        if value.lower() in existing:
            continue

        existing.add(value.lower())
        new_values.append(value)

    if len(active_hashtags) + len(new_values) > 30:
        raise HTTPException(
            status_code=400,
            detail="Maximum 30 hashtags allowed"
        )

    hashtags = [
        SalesHashtag(
            hashtag=value,
            is_active=True
        )
        for value in new_values
    ]

    db.add_all(hashtags)
    db.commit()

    return {
        "message": "Sales hashtags added successfully",
        "count": len(hashtags)
    }


@router.delete("/{hashtag_id}")
def delete_sales_hashtag(
    hashtag_id: int,
    db: Session = Depends(get_db)
):
    hashtag = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.id == hashtag_id)
        .first()
    )

    if not hashtag:
        raise HTTPException(
            status_code=404,
            detail="Sales hashtag not found"
        )

    db.delete(hashtag)
    db.commit()

    return {
        "message": "Sales hashtag deleted successfully"
    }