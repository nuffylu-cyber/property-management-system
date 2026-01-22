"""
Community Models - 小区和楼栋管理
"""
import uuid
from django.db import models


class Community(models.Model):
    """
    小区模型
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='小区名称')
    address = models.CharField(max_length=255, verbose_name='小区地址')
    total_households = models.IntegerField(default=0, verbose_name='总户数')
    total_buildings = models.IntegerField(default=0, verbose_name='楼栋数')
    developer = models.CharField(max_length=100, blank=True, null=True, verbose_name='开发商')
    property_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='物业公司')
    contact_person = models.CharField(max_length=50, blank=True, null=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    construction_area = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='建筑面积(㎡)')
    green_area = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='绿化面积(㎡)')
    description = models.TextField(blank=True, null=True, verbose_name='小区描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'community_community'
        verbose_name = '小区'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Building(models.Model):
    """
    楼栋模型
    """
    BUILDING_TYPE_CHOICES = [
        ('high', '高层'),
        ('multi', '多层'),
        ('villa', '别墅'),
        ('commercial', '商业'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='buildings', verbose_name='所属小区')
    name = models.CharField(max_length=50, verbose_name='楼栋号')
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPE_CHOICES, default='high', verbose_name='楼栋类型')
    total_floors = models.IntegerField(blank=True, null=True, verbose_name='总楼层数')
    total_units = models.IntegerField(default=1, verbose_name='单元数')
    description = models.TextField(blank=True, null=True, verbose_name='楼栋描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'community_building'
        verbose_name = '楼栋'
        verbose_name_plural = verbose_name
        ordering = ['community', 'name']
        unique_together = [['community', 'name']]

    def __str__(self):
        return f"{self.community.name} - {self.name}"
