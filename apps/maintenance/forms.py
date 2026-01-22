"""
Maintenance Forms
"""
from django import forms
from .models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    """报事单表单"""
    class Meta:
        model = MaintenanceRequest
        fields = ['property', 'category', 'priority', 'reporter',
                  'reporter_phone', 'description']
        widgets = {
            'property': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reporter': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入报事人姓名'
            }),
            'reporter_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系电话'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请详细描述问题'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只显示空置或装修中的房产
        self.fields['property'].queryset = self.fields['property'].queryset.select_related(
            'community', 'building'
        ).order_by('community__name', 'building__name', 'room_number')
