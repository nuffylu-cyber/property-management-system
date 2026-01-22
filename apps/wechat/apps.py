"""
WeChat App Configuration
"""
from django.apps import AppConfig


class WeChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.wechat'
    verbose_name = '微信集成'
