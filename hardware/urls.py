from rest_framework.routers import DefaultRouter
from .viewsets import HardwareCategoryViewSet
from hardware.viewsets import BrandViewSet

app_name = "hardware"


router = DefaultRouter()

router.register('brands', BrandViewSet, basename='brands')
router.register('categories', HardwareCategoryViewSet, basename='categories')

urlpatterns = [] + router.urls