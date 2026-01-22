"""
Maintenance App Configuration
"""
from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.maintenance'
    verbose_name = '报事管理'
