from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "customer_type", "credit_limit", "is_active", "created_at")
    list_filter = ("customer_type", "is_active")
    search_fields = ("name", "phone", "email")
    ordering = ("name",)
