from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    public_id = models.UUIDField(unique=True, default=uuid4, editable=False)

