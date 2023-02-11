from django.urls import path
from .views import TaskView

urlpatterns = [
    path(
        "",
        (TaskView.as_view({"get": "list", "post": "create"})),
        name="tasks",
    ),
    path(
        "<uuid:pk>/",
        (
            TaskView.as_view(
                {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
            )
        ),
        name="single_task",
    ),
]
