from django.utils import timezone
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_at"]
