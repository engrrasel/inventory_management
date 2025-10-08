# app_dashboard/views.py
from django.shortcuts import render
from django.utils import timezone
from datetime import date

from app_product.models import Product
from app_purchase.models import PurchaseInvoice
from app_sales.models import SalesInvoice
from app_supplier.models import Supplier
from app_customer.models import Customer

def dashboard_view(request):
    today = date.today()

    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_customers = Customer.objects.count()
    total_purchases = PurchaseInvoice.objects.count()
    total_sales = SalesInvoice.objects.count()

    today_sales = SalesInvoice.objects.filter(date=today).count()
    today_purchases = PurchaseInvoice.objects.filter(date=today).count()

    context = {
        "total_products": total_products,
        "total_suppliers": total_suppliers,
        "total_customers": total_customers,
        "total_purchases": total_purchases,
        "total_sales": total_sales,
        "today_sales": today_sales,
        "today_purchases": today_purchases,
    }
    return render(request, "dashboard/dashboard.html", context)
