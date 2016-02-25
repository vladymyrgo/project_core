from celery import task

from core.utils.utils import send_mail_alternatives


@task
def task_send_mail(*args, **kwargs):
    send_mail_alternatives(*args, **kwargs)
