from django.urls import path
from rest_framework import routers
from .views import (
    LoginAPIView,
    RegistrationAPIView,
)
app_name = 'authentication'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view()),
]