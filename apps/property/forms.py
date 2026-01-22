"""
Property Forms
"""
from django import forms
from .models import Property, Owner, Tenant


class PropertyForm(forms.ModelForm):
    """房产表单（包含业主信息）"""
    owner_name = forms.CharField(
        label='业主姓名',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入业主姓名'
        })
    )

    owner_phone = forms.CharField(
        label='联系电话',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入手机号码'
        })
    )

    class Meta:
        model = Property
        fields = ['community', 'building', 'unit', 'floor', 'room_number',
                  'area', 'property_type', 'status', 'description']
        widgets = {
            'community': forms.Select(attrs={
                'class': 'form-control'
            }),
            'building': forms.Select(attrs={
                'class': 'form-control'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：1单元'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：101'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'property_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = self.fields['community'].queryset.order_by('name')
        self.fields['building'].queryset = self.fields['building'].queryset.order_by('name')

        # 如果是编辑已有房产，预填充主要业主信息
        if self.instance and self.instance.pk:
            primary_owner = self.instance.owners.filter(
                owner__isnull=False
            ).order_by('-is_primary', '-created_at').first()

            if primary_owner and primary_owner.owner:
                self.fields['owner_name'].initial = primary_owner.owner.name
                self.fields['owner_phone'].initial = primary_owner.owner.phone


class OwnerForm(forms.ModelForm):
    """业主表单"""
    class Meta:
        model = Owner
        fields = ['name', 'phone', 'id_card']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入业主姓名'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入手机号码'
            }),
            'id_card': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入身份证号'
            })
        }


class TenantForm(forms.ModelForm):
    """租户表单"""
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'id_card', 'property',
                  'lease_start', 'lease_end']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入租户姓名'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入手机号码'
            }),
            'id_card': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入身份证号',
                'required': False
            }),
            'property': forms.Select(attrs={
                'class': 'form-control',
                'required': False
            }),
            'lease_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            }),
            'lease_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional for the form
        self.fields['id_card'].required = False
        self.fields['property'].required = False
        self.fields['lease_start'].required = False
        self.fields['lease_end'].required = False
        self.fields['property'].queryset = self.fields['property'].queryset.select_related(
            'community', 'building'
        ).order_by('community__name', 'building__name', 'room_number')
