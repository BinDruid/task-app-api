import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.tasks.models import Task
from model_bakery import baker
User = get_user_model()


@pytest.mark.django_db
class TestTaskEndPoint:
    def test_unauthorized_access(self, api):
        response = api.get("/v1/tasks/recent/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    
    def test_user_can_list_his_tasks(self, api):
        user = baker.make(User)
        tasks = baker.make(Task, owner=user, _quantity=10)
        api.force_authenticate(user=user)
        response = api.get("/v1/tasks/recent/")
        assert response.status_code == status.HTTP_200_OK

    # def test_user_has_access(self, api):
    #     user = User.objects.get(username='druid')
    #     api.force_authenticate(user=user)
    #     response = api.get("/v1/tasks/recent/")
    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED
