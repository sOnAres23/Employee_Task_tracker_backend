from rest_framework import serializers

from employees.models import Employee, Task
from employees.validators import validate_deadline, validate_status


class EmployeeSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    def get_task_count(self, obj):
        return obj.employee_task.count()

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'post', 'task_count', 'tg_chat_id']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        validators = [validate_deadline, validate_status]
