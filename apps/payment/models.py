"""
Payment Models - 缴费管理
"""
import uuid
from django.db import models
from apps.community.models import Community
from apps.property.models import Property, Owner


class FeeStandard(models.Model):
    """
    物业费标准模型
    """
    FEE_TYPE_CHOICES = [
        ('property', '物业费'),
        ('public_electric', '公摊电费'),
        ('water', '水费'),
        ('parking', '停车费'),
        ('payable', '应缴费用'),
        ('other', '其他'),
    ]

    BILLING_CYCLE_CHOICES = [
        ('month', '按月'),
        ('quarter', '按季'),
        ('year', '按年'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='fee_standards', verbose_name='所属小区')
    name = models.CharField(max_length=100, verbose_name='费用名称')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, verbose_name='费用类型')
    price_per_square = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='每平米单价(元)')
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default='month', verbose_name='计费周期')
    description = models.TextField(blank=True, null=True, verbose_name='费用说明')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'payment_fee_standard'
        verbose_name = '物业费标准'
        verbose_name_plural = verbose_name
        ordering = ['community', 'fee_type']

    def __str__(self):
        return f"{self.community.name} - {self.name}"


class PaymentBill(models.Model):
    """
    缴费账单模型
    """
    STATUS_CHOICES = [
        ('unpaid', '未缴'),
        ('partial', '部分缴'),
        ('paid', '已缴'),
        ('overdue', '逾期'),
    ]

    FEE_TYPE_CHOICES = [
        ('property', '物业费'),
        ('public_electric', '公摊电费'),
        ('water', '水费'),
        ('parking', '停车费'),
        ('payable', '应缴费用'),
        ('other', '其他'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('cash', '现金'),
        ('bank_transfer', '银行转账'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_number = models.CharField(max_length=50, unique=True, verbose_name='账单编号')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='bills', verbose_name='所属小区')
    property_unit = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bills', verbose_name='房产')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='bills', verbose_name='业主')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, verbose_name='费用类型')
    billing_period = models.CharField(max_length=20, verbose_name='账期（如：2026-01）')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='应缴金额(元)')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='已缴金额(元)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name='状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, verbose_name='支付方式')
    due_date = models.DateField(verbose_name='应缴日期')
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='缴费时间')
    description = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'payment_bill'
        verbose_name = '缴费账单'
        verbose_name_plural = verbose_name
        ordering = ['-billing_period', '-created_at']
        unique_together = [['property_unit', 'fee_type', 'billing_period']]

    def __str__(self):
        return f"{self.bill_number} - {self.amount}元"

    @property
    def unpaid_amount(self):
        """未缴金额"""
        return self.amount - self.paid_amount


class PaymentRecord(models.Model):
    """
    缴费记录模型
    """
    STATUS_CHOICES = [
        ('success', '成功'),
        ('refund', '退款'),
        ('failed', '失败'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('cash', '现金'),
        ('bank_transfer', '银行转账'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(PaymentBill, on_delete=models.CASCADE, related_name='payment_records', verbose_name='关联账单')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name='微信支付交易号')
    out_trade_no = models.CharField(max_length=100, unique=True, verbose_name='商户订单号')
    payer = models.CharField(max_length=50, verbose_name='缴费人')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='缴费金额(元)')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='wechat', verbose_name='支付方式')
    payment_time = models.DateTimeField(verbose_name='支付时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success', verbose_name='状态')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='退款金额(元)')
    operator = models.CharField(max_length=50, blank=True, null=True, verbose_name='操作人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'payment_record'
        verbose_name = '缴费记录'
        verbose_name_plural = verbose_name
        ordering = ['-payment_time']

    def __str__(self):
        return f"{self.out_trade_no} - {self.amount}元"
