"""
初始化系统权限数据
"""
from django.core.management.base import BaseCommand
from apps.core.models import Permission, RolePermission


class Command(BaseCommand):
    help = '初始化系统权限和角色权限配置'

    def handle(self, *args, **options):
        # 定义所有权限
        permissions_data = [
            # 小区管理模块
            {'code': 'community.view', 'name': '查看小区', 'module': '小区管理', 'description': '查看小区和楼宇信息'},
            {'code': 'community.create', 'name': '创建小区', 'module': '小区管理', 'description': '创建新小区'},
            {'code': 'community.edit', 'name': '编辑小区', 'module': '小区管理', 'description': '编辑小区信息'},
            {'code': 'community.delete', 'name': '删除小区', 'module': '小区管理', 'description': '删除小区'},
            {'code': 'community.export', 'name': '导出小区', 'module': '小区管理', 'description': '导出小区数据'},

            # 房产管理模块
            {'code': 'property.view', 'name': '查看房产', 'module': '房产管理', 'description': '查看房产信息'},
            {'code': 'property.create', 'name': '创建房产', 'module': '房产管理', 'description': '添加新房产'},
            {'code': 'property.edit', 'name': '编辑房产', 'module': '房产管理', 'description': '编辑房产信息'},
            {'code': 'property.delete', 'name': '删除房产', 'module': '房产管理', 'description': '删除房产'},
            {'code': 'property.export', 'name': '导出房产', 'module': '房产管理', 'description': '导出房产数据'},

            # 缴费管理模块
            {'code': 'payment.view', 'name': '查看缴费', 'module': '缴费管理', 'description': '查看缴费记录'},
            {'code': 'payment.create', 'name': '创建账单', 'module': '缴费管理', 'description': '创建缴费账单'},
            {'code': 'payment.edit', 'name': '编辑账单', 'module': '缴费管理', 'description': '编辑缴费账单'},
            {'code': 'payment.delete', 'name': '删除账单', 'module': '缴费管理', 'description': '删除缴费账单'},
            {'code': 'payment.export', 'name': '导出账单', 'module': '缴费管理', 'description': '导出缴费数据'},
            {'code': 'payment.confirm', 'name': '确认收款', 'module': '缴费管理', 'description': '确认收款'},
            {'code': 'payment.refund', 'name': '退款', 'module': '缴费管理', 'description': '处理退款'},

            # 报事管理模块
            {'code': 'maintenance.view', 'name': '查看报事', 'module': '报事管理', 'description': '查看报事记录'},
            {'code': 'maintenance.create', 'name': '创建报事', 'module': '报事管理', 'description': '创建新报事'},
            {'code': 'maintenance.edit', 'name': '编辑报事', 'module': '报事管理', 'description': '编辑报事信息'},
            {'code': 'maintenance.delete', 'name': '删除报事', 'module': '报事管理', 'description': '删除报事'},
            {'code': 'maintenance.export', 'name': '导出报事', 'module': '报事管理', 'description': '导出报事数据'},
            {'code': 'maintenance.assign', 'name': '派单', 'module': '报事管理', 'description': '分配报事任务'},
            {'code': 'maintenance.complete', 'name': '完成报事', 'module': '报事管理', 'description': '完成报事任务'},

            # 用户管理模块
            {'code': 'user.view', 'name': '查看用户', 'module': '用户管理', 'description': '查看用户信息'},
            {'code': 'user.create', 'name': '创建用户', 'module': '用户管理', 'description': '创建新用户'},
            {'code': 'user.edit', 'name': '编辑用户', 'module': '用户管理', 'description': '编辑用户信息'},
            {'code': 'user.delete', 'name': '删除用户', 'module': '用户管理', 'description': '删除用户'},
            {'code': 'user.export', 'name': '导出用户', 'module': '用户管理', 'description': '导出用户数据'},

            # 系统管理模块
            {'code': 'system.settings', 'name': '系统设置', 'module': '系统管理', 'description': '修改系统设置'},
            {'code': 'system.logs', 'name': '查看日志', 'module': '系统管理', 'description': '查看操作日志'},
            {'code': 'system.payment_config', 'name': '支付配置', 'module': '系统管理', 'description': '配置支付信息'},
            {'code': 'system.account_management', 'name': '账户管理', 'module': '系统管理', 'description': '管理系统账号'},
            {'code': 'system.permission_management', 'name': '权限管理', 'module': '系统管理', 'description': '配置角色权限'},

            # 报表模块
            {'code': 'report.view', 'name': '查看报表', 'module': '报表统计', 'description': '查看统计报表'},
            {'code': 'report.export', 'name': '导出报表', 'module': '报表统计', 'description': '导出统计报表'},
        ]

        # 创建权限
        created_count = 0
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults={
                    'name': perm_data['name'],
                    'module': perm_data['module'],
                    'description': perm_data['description'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建权限: {permission.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n共创建 {created_count} 个权限'))

        # 定义角色权限配置
        role_permissions_config = {
            'super_admin': {
                'description': '超级管理员 - 拥有所有权限',
                'all_permissions': True,
            },
            'admin': {
                'description': '管理员 - 小区、房产、报事、查看财务',
                'permissions': {
                    # 小区管理 - 全部权限
                    'community.view': True, 'community.create': True, 'community.edit': True,
                    'community.delete': True, 'community.export': True,
                    # 房产管理 - 全部权限
                    'property.view': True, 'property.create': True, 'property.edit': True,
                    'property.delete': True, 'property.export': True,
                    # 报事管理 - 全部权限
                    'maintenance.view': True, 'maintenance.create': True, 'maintenance.edit': True,
                    'maintenance.delete': True, 'maintenance.export': True,
                    'maintenance.assign': True, 'maintenance.complete': True,
                    # 缴费管理 - 仅查看
                    'payment.view': True, 'payment.export': True,
                    # 用户管理 - 仅查看
                    'user.view': True, 'user.export': True,
                    # 系统管理 - 查看日志
                    'system.logs': True,
                    # 报表
                    'report.view': True, 'report.export': True,
                }
            },
            'finance': {
                'description': '财务 - 缴费管理全部权限',
                'permissions': {
                    # 缴费管理 - 全部权限
                    'payment.view': True, 'payment.create': True, 'payment.edit': True,
                    'payment.delete': True, 'payment.export': True,
                    'payment.confirm': True, 'payment.refund': True,
                    # 房产管理 - 查看权限
                    'property.view': True, 'property.export': True,
                    # 用户管理 - 查看权限
                    'user.view': True, 'user.export': True,
                    # 报表
                    'report.view': True, 'report.export': True,
                }
            },
            'receptionist': {
                'description': '前台 - 基础操作权限',
                'permissions': {
                    # 小区管理 - 仅查看
                    'community.view': True,
                    # 房产管理 - 仅查看
                    'property.view': True,
                    # 报事管理 - 创建和查看
                    'maintenance.view': True, 'maintenance.create': True,
                    # 缴费管理 - 仅查看
                    'payment.view': True,
                    # 用户管理 - 仅查看
                    'user.view': True,
                }
            },
            'engineering': {
                'description': '工程部 - 报事处理权限',
                'permissions': {
                    # 报事管理 - 查看和完成
                    'maintenance.view': True, 'maintenance.edit': True,
                    'maintenance.complete': True,
                    # 小区管理 - 仅查看
                    'community.view': True,
                    # 房产管理 - 仅查看
                    'property.view': True,
                }
            },
            'owner': {
                'description': '业主 - 查看个人信息和报事',
                'permissions': {
                    # 查看自己的房产
                    'property.view': True,
                    # 报事管理 - 创建和查看自己的
                    'maintenance.view': True, 'maintenance.create': True,
                    # 缴费管理 - 查看自己的
                    'payment.view': True,
                }
            },
            'tenant': {
                'description': '租户 - 查看个人信息和报事',
                'permissions': {
                    # 查看自己的房产
                    'property.view': True,
                    # 报事管理 - 创建和查看自己的
                    'maintenance.view': True, 'maintenance.create': True,
                    # 缴费管理 - 查看自己的
                    'payment.view': True,
                }
            },
        }

        # 创建角色权限
        created_role_perm_count = 0
        for role, config in role_permissions_config.items():
            if config.get('all_permissions'):
                # 超级管理员拥有所有权限
                permissions = Permission.objects.all()
                for perm in permissions:
                    rp, created = RolePermission.objects.get_or_create(
                        role=role,
                        permission=perm,
                        defaults={
                            'can_view': True,
                            'can_create': True,
                            'can_edit': True,
                            'can_delete': True,
                            'can_export': True,
                        }
                    )
                    if created:
                        created_role_perm_count += 1
            else:
                # 其他角色按配置创建权限
                for perm_code, has_perm in config['permissions'].items():
                    try:
                        perm = Permission.objects.get(code=perm_code)
                        rp, created = RolePermission.objects.get_or_create(
                            role=role,
                            permission=perm,
                            defaults={
                                'can_view': has_perm,
                                'can_create': has_perm,
                                'can_edit': has_perm,
                                'can_delete': has_perm,
                                'can_export': has_perm,
                            }
                        )
                        if created:
                            created_role_perm_count += 1
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'警告: 权限 {perm_code} 不存在'))

        self.stdout.write(self.style.SUCCESS(f'共创建 {created_role_perm_count} 个角色权限配置'))
        self.stdout.write(self.style.SUCCESS('\n权限初始化完成！'))
