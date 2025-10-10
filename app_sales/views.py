from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from .models import SalesInvoice, SalesItem
from .forms import SalesInvoiceForm, SalesItemForm


def sales_create(request):
    SalesItemFormSet = modelformset_factory(SalesItem, form=SalesItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        invoice_form = SalesInvoiceForm(request.POST)
        formset = SalesItemFormSet(request.POST, queryset=SalesItem.objects.none())

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()
            total = 0
            for form in formset:
                if form.cleaned_data.get('product'):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.save()
                    total += item.total_price
            invoice.total_amount = total
            invoice.save()
            messages.success(request, f"Sales invoice #{invoice.invoice_no} created successfully!")
            return redirect('sales_list')
    else:
        invoice_form = SalesInvoiceForm()
        formset = SalesItemFormSet(queryset=SalesItem.objects.none())

    return render(request, 'sales/sales_form.html', {
        'invoice_form': invoice_form,
        'formset': formset,
    })


def sales_list(request):
    sales = SalesInvoice.objects.all().order_by('-id')
    return render(request, 'sales/sales_list.html', {'sales': sales})


def sales_detail(request, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)
    items = SalesItem.objects.filter(invoice=invoice)
    return render(request, 'sales/sales_detail.html', {
        'invoice': invoice,
        'items': items,
    })


def sales_edit(request, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)
    SalesItemFormSet = modelformset_factory(SalesItem, form=SalesItemForm, extra=0, can_delete=True)

    if request.method == 'POST':
        invoice_form = SalesInvoiceForm(request.POST, instance=invoice)
        formset = SalesItemFormSet(request.POST, queryset=SalesItem.objects.filter(invoice=invoice))

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()
            total = 0
            for form in formset:
                if form.cleaned_data.get('product') and not form.cleaned_data.get('DELETE'):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.save()
                    total += item.total_price
            invoice.total_amount = total
            invoice.save()
            messages.success(request, f"Invoice #{invoice.invoice_no} updated successfully!")
            return redirect('sales_list')
    else:
        invoice_form = SalesInvoiceForm(instance=invoice)
        formset = SalesItemFormSet(queryset=SalesItem.objects.filter(invoice=invoice))

    return render(request, 'sales/sales_form.html', {
        'invoice_form': invoice_form,
        'formset': formset,
        'edit_mode': True
    })

from django.shortcuts import get_object_or_404

def sales_delete(request, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        messages.success(request, f"Invoice #{invoice.invoice_no} deleted successfully!")
        return redirect('sales_list')

    return render(request, 'sales/sales_confirm_delete.html', {'invoice': invoice})
