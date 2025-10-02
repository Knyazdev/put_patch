from celery import Celery
from src.config import settings
from datetime import timedelta


celery_instance = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)

celery_instance.conf.beat_schedule = {
    'any-name': {
        'task': 'booking_today_checkin',
        'schedule': timedelta(seconds=5),
    }
}

celery_instance.conf.timezone = "UTC"
celery_instance.conf.enable_utc = True
