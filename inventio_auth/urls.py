from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views, viewsets

app_name = 'inventio_auth'

router = DefaultRouter()
router.register('roles', viewsets.RoleViewSet, basename='roles')
router.register('accounts', viewsets.AccountViewSet, basename='accounts')

urlpatterns = [
    path('auth/', include([
        path('register/', views.register_user, name='register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('user-info/', views.user_info, name='user_info'),
    ])),
    path('technicians/', include([
        path('', views.create_technician, name='create_technician'),
        path('<uuid:user_id>/', views.delete_technician, name='delete_technician'),
    ])),
] + router.urls