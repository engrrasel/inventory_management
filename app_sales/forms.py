from django import forms
from .models import SalesInvoice, SalesItem

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ['customer', 'date', 'payment_method', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'input'}),
        }

class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SalesItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'class': 'input'}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'class': 'input'}),
        }
