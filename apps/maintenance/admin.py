"""
Maintenance Admin Configuration
"""
from django.contrib import admin
from .models import MaintenanceRequest, MaintenanceLog


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    """报事记录管理"""
    list_display = ['request_number', 'community', 'property', 'category', 'status', 'priority', 'reporter', 'created_at']
    list_filter = ['community', 'category', 'status', 'priority', 'created_at']
    search_fields = ['request_number', 'reporter', 'description']
    readonly_fields = ['request_number', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    """报事处理日志管理"""
    list_display = ['request', 'operator', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['operator', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
