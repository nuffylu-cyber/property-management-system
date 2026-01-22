"""
Core Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OperationLog, SystemConfig, WeChatPayConfig, Permission, RolePermission

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'avatar', 'first_name', 'last_name', 'is_active',
                  'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'phone', 'role', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    operator_name = serializers.CharField(source='operator.username', read_only=True)

    class Meta:
        model = OperationLog
        fields = ['id', 'operator', 'operator_name', 'action', 'module', 'description', 'ip_address', 'created_at']
        read_only_fields = ['id', 'created_at']


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""

    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeChatPayConfigSerializer(serializers.ModelSerializer):
    """微信支付配置序列化器"""
    account_type_display = serializers.CharField(source='get_account_type_display', read_only=True)

    class Meta:
        model = WeChatPayConfig
        fields = ['id', 'name', 'account_type', 'account_type_display', 'app_id', 'app_secret',
                  'mch_id', 'api_key', 'api_v3_key', 'serial_no', 'cert_path', 'key_path',
                  'notify_url', 'is_active', 'is_default', 'remarks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """隐藏敏感信息"""
        data = super().to_representation(instance)
        # 隐藏部分敏感信息
        sensitive_fields = ['app_secret', 'api_key', 'api_v3_key']
        for field in sensitive_fields:
            if data.get(field) and len(data[field]) > 8:
                data[field] = data[field][:4] + '****' + data[field][-4:]
        return data


class WeChatPayConfigCreateSerializer(serializers.ModelSerializer):
    """微信支付配置创建序列化器（不隐藏敏感信息）"""

    class Meta:
        model = WeChatPayConfig
        fields = ['id', 'name', 'account_type', 'app_id', 'app_secret',
                  'mch_id', 'api_key', 'api_v3_key', 'serial_no', 'cert_path', 'key_path',
                  'notify_url', 'is_active', 'is_default', 'remarks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""

    class Meta:
        model = Permission
        fields = ['id', 'name', 'code', 'module', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class RolePermissionSerializer(serializers.ModelSerializer):
    """角色权限序列化器"""
    permission_detail = PermissionSerializer(source='permission', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'role_display', 'permission', 'permission_detail',
                  'can_view', 'can_create', 'can_edit', 'can_delete', 'can_export', 'created_at']
        read_only_fields = ['id', 'created_at']


class RolePermissionCreateSerializer(serializers.ModelSerializer):
    """角色权限创建序列化器"""

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'can_view', 'can_create',
                  'can_edit', 'can_delete', 'can_export', 'created_at']
        read_only_fields = ['id', 'created_at']
