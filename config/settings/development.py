"""
Development Settings
"""
from .base import *

DEBUG = True

# Database - SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show debug toolbar
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

# CORS - Allow specific origins in development
# 注意：不设置CORS_ALLOW_ALL_ORIGINS，避免干扰同源的Admin请求
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8080',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8080',
]
# 允许localhost:8000（同源请求，不需要CORS）
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
]

# Session Cookie 设置
SESSION_COOKIE_DOMAIN = None  # 使用默认域
SESSION_COOKIE_SECURE = False  # 开发环境不需要HTTPS
CSRF_COOKIE_SECURE = False  # 开发环境不需要HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'  # 防止CSRF攻击
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # 允许JavaScript访问

# Logging - Less verbose to avoid log rotation issues
LOGGING['loggers']['django']['level'] = 'INFO'
