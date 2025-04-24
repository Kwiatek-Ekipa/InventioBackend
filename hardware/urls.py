from rest_framework.routers import DefaultRouter
from .viewsets import HardwareCategoryViewSet

app_name = "hardware"
from hardware.viewsets import BrandViewSet


router = DefaultRouter()

router.register('brands', BrandViewSet, basename='brands')
router.register('categories', HardwareCategoryViewSet, basename='categories')

urlpatterns = [] + router.urls