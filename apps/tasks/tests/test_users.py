from urllib import response

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class TestUserAuthentication(TestCase):
    def setUp(self):
        self.base_api_url = "http://localhost:9000/v1"
        self.client = APIClient()
        self.payload = {"username": "druid", "password": "test_10001"}

    def create_test_user(self):
        url = self.base_api_url + "/auth/users/"
        return self.client.post(url, data=self.payload)

    def test_new_user_registration(self):
        response = self.create_test_user()
        user = User.objects.get(username=self.payload["username"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_can_get_token(self):
        self.create_test_user()
        url = self.base_api_url + "/auth/token/login/"
        response = self.client.post(url, data=self.payload)
        token = Token.objects.get(user__username=self.payload["username"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["auth_token"], token.key)
