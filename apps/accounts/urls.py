from django.urls import path
from rest_framework.authtoken import views

from .views import UserCreateView

app_name = "app.accounts"

urlpatterns = [
    path("", UserCreateView.as_view(), name="create"),
    path("token/", views.obtain_auth_token, name="token"),
]
