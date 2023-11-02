from django.db.models.functions import TruncDate
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Tag, Task
from .serializers import TagSerializer, TaskDetailSerializer, TaskSerializer


class TaskView(ModelViewSet):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).select_related("owner")

    def get_serializer_class(self):
        if self.action == "list":
            return TaskSerializer
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


class TagView(ModelViewSet):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).select_related("owner")
