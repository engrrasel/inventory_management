from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum
from datetime import date, timedelta

# তোমার মডেলগুলো ইমপোর্ট করো
from app_product.models import Product
from app_supplier.models import Supplier
from app_purchase.models import PurchaseInvoice
from app_sales.models import SalesInvoice  # যদি থাকে
#from app_expense.models import Expense   # যদি থাকে
from django.shortcuts import render
from django.apps import apps


@staff_member_required
def dashboard_view(request):
    # --- Basic Counts ---
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_purchases = PurchaseInvoice.objects.count()
    total_sales = SalesInvoice.objects.count() if 'app_sales' in request.resolver_match.app_names else 0
    #total_expenses = Expense.objects.count() if 'app_expense' in request.resolver_match.app_names else 0

    # --- Low Stock Products ---
    low_stock = Product.objects.filter(stock__lt=5)[:5]

    # --- Recent Purchases & Sales ---
    recent_purchases = PurchaseInvoice.objects.select_related("supplier").order_by("-id")[:5]
    recent_sales = SalesInvoice.objects.order_by("-id")[:5] if total_sales else []

    # --- Chart data (last 7 days Purchase & Sales) ---
    today = date.today()
    week_ago = today - timedelta(days=7)

    purchases_7days = (
        PurchaseInvoice.objects.filter(date__gte=week_ago)
        .values("date")
        .annotate(total=Sum("total_amount"))
        .order_by("date")
    )

    sales_7days = []
    if total_sales:
        sales_7days = (
            SalesInvoice.objects.filter(date__gte=week_ago)
            .values("date")
            .annotate(total=Sum("total_amount"))
            .order_by("date")
        )

    purchase_labels = [p["date"].strftime("%b %d") for p in purchases_7days]
    purchase_data = [float(p["total"]) for p in purchases_7days]
    sale_data = [float(s["total"]) for s in sales_7days] if total_sales else []

    context = {
        "product_count": total_products,
        "supplier_count": total_suppliers,
        "purchase_count": total_purchases,
        "sale_count": total_sales,
        #"expense_count": total_expenses,
        "low_stock": low_stock,
        "recent_purchases": recent_purchases,
        "recent_sales": recent_sales,
        "chart_labels": purchase_labels,
        "chart_purchase_data": purchase_data,
        "chart_sale_data": sale_data,
    }
    return render(request, "dashboard/home.html", context)


#=================new dashboard=================

def dashboard_home(request):
    app_list = []
    for app_config in apps.get_app_configs():
        models = [model.__name__ for model in app_config.get_models()]
        if models:
            app_list.append({
                'name': app_config.verbose_name,
                'models': models
            })
    return render(request, "home.html", {"app_list": app_list})