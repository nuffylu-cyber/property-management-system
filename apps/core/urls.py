"""
Core URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet, OperationLogViewSet, SystemConfigViewSet,
    WeChatPayConfigViewSet, PermissionViewSet, RolePermissionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'logs', OperationLogViewSet, basename='operationlog')
router.register(r'configs', SystemConfigViewSet, basename='systemconfig')
router.register(r'payment-config', WeChatPayConfigViewSet, basename='wechatpayconfig')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'role-permissions', RolePermissionViewSet, basename='rolepermission')

urlpatterns = [
    # JWT Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Router URLs
    path('', include(router.urls)),
]
