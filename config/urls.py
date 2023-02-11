from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("master/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += [
    path("", include("apps.core.urls")),
    path("v1/auth/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.authtoken")),
    path("v1/tasks/", include("apps.tasks.urls")),
]
