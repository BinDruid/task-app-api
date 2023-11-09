from time import sleep
from celery import shared_task


@shared_task()
def email_task():
    print(f"sending a temp email")
    sleep(5)
    print(f"email sent")
    return "done"
