from django.urls import path
from django.views.generic import TemplateView
from apps.staff.views import (
    StaffLoginView, DashboardView, DashboardStatsView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDetailView, ProductDeleteView,
    UserListView, UserDetailView,
    generate_slug, toggle_product_status, toggle_product_featured, bulk_action_products,
    toggle_user_active, toggle_user_staff
)

app_name = 'staff'

urlpatterns = [
    # Auth
    path('login/', StaffLoginView.as_view(), name='login'),
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    # Categories
    path('categorias/', CategoryListView.as_view(), name='category_list'),
    path('categorias/nueva/', CategoryCreateView.as_view(), name='category_create'),
    path('categorias/<int:pk>/editar/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categorias/<int:pk>/eliminar/', CategoryDeleteView.as_view(), name='category_delete'),
    # Brands
    path('marcas/', BrandListView.as_view(), name='brand_list'),
    path('marcas/nueva/', BrandCreateView.as_view(), name='brand_create'),
    path('marcas/<int:pk>/editar/', BrandUpdateView.as_view(), name='brand_edit'),
    path('marcas/<int:pk>/eliminar/', BrandDeleteView.as_view(), name='brand_delete'),
    # Products
    path('productos/', ProductListView.as_view(), name='product_list'),
    path('productos/nuevo/', ProductCreateView.as_view(), name='product_create'),
    path('productos/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('productos/<int:pk>/editar/', ProductUpdateView.as_view(), name='product_edit'),
    path('productos/<int:pk>/eliminar/', ProductDeleteView.as_view(), name='product_delete'),
    # Users
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # Orders (placeholder templates)
    path('pedidos/', TemplateView.as_view(template_name='staff/orders/order_list.html'), name='order_list'),
    path('pedidos/<int:pk>/', TemplateView.as_view(template_name='staff/orders/order_detail.html'), name='order_detail'),
    # Reports
    path('reportes/', TemplateView.as_view(template_name='staff/reports/dashboard.html'), name='reports_dashboard'),
    # AJAX endpoints
    path('ajax/generate-slug/', generate_slug, name='generate_slug'),
    path('ajax/product/<int:pk>/toggle-status/', toggle_product_status, name='toggle_product_status'),
    path('ajax/product/<int:pk>/toggle-featured/', toggle_product_featured, name='toggle_product_featured'),
    path('ajax/products/bulk-action/', bulk_action_products, name='bulk_action_products'),
    path('ajax/user/<int:pk>/toggle-active/', toggle_user_active, name='toggle_user_active'),
    path('ajax/user/<int:pk>/toggle-staff/', toggle_user_staff, name='toggle_user_staff'),
]