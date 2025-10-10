from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('create/', views.sales_create, name='sales_create'),
    path('<int:pk>/', views.sales_detail, name='sales_detail'),
    path('<int:pk>/edit/', views.sales_edit, name='sales_edit'),
    path('<int:pk>/delete/', views.sales_delete, name='sales_delete'),
    path('return/', views.sales_return_create, name='sales_return'),
    path('invoice-items/<int:invoice_id>/', views.get_invoice_items, name='get_invoice_items'),
]
