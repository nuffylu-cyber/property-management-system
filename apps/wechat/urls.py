"""
WeChat URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeChatUserViewSet, wechat_verify, wechat_oauth_url, wechat_callback, wechat_bind, wechat_jsapi_config

router = DefaultRouter()
router.register(r'users', WeChatUserViewSet, basename='wechatuser')

urlpatterns = [
    # 微信服务器验证和消息处理
    path('verify/', wechat_verify, name='wechat-verify'),

    # 微信授权
    path('oauth/url/', wechat_oauth_url, name='wechat-oauth-url'),
    path('callback/', wechat_callback, name='wechat-callback'),
    path('bind/', wechat_bind, name='wechat-bind'),

    # JS-SDK 配置
    path('jsapi/config/', wechat_jsapi_config, name='wechat-jsapi-config'),

    # Router URLs
    path('', include(router.urls)),
]
