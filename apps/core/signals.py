"""
Core Signals
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    用户创建时的信号处理
    """
    if created:
        # 可以在这里添加用户创建后的额外处理逻辑
        pass
