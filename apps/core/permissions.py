"""
Custom Permissions
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    仅允许超级管理员访问
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin')


class IsFinanceUser(permissions.BasePermission):
    """
    仅允许财务人员访问
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role in ['admin', 'finance'])


class IsReceptionistUser(permissions.BasePermission):
    """
    仅允许前台人员访问
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role in ['admin', 'receptionist'])


class IsOwnerOrTenant(permissions.BasePermission):
    """
    仅允许业主或租户访问
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['owner', 'tenant']


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    允许所有用户读取，但只有所有者可以修改
    """

    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只给予对象的所有者
        return hasattr(obj, 'owner') and obj.owner == request.user
