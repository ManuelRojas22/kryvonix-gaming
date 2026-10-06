from apps.staff.views.base import StaffLoginView, DashboardView, DashboardStatsView
from apps.staff.views.catalog import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDetailView, ProductDeleteView,
    generate_slug, toggle_product_status, toggle_product_featured, bulk_action_products
)
from apps.staff.views.users import UserListView, UserDetailView, toggle_user_active, toggle_user_staff

__all__ = [
    'StaffLoginView', 'DashboardView', 'DashboardStatsView',
    'CategoryListView', 'CategoryCreateView', 'CategoryUpdateView', 'CategoryDeleteView',
    'BrandListView', 'BrandCreateView', 'BrandUpdateView', 'BrandDeleteView',
    'ProductListView', 'ProductCreateView', 'ProductUpdateView', 'ProductDetailView', 'ProductDeleteView',
    'generate_slug', 'toggle_product_status', 'toggle_product_featured', 'bulk_action_products',
    'UserListView', 'UserDetailView', 'toggle_user_active', 'toggle_user_staff'
]