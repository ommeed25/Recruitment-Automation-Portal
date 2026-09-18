from pathlib import Path

from sqlalchemy.orm import Session
from datetime import datetime, date

from app.db.models import (
    SalesLinkedInAccount,
    SalesImage,
    SalesHashtag,
    SalesSettings,
    SalesPostHistory,
)
from app.services.linkedin_service import (
    upload_image_to_linkedin,
    publish_vendor_post,
)


def publish_sales_post(db: Session):
    settings = db.query(SalesSettings).first()

    if not settings or not settings.is_enabled:
        return {
            "status": "skipped",
            "message": "Sales posting is disabled"
        }

    image = None

    if settings.active_image_id:
        image = (
            db.query(SalesImage)
            .filter(SalesImage.id == settings.active_image_id)
            .first()
        )

    if not image:
        image = (
            db.query(SalesImage)
            .filter(SalesImage.is_active.is_(True))
            .first()
        )

    if not image:
        return {
            "status": "skipped",
            "message": "No active Sales image configured"
        }

    hashtags = (
        db.query(SalesHashtag)
        .filter(SalesHashtag.is_active.is_(True))
        .order_by(SalesHashtag.id.asc())
        .limit(30)
        .all()
    )

    hashtag_values = [hashtag.hashtag for hashtag in hashtags]

    accounts = (
        db.query(SalesLinkedInAccount)
        .filter(SalesLinkedInAccount.access_token.isnot(None))
        .all()
    )

    if not accounts:
        return {
            "status": "skipped",
            "message": "No connected Sales LinkedIn accounts"
        }

    image_path = Path(image.file_path)

    if not image_path.exists():
        return {
            "status": "failed",
            "message": f"Sales image file not found: {image.file_path}"
        }

    results = []

    for account in accounts:
        today = date.today()

        already_attempted = (
            db.query(SalesPostHistory)
            .filter(
                SalesPostHistory.sales_linkedin_account_id == account.id,
                SalesPostHistory.created_at >= today,
            )
            .first()
        )

        if already_attempted:
            continue
        history = SalesPostHistory(
            sales_linkedin_account_id=account.id,
            post_status="FAILED",
        )

        try:
            person_urn = f"urn:li:person:{account.linkedin_sub}"

            image_urn = upload_image_to_linkedin(
                access_token=account.access_token,
                image_path=str(image_path),
                person_urn=person_urn,
            )

            response = publish_vendor_post(
                access_token=account.access_token,
                person_urn=person_urn,
                image_urn=image_urn,
                hashtags=hashtag_values,
            )

            history.linkedin_post_id = response.headers.get("x-restli-id")
            history.post_status = "SUCCESS"
            history.posted_at = datetime.utcnow()

            results.append({
                "account_id": account.id,
                "status": "SUCCESS",
            })

        except Exception as exc:
            history.error_message = str(exc)

            results.append({
                "account_id": account.id,
                "status": "FAILED",
                "error": str(exc),
            })

        db.add(history)
        db.commit()

    return {
        "status": "completed",
        "image_id": image.id,
        "accounts": results,
    }