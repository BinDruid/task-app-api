from django.urls import path

from api.core.views import CeleryTaskView

app_name = "core"

urlpatterns = [path("email/", CeleryTaskView.as_view(), name="core-tasks")]
