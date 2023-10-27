from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer

UserModel = get_user_model()


class TaskView(ModelViewSet):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related("owner")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["message"] = "New task created!"
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        base_query = Task.objects.filter(owner=request.user).annotate(day=TruncDate("created_at"))

        recent_days = (base_query.values_list("day", flat=True).distinct().order_by("-day"))[:6]

        querysets = [base_query.filter(day=week_day) for week_day in recent_days]

        serializers = [TaskSerializer(queryset, many=True) for queryset in querysets]

        week_days = [day.strftime("%d %b, %Y") for day in recent_days]
        return Response(dict(zip(week_days, [serializer.data for serializer in serializers])))
