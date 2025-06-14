from rest_framework.routers import DefaultRouter
from .viewsets import StocktakingViewSet


app_name = "stocktaking"
router = DefaultRouter()

router.register('stocktakings', StocktakingViewSet, basename='stocktakings')

urlpatterns = [] + router.urls