from django.db import models
from django.utils import timezone
from app_supplier.models import Supplier
from app_product.models import Product, ProductPriceHistory
from app_account.models import Account
from app_stock.utils import update_stock


# ---------- Purchase Invoice ----------
class PurchaseInvoice(models.Model):
    invoice_no = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('due', 'Due'),
        ('mobile_banking', 'Mobile Banking'),
    ]

    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash'
    )
    accounts = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    lot_number = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Invoice {self.invoice_no}"

    def save(self, *args, **kwargs):
        # ---------- Auto Increment Lot Number ----------
        if not self.lot_number:
            last_invoice = PurchaseInvoice.objects.order_by('-lot_number').first()
            self.lot_number = (last_invoice.lot_number + 1) if last_invoice else 1

        # ---------- Auto Calculate Due ----------
        self.due_amount = self.total_amount - self.paid_amount

        super().save(*args, **kwargs)


# ---------- Purchase Item ----------
class PurchaseItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Optional fields for serialized/IMEI-based products
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    imei_number = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        """Override save method to auto-update stock and price history."""
        is_new = self._state.adding  # True if creating new item

        # ---------- Auto Calculate Total ----------
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        if is_new:
            # ---------- Stock auto-update ----------
            update_stock(
                product=self.product,
                quantity=self.quantity,
                change_type="IN",
                reference=f"Purchase #{self.invoice.id}",
                remarks="Purchase added"
            )

            # ---------- Product Purchase Price History ----------
            ProductPriceHistory.objects.create(
                product=self.product,
                purchase_price=self.unit_price,
                date=timezone.now(),
                invoice=self.invoice
            )

            # ---------- Auto Update Invoice Total ----------
            total = sum(item.total_price for item in self.invoice.items.all())
            self.invoice.total_amount = total
            self.invoice.due_amount = total - self.invoice.paid_amount
            self.invoice.save(update_fields=['total_amount', 'due_amount'])
