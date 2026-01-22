"""
创建超级管理员账号
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = '创建超级管理员账号'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='管理员用户名')
        parser.add_argument('--password', type=str, help='管理员密码')
        parser.add_argument('--email', type=str, help='管理员邮箱')
        parser.add_argument('--phone', type=str, help='管理员电话')

    def handle(self, *args, **options):
        User = get_user_model()

        # 获取参数或使用默认值
        username = options.get('username') or 'admin'
        password = options.get('password') or 'admin123'
        email = options.get('email') or 'admin@example.com'
        phone = options.get('phone') or '13800138000'

        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'用户 {username} 已存在'))
            return

        # 创建超级管理员
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            role='super_admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        # 设置姓名
        user.first_name = '超级'
        user.last_name = '管理员'
        user.save()

        self.stdout.write(self.style.SUCCESS(f'成功创建超级管理员账号:'))
        self.stdout.write(f'  用户名: {username}')
        self.stdout.write(f'  密码: {password}')
        self.stdout.write(f'  邮箱: {email}')
        self.stdout.write(f'  电话: {phone}')
        self.stdout.write(self.style.WARNING(f'\n请及时修改默认密码！'))
