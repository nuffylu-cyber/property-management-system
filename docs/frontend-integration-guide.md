# 物业管理系统 - 前端集成指南

## 📋 概述

本文档说明如何将设计好的前端界面集成到Django项目中。

## 🎯 集成步骤

### 步骤1：提取CSS到独立文件

CSS样式已从HTML中提取，保存为独立文件：
```
static/css/admin.css
```

### 步骤2：创建Django模板结构

```
templates/
├── base.html                 # 基础模板
├── admin/
│   ├── dashboard.html       # 仪表盘
│   ├── community.html       # 小区管理
│   ├── property.html        # 房产管理
│   ├── payment.html         # 缴费管理
│   └── maintenance.html     # 报事管理
└── components/
    ├── sidebar.html         # 侧边栏组件
    └── header.html          # 顶部栏组件
```

### 步骤3：配置Django设置

在 `config/settings/base.py` 中添加：

```python
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.media',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### 步骤4：创建视图函数

在 `apps/core/views.py` 中创建：

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """仪表盘"""
    context = {
        'page_title': '数据概览',
        'total_households': 1225,
        'monthly_revenue': 286540,
        'pending_requests': 12,
        'overdue_amount': 78920,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def community_list(request):
    """小区管理"""
    return render(request, 'admin/community.html')

@login_required
def property_list(request):
    """房产管理"""
    return render(request, 'admin/property.html')

@login_required
def payment_list(request):
    """缴费管理"""
    return render(request, 'admin/payment.html')

@login_required
def maintenance_list(request):
    """报事管理"""
    return render(request, 'admin/maintenance.html')
```

### 步骤5：配置URL路由

在 `config/urls.py` 中配置：

```python
from django.urls import path
from apps.core.views import (
    dashboard, community_list, property_list,
    payment_list, maintenance_list
)

urlpatterns = [
    path('admin/', dashboard, name='dashboard'),
    path('admin/community/', community_list, name='community'),
    path('admin/property/', property_list, name='property'),
    path('admin/payment/', payment_list, name='payment'),
    path('admin/maintenance/', maintenance_list, name='maintenance'),
]
```

## 🎨 模板使用示例

### base.html 结构

```django
{% load static %}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}物业管理系统{% endblock %}</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

    <!-- Icons -->
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="{% static 'css/admin.css' %}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="app-container">
        <!-- 侧边栏 -->
        {% include "components/sidebar.html" %}

        <!-- 主内容区 -->
        <main class="main-content">
            <!-- 顶部栏 -->
            {% include "components/header.html" %}

            <!-- 内容区域 -->
            <div class="content">
                {% block content %}{% endblock %}
            </div>
        </main>
    </div>

    <!-- JavaScript -->
    <script src="{% static 'js/admin.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 页面模板示例

```django
{% extends "base.html" %}

{% block title %}数据概览 - 物业管理系统{% endblock %}

{% block content %}
<div class="page-header animate-in">
    <div>
        <h1 class="page-title">数据概览</h1>
        <p class="page-subtitle">实时掌握物业运营核心指标</p>
    </div>
    <div style="display: flex; gap: 12px;">
        <button class="btn btn-secondary">
            <i class="ri-download-line"></i>
            导出报表
        </button>
        <button class="btn btn-primary">
            <i class="ri-refresh-line"></i>
            刷新数据
        </button>
    </div>
</div>

<!-- 统计卡片 -->
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-header">
            <div class="stat-icon blue">
                <i class="ri-building-4-line"></i>
            </div>
            <span class="stat-trend up">
                <i class="ri-arrow-up-line"></i>
                2.5%
            </span>
        </div>
        <div class="stat-value">{{ total_households }}</div>
        <div class="stat-label">总户数</div>
    </div>
    <!-- 更多卡片... -->
</div>

<!-- 其他内容 -->
{% endblock %}
```

## 🔄 数据集成

### 从视图传递数据到模板

```python
def payment_list(request):
    """缴费管理 - 示例"""
    from apps.payment.models import PaymentBill

    # 获取账单列表
    bills = PaymentBill.objects.select_related(
        'property', 'property__owner'
    ).all()

    # 分页
    from django.core.paginator import Paginator
    paginator = Paginator(bills, 20)  # 每页20条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'bills': page_obj,
    }
    return render(request, 'admin/payment.html', context)
```

### 在模板中循环显示数据

```django
<table class="table">
    <thead>
        <tr>
            <th>账单编号</th>
            <th>房号</th>
            <th>业主</th>
            <th>应缴金额</th>
            <th>状态</th>
        </tr>
    </thead>
    <tbody>
        {% for bill in bills %}
        <tr>
            <td><span style="font-family: monospace;">{{ bill.bill_number }}</span></td>
            <td>{{ bill.property.full_address }}</td>
            <td>{{ bill.property.owner.name }}</td>
            <td style="font-weight: 600;">¥{{ bill.amount }}</td>
            <td>
                <span class="badge badge-{{ bill.status_class }}">
                    {{ bill.get_status_display }}
                </span>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="5" class="empty-state">
                <i class="ri-inbox-line"></i>
                <p>暂无数据</p>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- 分页 -->
<div class="table-pagination">
    <div class="pagination-info">
        显示 {{ page_obj.start_index }}-{{ page_obj.end_index }} 条，
        共 {{ page_obj.paginator.count }} 条记录
    </div>
    <div class="pagination-controls">
        {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}" class="page-btn">
            <i class="ri-arrow-left-s-line"></i>
        </a>
        {% else %}
        <button class="page-btn" disabled>
            <i class="ri-arrow-left-s-line"></i>
        </button>
        {% endif %}

        <span class="page-btn active">{{ page_obj.number }}</span>

        {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="page-btn">
            <i class="ri-arrow-right-s-line"></i>
        </a>
        {% else %}
        <button class="page-btn" disabled>
            <i class="ri-arrow-right-s-line"></i>
        </button>
        {% endif %}
    </div>
</div>
```

## 🚀 运行服务器

```bash
# 1. 收集静态文件
python manage.py collectstatic

# 2. 运行开发服务器
python manage.py runserver

# 3. 访问管理后台
# http://localhost:8000/admin/
```

## 📝 下一步

1. ✅ 创建模板文件
2. ✅ 配置URL路由
3. ⏳ 添加模态框组件
4. ⏳ 实现真实数据集成
5. ⏳ 添加响应式移动端适配
6. ⏳ 增强可访问性

## 🔧 故障排除

### 静态文件无法加载
检查 `STATICFILES_DIRS` 配置是否正确，确保 `STATIC_URL = '/static/'`

### 模板找不到
检查 `TEMPLATES.DIRS` 是否包含 `os.path.join(BASE_DIR, 'templates')`

### 样式错乱
确保浏览器缓存已清除，检查CSS文件路径是否正确
