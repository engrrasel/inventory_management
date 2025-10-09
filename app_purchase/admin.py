from django.contrib import admin
from .models import PurchaseInvoice, PurchaseItem


# ---------- Inline Model for Items ----------
class PurchaseItemInline(admin.TabularInline):  # বা StackedInline চাইলে বদলাতে পারো
    model = PurchaseItem
    extra = 1
    fields = ("product", "quantity", "unit_price", "total_price", "serial_number", "imei_number")
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)
    show_change_link = True


# ---------- Main Invoice Admin ----------
@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_no", "lot_number", "supplier", "date",
        "total_amount", "paid_amount", "due_amount", "payment_method", "created_at"
    )
    list_filter = ("payment_method", "date", "supplier")
    search_fields = ("invoice_no", "supplier__name")
    inlines = [PurchaseItemInline]
    date_hierarchy = "date"
    list_per_page = 25
    ordering = ("-date",)
    readonly_fields = ('lot_number', 'total_amount', 'due_amount')

    fieldsets = (
        ("Invoice Info", {
            "fields": ("invoice_no", "lot_number", "supplier", "date", "remarks")
        }),
        ("Payment Info", {
            "fields": (
                "payment_method",
                "delivery_cost", "other_cost", "discount",
                "total_amount", "paid_amount", "due_amount"
            )
        }),
    )




    # ---------- Auto calculate totals ----------
    def save_model(self, request, obj, form, change):
        """
        Save invoice and auto calculate total, discount, and due amount.
        """
        super().save_model(request, obj, form, change)

        # 1️⃣ Calculate total from Purchase Items
        total_items = sum(item.total_price for item in obj.items.all())

        # 2️⃣ Add delivery & other cost, subtract discount
        total_invoice = total_items + obj.delivery_cost + obj.other_cost - obj.discount

        # 3️⃣ Calculate due
        obj.total_amount = total_invoice
        obj.due_amount = total_invoice - obj.paid_amount

        # 4️⃣ Save updated fields
        obj.save(update_fields=["total_amount", "due_amount"])


# ---------- Purchase Item Admin ----------
@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "invoice", "product", "quantity", "unit_price",
        "total_price", "serial_number", "imei_number"
    )
    list_filter = ("invoice", "product")
    search_fields = ("product__name", "invoice__invoice_no", "serial_number", "imei_number")
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)
