from django.db import models
from app_product.models import Product


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Current Stock"
        verbose_name_plural = "Current Stocks"


class StockHistory(models.Model):
    STOCK_TYPE_CHOICES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("ADJ", "Adjustment"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_history")
    change_type = models.CharField(max_length=3, choices=STOCK_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    previous_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True, null=True, help_text="Purchase/Sale/Return reference")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock History"
        verbose_name_plural = "Stock Histories"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity})"
