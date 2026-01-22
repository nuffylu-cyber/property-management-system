"""
Community Forms
"""
from django import forms
from .models import Community, Building


class CommunityForm(forms.ModelForm):
    """小区表单"""
    class Meta:
        model = Community
        fields = ['name', 'address', 'total_households', 'total_buildings',
                  'developer', 'property_company', 'contact_person', 'contact_phone',
                  'construction_area', 'green_area', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入小区名称'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入详细地址'
            }),
            'total_households': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'total_buildings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'developer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入开发商名称'
            }),
            'property_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入物业公司名称'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系人姓名'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系电话'
            }),
            'construction_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'green_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入小区描述'
            })
        }


class BuildingForm(forms.ModelForm):
    """楼栋表单"""
    class Meta:
        model = Building
        fields = ['community', 'name', 'building_type', 'total_floors',
                  'total_units', 'description']
        widgets = {
            'community': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入楼栋名称，如：1号楼'
            }),
            'building_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'total_units': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入楼栋描述'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 优化小区选择查询
        self.fields['community'].queryset = Community.objects.all().order_by('name')
