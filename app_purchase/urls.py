from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.purchase_create, name='purchase_create'),  # ✅ main form






]
