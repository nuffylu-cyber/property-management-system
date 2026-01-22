"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.core.views import (
    index, dashboard, dashboard_stats_api, community_list, property_list,
    payment_list, maintenance_list, user_list, settings_list, log_list,
    login_view, logout_view, payment_config_list, account_management_list,
    wechat_pay_config_list, wechat_pay_create_order, wechat_pay_notify,
    notification_list, notification_mark_read, notification_unread_count,
    notification_mark_all_read, send_test_notification, export_logs
)
from apps.community.views import community_form, building_form
from apps.property.views import property_form, owner_form, tenant_form, get_properties_by_community
from apps.payment.views import fee_standard_form, payment_bill_form, update_bill_status, update_bill_payment_method
from apps.maintenance.views import maintenance_request_form

schema_view = get_schema_view(
    openapi.Info(
        title="物业管理系统 API",
        default_version='v1',
        description="物业管理系统接口文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Home page
    path('', index, name='index'),

    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Admin Dashboard (管理后台)
    path('admin/', dashboard, name='dashboard'),
    path('admin/api/dashboard/stats/', dashboard_stats_api, name='dashboard_stats_api'),
    path('admin/community/', community_list, name='community'),
    path('admin/property/', property_list, name='property'),
    path('admin/payment/', payment_list, name='payment'),
    path('admin/maintenance/', maintenance_list, name='maintenance'),
    path('admin/users/', user_list, name='users'),
    path('admin/payment-config/', payment_config_list, name='payment_config'),
    path('admin/account-management/', account_management_list, name='account_management'),
    path('admin/settings/', settings_list, name='settings'),
    path('admin/logs/', log_list, name='logs'),
    path('admin/api/logs/export/', export_logs, name='export_logs'),

    # Notifications (消息推送)
    path('admin/api/notifications/', notification_list, name='notification_list'),
    path('admin/api/notifications/<str:notification_id>/mark-read/', notification_mark_read, name='notification_mark_read'),
    path('admin/api/notifications/unread-count/', notification_unread_count, name='notification_unread_count'),
    path('admin/api/notifications/mark-all-read/', notification_mark_all_read, name='notification_mark_all_read'),
    path('admin/api/notifications/send-test/', send_test_notification, name='send_test_notification'),

    # WeChat Pay (微信支付)
    path('admin/wechat-pay-config/', wechat_pay_config_list, name='wechat_pay_config'),
    path('admin/api/wechat/pay/create/', wechat_pay_create_order, name='wechat_pay_create_order'),
    path('api/wechat/pay/notify/', wechat_pay_notify, name='wechat_pay_notify'),

    # Form URLs (表单API)
    # 注意：带'new/'的路由必须放在带'<pk>/'的路由之前，否则'new'会被当作pk参数
    path('admin/forms/community/new/', community_form, name='community_form_new'),
    path('admin/forms/community/<str:pk>/', community_form, name='community_form_edit'),
    path('admin/forms/building/new/', building_form, name='building_form_new'),
    path('admin/forms/building/<str:pk>/', building_form, name='building_form_edit'),
    path('admin/forms/property/new/', property_form, name='property_form_new'),
    path('admin/forms/property/<str:pk>/', property_form, name='property_form_edit'),
    path('admin/forms/owner/new/', owner_form, name='owner_form_new'),
    path('admin/forms/owner/<str:pk>/', owner_form, name='owner_form_edit'),
    path('admin/forms/tenant/new/', tenant_form, name='tenant_form_new'),
    path('admin/forms/tenant/<str:pk>/', tenant_form, name='tenant_form_edit'),
    path('admin/api/properties-by-community/', get_properties_by_community, name='get_properties_by_community'),
    path('admin/forms/fee-standard/new/', fee_standard_form, name='fee_standard_form_new'),
    path('admin/forms/fee-standard/<str:pk>/', fee_standard_form, name='fee_standard_form_edit'),
    path('admin/forms/payment-bill/new/', payment_bill_form, name='payment_bill_form_new'),
    path('admin/forms/payment-bill/<str:pk>/', payment_bill_form, name='payment_bill_form_edit'),
    # 账单状态和支付方式更新API
    path('admin/api/bills/<str:bill_id>/update-status/', update_bill_status, name='update_bill_status'),
    path('admin/api/bills/<str:bill_id>/update-payment-method/', update_bill_payment_method, name='update_bill_payment_method'),
    path('admin/forms/maintenance/new/', maintenance_request_form, name='maintenance_request_form_new'),
    path('admin/forms/maintenance/<str:pk>/', maintenance_request_form, name='maintenance_request_form_edit'),

    # Django Admin
    path('dj-admin/', admin.site.urls),

    # API
    path('api/auth/', include('apps.core.urls')),
    path('api/community/', include('apps.community.urls')),
    path('api/property/', include('apps.property.urls')),
    path('api/payment/', include('apps.payment.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
    path('api/wechat/', include('apps.wechat.urls')),

    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add debug toolbar URLs in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
