"""
Payment Forms
"""
from django import forms
from .models import PaymentBill, FeeStandard, PaymentRecord


class FeeStandardForm(forms.ModelForm):
    """费用标准表单"""
    class Meta:
        model = FeeStandard
        fields = ['community', 'name', 'fee_type', 'price_per_square',
                  'billing_cycle', 'description']
        widgets = {
            'community': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：物业费'
            }),
            'fee_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price_per_square': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'billing_cycle': forms.Select(attrs={
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


class PaymentBillForm(forms.ModelForm):
    """缴费单表单"""
    class Meta:
        model = PaymentBill
        fields = ['community', 'property_unit', 'owner', 'fee_type',
                  'billing_period', 'amount', 'status', 'payment_method',
                  'due_date', 'description']
        widgets = {
            'community': forms.Select(attrs={
                'class': 'form-control'
            }),
            'property_unit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'owner': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fee_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'billing_period': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：2026-01'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = self.fields['community'].queryset.order_by('name')

        # 如果是编辑模式且有小区，只加载对应小区的房产
        # 如果是新增模式，不加载任何房产（由前端级联选择）
        if self.instance and self.instance.pk and hasattr(self.instance, 'community') and self.instance.community_id:
            self.fields['property_unit'].queryset = self.fields['property_unit'].queryset.filter(
                community_id=self.instance.community_id
            ).select_related('community', 'building').order_by('building__name', 'room_number')
        else:
            # 新增模式：清空queryset，让用户先选择小区
            self.fields['property_unit'].queryset = self.fields['property_unit'].queryset.none()
            self.fields['property_unit'].required = False
            self.fields['property_unit'].widget.attrs['placeholder'] = '请先选择小区'

        self.fields['owner'].queryset = self.fields['owner'].queryset.order_by('name')

    def clean(self):
        """表单验证：处理特殊场景"""
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        status = cleaned_data.get('status')

        # 允许金额为0的场景：预缴费用的后续月份应缴金额为0
        if amount is not None and amount < 0:
            raise forms.ValidationError({'amount': '金额不能为负数'})

        # 如果金额为0且状态为已缴，设置paid_amount为0
        if amount == 0 and status == 'paid':
            cleaned_data['paid_amount'] = 0

        return cleaned_data


class PaymentRecordForm(forms.ModelForm):
    """缴费记录表单"""
    class Meta:
        model = PaymentRecord
        fields = ['bill', 'transaction_id', 'out_trade_no', 'payer',
                  'amount', 'payment_method', 'payment_time', 'status']
        widgets = {
            'bill': forms.Select(attrs={
                'class': 'form-control'
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入交易流水号'
            }),
            'out_trade_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入商户订单号'
            }),
            'payer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入缴费人姓名'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bill'].queryset = self.fields['bill'].queryset.select_related(
            'community', 'property_unit', 'owner'
        ).order_by('-billing_period')
