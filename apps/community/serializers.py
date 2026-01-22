"""
Community Serializers
"""
from rest_framework import serializers
from .models import Community, Building


class BuildingSerializer(serializers.ModelSerializer):
    """楼栋序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)

    class Meta:
        model = Building
        fields = ['id', 'community', 'community_name', 'name', 'building_type', 'total_floors',
                  'total_units', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommunitySerializer(serializers.ModelSerializer):
    """小区序列化器"""
    buildings = BuildingSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'address', 'total_households', 'developer', 'property_company',
                  'description', 'buildings', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommunityListSerializer(serializers.ModelSerializer):
    """小区列表序列化器（不包含楼栋详情）"""
    building_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'name', 'address', 'total_households', 'developer', 'property_company',
                  'building_count', 'created_at', 'updated_at']

    def get_building_count(self, obj):
        return obj.buildings.count()
