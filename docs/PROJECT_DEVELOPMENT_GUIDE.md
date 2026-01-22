# 物业管理系统 - 项目开发文档

> **文档版本**: v1.0
> **最后更新**: 2026-01-12
> **开发状态**: 核心功能已完成，进入优化和扩展阶段
> **技术栈**: Django 4.2.7 + Django REST Framework + SQLite

---

## 📋 目录

1. [项目概述](#项目概述)
2. [开发历史记录](#开发历史记录)
3. [系统架构](#系统架构)
4. [数据模型](#数据模型)
5. [功能模块](#功能模块)
6. [API接口文档](#api接口文档)
7. [代码结构](#代码结构)
8. [权限系统](#权限系统)
9. [已知问题与优化建议](#已知问题与优化建议)
10. [下一步开发计划](#下一步开发计划)
11. [开发规范](#开发规范)

---

## 项目概述

### 系统简介
智慧物业管理系统是一个基于Django的综合性物业管理平台，支持小区管理、房产管理、缴费管理、报事管理、微信集成等功能。

### 核心特性
- ✅ 多角色权限管理（7种角色）
- ✅ 实时数据看板
- ✅ 微信支付配置（个人/企业）
- ✅ 完整的CRUD操作
- ✅ JWT认证
- ✅ RESTful API

### 技术栈
```
后端框架: Django 4.2.7
API框架: Django REST Framework
认证: JWT (Simple JWT)
数据库: SQLite (开发) / PostgreSQL (生产推荐)
前端模板: Django Templates + Vanilla JS
图标库: Remix Icon
字体: Google Fonts (IBM Plex Sans, Plus Jakarta Sans)
```

---

## 开发历史记录

### Phase 1: 基础架构搭建 ✅
**时间周期**: 2026-01-06 ~ 2026-01-08
**完成内容**:
- Django项目初始化
- 核心数据模型创建
- 用户认证系统（JWT）
- 基础API框架

### Phase 2: 核心功能开发 ✅
**时间周期**: 2026-01-08 ~ 2026-01-10
**完成内容**:
- 小区管理模块
- 房产管理模块
- 缴费管理模块
- 报事管理模块
- 用户管理模块

### Phase 3: 前端界面开发 ✅
**时间周期**: 2026-01-10 ~ 2026-01-11
**完成内容**:
- 响应式管理后台界面
- 数据概览仪表盘（实时数据）
- 各功能模块的CRUD页面
- 看板视图和统计分析
- 退出按钮修复

### Phase 4: 系统管理优化 ✅
**时间周期**: 2026-01-11 ~ 2026-01-12
**完成内容**:
- 支付管理模块（微信支付配置）
- 账户管理模块（权限系统）
- 完善REST API
- 实现权限验证逻辑
- 初始化系统权限数据（36个权限，92个角色权限配置）
- 创建超级管理员账号

---

## 系统架构

### 项目结构
```
物业管理系统/
├── apps/                          # 应用模块
│   ├── core/                      # 核心模块（用户、权限、配置）
│   │   ├── models.py              # 数据模型
│   │   ├── serializers.py         # 序列化器
│   │   ├── views.py               # 视图（包含API ViewSets和页面视图）
│   │   ├── urls.py                # API路由
│   │   ├── permissions.py         # 权限类
│   │   ├── permissions_utils.py   # 权限验证工具
│   │   └── management/commands/   # 管理命令
│   │       ├── init_permissions.py    # 初始化权限
│   │       └── create_superuser.py    # 创建超级管理员
│   ├── community/                 # 小区管理模块
│   ├── property/                  # 房产管理模块
│   ├── payment/                   # 缴费管理模块
│   ├── maintenance/               # 报事管理模块
│   └── wechat/                    # 微信集成模块
├── config/                        # 项目配置
│   ├── settings.py                # Django设置
│   ├── urls.py                    # 主路由配置
│   └── wsgi.py                    # WSGI配置
├── templates/                     # 模板文件
│   ├── admin/                     # 管理后台页面
│   │   ├── dashboard_full.html    # 数据概览
│   │   ├── community.html         # 小区管理
│   │   ├── property.html          # 房产管理
│   │   ├── payment.html           # 缴费管理
│   │   ├── maintenance.html       # 报事管理
│   │   ├── users.html             # 用户管理
│   │   ├── settings.html          # 系统设置
│   │   ├── logs.html              # 操作日志
│   │   ├── payment_config.html    # 支付管理
│   │   └── account_management.html # 账户管理
│   ├── components/                # 组件模板
│   │   ├── sidebar.html           # 侧边栏
│   │   └── header.html            # 顶部栏
│   └── registration/              # 认证模板
│       └── login.html             # 登录页面
├── static/                        # 静态文件
│   ├── css/                       # 样式文件
│   │   └── admin.css              # 管理后台样式
│   └── js/                        # JavaScript文件
│       └── admin.js               # 管理后台脚本
├── media/                         # 媒体文件
├── logs/                          # 日志文件
├── venv/                          # 虚拟环境
├── db.sqlite3                     # SQLite数据库
├── manage.py                      # Django管理脚本
├── OPTIMIZATION_SUMMARY.md        # 优化总结文档
└── PROJECT_DEVELOPMENT_GUIDE.md   # 本文档
```

### 架构设计原则
1. **模块化**: 每个功能模块独立，通过API通信
2. **RESTful API**: 前后端分离架构，支持多种客户端
3. **权限分层**: 超级管理员 > 管理员 > 职能角色 > 普通用户
4. **数据隔离**: 不同角色只能访问授权的数据

---

## 数据模型

### 核心模型关系图

```
User (用户)
  ├── role (角色)
  ├── is_active (激活状态)
  └── 关联到 PaymentBill (作为业主/租户)

Community (小区)
  ├── Building (楼宇) [1:N]
  └── Property (房产) [1:N]

Building (楼宇)
  ├── community (所属小区) [N:1]
  └── Property (房产) [1:N]

Property (房产)
  ├── community (所属小区) [N:1]
  ├── building (所属楼宇) [N:1]
  ├── owner (业主) [N:1]
  ├── tenant (租户) [N:1]
  └── PaymentBill (账单) [1:N]

PaymentBill (缴费账单)
  ├── property_unit (房产单元) [N:1]
  ├── owner (业主) [N:1]
  └── PaymentRecord (缴费记录) [1:N]

MaintenanceRequest (报事)
  ├── property (房产) [N:1]
  ├── community (小区) [N:1]
  └── status (状态: pending/assigned/processing/completed)

Permission (权限)
  └── RolePermission (角色权限) [1:N]

WeChatPayConfig (微信支付配置)
  ├── account_type (个人/企业)
  └── is_default (是否默认)

OperationLog (操作日志)
  └── operator (操作人) [N:1]
```

### 关键模型字段

#### User (用户模型)
```python
role: 选择字段
  - super_admin: 超级管理员
  - admin: 管理员
  - finance: 财务
  - receptionist: 前台
  - engineering: 工程部
  - owner: 业主
  - tenant: 租户
is_active: 布尔字段（是否激活）
phone: 联系电话
avatar: 头像URL
```

#### PaymentBill (缴费账单)
```python
billing_period: CharField (格式: "YYYY-MM")
amount: DecimalField (账单金额)
paid_amount: DecimalField (已缴金额)
status: CharField
  - unpaid: 未缴费
  - partial: 部分缴费
  - paid: 已缴费
due_date: DateField (到期日期)
```

#### MaintenanceRequest (报事)
```python
status: CharField
  - pending: 待派单
  - assigned: 已派单
  - processing: 处理中
  - completed: 已完成
priority: CharField
  - high: 高
  - medium: 中
  - low: 低
category: CharField
  - electric: 电力
  - plumbing: 水力
  - civil: 土建
  - elevator: 电梯
  - cleaning: 清洁
  - security: 安保
  - other: 其他
```

---

## 功能模块

### 1. 数据概览 (Dashboard)
**路由**: `/admin/`
**功能**:
- 实时统计卡片（总户数、本月收入、收缴率、待处理报事等）
- 小区收缴率排行榜
- 最近报事列表
- 逾期统计

**数据来源**: `apps/core/views.py:dashboard()`
**实时数据**: ✅ 已实现

### 2. 小区管理
**路由**: `/admin/community/`
**功能**:
- 小区CRUD
- 楼宇CRUD
- 实时数据展示

**API**: `/api/community/`

### 3. 房产管理
**路由**: `/admin/property/`
**功能**:
- 房产CRUD
- 业主管理
- 租户管理
- 关联关系管理

**API**: `/api/property/`

### 4. 缴费管理
**路由**: `/admin/payment/`
**功能**:
- 缴费账单管理
- 收款记录
- 费用标准配置
- 统计分析

**API**: `/api/payment/`

### 5. 报事管理
**路由**: `/admin/maintenance/`
**功能**:
- 报事列表
- 看板视图（4个状态列）
- 统计分析
- 实时数据展示

**API**: `/api/maintenance/`

### 6. 用户管理
**路由**: `/admin/users/`
**功能**:
- 用户列表
- 角色管理
- 统计数据

**API**: `/api/core/users/`

### 7. 支付管理
**路由**: `/admin/payment-config/`
**功能**:
- 微信支付配置管理
- 支持个人/企业账号
- 设为默认配置
- 敏感信息隐藏

**API**: `/api/core/payment-config/`

### 8. 账户管理
**路由**: `/admin/account-management/`
**功能**:
- 角色管理（7种角色）
- 权限配置
- 账号列表
- 批量权限更新

**API**:
- `/api/core/permissions/`
- `/api/core/role-permissions/`

### 9. 系统设置
**路由**: `/admin/settings/`
**功能**:
- 基本设置
- 微信配置
- 支付配置
- 通知设置

### 10. 操作日志
**路由**: `/admin/logs/`
**功能**:
- 操作记录查看
- 筛选和搜索
- 导出日志

---

## API接口文档

### 认证API

#### 登录获取Token
```
POST /api/auth/login/
Content-Type: application/json

Request:
{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 刷新Token
```
POST /api/auth/refresh/
Content-Type: application/json

Request:
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response:
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 核心API端点

| 模块 | 端点 | 方法 | 描述 |
|------|------|------|------|
| **用户管理** | `/api/core/users/` | GET/POST | 用户列表/创建 |
| | `/api/core/users/{id}/` | GET/PUT/PATCH/DELETE | 用户详情 |
| | `/api/core/users/me/` | GET | 当前用户信息 |
| | `/api/core/users/update_profile/` | PUT/PATCH | 更新个人信息 |
| **支付配置** | `/api/core/payment-config/` | GET/POST | 配置列表/创建 |
| | `/api/core/payment-config/{id}/` | GET/PUT/PATCH/DELETE | 配置详情 |
| | `/api/core/payment-config/{id}/set_default/` | POST | 设为默认 |
| **权限管理** | `/api/core/permissions/` | GET/POST | 权限列表/创建 |
| | `/api/core/role-permissions/` | GET/POST | 角色权限列表/创建 |
| | `/api/core/role-permissions/by_role/?role=xxx` | GET | 按角色查询 |
| | `/api/core/role-permissions/bulk_update/` | POST | 批量更新 |
| **操作日志** | `/api/core/logs/` | GET | 日志列表 |
| **系统配置** | `/api/core/configs/` | GET/POST/PUT | 系统配置 |
| **小区管理** | `/api/community/` | GET/POST | 小区列表/创建 |
| | `/api/community/buildings/` | GET/POST | 楼宇列表/创建 |
| **房产管理** | `/api/property/` | GET/POST | 房产列表/创建 |
| | `/api/property/owners/` | GET/POST | 业主列表/创建 |
| | `/api/property/tenants/` | GET/POST | 租户列表/创建 |
| **缴费管理** | `/api/payment/bills/` | GET/POST | 账单列表/创建 |
| | `/api/payment/records/` | GET/POST | 缴费记录列表/创建 |
| | `/api/payment/standards/` | GET/POST | 费用标准列表/创建 |
| **报事管理** | `/api/maintenance/requests/` | GET/POST | 报事列表/创建 |

### API认证

所有需要认证的API请求都需要在Header中携带Token：

```
Authorization: Bearer {access_token}
```

---

## 代码结构

### View层架构

#### API ViewSets (REST API)
```python
# 位置: apps/{module}/views.py
class ExampleViewSet(viewsets.ModelViewSet):
    """标准ViewSet结构"""
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """自定义查询集"""
        return super().get_queryset().select_related(...)

    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk=None):
        """自定义操作"""
        pass
```

#### 页面视图 (Template Views)
```python
# 位置: apps/core/views.py
@login_required
def page_view(request):
    """标准页面视图结构"""
    # 获取数据
    data = Model.objects.all()

    # 构建上下文
    context = {
        'data': data,
        'page_title': '页面标题',
    }
    context.update(get_common_context())

    # 渲染模板
    return render(request, 'admin/page.html', context)
```

### 前端JavaScript架构

#### CRUD模块标准结构
```javascript
// 位置: templates/admin/*.html 中的 <script> 标签

const ModuleCRUD = {
    // API端点配置
    api: {
        list: '/api/module/',
        create: '/api/module/',
        update: (id) => `/api/module/${id}/`,
        delete: (id) => `/api/module/${id}/`,
    },

    // 创建
    create() {
        // 打开模态框
        // 重置表单
    },

    // 编辑
    edit(id) {
        // 获取详情
        // 填充表单
        // 打开模态框
    },

    // 保存
    async save() {
        // 收集表单数据
        // 调用API
        // 处理响应
    },

    // 删除
    async delete(id) {
        // 确认对话框
        // 调用API
        // 刷新列表
    },

    // 关闭模态框
    closeModal() {
        // 关闭模态框
        // 清理状态
    }
};
```

### CSS架构

#### CSS变量定义
```css
/* 位置: static/css/admin.css */
:root {
    /* 颜色系统 */
    --primary-50: #eff6ff;
    --primary-500: #3b82f6;
    --primary-600: #2563eb;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #06b6d4;

    /* 灰度 */
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-500: #6b7280;
    --gray-900: #111827;

    /* 间距 */
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;

    /* 阴影 */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

---

## 权限系统

### 权限架构

#### 权限模型
```python
Permission (权限)
├── code: 唯一标识 (如 'community.view')
├── name: 显示名称 (如 '查看小区')
├── module: 所属模块 (如 '小区管理')
└── description: 描述

RolePermission (角色权限关联)
├── role: 角色 (如 'admin')
├── permission: 权限 [外键]
├── can_view: 可查看
├── can_create: 可创建
├── can_edit: 可编辑
├── can_delete: 可删除
└── can_export: 可导出
```

### 权限验证

#### 使用装饰器
```python
from apps.core.permissions_utils import permission_required

@permission_required('community.view', 'view')
def community_list(request):
    """只有有查看小区权限的用户才能访问"""
    pass
```

#### 代码中检查权限
```python
from apps.core.permissions_utils import has_permission

if has_permission(request.user, 'community.create', 'create'):
    # 用户有创建小区的权限
    pass
```

#### 获取用户权限
```python
from apps.core.permissions_utils import get_user_permissions

permissions = get_user_permissions(request.user)
# 返回: {
#     '小区管理': [
#         {'code': 'community.view', 'name': '查看小区', ...},
#         ...
#     ],
#     ...
# }
```

### 权限初始化

**初始化命令**:
```bash
python manage.py init_permissions
```

**初始化数据**:
- 36个权限（7大模块）
- 92个角色权限配置（7种角色）

### 角色权限预设

| 角色 | 小区管理 | 房产管理 | 缴费管理 | 报事管理 | 系统管理 |
|------|---------|---------|---------|---------|---------|
| 超级管理员 | 全部 | 全部 | 全部 | 全部 | 全部 |
| 管理员 | 全部 | 全部 | 查看 | 全部 | 日志 |
| 财务 | - | 查看 | 全部 | - | - |
| 前台 | 查看 | 查看 | 查看 | 查看/创建 | - |
| 工程部 | 查看 | 查看 | - | 查看/编辑/完成 | - |
| 业主 | - | 自己 | 自己 | 查看/创建 | - |
| 租户 | - | 自己 | 自己 | 查看/创建 | - |

---

## 已知问题与优化建议

### 已知问题

1. **日志文件轮转问题**
   - 问题: 日志文件过大时无法自动轮转
   - 位置: `logs/django.log`
   - 影响: 可能导致日志文件过大
   - 解决方案: 配置日志轮转策略

2. **前端JS代码分散**
   - 问题: JavaScript代码散布在各个HTML模板中
   - 影响: 代码复用性差，难以维护
   - 优化方案: 提取公共JS模块

3. **敏感信息显示**
   - 问题: 支付配置的敏感信息只在序列化时隐藏
   - 影响: 可能在日志中泄露
   - 优化方案: 在整个请求生命周期中保护敏感信息

### 代码优化建议

#### 1. 数据库查询优化
**当前状态**: 大部分查询已使用 `select_related()`
**建议**:
- 使用 `prefetch_related()` 处理多对多关系
- 添加数据库索引
- 使用 `only()` 和 `defer()` 限制查询字段

```python
# 优化前
properties = Property.objects.all()

# 优化后
properties = Property.objects.select_related(
    'community', 'building', 'owner', 'tenant'
).only('id', 'room_number', 'community__name', 'building__name')
```

#### 2. 缓存优化
**建议**:
- 为统计数据添加缓存（Redis）
- 缓存权限配置
- 缓存系统配置

```python
from django.core.cache import cache

def get_permissions_cache(role):
    cache_key = f'permissions:{role}'
    permissions = cache.get(cache_key)
    if permissions is None:
        permissions = get_user_permissions_by_role(role)
        cache.set(cache_key, permissions, 3600)  # 1小时
    return permissions
```

#### 3. API性能优化
**建议**:
- 实现分页（使用 `PageNumberPagination`）
- 添加请求限流（使用 `django-rest-framework-throttle`）
- 实现数据压缩（gzip）

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

#### 4. 前端优化
**建议**:
- 提取公共JavaScript模块
- 实现前端组件化
- 添加前端状态管理
- 实现前端路由

#### 5. 安全加固
**建议**:
- 实现CSRF保护（已启用）
- 添加CORS配置
- 实现请求签名验证
- 添加SQL注入防护（Django ORM已提供）
- 实现XSS防护（Django模板已提供）

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 6. 错误处理优化
**建议**:
- 实现全局异常处理中间件
- 统一API错误响应格式
- 添加详细的错误日志

```python
# apps/core/middleware.py
class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # 统一异常处理
        pass
```

#### 7. 测试覆盖
**当前状态**: 无自动化测试
**建议**:
- 添加单元测试（pytest + django-test-plus）
- 添加集成测试
- 实现API测试
- 添加前端测试（Cypress）

---

## 下一步开发计划

### Phase 5: 功能完善 (优先级: 高)

#### 5.1 微信集成
**预估时间**: 2-3周
**功能点**:
- [ ] 微信公众号接入
- [ ] 微信支付集成（调用支付API）
- [ ] 微信模板消息通知
- [ ] 微信用户绑定
- [ ] 微信端H5页面

**技术要点**:
```python
# 接入微信SDK
from wechatpy import WeChatClient

app_id = settings.WECHAT_APP_ID
app_secret = settings.WECHAT_APP_SECRET
client = WeChatClient(app_id, app_secret)

# 发送模板消息
client.message.send_template(...)
```

#### 5.2 报表系统
**预估时间**: 1-2周
**功能点**:
- [ ] 财务报表（月度/季度/年度）
- [ ] 收缴率统计报表
- [ ] 报事统计报表
- [ ] 自定义报表生成
- [ ] 报表导出（Excel/PDF）

**实现方式**:
```python
# 使用 pandas + openpyxl 生成Excel报表
import pandas as pd

def generate_report(start_date, end_date):
    data = PaymentRecord.objects.filter(
        payment_time__range=(start_date, end_date)
    ).values('date', 'amount')

    df = pd.DataFrame(data)
    df.to_excel('report.xlsx')
```

#### 5.3 消息通知系统
**预估时间**: 1周
**功能点**:
- [ ] 站内消息
- [ ] 短信通知（阿里云SMS）
- [ ] 邮件通知
- [ ] 微信模板消息
- [ ] 通知模板管理

### Phase 6: 性能优化 (优先级: 中)

#### 6.1 缓存层
**预估时间**: 1周
**功能点**:
- [ ] Redis缓存配置
- [ ] 查询结果缓存
- [ ] 权限缓存
- [ ] 统计数据缓存

#### 6.2 数据库优化
**预估时间**: 1周
**功能点**:
- [ ] 添加索引
- [ ] 查询优化
- [ ] 数据库分区（如果数据量大）
- [ ] 读写分离（主从复制）

#### 6.3 前端优化
**预估时间**: 1-2周
**功能点**:
- [ ] 提取公共JS模块
- [ ] 实现组件化
- [ ] 添加懒加载
- [ ] CDN静态资源
- [ ] 前端打包工具（Webpack/Vite）

### Phase 7: 高级功能 (优先级: 低)

#### 7.1 数据分析
**预估时间**: 2-3周
**功能点**:
- [ ] 数据可视化（ECharts/D3.js）
- [ ] 趋势分析
- [ ] 预测分析（机器学习）
- [ ] 异常检测

#### 7.2 移动端应用
**预估时间**: 4-6周
**功能点**:
- [ ] 移动端API优化
- [ ] 响应式设计改进
- [ ] PWA支持
- [ ] 原生App（React Native/Flutter）

#### 7.3 多租户支持
**预估时间**: 2-3周
**功能点**:
- [ ] 多物业公司支持
- [ ] 数据隔离
- [ ] 租户配置
- [ ] 租户管理后台

---

## 开发规范

### 代码风格

#### Python代码规范
- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 isort 进行import排序
- 添加类型注解（Type Hints）
- 编写文档字符串（Docstrings）

```python
# 示例
from typing import List
from django.db.models import QuerySet

def get_active_properties(community_id: str) -> QuerySet:
    """
    获取指定社区的活跃房产列表

    Args:
        community_id: 社区ID

    Returns:
        房产查询集
    """
    return Property.objects.filter(
        community_id=community_id,
        is_active=True
    )
```

#### JavaScript代码规范
- 使用 ES6+ 语法
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 变量命名使用 camelCase
- 常量命名使用 UPPER_CASE

```javascript
// 示例
const API_BASE_URL = '/api/core/';

class PaymentManager {
    async getPaymentList(filters = {}) {
        const response = await fetch(`${API_BASE_URL}payment/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filters)
        });
        return response.json();
    }
}
```

#### CSS代码规范
- 使用 BEM 命名规范
- 使用 CSS 变量
- 避免深层嵌套（不超过3层）
- 使用 flexbox 和 grid 布局

```css
/* 示例 */
.stat-card {
    padding: 16px;
    border-radius: var(--radius-lg);
}

.stat-card__value {
    font-size: 24px;
    font-weight: 700;
}

.stat-card__label {
    font-size: 14px;
    color: var(--gray-500);
}
```

### Git提交规范

#### Commit Message格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

#### 示例
```
feat(payment): 添加批量缴费功能

- 实现批量选择账单
- 添加统一支付接口
- 优化支付流程

Closes #123
```

### 文档规范

#### 函数文档字符串
```python
def calculate_collection_rate(start_date: date, end_date: date) -> Dict[str, float]:
    """
    计算指定时间段的收缴率

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        包含收缴率相关数据的字典：
        {
            'total_bills': 总账单数,
            'paid_bills': 已缴费账单数,
            'collection_rate': 收缴率(百分比),
            'total_amount': 总金额,
            'paid_amount': 已缴金额
        }

    Raises:
        ValueError: 当开始日期大于结束日期时

    Example:
        >>> calculate_collection_rate(
        ...     date(2026, 1, 1),
        ...     date(2026, 1, 31)
        ... )
        {'total_bills': 100, 'collection_rate': 85.5, ...}
    """
```

### API文档规范

使用 drf-yasg (Swagger) 自动生成API文档

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    operation_description="获取缴费账单列表",
    responses={
        200: PaymentBillSerializer(many=True),
        401: "未认证",
        403: "无权限"
    },
    manual_parameters=[
        openapi.Parameter(
            'status',
            openapi.IN_QUERY,
            description="账单状态",
            type=openapi.TYPE_STRING,
            enum=['unpaid', 'partial', 'paid']
        )
    ]
)
def list(self, request, *args, **kwargs):
    pass
```

---

## 快速开始

### 环境准备

```bash
# 1. 克隆项目
cd /path/to/物业管理系统

# 2. 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 应用数据库迁移
python manage.py migrate

# 5. 初始化权限数据
python manage.py init_permissions

# 6. 创建超级管理员
python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver
```

### 默认账号

```
用户名: admin
密码: admin123
角色: 超级管理员
```

### 访问地址

- 管理后台: http://127.0.0.1:8000/admin/
- API文档(Swagger): http://127.0.0.1:8000/swagger/
- API文档(ReDoc): http://127.0.0.1:8000/redoc/

---

## 常见问题

### Q: 如何添加新的权限？
A:
1. 在 `apps/core/management/commands/init_permissions.py` 中添加权限定义
2. 运行 `python manage.py init_permissions` 初始化

### Q: 如何修改数据库模型？
A:
1. 修改 `models.py`
2. 运行 `python manage.py makemigrations`
3. 运行 `python manage.py migrate`

### Q: 如何添加新的API端点？
A:
1. 在 `views.py` 中添加ViewSet或视图函数
2. 在 `urls.py` 中注册路由
3. 添加序列化器（如果是ViewSet）
4. 配置权限类

### Q: 如何自定义前端页面？
A:
1. 在 `templates/admin/` 中创建HTML模板
2. 在 `views.py` 中添加视图函数
3. 在 `urls.py` 中注册路由
4. 添加CSS样式和JavaScript交互

---

## 联系信息

**项目维护者**: Claude Code AI Assistant
**技术支持**: 查看项目文档或联系开发团队
**问题反馈**: GitHub Issues（如有）

---

## 版本历史

- **v1.0** (2026-01-12): 核心功能完成，权限系统实现，系统优化完成

---

**祝您开发愉快！** 🚀
