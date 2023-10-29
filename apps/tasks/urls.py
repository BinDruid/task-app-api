from django.urls import path

from apps.tasks.views import TaskView, TagView

app_name = "tasks"

urlpatterns = [
    path("", (TaskView.as_view({"post": "create", "get": "list"})), name="tasks"),
    path("recent/", (TaskView.as_view({"get": "list_recent_tasks"})), name="recent"),
    path(
        "<uuid:pk>/",
        (TaskView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
        name="detail",
    ),
    path("tag/", (TagView.as_view({"post": "create", "get": "list"})), name="tags"),
]
