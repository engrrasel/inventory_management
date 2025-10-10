from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from .models import SalesInvoice, SalesItem, ReturnItem
from .forms import SalesInvoiceForm, SalesItemForm, ReturnItemForm


# ----------------- Sales Create -----------------
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


# ----------------- Sales List -----------------
def sales_list(request):
    sales = SalesInvoice.objects.all().order_by('-id')
    return render(request, 'sales/sales_list.html', {'sales': sales})


# ----------------- Sales Detail -----------------
def sales_detail(request, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)
    items = SalesItem.objects.filter(invoice=invoice)
    return render(request, 'sales/sales_detail.html', {
        'invoice': invoice,
        'items': items,
    })


# ----------------- Sales Edit -----------------
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


# ----------------- Sales Delete -----------------
def sales_delete(request, pk):
    invoice = get_object_or_404(SalesInvoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        messages.success(request, f"Invoice #{invoice.invoice_no} deleted successfully!")
        return redirect('sales_list')

    return render(request, 'sales/sales_confirm_delete.html', {'invoice': invoice})


# ----------------- Sales Return -----------------
def sales_return_create(request):
    ReturnFormSet = modelformset_factory(ReturnItem, form=ReturnItemForm, extra=1, can_delete=True)
    invoices = SalesInvoice.objects.all().order_by('-id')
    today = timezone.now().date()

    if request.method == 'POST':
        formset = ReturnFormSet(request.POST, queryset=ReturnItem.objects.none())
        invoice_id = request.POST.get('invoice')
        date = request.POST.get('date', today)

        invoice = None
        if invoice_id:
            invoice = get_object_or_404(SalesInvoice, pk=invoice_id)

        if formset.is_valid() and invoice:
            for form in formset:
                if form.cleaned_data.get('product') and not form.cleaned_data.get('DELETE'):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.date = date
                    item.save()
            messages.success(request, f"Return recorded for Invoice #{invoice.invoice_no}")
            return redirect('sales_list')
        else:
            messages.error(request, "Please select invoice and check the items.")

    else:
        formset = ReturnFormSet(queryset=ReturnItem.objects.none())

    return render(request, 'sales/sales_return_form.html', {
        'formset': formset,
        'invoices': invoices,
        'today': today,
    })


# ----------------- Ajax: Fetch Invoice Items -----------------
def get_invoice_items(request, invoice_id):
    items = SalesItem.objects.filter(invoice_id=invoice_id)
    data = []
    for item in items:
        data.append({
            'id': item.id,
            'product': item.product.id,
            'product_name': item.product.name,
            'quantity': float(item.quantity),
            'unit_price': float(item.unit_price),
        })
    return JsonResponse({'items': data})


def sales_return_create(request):
    ReturnFormSet = modelformset_factory(ReturnItem, form=ReturnItemForm, extra=1, can_delete=True)
    invoices = SalesInvoice.objects.all().order_by('-id')
    today = timezone.now().date()

    if request.method == 'POST':
        formset = ReturnFormSet(request.POST, queryset=ReturnItem.objects.none())
        invoice_id = request.POST.get('invoice')
        invoice = get_object_or_404(SalesInvoice, pk=invoice_id) if invoice_id else None

        if formset.is_valid() and invoice:
            for form in formset:
                if form.cleaned_data.get('product') and not form.cleaned_data.get('DELETE'):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.date = request.POST.get('date', today)
                    item.save()
            messages.success(request, f"Return recorded for Invoice #{invoice.invoice_no}")
            return redirect('sales_list')
        else:
            messages.error(request, "Please select invoice and check the items.")
    else:
        formset = ReturnFormSet(queryset=ReturnItem.objects.none())

    return render(request, 'sales/sales_return_form.html', {
        'formset': formset,
        'invoices': invoices,
        'today': today,
    })