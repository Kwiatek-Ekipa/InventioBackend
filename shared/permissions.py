from rest_framework.permissions import BasePermission
from .enums import RoleEnum

class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.name == RoleEnum.TECHNICIAN.value

class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.name == RoleEnum.WORKER.value