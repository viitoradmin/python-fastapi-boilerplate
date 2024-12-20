"""
Module to initialize the celery app and redis backend along with broker.
"""

from celery import Celery
from config import redis_config

# Initialize Celery app with Redis broker and backend
celery_app = Celery(
    __name__,
    broker=f"{redis_config.REDIS_BROKER_URL}/0",
    backend=f"{redis_config.REDIS_BROKER_URL}/0",
    include=["celery_task.tasks"],
)

celery_app.conf.task_queues = {
    'sequential_queue': {
        'exchange': 'sequential',
        'exchange_type': 'direct',
        'binding_key': 'sequential_queue',
    }
}

celery_app.conf.task_routes = {
    'celery_task.tasks.fetch_and_prepare_records_data': {"queue": "sequential_queue"},
}
 
