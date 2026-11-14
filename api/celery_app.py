from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "fetch_cds_data",
    broker="redis://redis_queue:6379/0",
    backend="db+postgresql://postgres:postgres_password@postgres:5432/postgres_db",
    include=["tasks"],
)

celery_app.conf.timezone = "America/Bogota"
celery_app.conf.enable_utc = True

celery_app.conf.beat_schedule = {
    "my-daily-task-3pm": {
        "task": "task_service.fetch_data_process_and_save",
        "schedule": crontab(hour=15, minute=0),
    },
}