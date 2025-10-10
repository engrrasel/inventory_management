
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_index, name='custom_dashboard'),
]
