from rest_framework.routers import DefaultRouter
from .viewsets import HardwareCategoryViewSet

app_name = "hardware"

urlpatterns = []

router = DefaultRouter()
router.register('categories', HardwareCategoryViewSet, basename='categories')
urlpatterns += router.urls