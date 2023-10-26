from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from apps.tasks.models import Task

User = get_user_model()

RECENT_TASKS_URL = reverse("tasks:recent")
TASKS_CREATE_URL = reverse("tasks:create")


class TestTaskCreation(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.today_tasks_count = 10
        today = timezone.now()
        yesterday = today + timedelta(days=1)
        baker.make(Task, owner=self.user, created_at=today, _quantity=self.today_tasks_count)
        baker.make(Task, owner=self.user, created_at=yesterday, _quantity=20)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_recent_tasks_aggregation(self):
        response = self.client.get(RECENT_TASKS_URL)
        today = date.today().strftime("%d %b, %Y")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[today]), self.today_tasks_count)

    def test_user_can_create_task(self):
        payload = {"title": "new_test_task", "description": "test task to create"}
        response = self.client.post(TASKS_CREATE_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
