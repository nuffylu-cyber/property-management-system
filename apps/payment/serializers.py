"""
Payment Serializers
"""
from rest_framework import serializers
from .models import FeeStandard, PaymentBill, PaymentRecord


class FeeStandardSerializer(serializers.ModelSerializer):
    """物业费标准序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = FeeStandard
        fields = ['id', 'community', 'community_name', 'name', 'fee_type', 'price_per_square',
                  'billing_cycle', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentRecordSerializer(serializers.ModelSerializer):
    """缴费记录序列化器"""

    class Meta:
        model = PaymentRecord
        fields = ['id', 'transaction_id', 'out_trade_no', 'payer', 'amount', 'payment_method',
                  'payment_time', 'status', 'refund_amount', 'created_at']
        read_only_fields = ['id', 'transaction_id', 'created_at']


class PaymentBillSerializer(serializers.ModelSerializer):
    """缴费账单序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    property_address = serializers.CharField(source='property_unit.full_address', read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    unpaid_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    payment_records = PaymentRecordSerializer(many=True, read_only=True)

    class Meta:
        model = PaymentBill
        fields = ['id', 'bill_number', 'community', 'community_name', 'property_unit', 'property_address',
                  'owner', 'owner_name', 'fee_type', 'billing_period', 'amount', 'paid_amount',
                  'unpaid_amount', 'status', 'due_date', 'paid_at', 'description', 'payment_records',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'bill_number', 'created_at', 'updated_at']


class PaymentBillListSerializer(serializers.ModelSerializer):
    """缴费账单列表序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    property_address = serializers.CharField(source='property_unit.full_address', read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    unpaid_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = PaymentBill
        fields = ['id', 'bill_number', 'community_name', 'property_address', 'owner_name',
                  'fee_type', 'billing_period', 'amount', 'paid_amount', 'unpaid_amount',
                  'status', 'due_date']


class BatchCreateBillsSerializer(serializers.Serializer):
    """批量创建账单序列化器"""
    community_id = serializers.UUIDField()
    fee_type = serializers.ChoiceField(choices=[
        ('property', '物业费'),
        ('public_electric', '公摊电费'),
        ('water', '水费'),
        ('parking', '停车费'),
        ('other', '其他'),
    ])
    billing_period = serializers.CharField(max_length=20, help_text='账期，如：2026-01')
    due_date = serializers.DateField(help_text='应缴日期')
    description = serializers.CharField(required=False, allow_blank=True)


class WeChatPaymentSerializer(serializers.Serializer):
    """微信支付序列化器"""
    bill_ids = serializers.ListField(child=serializers.UUIDField(), help_text='账单ID列表')
