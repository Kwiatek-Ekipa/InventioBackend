from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import HardwareCategoryViewSet

app_name = "hardware"

urlpatterns = []

router = DefaultRouter()
router.register('categories', HardwareCategoryViewSet)
urlpatterns += router.urls