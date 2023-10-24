import datetime
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=datetime.datetime.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ اتمام")
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_at"]
