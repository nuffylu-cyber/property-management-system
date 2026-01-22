"""
消息推送服务
支持多种渠道的消息推送：站内消息、短信、微信推送
"""
import logging
from typing import Dict, List, Optional
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

from .models import Notification, User

logger = logging.getLogger(__name__)


class NotificationService:
    """消息推送服务类"""

    @staticmethod
    def send_payment_reminder(bill, days_before_due: int = 7) -> Notification:
        """
        发送缴费提醒

        Args:
            bill: PaymentBill实例
            days_before_due: 提前天数（默认7天）

        Returns:
            Notification实例
        """
        try:
            # 获取房产的业主
            owner = bill.property.owners.first()
            if not owner:
                logger.warning(f"房产 {bill.property} 没有业主，无法发送缴费提醒")
                return None

            # 构建通知内容
            title = f"缴费提醒 - {bill.bill_number}"
            content = f"""
尊敬的{owner.name}：

您本月的物业费账单已生成：
- 账单编号：{bill.bill_number}
- 应缴金额：¥{bill.amount}
- 应缴日期：{bill.due_date}
- 缴费周期：{bill.billing_period}

请您及时缴纳，以免产生滞纳金。

如有疑问，请联系物业管理处。
            """.strip()

            # 创建通知记录
            notification = Notification.objects.create(
                notification_type='payment_reminder',
                title=title,
                content=content,
                recipient_id=owner.user_id if owner.user else None,
                recipient_phone=owner.phone,
                related_bill=bill,
                status='pending',
                send_channels={
                    'email': True,
                    'sms': True,
                    'wechat': bool(owner.wechat_openid)
                }
            )

            # 尝试发送通知
            NotificationService._send_notification(notification)

            return notification

        except Exception as e:
            logger.error(f"发送缴费提醒失败: {str(e)}")
            return None

    @staticmethod
    def send_overdue_notice(bill, overdue_days: int = 0) -> Notification:
        """
        发送逾期催缴通知

        Args:
            bill: PaymentBill实例
            overdue_days: 逾期天数

        Returns:
            Notification实例
        """
        try:
            owner = bill.property.owners.first()
            if not owner:
                logger.warning(f"房产 {bill.property} 没有业主，无法发送逾期通知")
                return None

            # 计算滞纳金（假设每天0.05%）
            late_fee = bill.amount * 0.0005 * overdue_days

            title = f"逾期催缴 - {bill.bill_number}"
            content = f"""
尊敬的{owner.name}：

您的物业费账单已逾期{overdue_days}天：
- 账单编号：{bill.bill_number}
- 应缴金额：¥{bill.amount}
- 逾期天数：{overdue_days}天
- 滞纳金：¥{late_fee:.2f}
- 合计应付：¥{bill.amount + late_fee:.2f}

请您尽快缴纳，以免产生更多滞纳金。
如已缴费，请忽略此通知。

如有疑问，请联系物业管理处。
            """.strip()

            notification = Notification.objects.create(
                notification_type='payment_overdue',
                title=title,
                content=content,
                recipient_id=owner.user_id if owner.user else None,
                recipient_phone=owner.phone,
                related_bill=bill,
                status='pending',
                send_channels={
                    'email': True,
                    'sms': True,
                    'wechat': bool(owner.wechat_openid)
                }
            )

            NotificationService._send_notification(notification)

            return notification

        except Exception as e:
            logger.error(f"发送逾期催缴失败: {str(e)}")
            return None

    @staticmethod
    def send_maintenance_notification(maintenance, status: str) -> Notification:
        """
        发送报事状态通知

        Args:
            maintenance: MaintenanceRequest实例
            status: 状态变化

        Returns:
            Notification实例
        """
        try:
            # 获取报事人信息
            reporter_name = maintenance.reporter
            reporter_phone = maintenance.reporter_phone

            # 根据状态构建通知内容
            status_messages = {
                'assigned': '您的报事已派单，工作人员将尽快处理。',
                'processing': '工作人员正在处理您的报事，请耐心等待。',
                'completed': f'您的报事已处理完成。\n处理结果：{maintenance.result_description or "已完成"}',
                'closed': '您的报事已关闭。感谢您的反馈！'
            }

            status_titles = {
                'assigned': '报事已派单',
                'processing': '报事处理中',
                'completed': '报事已完成',
                'closed': '报事已关闭'
            }

            message = status_messages.get(status, '报事状态已更新')
            title = f"{status_titles.get(status, '报事通知')} - {maintenance.request_number}"

            content = f"""
尊敬的{reporter_name}：

您的报事请求状态已更新：
- 报事编号：{maintenance.request_number}
- 报事类别：{maintenance.get_category_display()}
- 当前状态：{maintenance.get_status_display()}
- 处理人：{maintenance.assigned_to or '待分配'}

{message}

如有疑问，请联系物业管理处。
报事时间：{maintenance.created_at.strftime('%Y-%m-%d %H:%M')}
            """.strip()

            notification = Notification.objects.create(
                notification_type=f'maintenance_{status}',
                title=title,
                content=content,
                recipient_phone=reporter_phone,
                related_maintenance=maintenance,
                status='pending',
                send_channels={
                    'email': False,
                    'sms': True,
                    'wechat': False
                }
            )

            NotificationService._send_notification(notification)

            return notification

        except Exception as e:
            logger.error(f"发送报事通知失败: {str(e)}")
            return None

    @staticmethod
    def send_system_announcement(title: str, content: str, target_roles: List[str] = None) -> List[Notification]:
        """
        发送系统公告

        Args:
            title: 公告标题
            content: 公告内容
            target_roles: 目标角色列表（None表示所有用户）

        Returns:
            Notification实例列表
        """
        try:
            # 获取目标用户
            if target_roles:
                users = User.objects.filter(role__in=target_roles, is_active=True)
            else:
                users = User.objects.filter(is_active=True)

            notifications = []
            for user in users:
                notification = Notification.objects.create(
                    notification_type='system_announcement',
                    title=title,
                    content=content,
                    recipient=user,
                    status='pending',
                    send_channels={
                        'email': False,
                        'sms': False,
                        'wechat': False
                    }
                )
                notifications.append(notification)

            # 批量标记为已发送（站内消息）
            Notification.objects.filter(id__in=[n.id for n in notifications]).update(status='sent', sent_at=timezone.now())

            return notifications

        except Exception as e:
            logger.error(f"发送系统公告失败: {str(e)}")
            return []

    @staticmethod
    def _send_notification(notification: Notification) -> bool:
        """
        实际发送通知到各个渠道

        Args:
            notification: Notification实例

        Returns:
            发送是否成功
        """
        success = True
        errors = []

        channels = notification.send_channels

        # 站内消息（总是启用）
        try:
            # 站内消息直接标记为已发送
            pass
        except Exception as e:
            errors.append(f"站内消息: {str(e)}")
            success = False

        # 短信通知
        if channels.get('sms') and notification.recipient_phone:
            try:
                # TODO: 集成短信服务商API
                # 示例：阿里云、腾讯云短信服务
                logger.info(f"发送短信到 {notification.recipient_phone}: {notification.title}")
            except Exception as e:
                errors.append(f"短信: {str(e)}")
                success = False

        # 微信推送
        if channels.get('wechat') and notification.recipient_openid:
            try:
                # TODO: 集成微信模板消息API
                logger.info(f"发送微信推送到 {notification.recipient_openid}: {notification.title}")
            except Exception as e:
                errors.append(f"微信推送: {str(e)}")
                success = False

        # 邮件通知
        if channels.get('email') and notification.recipient:
            try:
                # TODO: 集成邮件发送服务
                # 示例：Django SendMail + SMTP
                logger.info(f"发送邮件到 {notification.recipient.email}: {notification.title}")
            except Exception as e:
                errors.append(f"邮件: {str(e)}")
                success = False

        # 更新通知状态
        if success:
            notification.status = 'sent'
            notification.sent_at = timezone.now()
        else:
            notification.status = 'failed'
            notification.error_message = '; '.join(errors)
            notification.retry_count += 1

        notification.save()

        return success

    @staticmethod
    def check_and_send_payment_reminders():
        """
        检查并发送待缴费提醒

        定时任务：每天检查即将到期（7天内）的未缴账单
        """
        from django.utils import timezone
        from datetime import timedelta
        from apps.payment.models import PaymentBill

        today = timezone.now().date()
        due_date_threshold = today + timedelta(days=7)

        # 查找7天内到期的未缴账单
        upcoming_bills = PaymentBill.objects.filter(
            status__in=['unpaid', 'partial'],
            due_date__lte=due_date_threshold,
            due_date__gte=today
        ).select_related('property__community')

        count = 0
        for bill in upcoming_bills:
            # 检查是否已发送过提醒
            existing = Notification.objects.filter(
                related_bill=bill,
                notification_type='payment_reminder',
                created_at__date=today
            ).exists()

            if not existing:
                NotificationService.send_payment_reminder(bill)
                count += 1

        logger.info(f"缴费提醒发送完成，共发送 {count} 条")
        return count

    @staticmethod
    def check_and_send_overdue_notices():
        """
        检查并发送逾期催缴通知

        定时任务：每天检查已逾期的未缴账单
        """
        from django.utils import timezone
        from apps.payment.models import PaymentBill

        today = timezone.now().date()

        # 查找已逾期的未缴账单
        overdue_bills = PaymentBill.objects.filter(
            status__in=['unpaid', 'partial'],
            due_date__lt=today
        ).select_related('property__community')

        count = 0
        for bill in overdue_bills:
            overdue_days = (today - bill.due_date).days

            # 每隔7天发送一次逾期通知
            if overdue_days % 7 == 0:
                # 检查今天是否已发送
                existing = Notification.objects.filter(
                    related_bill=bill,
                    notification_type='payment_overdue',
                    created_at__date=today
                ).exists()

                if not existing:
                    NotificationService.send_overdue_notice(bill, overdue_days)
                    count += 1

        logger.info(f"逾期催缴发送完成，共发送 {count} 条")
        return count

    @staticmethod
    def get_user_notifications(user_id: str, unread_only: bool = False, limit: int = 50) -> List[Notification]:
        """
        获取用户通知列表

        Args:
            user_id: 用户ID
            unread_only: 是否只获取未读通知
            limit: 返回数量限制

        Returns:
            Notification列表
        """
        queryset = Notification.objects.filter(recipient_id=user_id)

        if unread_only:
            queryset = queryset.filter(status='sent')

        return queryset.order_by('-created_at')[:limit]

    @staticmethod
    def get_unread_count(user_id: str) -> int:
        """
        获取用户未读通知数量

        Args:
            user_id: 用户ID

        Returns:
            未读数量
        """
        return Notification.objects.filter(
            recipient_id=user_id,
            status='sent'
        ).count()
