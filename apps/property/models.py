"""
Property Models - 房产管理
"""
import uuid
from django.db import models
from apps.community.models import Community, Building


class Property(models.Model):
    """
    房产模型
    """
    PROPERTY_TYPE_CHOICES = [
        ('residential', '住宅'),
        ('commercial', '商业'),
        ('garage', '车库'),
        ('storage', '储藏室'),
    ]

    STATUS_CHOICES = [
        ('occupied', '自住'),
        ('rented', '出租'),
        ('vacant', '空置'),
        ('renovation', '装修中'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='properties', verbose_name='所属小区')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='properties', verbose_name='所属楼栋')
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name='单元号')
    floor = models.IntegerField(verbose_name='楼层')
    room_number = models.CharField(max_length=20, verbose_name='房号')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='面积(㎡)')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='residential', verbose_name='房产类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant', verbose_name='状态')
    description = models.TextField(blank=True, null=True, verbose_name='房产描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'property_property'
        verbose_name = '房产'
        verbose_name_plural = verbose_name
        ordering = ['community', 'building', 'unit', 'floor', 'room_number']
        unique_together = [['building', 'unit', 'floor', 'room_number']]

    def __str__(self):
        """房产标识，显示为1号楼-502格式（保持Excel房号格式）"""
        # 将楼层和房号组合成Excel格式的房号
        # floor=5, room_number="01" → "501"
        # floor=10, room_number="01" → "1001"
        room_number_full = f"{self.floor}{self.room_number}"

        # 如果有单元号，格式为：1号楼1单元-201
        # 如果没有单元号，格式为：1号楼-201
        if self.unit:
            return f"{self.building.name}{self.unit}-{room_number_full}"
        else:
            return f"{self.building.name}-{room_number_full}"

    @property
    def full_address(self):
        """完整地址"""
        room_number_full = f"{self.floor}{self.room_number}"

        # 如果有单元号，格式为：锦尚名都1号楼1单元-201
        # 如果没有单元号，格式为：锦尚名都1号楼-201
        if self.unit:
            return f"{self.community.name}{self.building.name}{self.unit}-{room_number_full}"
        else:
            return f"{self.community.name}{self.building.name}-{room_number_full}"

    @property
    def floor_room_display(self):
        """楼层/单元/楼号显示"""
        # 从楼栋名称中提取楼号
        # building.name = "1号楼" → 提取 "1"
        building_num = ""
        for char in self.building.name:
            if char.isdigit():
                building_num += char
            else:
                break

        # 如果有单元，显示格式：2层/1单元/1号楼
        # 如果没有单元，显示格式：2层/1号楼
        # 注意：unit字段可能已包含"单元"文字（如"1单元"）
        if self.unit:
            # 检查unit是否已包含"单元"文字
            if '单元' in self.unit:
                return f"{self.floor}层/{self.unit}/{building_num}号楼"
            else:
                return f"{self.floor}层/{self.unit}单元/{building_num}号楼"
        else:
            return f"{self.floor}层/{building_num}号楼"


class OwnerProperty(models.Model):
    """
    业主-房产关联模型（中间表）
    支持一名业主名下有多套房
    """
    OWNERSHIP_TYPE_CHOICES = [
        ('full', '完全所有权'),
        ('shared', '共同所有'),
        ('mortgage', '按揭中'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='owners', verbose_name='业主')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='owners', verbose_name='房产')
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPE_CHOICES, default='full', verbose_name='所有权类型')
    ownership_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=100.00, verbose_name='所有权比例(%)')
    is_primary = models.BooleanField(default=False, verbose_name='是否主要房产')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'property_owner_property'
        verbose_name = '业主房产关联'
        verbose_name_plural = verbose_name
        unique_together = [['owner', 'property']]

    def __str__(self):
        return f"{self.owner.name} - {self.property.full_address}"


class Owner(models.Model):
    """
    业主模型
    """
    VERIFICATION_STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]

    SOURCE_CHOICES = [
        ('system', '系统导入'),
        ('self_registered', '自行注册'),
        ('admin_added', '管理员添加'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='owner_profile',
                                verbose_name='关联用户')
    name = models.CharField(max_length=50, verbose_name='业主姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, blank=True, null=True, verbose_name='身份证号')
    wechat_openid = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='微信OpenID')
    wechat_nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信昵称')
    avatar_url = models.URLField(blank=True, null=True, verbose_name='头像URL')
    is_verified = models.BooleanField(default=False, verbose_name='是否已认证')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='approved',
                                          verbose_name='审核状态')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='system', verbose_name='数据来源')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'property_owner'
        verbose_name = '业主'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def get_properties(self):
        """获取业主的所有房产"""
        return [op.property for op in self.owners.all()]

    @property
    def owner_properties(self):
        """获取业主的所有房产（用于序列化器）"""
        return [op.property for op in self.owners.all()]


class Tenant(models.Model):
    """
    租户模型
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='tenant_profile',
                                verbose_name='关联用户')
    name = models.CharField(max_length=50, verbose_name='租户姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, verbose_name='身份证号')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='tenants', verbose_name='租赁房产')
    wechat_openid = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='微信OpenID')
    wechat_nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信昵称')
    lease_start = models.DateField(verbose_name='租赁开始日期')
    lease_end = models.DateField(verbose_name='租赁结束日期')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'property_tenant'
        verbose_name = '租户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.property.full_address}"
