from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from employees.models import Employee, Task
from employees.paginators import MyCustomPagination
from employees.serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(ModelViewSet):
    """Эндпоинт для вывода всех сотрудников"""
    queryset = Employee.objects.all().annotate(task_count=Count('employee_task'))
    serializer_class = EmployeeSerializer
    pagination_class = MyCustomPagination


class TaskViewSet(ModelViewSet):
    """Эндпоинт для вывода всех задач"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = MyCustomPagination


class BusyEmployeesAPIView(APIView):
    """Эндпоинт для сотрудников, отсортированных по количеству активных в работе задач"""
    def get(self, request):
        busy_employees = Employee.objects.annotate(
            active_task_count=Count('employee_task')).filter(active_task_count__gt=0).order_by('-active_task_count')

        response_data = [
            {
                'ФИО сотрудника': employee.full_name,
                'Должность': employee.post,
                'Количество задач': employee.active_task_count
            }
            for employee in busy_employees]

        return Response(response_data)


class ImportantTasksAPIView(APIView):
    """Эндпоинт для важных задач, которые не взяты в работу, и списка сотрудников, которые могут её взять"""
    def get(self, request):
        # Запрашиваем задачи, которые не взяты в работу, но от которых зависят другие задачи
        important_tasks = Task.objects.filter(status=Task.TaskStatus.CREATED, parent_task__isnull=False)

        response_data = []
        candidates = []

        # Получаем всех сотрудников, которые могут взять эту задачу
        for task in important_tasks:
            potential_employees = Employee.objects.annotate(
                active_task_count=Count('employee_task')).order_by('active_task_count')

        # Смотрим первого (наименее загруженного) сотрудника или сотрудника, выполняющий родительскую задачу,
        # если ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника
        least_loaded_employee = potential_employees.first()
        for employee in potential_employees:
            if employee.active_task_count <= least_loaded_employee.active_task_count + 2:
                candidates.append(employee.full_name)

        # Возвращаем список объектов в нужном формате
        response_data.append({
            "Важная задача": task.title,
            "Срок": task.deadline,
            "ФИО сотрудников": candidates
        })

        return Response(response_data)
