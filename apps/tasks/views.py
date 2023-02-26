from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDate
from apps.tasks.models import Task
from apps.tasks.serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
)

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
            "retrieve": TaskDetailSerializer,
            "create": TaskCreateSerializer,
            "partial_update": TaskDetailSerializer,
        }
        return serializer_classes[self.action]

    @property
    def queryset_per_action(self):
        queryset_classes = {
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

    def list(self, request, *args, **kwargs):
        base_query = Task.objects.filter(owner=request.user).annotate(
            day=TruncDate("created_at")
        )

        recent_days = (
            base_query.values_list("day", flat=True).distinct().order_by("-day")
        )[:6]

        querysets = [base_query.filter(day=week_day) for week_day in recent_days]

        serializers = [
            TaskListSerializer(queryset, many=True) for queryset in querysets
        ]

        week_days = [day.strftime("%d %b, %Y") for day in recent_days]

        return Response(
            dict(zip(week_days, [serializer.data for serializer in serializers]))
        )
