from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from apps.tasks.models import Task

User = get_user_model()


class TestTaskCreation(TestCase):
    def setUp(self):
        self.base_api_url = "http://localhost:9000/v1"
        self.user = baker.make(User)
        self.tasks = baker.make(Task, owner=self.user, _quantity=10)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_task_count(self):
        url = self.base_api_url + "/tasks/recent/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_task(self):
        url = self.base_api_url + "/tasks/"
        response = self.client.post(url, data={"title": "new_task", "description": "test task has been created"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "new_task")
