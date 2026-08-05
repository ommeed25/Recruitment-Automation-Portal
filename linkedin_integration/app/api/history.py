from fastapi import APIRouter, Depends ,Query
from sqlalchemy.orm import Session
import math


from app.db.dependencies import get_db
from app.db.models import LinkedInPost, Job, LinkedInAccount

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def get_history(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    query = (
        db.query(
            LinkedInPost,
            Job,
            LinkedInAccount
        )
        .join(Job, Job.job_id == LinkedInPost.job_id)
        .join(
            LinkedInAccount,
            LinkedInAccount.id == LinkedInPost.linkedin_account_id
        )
    )

    if search:
        query = query.filter(
            Job.job_posting_title.ilike(f"%{search}%")
        )

    total = query.count()
    total_pages = math.ceil(total / size)

    posts = (
    query
    .order_by(LinkedInPost.posted_at.desc())
    .offset(offset)
    .limit(size)
    .all()
    )
    
    return {
         "page": page,
        "size": size,
        "total_pages": total_pages,
        "items": [
        {
            "job_id": job.job_id,
            "title": job.job_posting_title,
            "recruiter": account.full_name,
            "email": account.email,
            "status": post.post_status,
            "linkedin_post_id": post.linkedin_post_id,
            "posted_at": post.posted_at,
        }
        for post, job, account in posts
        ]
    }