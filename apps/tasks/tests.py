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
        self.yesterday_count = 20
        today = timezone.now()
        yesterday = today + timedelta(days=1)
        baker.make(Task, owner=self.user, created_at=today, _quantity=self.today_tasks_count)
        baker.make(Task, owner=self.user, created_at=yesterday, _quantity=self.yesterday_count)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_single_task_details(self):
        task = baker.make(Task, owner=self.user)
        url = reverse("tasks:detail", kwargs={"pk": task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(task.id))

    def test_create_single_task(self):
        payload = {"title": "new_test_task", "description": "test task to create"}
        response = self.client.post(TASKS_CREATE_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_update_single_task(self):
        task = baker.make(Task, owner=self.user)
        url = reverse("tasks:detail", kwargs={"pk": task.pk})
        payload = {"title": "test_update"}
        response = self.client.patch(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_delete_single_task(self):
        task = baker.make(Task, owner=self.user)
        url = reverse("tasks:detail", kwargs={"pk": task.pk})
        response = self.client.delete(url)
        task_exists = Task.objects.filter(pk=task.pk).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(task_exists)

    def test_recent_tasks_aggregation(self):
        response = self.client.get(RECENT_TASKS_URL)
        today = date.today().strftime("%d %b, %Y")
        yesterday = (date.today() + timedelta(days=1)).strftime("%d %b, %Y")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[today]), self.today_tasks_count)
        self.assertEqual(len(response.data[yesterday]), self.yesterday_count)
