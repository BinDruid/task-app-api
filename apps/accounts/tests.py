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

    def create_test_user(self):
        return self.client.post(USER_CREATE_URL, data=PAYLOAD)

    def test_new_user_registration(self):
        response = self.create_test_user()
        user = User.objects.get(username=PAYLOAD["username"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(PAYLOAD["password"]))
        self.assertNotIn("password", response.data)

    def test_user_can_get_token(self):
        self.create_test_user()
        response = self.client.post(TOKEN_URL, data=PAYLOAD)
        token = Token.objects.get(user__username=PAYLOAD["username"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], token.key)
