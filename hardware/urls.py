from rest_framework.routers import DefaultRouter

from hardware.viewsets import BrandViewSet

app_name = 'hardware'

router = DefaultRouter()

router.register('brands', BrandViewSet, basename='brands')

urlpatterns = [] + router.urls