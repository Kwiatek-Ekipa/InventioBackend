from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
app_name = "hardware"

urlpatterns = []

router = DefaultRouter()
router.register('categories', views.HardwareCategoryViewSet)
urlpatterns += router.urls