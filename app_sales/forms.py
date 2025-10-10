from django import forms
from .models import SalesInvoice, SalesItem, ReturnItem, Product



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


class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ['product', 'quantity', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 1, 'class': 'border rounded px-2 py-1 w-full'}),
            'quantity': forms.NumberInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'product': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
        }

class ReturnForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-2 py-1 w-full'}))

    class Meta:
        model = ReturnItem
        fields = ['date']


class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ['product', 'quantity', 'reason']
        widgets = {
            'product': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'quantity': forms.NumberInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'reason': forms.Textarea(attrs={'rows': 1, 'class': 'border rounded px-2 py-1 w-full'}),
        }