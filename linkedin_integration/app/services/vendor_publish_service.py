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

    current_time = datetime.now().strftime("%H:%M")

    if current_time != settings.posting_time:
        return

    today = datetime.now().date()

    print(
        f"Vendor posting time matched: "
        f"{settings.posting_time}"
    )

    # ---------------------------------------------------------
    # LOAD ALL VENDOR IMAGES
    # ---------------------------------------------------------

    images = (
        db.query(VendorImage)
        .order_by(VendorImage.id.asc())
        .all()
    )

    if not images:
        print("No vendor images uploaded")
        return

    # ---------------------------------------------------------
    # PREVENT SECOND ROTATION CYCLE ON SAME DAY
    # ---------------------------------------------------------

    if settings.last_rotation_date == today:
        print(
            f"Vendor rotation already processed today "
            f"({today}). Skipping."
        )
        return

    rotation_index = settings.rotation_index % len(images)
    image = images[rotation_index]

    image_path = Path(image.file_path)

    if not image_path.exists():
        print(
            f"Vendor image file not found: "
            f"{image_path}"
        )
        return

    # ---------------------------------------------------------
    # LOAD HASHTAGS
    # ---------------------------------------------------------

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

    hashtag_values = [
        hashtag.hashtag
        for hashtag in hashtags
    ]

    # ---------------------------------------------------------
    # LOAD CONNECTED LINKEDIN ACCOUNTS
    # ---------------------------------------------------------

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

    print("====================================")
    print("VENDOR PUBLISHING")
    print("Date:", today)
    print("Image:", image.filename)
    print("Rotation index:", rotation_index)
    print("Total images:", len(images))
    print("Hashtags:", len(hashtag_values))
    print("Accounts:", len(accounts))
    print("====================================")

    successful_posts = 0
    attempted_accounts = 0

    today_start = datetime.combine(
        today,
        datetime.min.time()
    )

    # ---------------------------------------------------------
    # POST SAME FLYER TO ALL LINKEDIN ACCOUNTS
    # ---------------------------------------------------------

    for account in accounts:

        existing_post = (
            db.query(VendorPostHistory)
            .filter(
                VendorPostHistory.linkedin_account_id == account.id,
                VendorPostHistory.posted_at >= today_start,
            )
            .first()
        )

        if existing_post:
            print(
                f"Already attempted vendor post today "
                f"from {account.email} "
                f"({existing_post.post_status}). Skipping."
            )
            continue

        attempted_accounts += 1

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

            successful_posts += 1

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

            db.rollback()

            history = VendorPostHistory(
                linkedin_account_id=account.id,
                post_status="FAILED",
                error_message=str(e),
                posted_at=datetime.now(),
            )

            db.add(history)
            db.commit()

    # ---------------------------------------------------------
    # ADVANCE ROTATION ONLY AFTER SUCCESS
    # ---------------------------------------------------------

    if successful_posts > 0:

        settings.rotation_index = (
            rotation_index + 1
        ) % len(images)

        settings.last_rotation_date = today

        db.commit()

        print(
            "===================================="
        )
        print(
            "Vendor image rotation advanced:"
        )
        print(
            f"{rotation_index} -> "
            f"{settings.rotation_index}"
        )
        print(
            f"Last rotation date: "
            f"{settings.last_rotation_date}"
        )
        print(
            "Next flyer: "
            f"{images[settings.rotation_index].filename}"
        )
        print(
            "===================================="
        )

    elif attempted_accounts > 0:

        print(
            "No vendor posts succeeded. "
            "Keeping the same rotation index "
            "for retry."
        )

    else:

        print(
            "No accounts needed posting today."
        )
