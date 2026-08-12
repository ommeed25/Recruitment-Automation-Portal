from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Job, LinkedInAccount, LinkedInPost
from app.services.linkedin_service import build_linkedin_payload, publish_post


def publish_job_service(job_id: int, db: Session):
    print(">>> INSIDE publish_job_service")

    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        return {"message": "Job not found"}

    linkedin_accounts = (
        db.query(LinkedInAccount)
        .filter(LinkedInAccount.access_token.isnot(None))
        .all()
    )

    if not linkedin_accounts:
        return {
            "message": "No LinkedIn accounts connected"
        }
    
    success = False
    results = []

    for linkedin_account in linkedin_accounts:

        existing_post = (
            db.query(LinkedInPost)
            .filter(
                LinkedInPost.job_id == job.job_id,
                LinkedInPost.linkedin_account_id == linkedin_account.id,
                LinkedInPost.post_status == "SUCCESS",
            )
            .first()
        )

        if existing_post:
            results.append({
                "account": linkedin_account.email,
                "status": "Already Published"
            })
            continue

        payload = build_linkedin_payload(
            job,
            linkedin_account
        )

        print(f"Publishing from {linkedin_account.email}")

        try:
            response = publish_post(
                linkedin_account.access_token,
                payload
            )
        except Exception as e:
            results.append({
                "account": linkedin_account.email,
                "status": "Failed",
                "response": str(e)
            })
            continue


        if response.status_code == 201:

            success = True

            response_data = response.json()

            linkedin_post = LinkedInPost(
                job_id=job.job_id,
                linkedin_account_id=linkedin_account.id,
                linkedin_post_id=response_data["id"],
                post_status="SUCCESS",
                posted_at=datetime.now(),
            )

            db.add(linkedin_post)
           

            results.append({
                "account": linkedin_account.email,
                "status": "Published"
            })

        else:

            results.append({
                "account": linkedin_account.email,
                "status": "Failed",
                "response": response.text
            })

    if success:
        job.linkedin_posted = True

    db.commit()

    db.refresh(job)

    return {
        "job_id": job.job_id,
        "results": results
    }
