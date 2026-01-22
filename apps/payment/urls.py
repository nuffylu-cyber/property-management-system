"""
Payment URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeStandardViewSet, PaymentBillViewSet, PaymentRecordViewSet

router = DefaultRouter()
router.register(r'fee-standards', FeeStandardViewSet, basename='feestandard')
router.register(r'bills', PaymentBillViewSet, basename='paymentbill')
router.register(r'records', PaymentRecordViewSet, basename='paymentrecord')

urlpatterns = [
    path('', include(router.urls)),
]
