"""
报事管理模块单元测试
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta

from .models import MaintenanceRequest, MaintenanceLog
from apps.community.models import Community
from apps.property.models import Property, Building, Owner

User = get_user_model()


class MaintenanceRequestModelTest(TestCase):
    """报事记录模型测试"""

    def setUp(self):
        """测试前准备"""
        # 创建用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='admin'
        )

        # 创建小区
        self.community = Community.objects.create(
            name='测试小区',
            address='测试地址'
        )

        # 创建楼栋
        self.building = Building.objects.create(
            community=self.community,
            name='1号楼'
        )

        # 创建房产
        self.property = Property.objects.create(
            building=self.building,
            community=self.community,
            room_number='01',
            floor=1,
            area=100.00
        )

    def test_create_maintenance_request(self):
        """测试创建报事记录"""
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        self.assertEqual(maintenance.reporter, '张三')
        self.assertEqual(maintenance.status, 'pending')
        self.assertEqual(maintenance.category, 'electric')
        self.assertIsNotNone(maintenance.request_number)
        self.assertTrue(maintenance.request_number.startswith('BX'))

    def test_request_number_auto_generation(self):
        """测试报事编号自动生成"""
        maintenance1 = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='报事1'
        )

        maintenance2 = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='李四',
            reporter_phone='13800138001',
            category='plumbing',
            description='报事2'
        )

        # 验证编号唯一
        self.assertNotEqual(maintenance1.request_number, maintenance2.request_number)
        # 验证编号格式
        self.assertTrue(maintenance1.request_number.startswith('BX'))
        self.assertTrue(maintenance2.request_number.startswith('BX'))

    def test_status_choices(self):
        """测试状态选择"""
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        # 测试所有状态值
        valid_statuses = ['pending', 'assigned', 'processing', 'completed', 'closed']
        for status_value in valid_statuses:
            maintenance.status = status_value
            maintenance.save()
            self.assertEqual(maintenance.status, status_value)

    def test_category_choices(self):
        """测试报事类别选择"""
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        # 测试所有类别
        valid_categories = ['electric', 'plumbing', 'civil', 'elevator', 'cleaning', 'security', 'other']
        for category in valid_categories:
            maintenance.category = category
            maintenance.save()
            self.assertEqual(maintenance.category, category)

    def test_str_method(self):
        """测试__str__方法"""
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        expected = f"{maintenance.request_number} - 电工"
        self.assertEqual(str(maintenance), expected)


class MaintenanceLogModelTest(TestCase):
    """报事处理日志模型测试"""

    def setUp(self):
        """测试前准备"""
        # 创建用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='admin'
        )

        # 创建小区
        self.community = Community.objects.create(
            name='测试小区',
            address='测试地址'
        )

        # 创建楼栋
        self.building = Building.objects.create(
            community=self.community,
            name='1号楼'
        )

        # 创建房产
        self.property = Property.objects.create(
            building=self.building,
            community=self.community,
            room_number='01',
            floor=1,
            area=100.00
        )

        # 创建报事记录
        self.maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

    def test_create_maintenance_log(self):
        """测试创建处理日志"""
        log = MaintenanceLog.objects.create(
            request=self.maintenance,
            operator='工程师',
            action='派单',
            description='已指派给王工程师'
        )

        self.assertEqual(log.request, self.maintenance)
        self.assertEqual(log.operator, '工程师')
        self.assertEqual(log.action, '派单')
        self.assertEqual(log.description, '已指派给王工程师')

    def test_log_auto_timestamp(self):
        """测试日志自动时间戳"""
        before_time = timezone.now()

        log = MaintenanceLog.objects.create(
            request=self.maintenance,
            operator='工程师',
            action='派单',
            description='已指派给王工程师'
        )

        after_time = timezone.now()

        # 验证创建时间在合理范围内
        self.assertGreaterEqual(log.created_at, before_time)
        self.assertLessEqual(log.created_at, after_time)

    def test_str_method(self):
        """测试__str__方法"""
        log = MaintenanceLog.objects.create(
            request=self.maintenance,
            operator='工程师',
            action='派单',
            description='已指派给王工程师'
        )

        expected = f"{self.maintenance.request_number} - 派单"
        self.assertEqual(str(log), expected)


class MaintenanceRequestAPITest(APITestCase):
    """报事管理API测试"""

    def setUp(self):
        """测试前准备"""
        # 创建管理员用户
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin'
        )

        # 创建前台用户
        self.receptionist_user = User.objects.create_user(
            username='receptionist',
            password='receptionist123',
            role='receptionist'
        )

        # 创建小区
        self.community = Community.objects.create(
            name='测试小区',
            address='测试地址'
        )

        # 创建楼栋
        self.building = Building.objects.create(
            community=self.community,
            name='1号楼'
        )

        # 创建房产
        self.property = Property.objects.create(
            building=self.building,
            community=self.community,
            room_number='01',
            floor=1,
            area=100.00
        )

        # 创建报事记录
        self.maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        # API基础URL
        self.api_base_url = '/api/maintenance/requests'

    def test_list_maintenance_requests(self):
        """测试获取报事列表"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.api_base_url + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_maintenance_request(self):
        """测试创建报事"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'property': str(self.property.id),
            'reporter': '李四',
            'reporter_phone': '13900139000',
            'category': 'plumbing',
            'description': '水管漏水',
            'priority': 'medium'
        }
        response = self.client.post(self.api_base_url + '/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MaintenanceRequest.objects.count(), 2)

    def test_assign_maintenance(self):
        """测试派单功能"""
        self.client.force_authenticate(user=self.receptionist_user)
        url = '/api/maintenance/requests/{}/assign/'.format(self.maintenance.id)
        data = {'assigned_to': '王工程师'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 刷新对象并验证状态
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.status, 'assigned')
        self.assertEqual(self.maintenance.assigned_to, '王工程师')
        self.assertIsNotNone(self.maintenance.assigned_at)

        # 验证日志已创建
        self.assertEqual(MaintenanceLog.objects.count(), 1)
        log = MaintenanceLog.objects.first()
        self.assertEqual(log.action, '派单')

    def test_start_maintenance(self):
        """测试开始处理"""
        self.client.force_authenticate(user=self.receptionist_user)

        # 先派单
        self.maintenance.status = 'assigned'
        self.maintenance.assigned_to = '王工程师'
        self.maintenance.save()

        # 开始处理
        url = f'{self.api_base_url}/{self.maintenance.id}/start/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证状态
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.status, 'processing')
        self.assertIsNotNone(self.maintenance.started_at)

    def test_complete_maintenance(self):
        """测试完成报事"""
        self.client.force_authenticate(user=self.receptionist_user)

        # 设置为处理中
        self.maintenance.status = 'processing'
        self.maintenance.assigned_to = '王工程师'
        self.maintenance.started_at = timezone.now()
        self.maintenance.save()

        # 完成报事
        url = f'{self.api_base_url}/{self.maintenance.id}/complete/'
        data = {'result_description': '已更换新灯泡，照明恢复正常'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证状态
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.status, 'completed')
        self.assertIsNotNone(self.maintenance.completed_at)
        self.assertEqual(self.maintenance.result_description, '已更换新灯泡，照明恢复正常')

    def test_close_maintenance(self):
        """测试关闭报事"""
        self.client.force_authenticate(user=self.receptionist_user)

        # 设置为已完成
        self.maintenance.status = 'completed'
        self.maintenance.completed_at = timezone.now()
        self.maintenance.save()

        # 关闭报事
        url = f'{self.api_base_url}/{self.maintenance.id}/close/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证状态
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.status, 'closed')

    def test_reopen_maintenance(self):
        """测试重新打开报事（返工）"""
        self.client.force_authenticate(user=self.receptionist_user)

        # 设置为已完成
        self.maintenance.status = 'completed'
        self.maintenance.completed_at = timezone.now()
        self.maintenance.save()

        # 重新打开
        url = f'{self.api_base_url}/{self.maintenance.id}/reopen/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证状态返回处理中
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.status, 'processing')

    def test_get_maintenance_logs(self):
        """测试获取处理日志"""
        self.client.force_authenticate(user=self.admin_user)

        # 创建一些日志
        MaintenanceLog.objects.create(
            request=self.maintenance,
            operator='前台',
            action='创建',
            description='报事已创建'
        )

        url = f'{self.api_base_url}/{self.maintenance.id}/logs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_rate_maintenance(self):
        """测试评价功能"""
        self.client.force_authenticate(user=self.admin_user)

        # 设置为已完成
        self.maintenance.status = 'completed'
        self.maintenance.completed_at = timezone.now()
        self.maintenance.save()

        # 评价
        url = f'{self.api_base_url}/{self.maintenance.id}/rate/'
        data = {
            'rating': 5,
            'feedback': '服务很好，响应迅速'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证评价
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.rating, 5)
        self.assertEqual(self.maintenance.feedback, '服务很好，响应迅速')

    def test_invalid_rating(self):
        """测试无效评分"""
        self.client.force_authenticate(user=self.admin_user)

        # 设置为已完成
        self.maintenance.status = 'completed'
        self.maintenance.completed_at = timezone.now()
        self.maintenance.save()

        # 评分超出范围
        url = f'{self.api_base_url}/{self.maintenance.id}/rate/'
        data = {'rating': 6}  # 无效评分
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MaintenanceStatusFlowTest(TestCase):
    """报事状态流转测试"""

    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin'
        )

        self.community = Community.objects.create(
            name='测试小区',
            address='测试地址'
        )

        self.building = Building.objects.create(
            community=self.community,
            name='1号楼'
        )

        self.property = Property.objects.create(
            building=self.building,
            community=self.community,
            room_number='01',
            floor=1,
            area=100.00
        )

    def test_complete_status_flow(self):
        """测试完整的状态流转流程"""
        # 创建报事
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了'
        )

        # 初始状态
        self.assertEqual(maintenance.status, 'pending')

        # 派单
        maintenance.status = 'assigned'
        maintenance.assigned_to = '王工程师'
        maintenance.assigned_at = timezone.now()
        maintenance.save()
        self.assertEqual(maintenance.status, 'assigned')

        # 开始处理
        maintenance.status = 'processing'
        maintenance.started_at = timezone.now()
        maintenance.save()
        self.assertEqual(maintenance.status, 'processing')

        # 完成
        maintenance.status = 'completed'
        maintenance.completed_at = timezone.now()
        maintenance.result_description = '已修复'
        maintenance.save()
        self.assertEqual(maintenance.status, 'completed')

        # 关闭
        maintenance.status = 'closed'
        maintenance.save()
        self.assertEqual(maintenance.status, 'closed')

    def test_reopen_flow(self):
        """测试返工流程"""
        # 创建并完成报事
        maintenance = MaintenanceRequest.objects.create(
            community=self.community,
            property=self.property,
            reporter='张三',
            reporter_phone='13800138000',
            category='electric',
            description='灯泡坏了',
            status='completed',
            completed_at=timezone.now()
        )

        self.assertEqual(maintenance.status, 'completed')

        # 重新打开（返工）
        maintenance.status = 'processing'
        maintenance.save()
        self.assertEqual(maintenance.status, 'processing')

        # 再次完成
        maintenance.status = 'completed'
        maintenance.completed_at = timezone.now()
        maintenance.result_description = '已彻底修复'
        maintenance.save()
        self.assertEqual(maintenance.status, 'completed')


if __name__ == '__main__':
    import django
    django.setup()
