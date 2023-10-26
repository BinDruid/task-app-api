from django.urls import path

from apps.tasks.views import TaskView

app_name = "tasks"

urlpatterns = [
    path("", (TaskView.as_view({"post": "create"})), name="create"),
    path("recent/", (TaskView.as_view({"get": "list"})), name="recent"),
    path(
        "<uuid:pk>/",
        (TaskView.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
        name="detail",
    ),
]
