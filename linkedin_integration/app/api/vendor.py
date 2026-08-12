from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import (
    VendorImage,
    VendorSettings,
    VendorHashtag,
)

from app.schemas.vendor import VendorHashtagBulkCreate


router = APIRouter(
    prefix="/vendor",
    tags=["Vendor Partnership"]
)


UPLOAD_DIR = Path("uploads/vendor")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

@router.get("/settings")
def get_vendor_settings(
    db: Session = Depends(get_db)
):
    settings = db.query(VendorSettings).first()

    if not settings:
        settings = VendorSettings(
            is_enabled=True,
            posting_time="10:00"
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "id": settings.id,
        "is_enabled": settings.is_enabled,
        "posting_time": settings.posting_time,
        "active_image_id": settings.active_image_id,
    }


@router.put("/settings")
def update_vendor_settings(
    is_enabled: bool,
    posting_time: str,
    db: Session = Depends(get_db)
):
    settings = db.query(VendorSettings).first()

    if not settings:
        settings = VendorSettings(
            is_enabled=is_enabled,
            posting_time=posting_time
        )
        db.add(settings)
    else:
        settings.is_enabled = is_enabled
        settings.posting_time = posting_time

    db.commit()
    db.refresh(settings)

    return {
        "message": "Vendor settings updated",
        "is_enabled": settings.is_enabled,
        "posting_time": settings.posting_time,
        "active_image_id": settings.active_image_id,
    }


@router.get("/images")
def get_vendor_images(
    db: Session = Depends(get_db)
):
    images = (
        db.query(VendorImage)
        .order_by(VendorImage.created_at.desc())
        .all()
    )

    return [
        {
            "id": image.id,
            "filename": image.filename,
            "file_path": image.file_path,
            "is_active": image.is_active,
            "created_at": image.created_at,
        }
        for image in images
    ]


@router.post("/images/{image_id}/select")
def select_vendor_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(VendorImage)
        .filter(VendorImage.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Vendor image not found"
        )

    db.query(VendorImage).update(
        {"is_active": False}
    )

    image.is_active = True

    settings = db.query(VendorSettings).first()

    if not settings:
        settings = VendorSettings(
            is_enabled=True,
            posting_time="10:00",
            active_image_id=image.id
        )
        db.add(settings)
    else:
        settings.active_image_id = image.id

    db.commit()

    return {
        "message": "Vendor image selected",
        "image_id": image.id
    }

@router.post("/images/upload")
async def upload_vendor_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="Invalid file"
        )

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed"
        )

    extension = Path(file.filename).suffix

    filename = (
        f"vendor_{__import__('uuid').uuid4().hex}"
        f"{extension}"
    )

    file_path = UPLOAD_DIR / filename

    contents = await file.read()

    file_path.write_bytes(contents)

    image = VendorImage(
        filename=file.filename,
        file_path=str(file_path),
        is_active=False
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Vendor image uploaded successfully",
        "id": image.id,
        "filename": image.filename,
        "file_path": image.file_path,
        "is_active": image.is_active
    }

@router.delete("/images/{image_id}")
def delete_vendor_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(VendorImage)
        .filter(VendorImage.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Vendor image not found"
        )

    # Don't allow deleting the currently active image
    if image.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete the active vendor image. Select another image first."
        )

    # Remove database record
    db.delete(image)
    db.commit()

    return {
        "message": "Vendor image deleted successfully"
    }


@router.get("/hashtags")
def get_vendor_hashtags(
    db: Session = Depends(get_db)
):
    hashtags = (
        db.query(VendorHashtag)
        .filter(VendorHashtag.is_active.is_(True))
        .order_by(VendorHashtag.id.asc())
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


@router.post("/hashtags")
def add_vendor_hashtag(
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
        db.query(VendorHashtag)
        .filter(VendorHashtag.hashtag.ilike(hashtag))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Hashtag already exists"
        )

    new_hashtag = VendorHashtag(
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


@router.delete("/hashtags/{hashtag_id}")
def delete_vendor_hashtag(
    hashtag_id: int,
    db: Session = Depends(get_db)
):
    hashtag = (
        db.query(VendorHashtag)
        .filter(VendorHashtag.id == hashtag_id)
        .first()
    )

    if not hashtag:
        raise HTTPException(
            status_code=404,
            detail="Hashtag not found"
        )

    db.delete(hashtag)
    db.commit()

    return {
        "message": "Hashtag deleted successfully"
    }


@router.post("/hashtags/bulk")
def add_vendor_hashtags(
    data: VendorHashtagBulkCreate,
    db: Session = Depends(get_db)
):
    if not data.hashtags:
        raise HTTPException(
            status_code=400,
            detail="No hashtags provided"
        )

    existing_count = (
        db.query(VendorHashtag)
        .filter(VendorHashtag.is_active == True)
        .count()
    )

    if existing_count + len(data.hashtags) > 30:
        raise HTTPException(
            status_code=400,
            detail="Maximum 30 hashtags allowed"
        )

    hashtags = []

    for hashtag in data.hashtags:
        hashtag = hashtag.strip()

        if not hashtag:
            continue

        if not hashtag.startswith("#"):
            hashtag = f"#{hashtag}"

        hashtags.append(
            VendorHashtag(
                hashtag=hashtag,
                is_active=True
            )
        )

    db.add_all(hashtags)
    db.commit()

    return {
        "message": "Hashtags added successfully",
        "count": len(hashtags)
    }

@router.delete("/hashtags/{hashtag_id}")
def delete_vendor_hashtag(
    hashtag_id: int,
    db: Session = Depends(get_db)
):
    hashtag = (
        db.query(VendorHashtag)
        .filter(VendorHashtag.id == hashtag_id)
        .first()
    )

    if not hashtag:
        raise HTTPException(
            status_code=404,
            detail="Hashtag not found"
        )

    db.delete(hashtag)
    db.commit()

    return {
        "message": "Hashtag deleted successfully"
    }