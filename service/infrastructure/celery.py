from celery import Celery

from ..settings import Settings

# Load settings
settings = Settings()

# Validate that the required settings are set
assert settings.CELERY_BROKER_URL, "Environment variable CELERY_BROKER_URL is required"
assert settings.CELERY_RESULT_BACKEND, "Environment variable CELERY_RESULT_BACKEND is required"

# Create a Celery instance
celery = Celery(
    settings.NAME,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
)

# Configure Celery
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_annotations={"*": {"rate_limit": "10/s"}},
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=5,
)

# Autodiscover tasks
celery.autodiscover_tasks(["application.tasks"])
