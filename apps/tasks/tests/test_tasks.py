from datetime import datetime, date, timedelta
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
        self.today_tasks_count = 10
        today = datetime.now()
        yesterday = today + timedelta(days=2)
        baker.make(Task, owner=self.user, created_at=today, _quantity=self.today_tasks_count)
        baker.make(Task, owner=self.user, created_at=yesterday, _quantity=20)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_recent_tasks_aggregation(self):
        url = self.base_api_url + "/tasks/recent/"
        response = self.client.get(url)
        today = date.today().strftime("%d %b, %Y")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[today]), self.today_tasks_count)

    def test_user_can_create_task(self):
        url = self.base_api_url + "/tasks/"
        response = self.client.post(url, data={"title": "new_task", "description": "test task has been created"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "new_task")
