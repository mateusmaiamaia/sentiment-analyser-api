import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

@celery.task
def example_task(x, y):
    return x + y