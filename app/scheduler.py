from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app import database, models
from sqlalchemy.orm import Session

def delete_expired_tokens():
    db: Session = next(database.get_db())
    deleted = db.query(models.TokenBlacklist).filter(
        models.TokenBlacklist.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
    print(f"[{datetime.now()}] Deleted {deleted} expired tokens")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_tokens, 'interval', hours=1)
    scheduler.start()
