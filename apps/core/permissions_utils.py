"""
权限验证工具
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import RolePermission, Permission


def has_permission(user, permission_code, action='view'):
    """
    检查用户是否有指定权限

    Args:
        user: 用户实例
        permission_code: 权限代码
        action: 操作类型 (view, create, edit, delete, export)

    Returns:
        bool: 是否有权限
    """
    # 超级管理员拥有所有权限
    if user.is_superuser or user.role == 'super_admin':
        return True

    # 获取该角色的权限配置
    try:
        permission = Permission.objects.get(code=permission_code)
        role_permission = RolePermission.objects.get(
            role=user.role,
            permission=permission
        )

        # 根据操作类型检查权限
        action_map = {
            'view': role_permission.can_view,
            'create': role_permission.can_create,
            'edit': role_permission.can_edit,
            'delete': role_permission.can_delete,
            'export': role_permission.can_export,
        }

        return action_map.get(action, False)

    except (Permission.DoesNotExist, RolePermission.DoesNotExist):
        return False


def permission_required(permission_code, action='view'):
    """
    权限验证装饰器

    Usage:
        @permission_required('community.view', 'view')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not has_permission(request.user, permission_code, action):
                raise PermissionDenied("您没有执行此操作的权限")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def get_user_permissions(user):
    """
    获取用户的所有权限

    Returns:
        dict: 按模块分组的权限字典
    """
    if user.is_superuser or user.role == 'super_admin':
        # 超级管理员返回所有权限
        all_permissions = Permission.objects.all()
        result = {}
        for perm in all_permissions:
            if perm.module not in result:
                result[perm.module] = []
            result[perm.module].append({
                'code': perm.code,
                'name': perm.name,
                'can_view': True,
                'can_create': True,
                'can_edit': True,
                'can_delete': True,
                'can_export': True,
            })
        return result

    # 获取该角色的权限配置
    role_permissions = RolePermission.objects.select_related('permission').filter(
        role=user.role
    )

    result = {}
    for rp in role_permissions:
        module = rp.permission.module
        if module not in result:
            result[module] = []

        result[module].append({
            'code': rp.permission.code,
            'name': rp.permission.name,
            'can_view': rp.can_view,
            'can_create': rp.can_create,
            'can_edit': rp.can_edit,
            'can_delete': rp.can_delete,
            'can_export': rp.can_export,
        })

    return result


class PermissionMixin:
    """
    权限验证混入类（用于基于类的视图）
    """
    permission_code = None
    required_action = 'view'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())

        if self.permission_code and not has_permission(
            request.user, self.permission_code, self.required_action
        ):
            raise PermissionDenied("您没有执行此操作的权限")

        return super().dispatch(request, *args, **kwargs)
