"""
Maintenance Serializers
"""
from rest_framework import serializers
from .models import MaintenanceRequest, MaintenanceLog


class MaintenanceLogSerializer(serializers.ModelSerializer):
    """报事处理日志序列化器"""

    class Meta:
        model = MaintenanceLog
        fields = ['id', 'operator', 'action', 'description', 'images', 'created_at']
        read_only_fields = ['id', 'created_at']


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    """报事记录序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    property_address = serializers.CharField(source='property.full_address', read_only=True)
    logs = MaintenanceLogSerializer(many=True, read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'request_number', 'community', 'community_name', 'property', 'property_address',
                  'reporter', 'reporter_phone', 'category', 'description', 'images', 'status',
                  'priority', 'assigned_to', 'assigned_at', 'started_at', 'completed_at',
                  'result_images', 'result_description', 'rating', 'feedback', 'logs',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'request_number', 'created_at', 'updated_at']


class MaintenanceRequestListSerializer(serializers.ModelSerializer):
    """报事记录列表序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    property_address = serializers.CharField(source='property.full_address', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'request_number', 'community_name', 'property_address', 'reporter',
                  'category', 'category_display', 'description', 'status', 'status_display',
                  'priority', 'assigned_to', 'created_at']


class MaintenanceCreateSerializer(serializers.ModelSerializer):
    """创建报事序列化器（用于微信公众号）"""

    class Meta:
        model = MaintenanceRequest
        fields = ['property', 'reporter', 'reporter_phone', 'category', 'description', 'images', 'priority']


class MaintenanceAssignSerializer(serializers.Serializer):
    """派单序列化器"""
    assigned_to = serializers.CharField(max_length=50, help_text='指派给（如：电工张三）')


class MaintenanceCompleteSerializer(serializers.Serializer):
    """完成报事序列化器"""
    result_description = serializers.CharField(help_text='处理结果说明')
    result_images = serializers.ListField(child=serializers.URLField(), required=False, help_text='处理结果图片')
