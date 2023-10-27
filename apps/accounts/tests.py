from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

TOKEN_URL = reverse("accounts:token")
USER_CREATE_URL = reverse("accounts:create")
PAYLOAD = {"username": "ali", "email": "ali@example.com", "password": "test_10001"}


class TestUserAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_sample_user(self):
        user = User.objects.create_user(**PAYLOAD)
        return user

    def test_new_user_registration(self):
        response = self.client.post(USER_CREATE_URL, data=PAYLOAD)
        user = User.objects.get(username=PAYLOAD["username"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(PAYLOAD["password"]))
        self.assertNotIn("password", response.data)

    def test_user_can_get_token(self):
        user = self.create_sample_user()
        token = Token.objects.get(user=user)
        response = self.client.post(TOKEN_URL, data=PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], token.key)
