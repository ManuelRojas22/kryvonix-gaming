"""
URLs for VEXOR GAMING Catalog app.
"""
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('tienda/', views.shop, name='shop'),
    path('tienda/categoria/<slug:category_slug>/', views.shop, name='shop_category'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]