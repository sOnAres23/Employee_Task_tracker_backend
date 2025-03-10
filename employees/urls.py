from django.urls import path
from rest_framework.routers import DefaultRouter

from employees import views

app_name = 'employees'

router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="tasks")
router.register(r"employees", views.EmployeeViewSet, basename="employees")

urlpatterns = [
    path("important_tasks/", views.ImportantTasksAPIView.as_view(), name='important_tasks'),
    path("busy_employees/", views.BusyEmployeesAPIView.as_view(), name="busy_employees"),

] + router.urls
