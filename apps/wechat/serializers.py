"""
WeChat Serializers
"""
from rest_framework import serializers
from .models import WeChatUser, WeChatMessage


class WeChatUserSerializer(serializers.ModelSerializer):
    """微信用户序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = WeChatUser
        fields = ['id', 'openid', 'unionid', 'nickname', 'avatar_url', 'sex', 'city', 'province',
                  'country', 'subscribe_time', 'is_subscribed', 'username', 'user_role',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'openid', 'created_at', 'updated_at']


class WeChatMessageSerializer(serializers.ModelSerializer):
    """微信消息序列化器"""
    nickname = serializers.CharField(source='wechat_user.nickname', read_only=True)

    class Meta:
        model = WeChatMessage
        fields = ['id', 'wechat_user', 'nickname', 'message_type', 'event_type', 'content',
                  'media_id', 'recognition', 'latitude', 'longitude', 'label', 'title', 'url',
                  'created_at']
        read_only_fields = ['id', 'created_at']


class WeChatOAuthSerializer(serializers.Serializer):
    """微信授权序列化器"""
    code = serializers.CharField(help_text='微信授权 code')


class WeChatBindSerializer(serializers.Serializer):
    """微信绑定序列化器"""
    name = serializers.CharField(max_length=50, help_text='业主姓名')
    id_card = serializers.CharField(max_length=18, help_text='身份证号')
    property_id = serializers.UUIDField(help_text='房产ID')
