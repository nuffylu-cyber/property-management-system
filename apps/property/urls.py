"""
Property URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, OwnerViewSet, TenantViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'owners', OwnerViewSet, basename='owner')
router.register(r'tenants', TenantViewSet, basename='tenant')

urlpatterns = [
    path('', include(router.urls)),
]
