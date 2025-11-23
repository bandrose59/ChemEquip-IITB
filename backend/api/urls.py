from django.urls import path
from .views import upload_csv, history
from .auth.views import register, login

urlpatterns = [
    path("auth/register/", register),
    path("auth/login/", login),
    path("upload/", upload_csv),
    path("history/", history),
]