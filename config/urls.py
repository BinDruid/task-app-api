from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("master/", admin.site.urls),
    path("v1/auth/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.authtoken")),
    path("v1/tasks/", include("apps.tasks.urls")),
]

if settings.DEBUG:
    urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
]