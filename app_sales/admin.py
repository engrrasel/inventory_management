from django.contrib import admin
from .models import Customer, SalesInvoice, SalesItem, ReturnItem, SalesPayment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "opening_balance", "created_at")
    search_fields = ("name", "phone")


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_no", "customer", "total_amount", "paid_amount", "due_amount", "payment_method", "date")
    list_filter = ("payment_method", "date")
    search_fields = ("invoice_no", "customer__name")
    inlines = [SalesItemInline]


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "date")
    search_fields = ("invoice__invoice_no", "product__name")


@admin.register(SalesPayment)
class SalesPaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "date")
    list_filter = ("method",)
    search_fields = ("invoice__invoice_no",)
