import os
import tempfile
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tag, Task

User = get_user_model()

TASKS_URL = reverse("tasks:tasks-collection")
TAGS_URL = reverse("tasks:tags-collection")
RECENT_TASKS_URL = reverse("tasks:recent")


class TestTaskEndpoint(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.tags = baker.make(Tag, owner=cls.user, _quantity=5)
        cls.task = baker.make(Task, owner=cls.user, tags=cls.tags)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_single_task(self):
        payload = {"title": "sample task", "description": "sample description"}
        response = self.client.post(TASKS_URL, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_get_single_task_details(self):
        url = reverse("tasks:task-detail", args=[self.task.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.task.id))

    def test_single_task_has_tags(self):
        tags_titles = [tag.title for tag in self.tags]

        url = reverse("tasks:task-detail", args=[self.task.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tags", response.data)
        for tag in response.data["tags"]:
            self.assertIn(tag["title"], tags_titles)

    def test_update_single_task(self):
        url = reverse("tasks:task-detail", args=[self.task.pk])
        payload = {"title": "updated title", "description": "updated description"}
        response = self.client.put(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_update_single_task_with_tags(self):
        url = reverse("tasks:task-detail", args=[self.task.pk])
        payload = {
            "title": "updated title",
            "description": "updated description",
            "tags": [{"title": "update tag title", "description": "updated tag description"}],
        }
        response = self.client.put(url, data=payload, format="json")

        updated_task = Task.objects.get(pk=self.task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_task.title)
        self.assertEqual(response.data["description"], updated_task.description)
        for tag in payload["tags"]:
            tag_exists = updated_task.tags.filter(title=tag["title"], owner=self.user).exists()
            self.assertTrue(tag_exists)

    def test_delete_single_task(self):
        url = reverse("tasks:task-detail", args=[self.task.pk])
        response = self.client.delete(url)

        task_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(task_exists)


class TestTaskAggregation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_recent_tasks_aggregation(self):
        today_tasks_count = 10
        yesterday_count = 20
        today = timezone.now()
        yesterday = today + timedelta(days=1)
        baker.make(Task, owner=self.user, created_at=today, _quantity=today_tasks_count)
        baker.make(Task, owner=self.user, created_at=yesterday, _quantity=yesterday_count)

        response = self.client.get(RECENT_TASKS_URL)

        today_string = today.strftime("%d %b, %Y")
        yesterday_string = yesterday.strftime("%d %b, %Y")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[today_string]), today_tasks_count)
        self.assertEqual(len(response.data[yesterday_string]), yesterday_count)


class TestTaskAttachment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make(User)
        cls.task = baker.make(Task, owner=cls.user)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.task.attachment.delete()

    def test_single_task_attachment_file(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = {"attachment": image_file}
            url = reverse("tasks:task-attachment", args=[self.task.pk])
            response = self.client.post(url, data=payload, format="multipart")

        self.task.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(os.path.exists(self.task.attachment.path))
        self.assertIn("attachment", response.data)


class TestTagEndpoint(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.tag = baker.make(Tag, owner=self.user)
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
        url = reverse("tasks:tag-detail", args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.tag.id))

    def test_update_single_tag(self):
        payload = {"title": "new tag title"}
        url = reverse("tasks:tag-detail", args=[self.tag.pk])
        response = self.client.patch(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_delete_single_tag(self):
        url = reverse("tasks:tag-detail", args=[self.tag.pk])
        response = self.client.delete(url)

        tag_exists = Tag.objects.filter(pk=self.tag.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(tag_exists)
