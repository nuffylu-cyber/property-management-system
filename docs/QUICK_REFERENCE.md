# 物业管理系统 - 快速参考指南

> **供Claude Code使用的项目快速参考文档**

---

## 🎯 项目当前状态

- ✅ **核心功能**: 完成
- ✅ **权限系统**: 完成（36个权限，92个角色配置）
- ✅ **支付配置**: 完成（微信支付个人/企业账号）
- ✅ **实时数据**: 完成（Dashboard和所有模块）
- 🚧 **微信集成**: 待开发
- 🚧 **报表系统**: 待开发

---

## 📂 关键文件位置

```
配置文件
├── config/settings.py          # Django配置
├── config/urls.py              # 主路由

核心模块
├── apps/core/models.py         # 用户、权限、支付配置模型
├── apps/core/views.py          # 视图（API + 页面）
├── apps/core/serializers.py    # 序列化器
├── apps/core/urls.py           # API路由
├── apps/core/permissions_utils.py  # 权限验证工具

管理命令
├── apps/core/management/commands/init_permissions.py
└── apps/core/management/commands/create_superuser.py

模板
├── templates/admin/*.html      # 管理后台页面
├── templates/components/       # 公共组件
└── templates/registration/     # 认证页面

静态资源
├── static/css/admin.css        # 管理后台样式
└── static/js/admin.js          # 管理后台脚本
```

---

## 🗄️ 数据库模型速查

### 用户相关
```python
# User (apps/core/models.py)
role选项: super_admin, admin, finance, receptionist, engineering, owner, tenant
字段: username, email, phone, role, is_active
```

### 权限相关
```python
# Permission
code: 唯一标识 (如 'community.view')
name: 显示名称
module: 所属模块

# RolePermission
role: 角色
permission: 权限 [外键]
can_view, can_create, can_edit, can_delete, can_export
```

### 支付配置
```python
# WeChatPayConfig
account_type: personal / enterprise
app_id, app_secret, mch_id, api_key, api_v3_key
is_active, is_default
```

---

## 🔌 API端点速查

### 认证
```
POST /api/auth/login/          # 登录获取Token
POST /api/auth/refresh/        # 刷新Token
```

### 核心API
```
GET/POST    /api/core/users/              # 用户管理
GET/POST    /api/core/payment-config/     # 支付配置
GET/POST    /api/core/permissions/        # 权限管理
GET/POST    /api/core/role-permissions/   # 角色权限
GET         /api/core/role-permissions/by_role/?role=xxx  # 按角色查询
POST        /api/core/payment-config/{id}/set_default/    # 设为默认
POST        /api/core/role-permissions/bulk_update/       # 批量更新
```

### 业务API
```
GET/POST    /api/community/          # 小区
GET/POST    /api/community/buildings/ # 楼宇
GET/POST    /api/property/           # 房产
GET/POST    /api/property/owners/    # 业主
GET/POST    /api/property/tenants/   # 租户
GET/POST    /api/payment/bills/      # 账单
GET/POST    /api/payment/records/    # 缴费记录
GET/POST    /api/maintenance/requests/ # 报事
```

---

## 🎨 前端组件速查

### 页面路由
```
/                      # 首页
/login/                # 登录页
/admin/                # Dashboard（数据概览）
/admin/community/      # 小区管理
/admin/property/       # 房产管理
/admin/payment/        # 缴费管理
/admin/maintenance/    # 报事管理
/admin/users/          # 用户管理
/admin/payment-config/ # 支付管理
/admin/account-management/ # 账户管理
/admin/settings/       # 系统设置
/admin/logs/           # 操作日志
```

### 侧边栏菜单结构
```html
<!-- templates/components/sidebar.html -->
主菜单
├── 数据概览
├── 小区管理
└── 房产管理

业务管理
├── 缴费管理
├── 报事管理
└── 微信管理

系统管理
├── 用户管理
├── 支付管理        # 新增
├── 账户管理        # 新增
├── 系统设置
└── 操作日志
```

---

## 🔧 常用命令

### Django管理
```bash
python manage.py runserver                    # 启动服务器
python manage.py migrate                      # 应用迁移
python manage.py makemigrations               # 创建迁移
python manage.py createsuperuser              # 创建超级管理员
python manage.py shell                        # 进入Django Shell
```

### 自定义管理命令
```bash
python manage.py init_permissions             # 初始化权限数据
python manage.py create_superuser             # 创建超级管理员
```

