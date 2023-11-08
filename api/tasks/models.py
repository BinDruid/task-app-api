import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ اتمام")
    is_finished = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks")
    attachment = models.ImageField(
        upload_to="uploads",
        storage=FileSystemStorage(),
        blank=True,
        null=True,
        verbose_name="مستندات",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_at"]
