import time

from app.scheduler.scheduler import start_scheduler


if __name__ == "__main__":
    start_scheduler()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Scheduler stopped")
