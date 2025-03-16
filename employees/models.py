from django.db import models


class Employee(models.Model):
    """Модель создания сотрудника"""
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    post = models.CharField(max_length=150, verbose_name="Должность сотрудника")
    tg_chat_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Телеграм чат-id")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.full_name


class Task(models.Model):
    """Модель создания задачи"""
    class TaskStatus(models.TextChoices):
        CREATED = "Создана"
        PROCESSING = "Выполняется"
        COMPLETED = "Завершена"

    title = models.CharField(max_length=150, verbose_name="Название задачи")
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Связаная задача",
                                    blank=True, null=True, help_text="Укажите родительскую задачу")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Исполнитель задачи",
                                 related_name="employee_task", blank=True, null=True)
    deadline = models.DateField(verbose_name="День до выполнения задачи", help_text="Укажите дату дэдлайна")
    status = models.CharField(max_length=20, choices=TaskStatus, default=TaskStatus.CREATED,
                              verbose_name="Статус задачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания задачи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
