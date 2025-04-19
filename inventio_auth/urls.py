from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'inventio_auth'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', views.user_info, name='user_info'),
    path('technician/', views.create_technician, name='create_technician'),
    path('technician/<uuid:user_id>/', views.delete_technician, name='delete_technician'),
]