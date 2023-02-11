from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Task


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "email"]


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "finished_at",
            "is_finished",
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "created_at",
            "updated_at",
            "finished_at",
            "is_finished",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("owner",)
