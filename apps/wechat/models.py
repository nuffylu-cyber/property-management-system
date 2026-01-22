"""
WeChat Models - 微信集成
"""
import uuid
from django.db import models


class WeChatUser(models.Model):
    """
    微信用户模型
    存储微信公众号的用户信息
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    openid = models.CharField(max_length=100, unique=True, verbose_name='OpenID')
    unionid = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='UnionID')
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='昵称')
    avatar_url = models.URLField(blank=True, null=True, verbose_name='头像URL')
    sex = models.IntegerField(blank=True, null=True, verbose_name='性别(0未知 1男 2女)')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='城市')
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name='省份')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='国家')
    language = models.CharField(max_length=20, default='zh_CN', verbose_name='语言')
    subscribe_time = models.DateTimeField(blank=True, null=True, verbose_name='关注时间')
    is_subscribed = models.BooleanField(default=True, verbose_name='是否关注')
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='wechat_profile', verbose_name='关联系统用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'wechat_user'
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nickname or self.openid}"


class WeChatMessage(models.Model):
    """
    微信消息记录
    记录微信公众号的交互消息
    """
    MESSAGE_TYPE_CHOICES = [
        ('text', '文本消息'),
        ('image', '图片消息'),
        ('voice', '语音消息'),
        ('video', '视频消息'),
        ('event', '事件消息'),
        ('location', '位置消息'),
        ('link', '链接消息'),
    ]

    EVENT_TYPE_CHOICES = [
        ('subscribe', '关注事件'),
        ('unsubscribe', '取消关注'),
        ('scan', '扫描带参数二维码'),
        ('location', '上报地理位置'),
        ('click', '点击菜单拉取消息'),
        ('view', '点击菜单跳转链接'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wechat_user = models.ForeignKey(WeChatUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='messages', verbose_name='微信用户')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, verbose_name='消息类型')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, blank=True, null=True, verbose_name='事件类型')
    content = models.TextField(blank=True, null=True, verbose_name='消息内容')
    media_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='媒体ID')
    recognition = models.TextField(blank=True, null=True, verbose_name='语音识别结果')
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True, verbose_name='经度')
    label = models.CharField(max_length=200, blank=True, null=True, verbose_name='位置信息')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='消息标题')
    url = models.URLField(blank=True, null=True, verbose_name='链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'wechat_message'
        verbose_name = '微信消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_message_type_display()} - {self.created_at}"
