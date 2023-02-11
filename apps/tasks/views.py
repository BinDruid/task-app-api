from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
)

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ActionMixin:
    def get_serializer_class(self):
        return self.serializer_per_action

    def get_queryset(self):
        return self.queryset_per_action


class TaskView(ActionMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"

    @property
    def serializer_per_action(self):
        serializer_classes = {
            "list": TaskListSerializer,
            "retrieve": TaskDetailSerializer,
            "create": TaskCreateSerializer,
            "partial_update": TaskDetailSerializer,
        }
        return serializer_classes[self.action]

    @property
    def queryset_per_action(self):
        queryset_classes = {
            "list": Task.objects.filter(owner=self.request.user),
            "retrieve": Task.objects.filter(owner=self.request.user),
            "create": Task.objects.all(),
            "partial_update": Task.objects.all(),
            "destroy": Task.objects.all(),
        }
        return queryset_classes[self.action]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["message"] = "New task created!"
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
