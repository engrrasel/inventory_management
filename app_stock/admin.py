from django.contrib import admin
from .models import Stock, StockHistory


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    search_fields = ("product__name", "product__sku")
    list_per_page = 25


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ("product", "change_type", "quantity", "previous_quantity", "new_quantity", "created_at")
    list_filter = ("change_type", "created_at")
    search_fields = ("product__name", "product__sku", "reference")
    readonly_fields = ("previous_quantity", "new_quantity", "created_at")
    list_per_page = 25
