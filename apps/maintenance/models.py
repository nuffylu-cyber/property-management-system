"""
Maintenance Models - 物业报事管理
"""
import uuid
from django.db import models
from apps.community.models import Community
from apps.property.models import Property


class MaintenanceRequest(models.Model):
    """
    报事记录模型
    """
    STATUS_CHOICES = [
        ('pending', '待派单'),
        ('assigned', '已派单'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('closed', '已关闭'),
    ]

    CATEGORY_CHOICES = [
        ('electric', '电工'),
        ('plumbing', '水工'),
        ('civil', '土木'),
        ('elevator', '电梯'),
        ('cleaning', '清洁'),
        ('security', '安保'),
        ('other', '其他'),
    ]

    PRIORITY_CHOICES = [
        ('low', '一般'),
        ('medium', '紧急'),
        ('high', '非常紧急'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_number = models.CharField(max_length=50, unique=True, verbose_name='报事编号')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='maintenance_requests', verbose_name='所属小区')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests', verbose_name='房产')
    reporter = models.CharField(max_length=50, verbose_name='报事人')
    reporter_phone = models.CharField(max_length=20, verbose_name='联系电话')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='报事类别')
    description = models.TextField(verbose_name='问题描述')
    images = models.JSONField(default=list, blank=True, verbose_name='图片列表')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low', verbose_name='优先级')
    assigned_to = models.CharField(max_length=50, blank=True, null=True, verbose_name='指派给')
    assigned_at = models.DateTimeField(blank=True, null=True, verbose_name='派单时间')
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='开始处理时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    result_images = models.JSONField(default=list, blank=True, verbose_name='处理结果图片')
    result_description = models.TextField(blank=True, null=True, verbose_name='处理结果说明')
    rating = models.IntegerField(blank=True, null=True, verbose_name='评分(1-5)')
    feedback = models.TextField(blank=True, null=True, verbose_name='用户反馈')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'maintenance_request'
        verbose_name = '报事记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_number} - {self.get_category_display()}"

    def save(self, *args, **kwargs):
        """保存时自动生成报事编号"""
        if not self.request_number:
            # 生成报事编号：BX + 年月日 + 4位随机数
            from django.utils import timezone
            now = timezone.now()
            date_str = now.strftime('%Y%m%d')
            random_str = str(uuid.uuid4().int)[:4]
            self.request_number = f"BX{date_str}{random_str}"
        super().save(*args, **kwargs)


class MaintenanceLog(models.Model):
    """
    报事处理日志
    记录报事的处理过程
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='logs', verbose_name='报事记录')
    operator = models.CharField(max_length=50, verbose_name='操作人')
    action = models.CharField(max_length=50, verbose_name='操作类型')
    description = models.TextField(verbose_name='操作说明')
    images = models.JSONField(default=list, blank=True, verbose_name='图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'maintenance_log'
        verbose_name = '报事处理日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request.request_number} - {self.action}"
