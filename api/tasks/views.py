from django.db.models.functions import TruncDate
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Task
from .serializers import (
    TagSerializer,
    TaskAttachmentSerializer,
    TaskDetailSerializer,
    TaskSerializer,
)


class TaskView(ModelViewSet):
    lookup_field = "pk"
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["title", "is_finished"]
    search_fields = ["title", "tags__title"]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).select_related("owner")

    def get_serializer_class(self):
        if self.action == "list":
            return TaskSerializer
        if self.action == "upload_attachment":
            return TaskAttachmentSerializer
        return self.serializer_class

    @extend_schema(
        description="Aggregates user tasks based on creation date and shows a list of tasks for last 7 recent days.",
        examples=[
            OpenApiExample(
                "Example",
                value={
                    "28 Oct, 2023": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "title": "string",
                            "description": "string",
                            "created_at": "2023-10-27T11:50:08.470Z",
                            "updated_at": "2023-10-27T11:50:08.470Z",
                            "finished_at": "2023-10-27T11:50:08.470Z",
                            "is_finished": True,
                        }
                    ],
                    "25 Oct, 2023": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "title": "string",
                            "description": "string",
                            "created_at": "2023-10-27T11:56:15.187Z",
                            "updated_at": "2023-10-27T11:56:15.187Z",
                            "finished_at": "2023-10-27T11:56:15.187Z",
                            "is_finished": True,
                        }
                    ],
                },
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def list_recent_tasks(self, request, *args, **kwargs):
        base_query = Task.objects.filter(owner=request.user).annotate(day=TruncDate("created_at"))
        recent_days = (base_query.values_list("day", flat=True).distinct().order_by("-day"))[:6]
        querysets = [base_query.filter(day=week_day) for week_day in recent_days]
        serializers = [TaskSerializer(queryset, many=True) for queryset in querysets]
        week_days = [day.strftime("%d %b, %Y") for day in recent_days]
        return Response(dict(zip(week_days, [serializer.data for serializer in serializers])))

    @action(detail=True, methods=["post"])
    def upload_attachment(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class TagView(ModelViewSet):
    lookup_field = "pk"
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["title"]
    search_fields = ["description"]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).select_related("owner")
