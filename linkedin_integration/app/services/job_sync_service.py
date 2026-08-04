from app.db.models import Job
from app.services.oracle_sync_service import fetch_jobs


def sync_jobs(db):
    jobs = fetch_jobs()

    inserted = 0
    updated = 0

    for job in jobs:

        existing_job = db.query(Job).filter(
            Job.job_id == job["job_id"]
        ).first()

        if existing_job:
            existing_job.job_posting_title = job["job_posting_title"]
            existing_job.job_posting_skills = job["job_posting_skills"]
            existing_job.job_type = job["job_type"]
            existing_job.experience_slab = job["experience_slab"]
            existing_job.job_work_location = job["job_work_location"]
            existing_job.job_mode = job["job_mode"]
            existing_job.notice_period = job["notice_period"]
            existing_job.priority = job["priority"]
            existing_job.no_of_position = job["no_of_position"]
            existing_job.created_by = job["created_by"]

            updated += 1

        else:
            new_job = Job(
                job_id=job["job_id"],
                job_posting_title=job["job_posting_title"],
                job_posting_skills=job["job_posting_skills"],
                job_type=job["job_type"],
                experience_slab=job["experience_slab"],
                job_work_location=job["job_work_location"],
                job_mode=job["job_mode"],
                notice_period=job["notice_period"],
                priority=job["priority"],
                no_of_position=job["no_of_position"],
                created_by=job["created_by"]
            )

            db.add(new_job)
            inserted += 1

    db.commit()

    return {
        "inserted": inserted,
        "updated": updated,
        "total": len(jobs)
    }

def get_unposted_jobs(db):
    jobs = (
        db.query(Job)
        .filter(Job.linkedin_posted == False)
        .all()
    )

    return jobs


def mark_job_as_posted(job_id, db):
    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not job:
        return {"message": "Job not found"}

    job.linkedin_posted = True

    db.commit()

    return {
        "message": "Job marked as posted",
        "job_id": job_id
    }

