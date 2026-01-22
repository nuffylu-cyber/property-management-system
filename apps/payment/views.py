"""
Payment Views
"""
import uuid
from decimal import Decimal
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.db import transaction
import re

from .models import FeeStandard, PaymentBill, PaymentRecord
from .serializers import (FeeStandardSerializer, PaymentBillSerializer, PaymentBillListSerializer,
                           PaymentRecordSerializer, BatchCreateBillsSerializer, WeChatPaymentSerializer)
from apps.core.permissions import IsFinanceUser, IsAdminUser


class FeeStandardViewSet(viewsets.ModelViewSet):
    """物业费标准管理视图集"""
    queryset = FeeStandard.objects.all()
    serializer_class = FeeStandardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['community', 'fee_type', 'is_active']
    search_fields = ['name']
    ordering = ['community', 'fee_type']

    def get_permissions(self):
        """只有管理员和财务可以创建/修改/删除"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'batch_delete']:
            return [IsFinanceUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """
        批量删除费用标准
        接收standard_ids列表，批量删除指定的费用标准
        """
        standard_ids = request.data.get('standard_ids', [])

        if not standard_ids:
            return Response({
                'success': False,
                'error': '请选择要删除的费用标准'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查询要删除的费用标准（直接使用UUID字符串）
        standards = FeeStandard.objects.filter(id__in=standard_ids)

        if not standards.exists():
            return Response({
                'success': False,
                'error': '未找到要删除的费用标准'
            }, status=status.HTTP_404_NOT_FOUND)

        count = standards.count()

        # 执行删除
        try:
            standards.delete()
            return Response({
                'success': True,
                'message': f'成功删除 {count} 个费用标准'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': f'删除失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentBillViewSet(viewsets.ModelViewSet):
    """缴费账单管理视图集"""
    queryset = PaymentBill.objects.select_related('community', 'property_unit', 'owner').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['community', 'property_unit', 'owner', 'fee_type', 'status', 'billing_period']
    search_fields = ['bill_number', 'property_unit__room_number', 'owner__name']
    ordering_fields = ['billing_period', 'due_date', 'created_at']
    ordering = ['-billing_period', '-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentBillListSerializer
        return PaymentBillSerializer

    def get_permissions(self):
        """只有管理员和财务可以创建/修改/删除"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'batch_create', 'batch_delete', 'import_excel']:
            return [IsFinanceUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        """
        批量生成账单
        根据小区和费率标准，批量生成所有房产的账单
        """
        serializer = BatchCreateBillsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        community_id = serializer.validated_data['community_id']
        fee_type = serializer.validated_data['fee_type']
        billing_period = serializer.validated_data['billing_period']
        due_date = serializer.validated_data['due_date']
        description = serializer.validated_data.get('description', '')

        # 获取小区所有房产
        from apps.property.models import Property
        properties = Property.objects.filter(community_id=community_id)

        created_count = 0
        failed_count = 0
        errors = []

        for prop in properties:
            try:
                # 获取业主
                owner_relation = prop.owners.first()
                if not owner_relation:
                    failed_count += 1
                    errors.append(f"{prop.full_address}: 未找到业主")
                    continue

                owner = owner_relation.owner

                # 检查是否已存在账单
                if PaymentBill.objects.filter(
                    property=prop,
                    fee_type=fee_type,
                    billing_period=billing_period
                ).exists():
                    failed_count += 1
                    errors.append(f"{prop.full_address}: 账单已存在")
                    continue

                # 计算金额（这里简化处理，实际应根据费率标准计算）
                fee_standard = FeeStandard.objects.filter(
                    community_id=community_id,
                    fee_type=fee_type,
                    is_active=True
                ).first()

                if not fee_standard:
                    failed_count += 1
                    errors.append(f"{prop.full_address}: 未找到费率标准")
                    continue

                amount = prop.area * fee_standard.price_per_square

                # 生成账单编号
                bill_number = f"{billing_period.replace('-', '')}{str(uuid.uuid4().int)[:6]}"

                # 创建账单
                PaymentBill.objects.create(
                    bill_number=bill_number,
                    community_id=community_id,
                    property=prop,
                    owner=owner,
                    fee_type=fee_type,
                    billing_period=billing_period,
                    amount=amount,
                    due_date=due_date,
                    description=description
                )
                created_count += 1

            except Exception as e:
                failed_count += 1
                errors.append(f"{prop.full_address}: {str(e)}")

        return Response({
            'message': '批量创建完成',
            'created_count': created_count,
            'failed_count': failed_count,
            'errors': errors
        })

    @action(detail=False, methods=['get'])
    def my_bills(self, request):
        """获取我的账单（业主）"""
        user = request.user

        if user.role == 'owner':
            from apps.property.models import Owner
            try:
                owner = Owner.objects.get(user=user)
                # 获取业主所有房产的账单
                properties = [op.property for op in owner.owners.all()]
                bills = PaymentBill.objects.filter(property_unit__in=properties)
                serializer = PaymentBillListSerializer(bills, many=True)
                return Response(serializer.data)
            except Owner.DoesNotExist:
                return Response({'error': '未找到业主信息'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': '无权访问'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """缴费统计"""
        total_bills = PaymentBill.objects.count()
        total_amount = PaymentBill.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = PaymentBill.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_unpaid = total_amount - total_paid

        unpaid_count = PaymentBill.objects.filter(status='unpaid').count()
        paid_count = PaymentBill.objects.filter(status='paid').count()

        return Response({
            'total_bills': total_bills,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_unpaid': total_unpaid,
            'unpaid_count': unpaid_count,
            'paid_count': paid_count,
        })

    @action(detail=False, methods=['delete'])
    def batch_delete(self, request):
        """
        批量删除账单
        接收bill_ids列表，批量删除指定的账单
        """
        bill_ids = request.data.get('bill_ids', [])

        if not bill_ids:
            return Response({
                'success': False,
                'error': '请选择要删除的账单'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查询要删除的账单（直接使用UUID字符串）
        bills = PaymentBill.objects.filter(id__in=bill_ids)

        if not bills.exists():
            return Response({
                'success': False,
                'error': '未找到要删除的账单'
            }, status=status.HTTP_404_NOT_FOUND)

        count = bills.count()

        # 执行删除
        try:
            bills.delete()
            return Response({
                'success': True,
                'message': f'成功删除 {count} 个账单'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': f'删除失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        """从Excel导入应缴费用单"""
        if 'file' not in request.FILES:
            return Response({'error': '请上传Excel文件'}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']

        # 检查文件扩展名
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            return Response({'error': '只支持.xlsx或.xls格式的文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取参数
        community_id = request.data.get('community_id')
        fee_type = request.data.get('fee_type', 'other')
        billing_period = request.data.get('billing_period', '2026-01')
        fee_name = request.data.get('fee_name', '应缴费用')

        if not community_id:
            return Response({'error': '请选择小区'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 读取Excel文件
            # 根据文件扩展名选择引擎
            if excel_file.name.endswith('.xls'):
                df = pd.read_excel(excel_file, engine='xlrd')
            else:
                df = pd.read_excel(excel_file)

            # 验证必需的列
            required_columns = ['房号', '业主', '应缴金额']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response({
                    'error': f'Excel文件缺少必需的列: {", ".join(missing_columns)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取小区
            from apps.community.models import Community
            try:
                community = Community.objects.get(id=community_id)
            except Community.DoesNotExist:
                return Response({'error': '小区不存在'}, status=status.HTTP_400_BAD_REQUEST)

            # 统计信息
            stats = {
                'total_rows': len(df),
                'success_count': 0,
                'skip_count': 0,
                'error_count': 0,
                'errors': [],
                'failed_records': []  # 新增：保存失败记录的完整数据
            }

            # 处理每一行数据（不使用外层事务，每行独立处理）
            for idx, row in df.iterrows():
                    try:
                        # 提取数据
                        room_number_raw = str(row['房号']).strip()
                        owner_names_raw = str(row['业主']).strip()
                        amount = row['应缴金额']

                        # 清理房号（去除可能的.0）
                        if room_number_raw.endswith('.0'):
                            room_number_raw = room_number_raw[:-2]

                        # 解析房号 - 支持多种格式:
                        # 无单元: 1号楼-501、2-601
                        # 有单元: 1号楼1单元-201、1-2-201

                        # 移除"号楼"或"栋"
                        room_cleaned = re.sub(r'[号楼栋]', '-', room_number_raw)
                        # 合并多个连字符
                        room_cleaned = re.sub(r'-+', '-', room_cleaned)
                        # 去除首尾连字符
                        room_cleaned = room_cleaned.strip('-')

                        # 分割并判断格式
                        parts = room_cleaned.split('-')

                        if len(parts) == 2:
                            # 无单元号格式: 楼栋-房号 (例如: 1-501)
                            building_num = parts[0]
                            floor_room = parts[1]

                            # 从楼层房号中提取楼层和房号
                            if len(floor_room) <= 3:
                                floor = int(floor_room[0])
                                room_number = floor_room[1:].zfill(2)
                            else:
                                floor = int(floor_room[:-2])
                                room_number = floor_room[-2:]

                            # 获取楼栋
                            from apps.community.models import Building
                            building = Building.objects.filter(
                                community=community,
                                name=f'{building_num}号楼'
                            ).first()

                            if not building:
                                error_msg = f'未找到楼栋 {building_num}号楼'
                                stats['errors'].append(f'第{idx+2}行: {error_msg}')
                                stats['error_count'] += 1
                                # 保存失败记录
                                stats['failed_records'].append({
                                    'row': idx + 2,
                                    '房号': room_number_raw,
                                    '业主': owner_names_raw,
                                    '应缴金额': amount,
                                    '失败原因': error_msg
                                })
                                continue

                            # 获取房产（无单元号，unit为空）
                            from apps.property.models import Property
                            property_obj = Property.objects.filter(
                                building=building,
                                unit__isnull=True,  # 无单元号
                                floor=floor,
                                room_number=room_number
                            ).first()

                            if not property_obj:
                                error_msg = f'未找到房产 {room_number_raw}'
                                stats['errors'].append(f'第{idx+2}行: {error_msg}')
                                stats['error_count'] += 1
                                # 保存失败记录
                                stats['failed_records'].append({
                                    'row': idx + 2,
                                    '房号': room_number_raw,
                                    '业主': owner_names_raw,
                                    '应缴金额': amount,
                                    '失败原因': error_msg
                                })
                                continue

                        elif len(parts) == 3:
                            # 有单元号格式: 楼栋-单元-房号 (例如: 1-2-201 或 1号楼1单元-201处理后的结果)
                            building_num = parts[0]
                            unit_part = parts[1]  # 可能是 "1" 或 "1单元"
                            floor_room = parts[2]

                            # 数据库中unit字段格式为"1单元"、"2单元"等
                            # 检查unit_part是否已包含"单元"文字
                            if '单元' in unit_part:
                                unit_str = unit_part
                            else:
                                unit_str = f"{unit_part}单元"

                            # 从楼层房号中提取楼层和房号
                            if len(floor_room) <= 3:
                                floor = int(floor_room[0])
                                room_number = floor_room[1:].zfill(2)
                            else:
                                floor = int(floor_room[:-2])
                                room_number = floor_room[-2:]

                            # 获取楼栋
                            from apps.community.models import Building
                            building = Building.objects.filter(
                                community=community,
                                name=f'{building_num}号楼'
                            ).first()

                            if not building:
                                error_msg = f'未找到楼栋 {building_num}号楼'
                                stats['errors'].append(f'第{idx+2}行: {error_msg}')
                                stats['error_count'] += 1
                                # 保存失败记录
                                stats['failed_records'].append({
                                    'row': idx + 2,
                                    '房号': room_number_raw,
                                    '业主': owner_names_raw,
                                    '应缴金额': amount,
                                    '失败原因': error_msg
                                })
                                continue

                            # 获取房产（包含单元号）
                            from apps.property.models import Property
                            property_obj = Property.objects.filter(
                                building=building,
                                unit=unit_str,
                                floor=floor,
                                room_number=room_number
                            ).first()

                            if not property_obj:
                                error_msg = f'未找到房产 {room_number_raw}'
                                stats['errors'].append(f'第{idx+2}行: {error_msg}')
                                stats['error_count'] += 1
                                # 保存失败记录
                                stats['failed_records'].append({
                                    'row': idx + 2,
                                    '房号': room_number_raw,
                                    '业主': owner_names_raw,
                                    '应缴金额': amount,
                                    '失败原因': error_msg
                                })
                                continue
                        else:
                            error_msg = f'房号格式错误 "{room_number_raw}" (支持的格式: 1号楼-501, 1-2-201)'
                            stats['errors'].append(f'第{idx+2}行: {error_msg}')
                            stats['error_count'] += 1
                            # 保存失败记录
                            stats['failed_records'].append({
                                'row': idx + 2,
                                '房号': room_number_raw,
                                '业主': owner_names_raw,
                                '应缴金额': amount,
                                '失败原因': '房号格式错误'
                            })
                            continue

                        # 解析业主姓名（可能包含多个姓名）
                        # 提取所有中文姓名
                        owner_names = re.findall(r'[\u4e00-\u9fa5]+', owner_names_raw)

                        if not owner_names:
                            error_msg = '业主姓名为空'
                            stats['errors'].append(f'第{idx+2}行: {error_msg}')
                            stats['error_count'] += 1
                            # 保存失败记录
                            stats['failed_records'].append({
                                'row': idx + 2,
                                '房号': room_number_raw,
                                '业主': owner_names_raw,
                                '应缴金额': amount,
                                '失败原因': error_msg
                            })
                            continue

                        # 获取房产的所有业主
                        from apps.property.models import OwnerProperty
                        owner_properties = OwnerProperty.objects.filter(
                            property=property_obj
                        ).select_related('owner')

                        # 检查是否有业主匹配
                        matched_owner = None
                        for op in owner_properties:
                            for excel_owner_name in owner_names:
                                if excel_owner_name in op.owner.name or op.owner.name in excel_owner_name:
                                    matched_owner = op.owner
                                    break
                            if matched_owner:
                                break

                        if not matched_owner:
                            system_owners = [op.owner.name for op in owner_properties]
                            error_msg = f'业主不匹配。Excel: {owner_names_raw}, 系统: {system_owners}'
                            stats['errors'].append(f'第{idx+2}行: {error_msg}')
                            stats['error_count'] += 1
                            # 保存失败记录
                            stats['failed_records'].append({
                                'row': idx + 2,
                                '房号': room_number_raw,
                                '业主': owner_names_raw,
                                '应缴金额': amount,
                                '失败原因': f'业主不匹配 (系统业主: {", ".join(system_owners)})'
                            })
                            continue

                        # 验证金额
                        try:
                            amount = float(amount)
                            if amount < 0:
                                raise ValueError('金额不能为负数')
                            # 注意：允许金额为0，因为有些业主可能预缴了费用
                        except (ValueError, TypeError):
                            error_msg = '金额格式错误'
                            stats['errors'].append(f'第{idx+2}行: {error_msg}')
                            stats['error_count'] += 1
                            # 保存失败记录
                            stats['failed_records'].append({
                                'row': idx + 2,
                                '房号': room_number_raw,
                                '业主': owner_names_raw,
                                '应缴金额': amount,
                                '失败原因': error_msg
                            })
                            continue

                        # 检查是否已存在相同的账单
                        existing_bill = PaymentBill.objects.filter(
                            property_unit=property_obj,
                            fee_type=fee_type,
                            billing_period=billing_period
                        ).first()

                        if existing_bill:
                            # 更新已存在的账单（使用独立事务确保立即提交）
                            with transaction.atomic():
                                existing_bill.amount = amount
                                existing_bill.owner = matched_owner
                                existing_bill.save()
                            stats['success_count'] += 1
                        else:
                            # 生成账单编号
                            bill_number = f"{billing_period.replace('-', '')}{str(uuid.uuid4().int)[:6]}"

                            # 创建新账单（使用独立事务确保立即提交）
                            from datetime import date, timedelta
                            due_date = date.today() + timedelta(days=30)

                            with transaction.atomic():
                                PaymentBill.objects.create(
                                    bill_number=bill_number,
                                    community=community,
                                    property_unit=property_obj,
                                    owner=matched_owner,
                                    fee_type=fee_type,
                                    billing_period=billing_period,
                                    amount=amount,
                                    due_date=due_date,
                                    status='unpaid'
                                )
                            stats['success_count'] += 1

                    except Exception as e:
                        error_msg = str(e)
                        stats['errors'].append(f'第{idx+2}行: {error_msg}')
                        stats['error_count'] += 1
                        # 保存失败记录
                        stats['failed_records'].append({
                            'row': idx + 2,
                            '房号': row.get('房号', ''),
                            '业主': row.get('业主', ''),
                            '应缴金额': row.get('应缴金额', ''),
                            '失败原因': f'系统错误: {error_msg}'
                        })


            return Response({
                'message': '导入完成',
                'stats': stats
            })

        except Exception as e:
            return Response({
                'error': f'文件处理失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """缴费记录管理视图集"""
    queryset = PaymentRecord.objects.select_related('bill').all()
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bill', 'status', 'payment_method']
    search_fields = ['transaction_id', 'out_trade_no', 'payer']
    ordering_fields = ['payment_time', 'created_at']
    ordering = ['-payment_time']

    def get_permissions(self):
        """只有管理员和财务可以删除"""
        if self.action in ['batch_delete']:
            return [IsFinanceUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """
        批量删除缴费记录
        接收record_ids列表，批量删除指定的缴费记录
        """
        record_ids = request.data.get('record_ids', [])

        if not record_ids:
            return Response({
                'success': False,
                'error': '请选择要删除的缴费记录'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查询要删除的缴费记录（直接使用UUID字符串）
        records = PaymentRecord.objects.filter(id__in=record_ids)

        if not records.exists():
            return Response({
                'success': False,
                'error': '未找到要删除的缴费记录'
            }, status=status.HTTP_404_NOT_FOUND)

        count = records.count()

        # 执行删除
        try:
            records.delete()
            return Response({
                'success': True,
                'message': f'成功删除 {count} 条缴费记录'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': f'删除失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============================================
# Form Views for Admin Interface
# ============================================

@csrf_exempt
@login_required
def fee_standard_form(request, pk=None):
    """渲染费用标准表单"""
    from .forms import FeeStandardForm

    if pk:
        standard = get_object_or_404(FeeStandard, pk=pk)
        form = FeeStandardForm(request.POST or None, instance=standard)
    else:
        form = FeeStandardForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            standard = form.save()
            return JsonResponse({
                'success': True,
                'message': '保存成功',
                'data': {
                    'id': standard.id,
                    'name': standard.name,
                    'price_per_square': str(standard.price_per_square)
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict([(field, [str(e) for e in errors]) for field, errors in form.errors.items()])
            })

    from django.template.loader import render_to_string
    form_html = render_to_string('admin/forms/fee_standard_form.html', {
        'form': form,
        'csrf_token': request.META.get('CSRF_COOKIE', '')
    })

    return JsonResponse({'html': form_html})


@csrf_exempt
@login_required
def payment_bill_form(request, pk=None):
    """渲染缴费单表单"""
    from .forms import PaymentBillForm
    from apps.property.models import Owner

    if pk:
        bill = get_object_or_404(PaymentBill, pk=pk)
        form = PaymentBillForm(request.POST or None, instance=bill)
    else:
        form = PaymentBillForm(request.POST or None)

    if request.method == 'POST':
        # 处理业主姓名输入
        owner_name = request.POST.get('owner_name', '').strip()
        if owner_name:
            # 根据业主姓名查找Owner对象
            owner = Owner.objects.filter(name=owner_name).first()
            if not owner:
                return JsonResponse({
                    'success': False,
                    'errors': {'owner': [f'未找到业主：{owner_name}，请先在房产管理中添加该业主']}
                })
            # 将owner字段设置为找到的Owner对象的ID
            request.POST._mutable = True
            request.POST['owner'] = str(owner.id)
            request.POST._mutable = False
            # 重新创建form对象
            if pk:
                form = PaymentBillForm(request.POST, instance=bill)
            else:
                form = PaymentBillForm(request.POST)

        if form.is_valid():
            bill = form.save(commit=False)

            # 验证：如果状态是已缴或部分缴，支付方式必须选择
            if bill.status in ['paid', 'partial']:
                payment_method = request.POST.get('payment_method', '').strip()
                if not payment_method:
                    return JsonResponse({
                        'success': False,
                        'errors': {'payment_method': ['当状态为"已缴"或"部分缴"时，支付方式为必填项']}
                    })

            # 处理paid_at字段
            paid_at_str = request.POST.get('paid_at', '').strip()
            if paid_at_str and (bill.status == 'paid' or bill.status == 'partial'):
                from django.utils import timezone
                from datetime import datetime
                try:
                    # 解析datetime-local格式 (YYYY-MM-DDTHH:MM:SS)
                    bill.paid_at = datetime.strptime(paid_at_str, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    # 如果解析失败，使用当前时间
                    bill.paid_at = timezone.now()
            elif bill.status == 'paid' or bill.status == 'partial':
                # 如果状态为已缴或部分缴但没有提供paid_at，使用当前时间
                from django.utils import timezone
                if not bill.paid_at:
                    bill.paid_at = timezone.now()

            # 处理paid_amount和payment_method
            if bill.status == 'paid':
                # 已缴：设置paid_amount为全额
                bill.paid_amount = bill.amount
            elif bill.status == 'partial':
                # 部分缴：从表单获取用户输入的已缴金额
                paid_amount_input = request.POST.get('paid_amount_input', '').strip()
                if paid_amount_input:
                    try:
                        paid_amount_value = float(paid_amount_input)
                        # 验证已缴金额不能超过应缴金额
                        if paid_amount_value > float(bill.amount):
                            return JsonResponse({
                                'success': False,
                                'errors': {'paid_amount_input': ['已缴金额不能超过应缴金额']}
                            })
                        bill.paid_amount = paid_amount_value
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'errors': {'paid_amount_input': ['已缴金额格式不正确']}
                        })
                else:
                    # 如果用户没有输入，提示必须输入
                    return JsonResponse({
                        'success': False,
                        'errors': {'paid_amount_input': ['部分缴时必须输入已缴金额']}
                    })

            # 如果状态改为未缴或逾期，清空paid_at和payment_method
            if bill.status in ['unpaid', 'overdue']:
                bill.paid_at = None
                # 注意：保留payment_method，不删除

            # 特殊处理：如果金额为0且状态为已缴
            if bill.amount == 0 and bill.status == 'paid':
                bill.paid_amount = 0

            bill.save()

            # 处理缴费记录的创建和更新
            from apps.payment.models import PaymentRecord

            if bill.status in ['paid', 'partial']:
                # 查找该账单的缴费记录
                records = PaymentRecord.objects.filter(bill=bill).order_by('-payment_time')

                if records.exists():
                    # 如果已有缴费记录，更新支付方式、金额和时间
                    latest_record = records.first()
                    latest_record.payment_method = bill.payment_method or 'cash'
                    latest_record.amount = bill.paid_amount
                    latest_record.payment_time = bill.paid_at
                    latest_record.save()
                else:
                    # 如果没有缴费记录，创建新记录
                    # 获取旧状态，判断是否是首次创建
                    old_status = PaymentBill.objects.filter(id=bill.id).values_list('status', flat=True).first()

                    # 自动生成交易号和订单号
                    import uuid
                    transaction_id = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
                    out_trade_no = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"

                    # 获取操作人
                    current_user = request.user
                    operator_name = current_user.get_role_display() if current_user.is_authenticated else '系统'

                    # 创建缴费记录
                    PaymentRecord.objects.create(
                        bill=bill,
                        transaction_id=transaction_id,
                        out_trade_no=out_trade_no,
                        payer=bill.owner.name,
                        amount=bill.paid_amount,
                        payment_method=bill.payment_method or 'cash',
                        payment_time=bill.paid_at,
                        operator=operator_name
                    )
            else:
                # 如果状态改为未缴或逾期，可以考虑删除或标记缴费记录
                # 这里选择保留缴费记录，不做删除
                pass

            return JsonResponse({
                'success': True,
                'message': '保存成功',
                'data': {
                    'id': bill.id,
                    'amount': str(bill.amount),
                    'owner_name': bill.owner.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict([(field, [str(e) for e in errors]) for field, errors in form.errors.items()])
            })

    from django.template.loader import render_to_string
    form_html = render_to_string('admin/forms/payment_bill_form.html', {
        'form': form,
        'csrf_token': request.META.get('CSRF_COOKIE', '')
    })

    return JsonResponse({'html': form_html})


@login_required
def update_bill_status(request, bill_id):
    """
    更新账单状态
    当状态改为'paid'或'partial'时，需要同时更新paid_amount、paid_at，并创建缴费记录
    """
    import json
    from django.utils import timezone
    from apps.payment.models import PaymentRecord

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '只支持POST请求'}, status=405)

    try:
        data = json.loads(request.body)
        new_status = data.get('status')

        if not new_status:
            return JsonResponse({'success': False, 'error': '缺少status参数'}, status=400)

        # 获取账单
        bill = PaymentBill.objects.get(id=bill_id)

        # 更新状态
        old_status = bill.status
        bill.status = new_status

        # 获取当前登录用户的信息
        current_user = request.user
        operator_name = current_user.get_role_display() if current_user.is_authenticated else '系统'

        # 如果状态改为'paid'或'partial'，需要更新paid_amount和paid_at，并创建缴费记录
        if new_status in ['paid', 'partial']:
            if new_status == 'paid':
                # 全部支付
                bill.paid_amount = bill.amount
            elif new_status == 'partial':
                # 部分支付，默认为0（可以通过API调整）
                if bill.paid_amount == 0:
                    bill.paid_amount = bill.amount / 2  # 默认设置为50%

            # 设置缴费时间
            if not bill.paid_at:
                bill.paid_at = timezone.now()

            # 创建缴费记录（仅当状态从未缴/逾期变为已缴/部分缴时）
            if old_status not in ['paid', 'partial']:
                # 自动生成交易号和订单号
                import uuid
                transaction_id = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
                out_trade_no = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"

                # 获取支付方式（如果账单已有记录）
                payment_method = bill.payment_method or 'cash'

                # 创建缴费记录
                PaymentRecord.objects.create(
                    bill=bill,
                    transaction_id=transaction_id,
                    out_trade_no=out_trade_no,
                    payer=bill.owner.name,  # 使用业主姓名作为缴费人
                    amount=bill.paid_amount,
                    payment_method=payment_method,
                    payment_time=bill.paid_at,
                    operator=operator_name  # 记录操作人
                )

        # 如果状态改为'unpaid'或'overdue'，清空paid_at
        elif new_status in ['unpaid', 'overdue']:
            bill.paid_at = None

        bill.save()

        return JsonResponse({
            'success': True,
            'message': f'状态已从{old_status}更新为{new_status}'
        })

    except PaymentBill.DoesNotExist:
        return JsonResponse({'success': False, 'error': '账单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def update_bill_payment_method(request, bill_id):
    """
    更新账单的支付方式
    如果账单状态是'paid'或'partial'，需要同步更新缴费记录中的支付方式
    """
    import json
    from django.utils import timezone
    from apps.payment.models import PaymentRecord

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '只支持POST请求'}, status=405)

    try:
        data = json.loads(request.body)
        payment_method = data.get('payment_method')

        if not payment_method:
            return JsonResponse({'success': False, 'error': '缺少payment_method参数'}, status=400)

        # 验证支付方式是否有效
        valid_methods = ['wechat', 'alipay', 'cash', 'bank_transfer']
        if payment_method not in valid_methods:
            return JsonResponse({'success': False, 'error': '无效的支付方式'}, status=400)

        # 获取并更新账单
        bill = PaymentBill.objects.get(id=bill_id)
        old_payment_method = bill.payment_method
        bill.payment_method = payment_method
        bill.save()

        # 如果账单状态是'paid'或'partial'，需要同步更新缴费记录
        if bill.status in ['paid', 'partial']:
            # 查找该账单的缴费记录
            records = PaymentRecord.objects.filter(bill=bill).order_by('-payment_time')

            if records.exists():
                # 如果已有缴费记录，更新最新一条记录的支付方式
                latest_record = records.first()
                latest_record.payment_method = payment_method
                latest_record.save()
            else:
                # 如果没有缴费记录，创建一条新的缴费记录
                # 获取当前登录用户的信息
                current_user = request.user
                operator_name = current_user.get_role_display() if current_user.is_authenticated else '系统'

                # 自动生成交易号和订单号
                import uuid
                transaction_id = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
                out_trade_no = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"

                # 创建缴费记录
                PaymentRecord.objects.create(
                    bill=bill,
                    transaction_id=transaction_id,
                    out_trade_no=out_trade_no,
                    payer=bill.owner.name,
                    amount=bill.paid_amount,
                    payment_method=payment_method,
                    payment_time=bill.paid_at or timezone.now(),
                    operator=operator_name
                )

        return JsonResponse({
            'success': True,
            'message': f'支付方式已更新为{bill.get_payment_method_display()}'
        })

    except PaymentBill.DoesNotExist:
        return JsonResponse({'success': False, 'error': '账单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
