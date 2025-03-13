from django.contrib import admin

from employees.models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "post", "tg_chat_id",)
    list_filter = ("full_name",)
    search_fields = ("full_name", "post",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent_task", "employee", "deadline", "status")
    list_filter = ("title",)
    search_fields = ("title", "status",)
