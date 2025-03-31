from django.urls import path, include
from . import views

# app_name = "inventio_auth"

urlpatterns = [
    path('register/', views.register_user, name='register'),
]