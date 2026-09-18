from pathlib import Path, PureWindowsPath
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import SalesImage


router = APIRouter(
    prefix="/sales/images",
    tags=["Sales Images"]
)


UPLOAD_DIR = Path("uploads/sales")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _image_url(file_path: str) -> str:
    path = (
        PureWindowsPath(file_path)
        if "\\" in file_path
        else Path(file_path)
    )

    return f"/{path.as_posix().lstrip('/')}"


@router.get("/")
def get_sales_images(
    db: Session = Depends(get_db)
):
    images = (
        db.query(SalesImage)
        .order_by(SalesImage.created_at.desc())
        .all()
    )

    return [
        {
            "id": image.id,
            "filename": image.filename,
            "file_path": _image_url(image.file_path),
            "is_active": image.is_active,
            "created_at": image.created_at,
        }
        for image in images
    ]


@router.post("/{image_id}/select")
def select_sales_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(SalesImage)
        .filter(SalesImage.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Sales image not found"
        )

    db.query(SalesImage).update(
        {"is_active": False}
    )

    image.is_active = True

    db.commit()

    return {
        "message": "Sales image selected",
        "image_id": image.id
    }


@router.post("/upload")
async def upload_sales_image(
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
        f"sales_{uuid.uuid4().hex}"
        f"{extension}"
    )

    file_path = UPLOAD_DIR / filename

    contents = await file.read()

    file_path.write_bytes(contents)

    image = SalesImage(
        filename=file.filename,
        file_path=str(file_path),
        is_active=False
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Sales image uploaded successfully",
        "id": image.id,
        "filename": image.filename,
        "file_path": _image_url(image.file_path),
        "is_active": image.is_active
    }


@router.delete("/{image_id}")
def delete_sales_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image = (
        db.query(SalesImage)
        .filter(SalesImage.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Sales image not found"
        )

    if image.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete the active sales image. Select another image first."
        )

    db.delete(image)
    db.commit()

    return {
        "message": "Sales image deleted successfully"
    }