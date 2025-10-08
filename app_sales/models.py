# app_sales/models.py
from django.db import models
from django.utils import timezone
from app_product.models import Product


# -------- Customer --------
class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------- Sales Invoice --------
class SalesInvoice(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('due', 'Due'),
        ('mobile', 'Mobile Banking'),
    ]

    invoice_no = models.PositiveIntegerField(unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_no}"

    def save(self, *args, **kwargs):
        # Auto-generate invoice number
        if not self.invoice_no:
            last_invoice = SalesInvoice.objects.all().order_by('id').last()
            if last_invoice:
                self.invoice_no = last_invoice.invoice_no + 1
            else:
                self.invoice_no = 1

        # Auto-calculate due amount
        self.due_amount = self.total_amount - self.received_amount
        super().save(*args, **kwargs)

    # 🔹 নতুন যোগ করা মেথড: ইনভয়েসের টোটাল আপডেট
    def update_total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.due_amount = self.total_amount - self.received_amount
        self.save(update_fields=["total_amount", "due_amount"])


# -------- Sales Item --------
class SalesItem(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    imei_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Auto calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        # ---------- Stock auto update ----------
        from app_stock.utils import update_stock
        update_stock(
            product=self.product,
            quantity=self.quantity,
            change_type="OUT",
            reference=f"Sales #{self.invoice.id}",
            remarks="Sale made"
        )

        # 🔹 নতুন যোগ করা অংশ: ইনভয়েস টোটাল আপডেট
        self.invoice.update_total_amount()


# -------- Return Item --------
class ReturnItem(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name="returns")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Return: {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ---------- Stock Revert ----------
        from app_stock.utils import update_stock
        update_stock(
            product=self.product,
            quantity=self.quantity,
            change_type="IN",
            reference=f"Return #{self.invoice.id}",
            remarks="Product returned"
        )


# -------- Payment --------
class SalesPayment(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=20, choices=SalesInvoice.PAYMENT_METHODS, default='cash')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.invoice.invoice_no} - {self.amount} ({self.method})"

    # 🔹 ঐচ্ছিক: পেমেন্ট হলে due/received অটো আপডেট
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        invoice = self.invoice
        received_total = sum(p.amount for p in invoice.payments.all())
        invoice.received_amount = received_total
        invoice.due_amount = invoice.total_amount - received_total
        invoice.save(update_fields=["received_amount", "due_amount"])
