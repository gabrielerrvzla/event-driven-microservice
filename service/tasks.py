from celery import shared_task


@shared_task(name="add")
def add(x: int, y: int) -> int:
    return x + y
