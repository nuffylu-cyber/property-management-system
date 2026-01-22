# 项目配置清单

> **项目启动前的检查清单**

---

## ✅ 环境配置

### Python环境
- [x] Python 3.12+
- [x] 虚拟环境已创建 (`venv/`)
- [x] 依赖包已安装

### 依赖包清单
```
# requirements.txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.5
drf-yasg==1.21.7
djangorestframework-simplejwt==5.3.1
Pillow==10.1.0
python-dotenv==1.0.0
```

### 数据库
- [x] SQLite已配置（开发环境）
- [ ] PostgreSQL已配置（生产环境，需配置）
- [x] 数据库迁移已应用
- [x] 初始数据已导入

---

## ✅ 系统配置

### Django设置 (config/settings.py)

#### 必须配置的设置
```python
# 已配置项
SECRET_KEY = '...'                    # 密钥
DEBUG = True                          # 调试模式（生产改为False）
ALLOWED_HOSTS = ['*']                 # 允许的主机（生产需修改）

INSTALLED_APPS = [...]                # 已安装应用
MIDDLEWARE = [...]                    # 中间件
ROOT_URLCONF = 'config.urls'          # URL配置
TEMPLATES = [...]                     # 模板配置
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {...}                     # 数据库配置

AUTH_PASSWORD_VALIDATORS = [...]      # 密码验证器

LANGUAGE_CODE = 'zh-hans'             # 语言
TIME_ZONE = 'Asia/Shanghai'           # 时区
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'                # 静态文件
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    ...
}

# Celery配置（已添加但未完全配置）
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

### 生产环境待配置
```python
# 需要添加的配置
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 静态文件服务（白名单）
INTERNAL_IPS = ['127.0.0.1']

# 缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Celery（生产环境）
CELERY_BROKER_URL = 'redis://:password@localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://:password@localhost:6379/0'

# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## ✅ 数据库配置

### 当前状态
```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 生产环境配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'property_management',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

---

## ✅ 权限配置

### 初始化状态
- [x] 权限表已创建（36个权限）
- [x] 角色权限表已创建（92个配置）
- [x] 管理命令已添加

### 用户角色
```
super_admin - 超级管理员
admin       - 管理员
finance     - 财务
receptionist - 前台
engineering - 工程部
owner       - 业主
tenant      - 租户
```

### 默认管理员
```
用户名: admin
密码: admin123
角色: super_admin
```

---

## ✅ API配置

### 认证方式
- [x] JWT (Simple JWT)
- [x] Token刷新机制
- [x] Token过期时间（访问2小时，刷新7天）

### API文档
- [x] Swagger UI (`/swagger/`)
- [x] ReDoc (`/redoc/`)
- [x] 自动生成

---

## ✅ 前端配置

### 静态资源
```
static/
├── css/
│   └── admin.css           # 管理后台样式
├── js/
│   └── admin.js            # 管理后台脚本
└── images/                 # 图片资源
```

### 模板结构
```
templates/
├── admin/                  # 管理后台页面
│   ├── dashboard_full.html
│   ├── community.html
│   ├── property.html
│   ├── payment.html
│   ├── maintenance.html
│   ├── users.html
│   ├── settings.html
│   ├── logs.html
│   ├── payment_config.html
│   └── account_management.html
├── components/             # 公共组件
│   ├── sidebar.html
│   └── header.html
└── registration/           # 认证模板
    └── login.html
```

### 外部资源
```html
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

