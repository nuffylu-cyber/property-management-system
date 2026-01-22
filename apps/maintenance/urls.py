"""
Maintenance URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceRequestViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'requests', MaintenanceRequestViewSet, basename='maintenancerequest')
router.register(r'logs', MaintenanceLogViewSet, basename='maintenancelog')

urlpatterns = [
    path('', include(router.urls)),
]
