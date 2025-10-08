# app_asset/models.py
from django.db import models
from django.utils import timezone


class AssetCategory(models.Model):
    """Asset এর ক্যাটাগরি যেমন: Vehicle, Furniture, Equipment ইত্যাদি"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    """মূল Fixed Asset তথ্য"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('damaged', 'Damaged'),
        ('disposed', 'Disposed'),
    ]

    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    asset_code = models.CharField(max_length=50, unique=True, editable=False)
    purchase_date = models.DateField(default=timezone.now)
    purchase_value = models.DecimalField(max_digits=12, decimal_places=2)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text="Annual depreciation rate (%)")
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.asset_code})"

    def save(self, *args, **kwargs):
        # asset_code generate (যদি নতুন হয়)
        if not self.asset_code:
            prefix = (self.category.name[:3].upper() if self.category else "AST")
            last_id = Asset.objects.count() + 1
            self.asset_code = f"{prefix}-{last_id:04d}"

        # depreciation হিসাব করা
        years = (timezone.now().date().year - self.purchase_date.year)
        dep_value = self.purchase_value * (self.depreciation_rate / 100) * years
        self.current_value = max(self.purchase_value - dep_value, 0)

        super().save(*args, **kwargs)


class AssetDepreciation(models.Model):
    """বার্ষিক Depreciation হিসাব রাখে"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="depreciations")
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_calculated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.asset.name} - {self.year}"


class AssetDisposal(models.Model):
    """যখন কোনো asset বিক্রি বা বাতিল হয়"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="disposals")
    disposal_date = models.DateField(default=timezone.now)
    sale_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)
