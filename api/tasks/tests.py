from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tag, Task

User = get_user_model()

TASKS_URL = reverse("tasks:tasks-collection")
TAGS_URL = reverse("tasks:tags-collection")
RECENT_TASKS_URL = reverse("tasks:recent")


class TestTaskEndpoint(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.today_tasks_count = 10
        self.yesterday_count = 20
        today = timezone.now()
        yesterday = today + timedelta(days=1)
        self.tags = baker.make(Tag, owner=self.user, _quantity=5)
        baker.make(Task, owner=self.user, created_at=today, _quantity=self.today_tasks_count)
        baker.make(Task, owner=self.user, created_at=yesterday, _quantity=self.yesterday_count)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_single_task(self):
        payload = {"title": "sample task", "description": "sample description"}
        response = self.client.post(TASKS_URL, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_get_single_task_details(self):
        task = baker.make(Task, owner=self.user)

        url = reverse("tasks:task-detail", args=[task.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(task.id))

    def test_single_task_has_tags(self):
        tags_titles = [tag.title for tag in self.tags]
        task = baker.make(Task, owner=self.user, tags=self.tags)

        url = reverse("tasks:task-detail", args=[task.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tags", response.data)
        for tag in response.data["tags"]:
            self.assertIn(tag["title"], tags_titles)

    def test_update_single_task(self):
        task = baker.make(Task, owner=self.user)

        url = reverse("tasks:task-detail", args=[task.pk])
        payload = {"title": "updated title", "description": "updated description"}
        response = self.client.put(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_update_single_task_with_tags(self):
        task = baker.make(Task, owner=self.user)

        url = reverse("tasks:task-detail", args=[task.pk])
        payload = {
            "title": "updated title",
            "description": "updated description",
            "tags": [{"title": "update tag title", "description": "updated tag description"}],
        }
        response = self.client.put(url, data=payload, format="json")

        updated_task = Task.objects.get(pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_task.title)
        self.assertEqual(response.data["description"], updated_task.description)
        for tag in payload["tags"]:
            tag_exists = updated_task.tags.filter(title=tag["title"], owner=self.user).exists()
            self.assertTrue(tag_exists)

    def test_delete_single_task(self):
        task = baker.make(Task, owner=self.user)

        url = reverse("tasks:task-detail", args=[task.pk])
        response = self.client.delete(url)

        task_exists = Task.objects.filter(pk=task.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(task_exists)

    def test_recent_tasks_aggregation(self):
        today = date.today().strftime("%d %b, %Y")
        yesterday = (date.today() + timedelta(days=1)).strftime("%d %b, %Y")

        response = self.client.get(RECENT_TASKS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[today]), self.today_tasks_count)
        self.assertEqual(len(response.data[yesterday]), self.yesterday_count)


class TestTagEndpoint(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_single_tag(self):
        payload = {"title": "sample tag", "description": "sample description"}
        response = self.client.post(TAGS_URL, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_create_duplicate_tag(self):
        tag = baker.make(Tag, owner=self.user)

        payload = {"title": tag.title, "description": tag.description}
        response = self.client.post(TAGS_URL, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_get_single_tag_details(self):
        tag = baker.make(Tag, owner=self.user)

        url = reverse("tasks:tag-detail", args=[tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(tag.id))

    def test_update_single_tag(self):
        tag = baker.make(Tag, owner=self.user)

        payload = {"title": "new tag title"}
        url = reverse("tasks:tag-detail", args=[tag.pk])
        response = self.client.patch(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_delete_single_tag(self):
        tag = baker.make(Tag, owner=self.user)

        url = reverse("tasks:tag-detail", args=[tag.pk])
        response = self.client.delete(url)

        tag_exists = Tag.objects.filter(pk=tag.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(tag_exists)
