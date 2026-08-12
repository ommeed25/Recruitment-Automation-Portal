from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.db.models import (
    VendorSettings,
    VendorImage,
    VendorHashtag,
    VendorPostHistory,
    LinkedInAccount,
)

from app.services.linkedin_service import (
    upload_image_to_linkedin,
    publish_vendor_post,
)


def scheduled_vendor_post():
    db = SessionLocal()

    try:
        publish_vendor_posts(db)
    except Exception:
        print("========== VENDOR SCHEDULER ERROR ==========")
        import traceback

        traceback.print_exc()
        print("=============================================")
    finally:
        db.close()


def publish_vendor_posts(db: Session):

    settings = db.query(VendorSettings).first()

    if not settings:
        print("No vendor settings found")
        return

    if not settings.is_enabled:
        print("Vendor posting is disabled")
        return

    if not settings.active_image_id:
        print("No active vendor image selected")
        return

    image = (
        db.query(VendorImage)
        .filter(
            VendorImage.id == settings.active_image_id
        )
        .first()
    )

    if not image:
        print("Active vendor image not found")
        return

    hashtags = (
        db.query(VendorHashtag)
        .filter(
            VendorHashtag.is_active.is_(True)
        )
        .order_by(VendorHashtag.id.asc())
        .all()
    )

    if not hashtags:
        print("No active hashtags found")
        return

    if len(hashtags) > 30:
        print("More than 30 hashtags found")
        return

    accounts = (
        db.query(LinkedInAccount)
        .filter(
            LinkedInAccount.access_token.isnot(None)
        )
        .all()
    )

    if not accounts:
        print("No connected LinkedIn accounts")
        return

    image_path = Path(image.file_path)

    if not image_path.exists():
        print(f"Vendor image file not found: {image_path}")
        return

    hashtag_values = [
        hashtag.hashtag
        for hashtag in hashtags
    ]

    print("====================================")
    print("VENDOR PUBLISHING")
    print("Image:", image.filename)
    print("Hashtags:", len(hashtag_values))
    print("Accounts:", len(accounts))
    print("====================================")

    for account in accounts:
        today = datetime.now().date()

        existing_post = (
            db.query(VendorPostHistory)
            .filter(
                VendorPostHistory.linkedin_account_id == account.id,
                VendorPostHistory.post_status == "SUCCESS",
                VendorPostHistory.posted_at >= datetime.combine(
                    today,
                    datetime.min.time()
                ),
            )
            .first()
        )

        if existing_post:
            print(
                f"Already posted today from {account.email}. "
                "Skipping."
            )
            continue
        print(
            f"Publishing vendor post from "
            f"{account.email}"
        )

        try:
            person_urn = (
                f"urn:li:person:{account.linkedin_sub}"
            )

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

            linkedin_post_id = response.headers.get(
                "x-restli-id"
            )

            history = VendorPostHistory(
                linkedin_account_id=account.id,
                linkedin_post_id=linkedin_post_id,
                post_status="SUCCESS",
                posted_at=datetime.now(),
            )

            db.add(history)
            db.commit()

            print(
                f"Vendor post successful: "
                f"{account.email}"
            )

        except Exception as e:

            print(
                f"Vendor post failed: "
                f"{account.email}"
            )

            print(str(e))

            history = VendorPostHistory(
                linkedin_account_id=account.id,
                post_status="FAILED",
                error_message=str(e),
                posted_at=datetime.now(),
            )

            db.add(history)
            db.commit()