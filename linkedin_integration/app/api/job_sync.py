from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.job_sync_service import (
    sync_jobs,
    get_unposted_jobs,
    mark_job_as_posted,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/sync")
def sync_jobs_api(db: Session = Depends(get_db)):
    return sync_jobs(db)



@router.get("/unposted")
def get_unposted_jobs_api(db: Session = Depends(get_db)):
    return get_unposted_jobs(db)


@router.put("/{job_id}/mark-posted")
def mark_job_posted_api(job_id: int, db: Session = Depends(get_db)):
    return mark_job_as_posted(job_id, db)