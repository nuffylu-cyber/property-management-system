"""
Payment Admin Configuration
"""
from django.contrib import admin
from .models import FeeStandard, PaymentBill, PaymentRecord


@admin.register(FeeStandard)
class FeeStandardAdmin(admin.ModelAdmin):
    """物业费标准管理"""
    list_display = ['name', 'community', 'fee_type', 'price_per_square', 'billing_cycle', 'is_active']
    list_filter = ['community', 'fee_type', 'billing_cycle', 'is_active']
    search_fields = ['name']
    ordering = ['community', 'fee_type']


@admin.register(PaymentBill)
class PaymentBillAdmin(admin.ModelAdmin):
    """缴费账单管理"""
    list_display = ['bill_number', 'community', 'property_unit', 'owner', 'fee_type', 'billing_period',
                    'amount', 'paid_amount', 'status', 'due_date']
    list_filter = ['community', 'fee_type', 'status', 'billing_period', 'created_at']
    search_fields = ['bill_number', 'property_unit__room_number', 'owner__name']
    readonly_fields = ['bill_number', 'created_at', 'updated_at']
    ordering = ['-billing_period', '-created_at']


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    """缴费记录管理"""
    list_display = ['out_trade_no', 'bill', 'payer', 'amount', 'payment_method', 'status', 'payment_time']
    list_filter = ['status', 'payment_method', 'payment_time']
    search_fields = ['transaction_id', 'out_trade_no', 'payer']
    readonly_fields = ['transaction_id', 'created_at']
    ordering = ['-payment_time']
