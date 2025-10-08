from django.contrib import admin

from .models import PurchaseInvoice, PurchaseItem


# ---------- Inline Model for Items ----------
class PurchaseItemInline(admin.StackedInline):  #TabularInline
    model = PurchaseItem
    extra = 1  # নতুন ফাঁকা ১টা রো দেখাবে
    fields = ("product", "quantity", "unit_price", "total_price", "serial_number", "imei_number")
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)
    show_change_link = True


# ---------- Main Invoice Admin ----------
@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_no", "lot_number", "supplier", "date", "total_amount", "created_at")
    list_filter = ("payment_method", "date", "supplier")
    search_fields = ("invoice_no", "supplier__name")
    inlines = [PurchaseItemInline]
    date_hierarchy = "date"
    list_per_page = 25
    ordering = ("-date",)
    readonly_fields = ('lot_number',)


    fieldsets = (
        ("Invoice Info", {
            "fields": ("invoice_no", "lot_number", "supplier", "date", "remarks")
        }),
        ("Payment Info", {
            "fields": ("payment_method", "total_amount")
        }),
    )

    # Auto calculate total amount
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        total = sum(item.total_price for item in obj.items.all())
        obj.total_amount = total
        obj.save(update_fields=["total_amount"])


# ---------- Purchase Item Admin ----------
@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "unit_price", "total_price", "serial_number", "imei_number")
    list_filter = ("invoice", "product")
    search_fields = ("product__name", "invoice__invoice_no", "serial_number", "imei_number")
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)
