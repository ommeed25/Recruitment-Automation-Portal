from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import Job

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/")
def get_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
  offset = (page - 1) * page_size

  total = db.query(Job).count()

  jobs = (
        db.query(Job)
        .offset(offset)
        .limit(page_size)
        .all()
    )

  total_pages = (total + page_size - 1) // page_size

  return {
        "items": jobs,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }

@router.get("/analytics")
def get_job_analytics(
    db: Session = Depends(get_db),
):
  total_jobs = db.query(Job).count()

  published_jobs = (
    db.query(Job)
    .filter(Job.linkedin_posted == True)
    .count()
)
  pending_jobs = (
    db.query(Job)
    .filter(Job.linkedin_posted == False)
    .count()
)
  
  return {
    "total_jobs": total_jobs,
    "published_jobs": published_jobs,
    "pending_jobs": pending_jobs
}
   