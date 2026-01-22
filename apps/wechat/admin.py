"""
WeChat Admin Configuration
"""
from django.contrib import admin
from .models import WeChatUser, WeChatMessage


@admin.register(WeChatUser)
class WeChatUserAdmin(admin.ModelAdmin):
    """微信用户管理"""
    list_display = ['nickname', 'openid', 'is_subscribed', 'user', 'created_at']
    list_filter = ['is_subscribed', 'sex', 'created_at']
    search_fields = ['nickname', 'openid', 'unionid']
    readonly_fields = ['openid', 'unionid', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(WeChatMessage)
class WeChatMessageAdmin(admin.ModelAdmin):
    """微信消息管理"""
    list_display = ['wechat_user', 'message_type', 'event_type', 'created_at']
    list_filter = ['message_type', 'event_type', 'created_at']
    search_fields = ['content', 'wechat_user__nickname']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
