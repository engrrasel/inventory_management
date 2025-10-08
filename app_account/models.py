# app_account/models.py
from django.db import models
from django.utils import timezone


class Account(models.Model):
    """
    হিসাবের মূল বিভাগ (e.g., Purchase, Sales, Expense, Capital)
    """
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('equity', 'Equity'),
    ]

    name = models.CharField(max_length=100, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"


class Transaction(models.Model):
    """
    Generic Transaction Table — সব হিসাবের কেন্দ্রবিন্দু
    """
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    account_head = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=200, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.account_head.name} - {self.transaction_type.upper()} {self.amount}"


class Payment(models.Model):
    """
    Payment record for Suppliers / Customers
    """
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mobile', 'Mobile Banking'),
        ('other', 'Other'),
    ]

    supplier = models.ForeignKey('app_supplier.Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('app_sales.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=150, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        target = self.supplier or self.customer or "N/A"
        return f"{target} - {self.amount} ({self.method})"


class Expense(models.Model):
    """
    General expense record (like Office Rent, Utility Bills etc.)
    """
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
