import os

from apscheduler.schedulers.blocking import BlockingScheduler

from models import SessionLocal, init_db
from services.ctk_ingest import ingest

scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", hours=1)
def scheduled_ingest() -> None:
    db = SessionLocal()
    try:
        ingest(
            db_session=db,
            api_key=os.getenv("API_KEY"),
            api_url=os.getenv("API_URL"),
            rss_url=os.getenv("RSS_URL"),
        )
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    scheduler.start()
