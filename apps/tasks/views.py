from django.db.models.functions import TruncDate
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TaskView(ModelViewSet):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related("owner")

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
    @action(detail=True, methods=["get"])
    def list_recent_tasks(self, request, *args, **kwargs):
        base_query = Task.objects.filter(owner=request.user).annotate(day=TruncDate("created_at"))
        recent_days = (base_query.values_list("day", flat=True).distinct().order_by("-day"))[:6]
        querysets = [base_query.filter(day=week_day) for week_day in recent_days]
        serializers = [TaskSerializer(queryset, many=True) for queryset in querysets]
        week_days = [day.strftime("%d %b, %Y") for day in recent_days]
        return Response(dict(zip(week_days, [serializer.data for serializer in serializers])))
