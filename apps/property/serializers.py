"""
Property Serializers
"""
from rest_framework import serializers
from .models import Property, Owner, Tenant


class PropertySerializer(serializers.ModelSerializer):
    """房产序列化器"""
    community_name = serializers.CharField(source='community.name', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)
    full_address = serializers.CharField(read_only=True)
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'community', 'community_name', 'building', 'building_name', 'unit', 'floor',
                  'room_number', 'area', 'property_type', 'status', 'description', 'full_address',
                  'owner_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_owner_name(self, obj):
        """获取业主姓名"""
        owner_relation = obj.owners.first()
        return owner_relation.owner.name if owner_relation else None


class PropertyListSerializer(serializers.ModelSerializer):
    """房产列表序列化器"""
    full_address = serializers.CharField(read_only=True)
    floor_room_display = serializers.CharField(read_only=True)
    owner_name = serializers.SerializerMethodField()
    community_id = serializers.UUIDField(source='community.id', read_only=True)
    community_name = serializers.CharField(source='community.name', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)
    room_number = serializers.CharField(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'full_address', 'floor_room_display', 'area', 'property_type',
                  'status', 'owner_name', 'community_id', 'community_name', 'building_name', 'room_number']

    def get_owner_name(self, obj):
        owner_relation = obj.owners.first()
        return owner_relation.owner.name if owner_relation else None


class OwnerSerializer(serializers.ModelSerializer):
    """业主序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    properties = PropertySerializer(many=True, read_only=True, source='owner_properties')

    class Meta:
        model = Owner
        fields = ['id', 'user', 'username', 'name', 'phone', 'id_card', 'wechat_openid', 'wechat_nickname',
                  'avatar_url', 'is_verified', 'properties', 'created_at', 'updated_at']
        read_only_fields = ['id', 'wechat_openid', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 身份证号脱敏
        if 'id_card' in data and data['id_card']:
            id_card = data['id_card']
            data['id_card'] = id_card[:6] + '********' + id_card[-4:]
        # 手机号脱敏
        if 'phone' in data and data['phone']:
            phone = data['phone']
            data['phone'] = phone[:3] + '****' + phone[-4:]
        return data


class OwnerListSerializer(serializers.ModelSerializer):
    """业主列表序列化器"""
    property_count = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ['id', 'name', 'phone', 'is_verified', 'property_count', 'created_at']

    def get_property_count(self, obj):
        return obj.owners.count()


class TenantSerializer(serializers.ModelSerializer):
    """租户序列化器"""
    property_address = serializers.CharField(source='property.full_address', read_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'user', 'name', 'phone', 'id_card', 'property', 'property_address',
                  'wechat_openid', 'wechat_nickname', 'lease_start', 'lease_end', 'is_active',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'wechat_openid', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 身份证号脱敏
        if 'id_card' in data and data['id_card']:
            id_card = data['id_card']
            data['id_card'] = id_card[:6] + '********' + id_card[-4:]
        # 手机号脱敏
        if 'phone' in data and data['phone']:
            phone = data['phone']
            data['phone'] = phone[:3] + '****' + phone[-4:]
        return data


class OwnerPropertyRelationSerializer(serializers.Serializer):
    """业主-房产关联序列化器（用于批量关联）"""
    owner_id = serializers.UUIDField()
    property_id = serializers.UUIDField()
    ownership_type = serializers.ChoiceField(choices=[
        ('full', '完全所有权'),
        ('shared', '共同所有'),
        ('mortgage', '按揭中'),
    ], default='full')
