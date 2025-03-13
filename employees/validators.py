from django.utils import timezone
from rest_framework import serializers

from employees.models import Task


def validate_deadline(task):
    """Валидатор для проверки срока, проверяет, что срок выполнения не может быть раньше текущей даты"""
    if task.get("deadline") and task.get("deadline") < timezone.now().date():
        raise serializers.ValidationError("Срок выполнения не может быть раньше текущей даты!")


def validate_status(task):
    """Валидатор для проверки присваивания статуса задачи при её создании"""
    if task.get("employee"):
        if task.get("status") == Task.TaskStatus.CREATED:
            raise serializers.ValidationError("Если сотрудник указан, то задача должна выполняться.")
    else:
        if task.get("status") in (Task.TaskStatus.PROCESSING, Task.TaskStatus.COMPLETED):
            raise serializers.ValidationError("Задача не может выполняться или быть выполненой, без сотрудника.")
