from django.contrib import admin
from .models import Customer, SalesInvoice, SalesItem, ReturnItem, SalesPayment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "opening_balance", "created_at")
    search_fields = ("name", "phone")



class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'total_price', 'imei_number', 'serial_number')
    readonly_fields = ('total_price',)

    class Media:
        js = ('admin/js/sales_inline.js',)  # নিচের ফাইলটা আমরা তৈরি করবো


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer', 'date', 'total_amount', 'received_amount', 'due_amount', 'payment_method')
    inlines = [SalesItemInline]

        # -------- readonly fields --------
    readonly_fields = ("invoice_no", "total_amount", "due_amount")

    # -------- field order --------
    fieldsets = (
        ("General Info", {
            "fields": (
                "invoice_no",
                "customer",
                "date",
                "payment_method",
                "received_amount",
                "total_amount",
                "due_amount",
                "remarks",
            )
        }),
    )


    

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Inline item গুলার total যোগ করে total_amount আপডেট করবো
        total = sum(item.total_price for item in obj.items.all())
        obj.total_amount = total
        obj.due_amount = obj.total_amount - obj.received_amount
        obj.save()


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "date")
    search_fields = ("invoice__invoice_no", "product__name")


@admin.register(SalesPayment)
class SalesPaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "date")
    list_filter = ("method",)
    search_fields = ("invoice__invoice_no",)
