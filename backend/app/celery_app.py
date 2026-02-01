import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery = Celery(
    "smart_image_api",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Time
    timezone="UTC",
    enable_utc=True,

    # Reliability
    broker_connection_retry_on_startup=True,
    task_track_started=True,

    # Safety limits (prevents runaway tasks)
    task_time_limit=300,        # Hard kill after 5 minutes
    task_soft_time_limit=270,   # Graceful warning at 4.5 minutes
)

# Only scan the tasks module, not the whole app
celery.autodiscover_tasks(["backend.app.tasks"])
