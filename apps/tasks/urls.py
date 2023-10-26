from django.urls import path

from apps.tasks.views import TaskView

app_name = "tasks"

urlpatterns = [
    path("", (TaskView.as_view({"post": "create"})), name="new_task"),
    path("recent/", (TaskView.as_view({"get": "list"})), name="tasks"),
    path(
        "<uuid:pk>/",
        (TaskView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
        name="single_task",
    ),
]
