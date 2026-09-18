from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from app.services.vendor_publish_service import scheduled_vendor_post
from app.scheduler.jobs import scheduled_sync
from app.services.sales_publish_service import publish_sales_post

scheduler = BackgroundScheduler()
_scheduler_started = False


def start_scheduler():
    global _scheduler_started

    if _scheduler_started:
        return

    scheduler.add_job(
        scheduled_sync,
        trigger="interval",
        minutes=5,
        id="oracle_sync",
        replace_existing=True,
        next_run_time=datetime.utcnow(),
       
    )

    scheduler.add_job(
        scheduled_vendor_post,
        trigger="interval",
        minutes=1,
        id="vendor_test",
        replace_existing=True,
    )

    scheduler.add_job(
        scheduled_sales_post,
        trigger="interval",
        minutes=1,
        id="sales_test",
        replace_existing=True,
    )

    scheduler.start()
    _scheduler_started = True

    print("Scheduler Started")


def scheduled_sales_post():
    from app.db.database import SessionLocal

    db = SessionLocal()

    try:
        publish_sales_post(db)
    finally:
        db.close()