from django.urls import path, include
from . import views
from uuid import UUID
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_info/', views.user_info, name='user_info'),
    path('technician/create', views.create_technician, name='create_technician'),
    path('technician/delete/<uuid:user_id>/', views.delete_technician, name='delete_technician'),
]