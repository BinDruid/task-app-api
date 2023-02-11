from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels


UserModel = get_user_model()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    finished_at = jmodels.jDateTimeField(
        null=True, blank=True, verbose_name="تاریخ اتمام"
    )
    is_finished = models.BooleanField(default=False)

    class Meta:
        ordering = [
            "created_at",
        ]

    def __str__(self):
        return self.title
