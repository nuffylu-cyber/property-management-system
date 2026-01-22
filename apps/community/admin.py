"""
Community Admin Configuration
"""
from django.contrib import admin
from .models import Community, Building


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    """小区管理"""
    list_display = ['name', 'address', 'total_households', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'address']
    ordering = ['name']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """楼栋管理"""
    list_display = ['community', 'name', 'building_type', 'total_floors', 'total_units', 'created_at']
    list_filter = ['building_type', 'community', 'created_at']
    search_fields = ['name', 'community__name']
    ordering = ['community', 'name']
