from django.contrib import admin
from .models import Brand, Category, SubCategory, Unit, Color, Product, ProductPriceHistory


# ---------- Brand ----------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ---------- Category ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ---------- SubCategory ----------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")


# ---------- Unit ----------
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", )


# ---------- Color ----------
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ---------- Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku", "name", "brand", "subcategory", "color",
        "unit", "purchase_price", "sale_price", "is_active"
    )
    list_filter = ("brand", "category", "subcategory", "color", "is_active")
    search_fields = ("sku", "name", "brand__name", "category__name", "color__name")
    readonly_fields = ("sku", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",), "name": ("brand", "model")}
    list_per_page = 25
    ordering = ("brand", "category", "name")
    


# ---------- Product Price History ----------
@admin.register(ProductPriceHistory)
class ProductPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("product", "purchase_price", "date", "invoice")
    list_filter = ("date", "product__brand", "product__category")
    search_fields = ("product__name", "product__sku", "invoice__invoice_no")
    date_hierarchy = "date"
