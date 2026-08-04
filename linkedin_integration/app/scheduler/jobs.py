from app.db.database import SessionLocal
import traceback
from app.services.job_sync_service import (
    sync_jobs,
    get_unposted_jobs,
)

from app.services.linkedin_publish_service import publish_job_service


def scheduled_sync():
    db = SessionLocal()

    try:
        print("Running scheduled job sync...")

        result = sync_jobs(db)
        print(result)

        jobs = get_unposted_jobs(db)

        print(f"Found {len(jobs)} unposted jobs")

        for job in jobs:
            print(f"Publishing Job {job.job_id}")
            print(">>> Calling publish_job_service")
            result = publish_job_service(job.job_id, db)
            print(">>> Result:", result)

    except Exception as e:
        print("========== SCHEDULER ERROR ==========")
        traceback.print_exc()
        print("=====================================")

    finally:
        db.close()