"""
Core Models - User and Operation Log
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型
    扩展 Django 默认用户，添加角色和权限
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    role = models.CharField(
        max_length=20,
        choices=[
            ('super_admin', '超级管理员'),
            ('admin', '管理员'),
            ('finance', '财务'),
            ('receptionist', '前台'),
            ('engineering', '工程部'),
            ('owner', '业主'),
            ('tenant', '租户'),
        ],
        default='owner',
        verbose_name='角色'
    )
    avatar = models.URLField(blank=True, null=True, verbose_name='头像URL')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'core_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_role_display()} - {self.username}"

    def get_role_display(self):
        """获取角色显示名称"""
        role_dict = {
            'super_admin': '超级管理员',
            'admin': '管理员',
            'finance': '财务',
            'receptionist': '前台',
            'engineering': '工程部',
            'owner': '业主',
            'tenant': '租户',
        }
        return role_dict.get(self.role, self.role)


class OperationLog(models.Model):
    """
    操作日志
    记录所有用户的关键操作
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='操作人')
    action = models.CharField(max_length=50, verbose_name='操作类型')
    module = models.CharField(max_length=50, verbose_name='模块')
    description = models.TextField(verbose_name='操作描述')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='用户代理')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'core_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operator} - {self.action} - {self.created_at}"


class SystemConfig(models.Model):
    """
    系统配置
    存储系统级别的配置项
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'core_system_config'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.key}: {self.value}"


class WeChatPayConfig(models.Model):
    """
    微信支付配置
    支持个人账号和企业对公账户
    """
    ACCOUNT_TYPE_CHOICES = [
        ('personal', '个人账号'),
        ('enterprise', '企业对公账户'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='配置名称')
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='enterprise',
        verbose_name='账号类型'
    )
    # 公众号/小程序配置
    app_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='应用ID(AppID)')
    app_secret = models.CharField(max_length=200, blank=True, null=True, verbose_name='应用密钥(AppSecret)')
    # 商户配置
    mch_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='商户号(MchID)')
    api_key = models.CharField(max_length=200, blank=True, null=True, verbose_name='API密钥')
    api_v3_key = models.CharField(max_length=200, blank=True, null=True, verbose_name='APIv3密钥')
    serial_no = models.CharField(max_length=100, blank=True, null=True, verbose_name='证书序列号')
    cert_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='证书路径')
    key_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='密钥路径')
    # 回调地址
    notify_url = models.URLField(blank=True, null=True, verbose_name='支付回调地址')
    # 状态
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    # 备注
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'core_wechat_pay_config'
        verbose_name = '微信支付配置'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"


class Permission(models.Model):
    """
    权限
    定义系统中的各种操作权限
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='权限名称')
    code = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    module = models.CharField(max_length=50, verbose_name='所属模块')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'core_permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['module', 'code']

    def __str__(self):
        return f"{self.module} - {self.name}"


class RolePermission(models.Model):
    """
    角色权限关联
    定义不同角色拥有的权限
    """
    ROLE_CHOICES = [
        ('super_admin', '超级管理员'),
        ('admin', '管理员'),
        ('finance', '财务'),
        ('receptionist', '前台'),
        ('engineering', '工程部'),
        ('owner', '业主'),
        ('tenant', '租户'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    can_view = models.BooleanField(default=True, verbose_name='可查看')
    can_create = models.BooleanField(default=False, verbose_name='可创建')
    can_edit = models.BooleanField(default=False, verbose_name='可编辑')
    can_delete = models.BooleanField(default=False, verbose_name='可删除')
    can_export = models.BooleanField(default=False, verbose_name='可导出')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'core_role_permission'
        verbose_name = '角色权限'
        verbose_name_plural = verbose_name
        unique_together = ['role', 'permission']
        ordering = ['role', 'permission__module']

    def __str__(self):
        return f"{self.get_role_display()} - {self.permission.name}"


class Notification(models.Model):
    """
    系统通知模型
    支持站内消息、短信、微信推送等多种通知方式
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('payment_reminder', '缴费提醒'),
        ('payment_overdue', '逾期催缴'),
        ('maintenance_assigned', '报事派单'),
        ('maintenance_processing', '报事处理中'),
        ('maintenance_completed', '报事完成'),
        ('maintenance_closed', '报事关闭'),
        ('system_announcement', '系统公告'),
    ]

    STATUS_CHOICES = [
        ('pending', '待发送'),
        ('sent', '已发送'),
        ('failed', '发送失败'),
        ('read', '已读'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='通知类型')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')

    # 接收用户
    recipient = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name='接收人')
    recipient_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='接收人电话')
    recipient_openid = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信OpenID')

    # 关联对象
    related_bill = models.ForeignKey('payment.PaymentBill', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name='关联账单')
    related_maintenance = models.ForeignKey('maintenance.MaintenanceRequest', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name='关联报事')

    # 发送状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    send_channels = models.JSONField(default=dict, verbose_name='发送渠道')  # {'email': true, 'sms': true, 'wechat': true}
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')

    # 错误信息
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    retry_count = models.IntegerField(default=0, verbose_name='重试次数')
    max_retries = models.IntegerField(default=3, verbose_name='最大重试次数')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'notification'
        verbose_name = '系统通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['notification_type', 'status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        """标记为已读"""
        from django.utils import timezone
        self.status = 'read'
        self.read_at = timezone.now()
        self.save(update_fields=['status', 'read_at'])
