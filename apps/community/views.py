"""
Community Views
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import CommunityForm, BuildingForm

from .models import Community, Building
from .serializers import CommunitySerializer, CommunityListSerializer, BuildingSerializer
from apps.core.permissions import IsAdminUser, IsReceptionistUser


class CommunityViewSet(viewsets.ModelViewSet):
    """小区管理视图集"""
    queryset = Community.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CommunityListSerializer
        return CommunitySerializer

    def get_permissions(self):
        """只有管理员和前台可以创建/修改/删除，其他用户只能查看"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def buildings(self, request, pk=None):
        """获取小区的所有楼栋"""
        community = self.get_object()
        buildings = community.buildings.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)


class BuildingViewSet(viewsets.ModelViewSet):
    """楼栋管理视图集"""
    queryset = Building.objects.select_related('community').all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['community', 'building_type']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['community', 'name']

    def get_permissions(self):
        """只有管理员和前台可以创建/修改/删除，其他用户只能查看"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

# ============================================
# Form Views for Admin Interface
# ============================================

@csrf_exempt
def community_form(request, pk=None):
    """渲染小区表单"""
    if pk:
        community = get_object_or_404(Community, pk=pk)
        form = CommunityForm(request.POST or None, instance=community)
    else:
        form = CommunityForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            community = form.save()
            return JsonResponse({
                'success': True,
                'message': '保存成功',
                'data': {
                    'id': community.id,
                    'name': community.name,
                    'address': community.address
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict([(field, [str(e) for e in errors]) for field, errors in form.errors.items()])
            })

    # GET请求 - 返回表单HTML
    url = f"/admin/forms/community/{pk}/" if pk else "/admin/forms/community/new/"

    # 获取CSRF token
    csrf_token = getattr(request, 'csrf_token', None)

    # 安全地获取表单字段值
    def get_field_value(field_name):
        """安全获取表单字段值"""
        try:
            if field_name in form.fields:
                value = form[field_name].value()
                return value if value is not None else ''
            return ''
        except:
            return ''

    # 获取所有字段值
    name_value = get_field_value('name')
    address_value = get_field_value('address')
    total_households_value = get_field_value('total_households') or '0'
    total_buildings_value = get_field_value('total_buildings') or '0'
    developer_value = get_field_value('developer')
    property_company_value = get_field_value('property_company')
    contact_person_value = get_field_value('contact_person')
    contact_phone_value = get_field_value('contact_phone')
    construction_area_value = get_field_value('construction_area') or '0'
    green_area_value = get_field_value('green_area') or '0'
    description_value = get_field_value('description')

    form_html = f'''
    <form method="post" class="ajax-form" data-url="{url}" style="padding: 20px;">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">小区名称 <span style="color: #ef4444;">*</span></label>
            <input type="text" name="name" value="{name_value}" required
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入小区名称">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">详细地址 <span style="color: #ef4444;">*</span></label>
            <input type="text" name="address" value="{address_value}" required
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入详细地址">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">总户数</label>
            <input type="number" name="total_households" value="{total_households_value}" min="0"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入总户数">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">楼栋数</label>
            <input type="number" name="total_buildings" value="{total_buildings_value}" min="0"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入楼栋数">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">开发商</label>
            <input type="text" name="developer" value="{developer_value}"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入开发商名称">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">物业公司</label>
            <input type="text" name="property_company" value="{property_company_value}"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入物业公司名称">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">联系人</label>
            <input type="text" name="contact_person" value="{contact_person_value}"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入联系人姓名">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">联系电话</label>
            <input type="text" name="contact_phone" value="{contact_phone_value}"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入联系电话">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">建筑面积(㎡)</label>
            <input type="number" name="construction_area" value="{construction_area_value}" min="0" step="0.01"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入建筑面积">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">绿化面积(㎡)</label>
            <input type="number" name="green_area" value="{green_area_value}" min="0" step="0.01"
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入绿化面积">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">描述</label>
            <textarea name="description" rows="4"
                      style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s; resize: vertical;"
                      placeholder="请输入小区描述">{description_value}</textarea>
        </div>
        <script>
            // 添加输入框聚焦效果
            document.querySelectorAll('input, textarea').forEach(input => {{
                input.addEventListener('focus', function() {{
                    this.style.borderColor = '#3b82f6';
                    this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                }});
                input.addEventListener('blur', function() {{
                    this.style.borderColor = '#e2e8f0';
                    this.style.boxShadow = 'none';
                }});
            }});
        </script>
    </form>
    '''

    return JsonResponse({'html': form_html})


@csrf_exempt
def building_form(request, pk=None):
    """渲染楼栋表单"""
    if pk:
        building = get_object_or_404(Building, pk=pk)
        form = BuildingForm(request.POST or None, instance=building)
    else:
        form = BuildingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            building = form.save()
            return JsonResponse({
                'success': True,
                'message': '保存成功',
                'data': {
                    'id': building.id,
                    'name': building.name,
                    'community': building.community.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict([(field, [str(e) for e in errors]) for field, errors in form.errors.items()])
            })

    # GET请求 - 返回表单HTML
    url = f"/admin/forms/building/{pk}/" if pk else "/admin/forms/building/new/"

    # 获取CSRF token
    csrf_token = getattr(request, 'csrf_token', None)

    # 安全地获取表单字段值
    def get_field_value(field_name):
        """安全获取表单字段值"""
        try:
            if field_name in form.fields:
                value = form[field_name].value()
                return value if value is not None else ''
            return ''
        except:
            return ''

    # 获取所有小区列表
    from .models import Community
    communities = Community.objects.all()

    # 获取当前选中小区的ID
    selected_community_id = get_field_value('community')

    community_options = ''
    for community in communities:
        selected = 'selected' if str(community.id) == str(selected_community_id) else ''
        community_options += f'<option value="{community.id}" {selected}>{community.name}</option>'

    # 获取字段值
    name_value = get_field_value('name')
    building_type_value = get_field_value('building_type')
    total_floors_value = get_field_value('total_floors') or '1'
    total_units_value = get_field_value('total_units') or '1'
    description_value = get_field_value('description')

    form_html = f'''
    <form method="post" class="ajax-form" data-url="{url}" style="padding: 20px;">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">所属小区 <span style="color: #ef4444;">*</span></label>
            <select name="community" required
                    style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;">
                <option value="">请选择小区</option>
                {community_options}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">楼栋号 <span style="color: #ef4444;">*</span></label>
            <input type="text" name="name" value="{name_value}" required
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="例如:1号楼">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">楼栋类型 <span style="color: #ef4444;">*</span></label>
            <select name="building_type" required
                    style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;">
                <option value="">请选择楼栋类型</option>
                <option value="high" {'selected' if building_type_value == 'high' else ''}>高层</option>
                <option value="multi" {'selected' if building_type_value == 'multi' else ''}>多层</option>
                <option value="villa" {'selected' if building_type_value == 'villa' else ''}>别墅</option>
                <option value="commercial" {'selected' if building_type_value == 'commercial' else ''}>商业</option>
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">总楼层 <span style="color: #ef4444;">*</span></label>
            <input type="number" name="total_floors" value="{total_floors_value}" min="1" required
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入总楼层">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">单元数 <span style="color: #ef4444;">*</span></label>
            <input type="number" name="total_units" value="{total_units_value}" min="1" required
                   style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s;"
                   placeholder="请输入单元数">
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #334155;">描述</label>
            <textarea name="description" rows="4"
                      style="width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s; resize: vertical;"
                      placeholder="请输入楼栋描述">{description_value}</textarea>
        </div>
        <script>
            // 添加输入框聚焦效果
            document.querySelectorAll('input, select, textarea').forEach(input => {{
                input.addEventListener('focus', function() {{
                    this.style.borderColor = '#3b82f6';
                    this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                }});
                input.addEventListener('blur', function() {{
                    this.style.borderColor = '#e2e8f0';
                    this.style.boxShadow = 'none';
                }});
            }});
        </script>
    </form>
    '''

    return JsonResponse({'html': form_html})
