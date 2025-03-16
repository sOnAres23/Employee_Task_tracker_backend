from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from employees.models import Task
from users.models import User


class TrackerTest(APITestCase):
    def setUp(self):
        """Прописывем исходные данные и необходимые параметры"""

        # Создаем необходимы модели
        self.user = User.objects.create(email="test@example.com", password="password123")
        # self.employee = Employee.objects.create(full_name="Тони Старк", post="Кодер", tg_chat_id="12345")
        # self.task = Task.objects.create(title="Test", employee=self.employee, deadline="2025-12-31",
        #                                 status=Task.TaskStatus.CREATED)

        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        """Тестирование создания задачи"""
        url = reverse("employees:tasks-list")
        data = {
            "title": "Test",
            "deadline": "2025-12-31",
            "status": Task.TaskStatus.CREATED
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["deadline"], data["deadline"])
        self.assertEqual(response.json()["status"], data["status"])

    def test_retrieve_all_tasks(self):
        """Тестирование на вывод списка всех задач"""
        url = reverse("employees:tasks-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_employees(self):
        """Тестирование на вывод списка всех сотрудников"""
        url = reverse("employees:employees-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_status(self):
        """Тест по валидации статуса задачи"""
        url = reverse("employees:tasks-list")
        data = {
            "title": "Test",
            "deadline": "2025-12-31",
            "status": Task.TaskStatus.PROCESSING
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Задача не может выполняться или быть выполненой, без сотрудника.", str(response.data),)
