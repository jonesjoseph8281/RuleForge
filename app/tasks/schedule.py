from celery.schedules import crontab
from app.tasks.celery_app import celery_app
from app.tasks.batch import enforce_batch_window, recover_stuck_items
import os

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Nightly batch schedule
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        schedule_nightly_batch.s(),
    )
    
    # Maintenance
    sender.add_periodic_task(
        crontab(minute="*/15"),
        enforce_batch_window.s(),
    )
    sender.add_periodic_task(
        crontab(minute="*/30"),
        recover_stuck_items.s(),
    )

@celery_app.task
def schedule_nightly_batch():
    pass
