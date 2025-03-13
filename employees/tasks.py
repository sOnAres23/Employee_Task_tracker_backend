from celery import shared_task

from employees.models import Task
from employees.services import send_message


@shared_task
def send_message_for_employer():
    """Задача для напоминания о задаче пользователю в телеграм"""
    # Получаем все задачи со статусом, которые выполняются
    tasks = Task.objects.filter(status="Выполняется")
    for task in tasks:
        send_message(task)
