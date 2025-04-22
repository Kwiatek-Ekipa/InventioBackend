from django.urls import path
from . import views

app_name = "hardware"

urlpatterns = [
    path('categories/', views.create_category, name='create_category'),
]