from django import forms
from .models import PurchaseInvoice, PurchaseItem


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseInvoice
        fields = [
            'supplier', 'date', 'payment_method', 'remarks',
            'delivery_cost', 'other_cost', 'discount',
            'paid_amount', 'total_amount', 'due_amount'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
            'total_amount': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'due_amount': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'delivery_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }
