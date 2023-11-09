from time import sleep
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task()
def send_single_email():
    logger.info("sending single email")
    sleep(5)
    return "done"

@shared_task()
def send_group_email():
    logger.info("sending group email")
    sleep(5)
    return "done"
