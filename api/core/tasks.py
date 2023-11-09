from time import sleep
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task()
def email_task():
    logger.info("task called")
    sleep(5)
    return "done"
