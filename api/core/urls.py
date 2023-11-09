from django.urls import path

from api.core.views import CeleryTaskView

app_name = "core"

urlpatterns = [
    path("status/<pk>/", CeleryTaskView.as_view(), name="core-status"),
    path("email/", CeleryTaskView.as_view(), name="core-tasks")
]
