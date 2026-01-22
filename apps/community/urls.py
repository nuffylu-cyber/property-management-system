"""
Community URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunityViewSet, BuildingViewSet

router = DefaultRouter()
router.register(r'communities', CommunityViewSet, basename='community')
router.register(r'buildings', BuildingViewSet, basename='building')

urlpatterns = [
    path('', include(router.urls)),
]
