from django.contrib import admin
from .models import Account, Transaction, Payment, Expense


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "description")
    search_fields = ("name", "account_type")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account_head", "transaction_type", "amount", "date", "reference")
    list_filter = ("transaction_type", "date")
    search_fields = ("reference", "account_head__name")
    date_hierarchy = "date"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("supplier", "customer", "method", "amount", "date")
    list_filter = ("method", "date")
    search_fields = ("supplier__name", "customer__name")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "date", "description")
    list_filter = ("date",)
    search_fields = ("category",)
