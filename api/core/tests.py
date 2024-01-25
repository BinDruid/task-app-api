from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from .tasks import send_single_email

User = get_user_model()

CELERY_TASK_URL = reverse("core:core-tasks")


class TestCeleryTasks(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_send_single_email(self):
        result = send_single_email.delay()
        result.get()
        self.assertTrue(result.successful())

    @patch('api.core.tasks.send_single_email.delay')
    def test_send_single_email_endpoint(self, mock_send_single_email):
        payload = {}
        response = self.client.post(CELERY_TASK_URL, data=payload, format="json")
        send_single_email.delay.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
