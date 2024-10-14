from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # BASE
    NAME: str = "event-driven-microservice"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # KAFKA
    KAFKA_SERVER: str
    KAFKA_GROUP_ID: str
    KAFKA_TOPICS: str
    KAFKA_AUTO_OFFSET_RESET: str = "latest"

    # CELERY
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # MINIO
    MINIO_HOST: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    MINIO_SECURE: str
