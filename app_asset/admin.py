from django.contrib import admin
from .models import AssetCategory, Asset, AssetDepreciation, AssetDisposal


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "asset_code", "purchase_value", "current_value", "status")
    list_filter = ("status", "category")
    search_fields = ("name", "asset_code")


@admin.register(AssetDepreciation)
class AssetDepreciationAdmin(admin.ModelAdmin):
    list_display = ("asset", "year", "amount", "date_calculated")
    list_filter = ("year",)
    search_fields = ("asset__name",)


@admin.register(AssetDisposal)
class AssetDisposalAdmin(admin.ModelAdmin):
    list_display = ("asset", "disposal_date", "sale_value", "remarks")
    search_fields = ("asset__name",)
