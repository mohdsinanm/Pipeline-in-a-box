from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://valkey:6379/0",
    backend="redis://valkey:6379/1"
)

celery.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=300,
    task_soft_time_limit=240,
)

celery.autodiscover_tasks(["src"], related_name="task")