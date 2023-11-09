from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from .tasks import email_task

User = get_user_model()

CELERY_TASK_URL = reverse("core:core-tasks")


class TestCeleryTasks(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_email_task(self):
        result = email_task.delay()
        result.get()
        self.assertTrue(result.successful())

    @patch('api.core.tasks.email_task')
    def test_email_task_endpoint(self, email_task):
        payload = {}
        response = self.client.post(CELERY_TASK_URL, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
