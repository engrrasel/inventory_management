# app_product/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=80, unique=True, editable=False)
    name = models.CharField(unique=True,max_length=150, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_color_code(self):
        """Return color code using predefined mapping (case-insensitive)."""
        color_map = {
            "black": "BK", "blue": "BL", "brown": "BR", "green": "GN",
            "grey": "GR", "gray": "GR", "orange": "OR", "purple": "PP",
            "red": "RD", "white": "WH", "yellow": "YL"
        }
        if self.color and self.color.name:
            key = self.color.name.strip().lower()
            return color_map.get(key, key[:2].upper())
        return "NA"

    def _part_code(self, text):
        """Helper: first 2 letters uppercase or 'XX' if missing."""
        if text:
            txt = text.strip().upper()
            return txt[:2]
        return "XX"

    def generate_sku(self):
        """
        Build SKU from category, subcategory, brand, color, and model.
        Format: CAT-SUB-BR-CLR-MDL  (e.g. MO-PH-SA-BK-A15)
        Ensures uniqueness by adding suffix -1, -2... if collision.
        """
        cat = self._part_code(self.category.name) if self.category else "XX"
        sub = self._part_code(self.subcategory.name) if self.subcategory else "XX"
        brd = self._part_code(self.brand.name) if self.brand else "XX"
        clr = self.get_color_code()
        mdl = (self.model.replace(" ", "").upper() if self.model else "GEN")

        base = f"{cat}-{sub}-{brd}-{clr}-{mdl}"
        sku = base
        counter = 1

        # Ensure unique SKU (avoid race conditions in highly concurrent envs but sufficient for most cases)
        while Product.objects.filter(sku=sku).exists():
            sku = f"{base}-{counter}"
            counter += 1

        return sku
    
    def save(self, *args, **kwargs):
        # 1️⃣ Name auto generate from brand + model
        if self.brand and self.model:
            self.name = f"{self.brand.name} {self.model}"

        # 2️⃣ SKU generate only when missing
        if not self.sku:
            self.sku = self.generate_sku()

        # 3️⃣ Slug auto generate from name
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)



class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_history")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    invoice = models.ForeignKey(
        'app_purchase.PurchaseInvoice',  # use string to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="price_history"
    )

    def __str__(self):
        return f"{self.product.name} - {self.purchase_price} ({self.date.strftime('%Y-%m-%d')})"