<!-- Remix Icon -->
<link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
```

---

## ✅ URL配置

### 主路由 (config/urls.py)
```python
urlpatterns = [
    # 首页
    path('', index, name='index'),

    # 认证
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 管理后台
    path('admin/', dashboard, name='dashboard'),
    path('admin/community/', community_list, name='community'),
    path('admin/property/', property_list, name='property'),
    path('admin/payment/', payment_list, name='payment'),
    path('admin/maintenance/', maintenance_list, name='maintenance'),
    path('admin/users/', user_list, name='users'),
    path('admin/payment-config/', payment_config_list, name='payment_config'),
    path('admin/account-management/', account_management_list, name='account_management'),
    path('admin/settings/', settings_list, name='settings'),
    path('admin/logs/', log_list, name='logs'),

    # 表单路由
    ...

    # API
    path('api/auth/', include('apps.core.urls')),
    path('api/community/', include('apps.community.urls')),
    path('api/property/', include('apps.property.urls')),
    path('api/payment/', include('apps.payment.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
    path('api/wechat/', include('apps.wechat.urls')),

    # API文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

---

## ✅ 功能模块状态

### 核心模块
| 模块 | 状态 | 说明 |
|------|------|------|
| 用户认证 | ✅ 完成 | JWT认证 |
| 用户管理 | ✅ 完成 | CRUD + 角色管理 |
| 权限系统 | ✅ 完成 | 36个权限，92个配置 |
| 小区管理 | ✅ 完成 | 小区 + 楼宇 |
| 房产管理 | ✅ 完成 | 房产 + 业主 + 租户 |
| 缴费管理 | ✅ 完成 | 账单 + 记录 + 标准 |
| 报事管理 | ✅ 完成 | 报事 + 看板 + 统计 |
| 支付配置 | ✅ 完成 | 微信支付配置 |
| 系统设置 | ✅ 完成 | 基本设置 |
| 操作日志 | ✅ 完成 | 日志记录 |

### 待开发模块
| 模块 | 状态 | 优先级 |
|------|------|--------|
| 微信集成 | 🚧 待开发 | 高 |
| 报表系统 | 🚧 待开发 | 高 |
| 消息通知 | 🚧 待开发 | 中 |
| 数据分析 | 🚧 待开发 | 低 |
| 移动端 | 🚧 待开发 | 低 |

---

## ✅ 性能优化

### 已实现
- [x] 数据库查询优化（select_related）
- [x] 实时数据统计
- [x] 敏感信息隐藏

### 待实现
- [ ] Redis缓存
- [ ] API分页（已配置但未完全实现）
- [ ] 数据库索引
- [ ] CDN静态资源
- [ ] 前端资源压缩

---

## ✅ 安全配置

### 已实现
- [x] CSRF保护
- [x] XSS防护（Django模板）
- [x] SQL注入防护（Django ORM）
- [x] JWT认证
- [x] 密码哈希存储

### 待实现
- [ ] HTTPS强制
- [ ] Cookie安全标志
- [ ] 请求签名验证
- [ ] API限流
- [ ] 输入验证增强

---

## 📋 部署前检查清单

### 代码质量
- [ ] 代码格式化（Black）
- [ ] 代码检查（flake8/pylint）
- [ ] 类型检查（mypy）
- [ ] 测试覆盖率 > 80%

### 性能测试
- [ ] API响应时间测试
- [ ] 数据库查询分析
- [ ] 压力测试
- [ ] 内存泄漏检查

### 安全测试
- [ ] SQL注入测试
- [ ] XSS测试
- [ ] CSRF测试
- [ ] 权限测试
- [ ] 敏感数据泄露测试

### 文档
- [x] API文档（Swagger）
- [x] 项目文档（PROJECT_DEVELOPMENT_GUIDE.md）
- [x] 快速参考（QUICK_REFERENCE.md）
- [ ] 部署文档
- [ ] 用户手册

---

## 🚀 部署环境配置

### 服务器要求
```
操作系统: Linux (Ubuntu 20.04+ 推荐)
Python: 3.12+
数据库: PostgreSQL 13+
缓存: Redis 6+
Web服务器: Nginx
WSGI服务器: Gunicorn
进程管理: Supervisor
```

### 环境变量 (.env)
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=property_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# WeChat
WECHAT_APP_ID=your-wechat-appid
WECHAT_APP_SECRET=your-wechat-secret
WECHAT_MCH_ID=your-mch-id
WECHAT_API_KEY=your-api-key
```

---

## 📞 支持与维护

### 日志位置
```
logs/
├── django.log              # Django日志
└── celery.log              # Celery日志（待配置）
```

### 备份策略
- [ ] 数据库每日备份
- [ ] 媒体文件定期备份
- [ ] 配置文件版本控制

### 监控
- [ ] 服务器监控（CPU、内存、磁盘）
- [ ] 应用监控（错误日志、性能）
- [ ] 数据库监控（查询性能、连接数）

---

**检查完成后，系统即可部署到生产环境！** ✅