### 数据库操作
```bash
python manage.py dbshell                      # 进入数据库Shell
python manage.py showmigrations               # 显示迁移状态
python manage.py sqlmigrate app_name 0001     # 显示SQL
```

---

## 📝 开发模板

### 添加新模型
```python
# apps/{module}/models.py
from django.db import models
import uuid

class NewModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'module_newmodel'
        verbose_name = '新模型'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

### 添加API ViewSet
```python
# apps/{module}/views.py
from rest_framework import viewsets
from .models import NewModel
from .serializers import NewModelSerializer
from .permissions import IsAdminUser

class NewModelViewSet(viewsets.ModelViewSet):
    """新模型视图集"""
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
```

### 添加页面视图
```python
# apps/core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def new_page(request):
    """新页面视图"""
    from apps.core.models import NewModel
    from .models import get_common_context

    items = NewModel.objects.all()

    context = {
        'items': items,
        'page_title': '新页面',
    }
    context.update(get_common_context())
    return render(request, 'admin/new_page.html', context)
```

### 添加权限验证
```python
from apps.core.permissions_utils import permission_required

@permission_required('module.view', 'view')
def view_with_permission(request):
    """需要权限的视图"""
    pass
```

---

## 🎯 下一步开发重点

### 优先级1: 微信集成
- [ ] 接入微信公众号SDK
- [ ] 实现微信支付功能
- [ ] 发送模板消息通知
- [ ] 微信用户绑定

### 优先级2: 报表系统
- [ ] 财务报表生成
- [ ] 数据统计图表
- [ ] 报表导出（Excel/PDF）
- [ ] 自定义报表

### 优先级3: 性能优化
- [ ] 添加Redis缓存
- [ ] 实现API分页
- [ ] 添加数据库索引
- [ ] 前端资源优化

### 优先级4: 测试
- [ ] 单元测试
- [ ] API集成测试
- [ ] 前端E2E测试

---

## ⚠️ 重要注意事项

### 数据库迁移
- 修改模型后必须运行 `makemigrations` 和 `migrate`
- 删除字段时要小心，会丢失数据
- 建议先在测试环境验证迁移

### 权限系统
- 新增权限后运行 `python manage.py init_permissions`
- 权限代码格式: `{module}.{action}` (如 `community.view`)
- 超级管理员自动拥有所有权限

### API开发
- 所有API需要JWT认证（除了登录接口）
- 使用 `@permission_required` 装饰器验证权限
- API响应统一使用JSON格式

### 前端开发
- 遵循现有的组件结构
- 使用 Remix Icon 图标库
- CSS变量定义在 `static/css/admin.css`
- 公共JS函数可以在多个页面复用

---

## 🐛 已知问题

1. **日志文件轮转**: 需要配置日志轮转策略
2. **前端JS分散**: 建议提取公共模块
3. **敏感信息保护**: 增强支付配置的安全性

---

## 📚 相关文档

- `PROJECT_DEVELOPMENT_GUIDE.md` - 完整开发文档
- `OPTIMIZATION_SUMMARY.md` - 优化总结文档
- `/swagger/` - API交互文档（运行服务器后访问）

---

## 🚀 快速开始新功能开发

### 1. 添加新的业务模块
```bash
# 1. 创建应用
python manage.py startapp new_module

# 2. 添加到 INSTALLED_APPS (config/settings.py)

# 3. 创建模型
# 编辑 apps/new_module/models.py

# 4. 创建迁移
python manage.py makemigrations new_module
python manage.py migrate

# 5. 创建序列化器
# 编辑 apps/new_module/serializers.py

# 6. 创建视图
# 编辑 apps/new_module/views.py

# 7. 配置URL
# 编辑 apps/new_module/urls.py
# 编辑 config/urls.py 添加include

# 8. 创建模板
# 创建 templates/admin/new_module.html

# 9. 在侧边栏添加菜单
# 编辑 templates/components/sidebar.html
```

### 2. 添加新的权限
```bash
# 1. 编辑 apps/core/management/commands/init_permissions.py
# 在 permissions_data 中添加新权限

# 2. 运行初始化命令
python manage.py init_permissions
```

### 3. 添加新的API端点
```python
# 1. 在 ViewSet 中添加方法或创建新 ViewSet

# 2. 在 urls.py 中注册路由

# 3. 添加序列化器（如果需要）

# 4. 配置权限

# 5. 访问 /swagger/ 查看API文档
```

---

**提示**: 阅读完整的 `PROJECT_DEVELOPMENT_GUIDE.md` 了解更多详细信息！
