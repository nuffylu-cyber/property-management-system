"""
Property Admin Configuration
"""
from django.contrib import admin
from .models import Property, Owner, Tenant


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """房产管理"""
    list_display = ['full_address', 'community', 'building', 'area', 'property_type', 'status']
    list_filter = ['community', 'building', 'property_type', 'status', 'created_at']
    search_fields = ['room_number', 'unit']
    ordering = ['community', 'building', 'floor', 'room_number']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    """业主管理"""
    list_display = ['name', 'phone', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['name', 'phone', 'id_card']
    readonly_fields = ['wechat_openid', 'wechat_nickname', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """租户管理"""
    list_display = ['name', 'property', 'lease_start', 'lease_end', 'is_active', 'created_at']
    list_filter = ['is_active', 'lease_start', 'lease_end', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['wechat_openid', 'wechat_nickname', 'created_at', 'updated_at']
    ordering = ['-created_at']
