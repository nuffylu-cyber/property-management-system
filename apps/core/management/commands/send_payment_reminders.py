"""
Django管理命令：发送缴费提醒和逾期催缴

使用方法：
    python manage.py send_payment_reminders

可以设置cron定时任务：
    每天早上9点执行：0 9 * * * cd /path/to/project && python manage.py send_payment_reminders
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '发送缴费提醒和逾期催缴通知'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reminder-days',
            type=int,
            default=7,
            help='提前多少天发送缴费提醒（默认7天）'
        )
        parser.add_argument(
            '--overdue-interval',
            type=int,
            default=7,
            help='逾期每隔多少天发送催缴通知（默认7天）'
        )
        parser.add_argument(
            '--reminders-only',
            action='store_true',
            help='仅发送缴费提醒，不发送逾期催缴'
        )
        parser.add_argument(
            '--overdue-only',
            action='store_true',
            help='仅发送逾期催缴，不发送缴费提醒'
        )

    def handle(self, *args, **options):
        """执行命令"""
        from apps.core.notification_service import NotificationService

        reminder_days = options['reminder_days']
        overdue_interval = options['overdue_interval']
        reminders_only = options['reminders_only']
        overdue_only = options['overdue_only']

        self.stdout.write(self.style.SUCCESS(f'\n开始执行消息推送任务...'))
        self.stdout.write(f'执行时间: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

        total_sent = 0

        # 发送缴费提醒
        if not overdue_only:
            self.stdout.write('📋 正在检查待缴费账单...')
            try:
                count = NotificationService.check_and_send_payment_reminders()
                total_sent += count
                self.stdout.write(self.style.SUCCESS(f'✓ 缴费提醒发送完成，共发送 {count} 条'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ 缴费提醒发送失败: {str(e)}'))
                logger.error(f'发送缴费提醒失败: {str(e)}')
        else:
            self.stdout.write('⊘ 跳过缴费提醒（--overdue-only）')

        # 发送逾期催缴
        if not reminders_only:
            self.stdout.write('\n⚠️  正在检查逾期账单...')
            try:
                count = NotificationService.check_and_send_overdue_notices()
                total_sent += count
                self.stdout.write(self.style.SUCCESS(f'✓ 逾期催缴发送完成，共发送 {count} 条'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ 逾期催缴发送失败: {str(e)}'))
                logger.error(f'发送逾期催缴失败: {str(e)}')
        else:
            self.stdout.write('⊘ 跳过逾期催缴（--reminders-only）')

        # 总结
        self.stdout.write(f'\n{"="*50}')
        self.stdout.write(f'总计发送: {total_sent} 条通知')
        self.stdout.write(self.style.SUCCESS('✓ 任务执行完成'))
        self.stdout.write(f'{"="*50}\n')
