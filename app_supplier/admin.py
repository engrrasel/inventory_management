from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'company_name', 'phone', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
