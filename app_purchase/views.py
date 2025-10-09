from django.shortcuts import render, redirect
from .forms import PurchaseForm, PurchaseItemForm
from .models import PurchaseInvoice, PurchaseItem

def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        item_form = PurchaseItemForm(request.POST)

        if form.is_valid() and item_form.is_valid():
            # ✅ প্রথমে PurchaseInvoice সেভ করো
            invoice = form.save(commit=False)

            # যদি invoice_no অটো জেনারেট করতে চাও, তাহলে:
            if not invoice.invoice_no:
                last_invoice = PurchaseInvoice.objects.order_by('-id').first()
                next_no = (last_invoice.id + 1) if last_invoice else 1
                invoice.invoice_no = f"PUR-{next_no:04d}"

            invoice.save()

            # ✅ তারপর PurchaseItem কে সেই invoice এর সাথে যুক্ত করো
            item = item_form.save(commit=False)
            item.invoice = invoice  # ⚡️ এখানে সঠিক ফিল্ড নাম ব্যবহার করা জরুরি
            item.save()

            return redirect('purchase_create')  # পুনরায় নতুন ইনভয়েস তৈরি পেজে যাবে

    else:
        form = PurchaseForm()
        item_form = PurchaseItemForm()

    context = {
        'form': form,
        'item_form': item_form
    }
    return render(request, 'app_purchase/purchase_form.html', context)
