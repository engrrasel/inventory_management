from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, SalesInvoice, SalesItem, ReturnItem, SalesPayment


# ---------- Customer Admin ----------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "opening_balance", "created_at")
    search_fields = ("name", "phone")


# ---------- Sales Item Inline ----------
class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'total_price', 'imei_number', 'serial_number')
    readonly_fields = ('total_price',)

    class Media:
        js = ('admin/js/sales_inline.js',)


# ---------- Custom Filter for Due Invoices ----------
class DueAmountFilter(admin.SimpleListFilter):
    title = 'Due Status'
    parameter_name = 'due_status'

    def lookups(self, request, model_admin):
        return [
            ('due', 'Has Due'),
            ('paid', 'Fully Paid'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'due':
            return queryset.filter(due_amount__gt=0)
        elif self.value() == 'paid':
            return queryset.filter(due_amount=0)
        return queryset


# ---------- Sales Invoice Admin ----------
@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer_link', 'date', 'total_amount', 'received_amount', 'due_amount', 'payment_method')
    inlines = [SalesItemInline]

    readonly_fields = ("invoice_no", "total_amount", "due_amount")

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

    # ---------- Filters ----------
    list_filter = ('payment_method', 'date', DueAmountFilter, 'customer')
    search_fields = ('invoice_no', 'customer__name')
    date_hierarchy = 'date'
    list_per_page = 25

    # ---------- Clickable Customer ----------
    def customer_link(self, obj):
        if obj.customer_id:
            url = reverse("admin:app_customer_customer_change", args=[obj.customer.id])
            return format_html('<a href="{}">{}</a>', url, obj.customer.name)
        return "-"
    customer_link.short_description = "Customer"

    # ---------- Auto Calculate Totals ----------
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        total = sum(item.total_price for item in obj.items.all())
        obj.total_amount = total
        obj.due_amount = obj.total_amount - obj.received_amount
        obj.save(update_fields=["total_amount", "due_amount"])


# ---------- Return Item ----------
@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "date")
    search_fields = ("invoice__invoice_no", "product__name")


# ---------- Sales Payment ----------
@admin.register(SalesPayment)
class SalesPaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "date")
    list_filter = ("method",)
    search_fields = ("invoice__invoice_no",)
