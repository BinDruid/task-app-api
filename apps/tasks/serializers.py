from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
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
