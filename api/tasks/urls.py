from django.urls import path

from api.tasks.views import TaskView, TagView

app_name = "tasks"

urlpatterns = [
    path("task/", (TaskView.as_view({"post": "create", "get": "list"})), name="tasks-collection"),
    path("task/recent/", (TaskView.as_view({"get": "list_recent_tasks"})), name="recent"),
    path(
        "task/<uuid:pk>/",
        (TaskView.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),
        name="task-detail",
    ),
    path("tag/", (TagView.as_view({"post": "create", "get": "list"})), name="tags-collection"),
        path(
        "tag/<uuid:pk>/",
        (TagView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
        name="tag-detail",
    ),

]
