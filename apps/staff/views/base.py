from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone

from apps.staff.mixins import StaffRequiredMixin


class StaffLoginView(LoginView):
    """Login específico para staff - redirige a dashboard si ya autenticado."""
    template_name = 'staff/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('staff:dashboard')


class DashboardView(StaffRequiredMixin, TemplateView):
    """Dashboard principal del panel de administración."""
    template_name = 'staff/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.catalog.models import Product, Category, Brand
        from apps.accounts.models import User, Address
        from apps.cart.models import Cart
        from django.db.models import Sum
        from datetime import timedelta

        now = timezone.now()
        month_ago = now - timedelta(days=30)

        # KPIs
        context['stats'] = {
            'productos_totales': Product.objects.count(),
            'productos_activos': Product.objects.filter(is_active=True).count(),
            'productos_stock_bajo': Product.objects.filter(is_active=True, stock__lt=5).count(),
            'productos_sin_stock': Product.objects.filter(is_active=True, stock=0).count(),
            'productos_destacados': Product.objects.filter(is_active=True, is_featured=True).count(),
            'categorias': Category.objects.filter(is_active=True).count(),
            'marcas': Brand.objects.filter(is_active=True).count(),
            'usuarios_totales': User.objects.count(),
            'usuarios_nuevos_mes': User.objects.filter(date_joined__gte=month_ago).count(),
            'usuarios_staff': User.objects.filter(is_staff=True).count(),
            'carritos_activos': Cart.objects.filter(updated_at__gte=now - timedelta(hours=24)).count(),
            'direcciones_totales': Address.objects.count(),
        }

        # Productos recientes (últimos 10)
        context['productos_recientes'] = Product.objects.select_related(
            'category', 'brand'
        ).order_by('-created_at')[:10]

        # Usuarios recientes
        context['usuarios_recientes'] = User.objects.order_by('-date_joined')[:10]

        # Productos con stock bajo para alerta
        context['alertas_stock'] = Product.objects.filter(
            is_active=True, stock__lt=5
        ).select_related('category', 'brand').order_by('stock')[:5]

        return context


class DashboardStatsView(StaffRequiredMixin, TemplateView):
    """API endpoint para estadísticas del dashboard (gráficos)."""

    def get(self, request, *args, **kwargs):
        from apps.catalog.models import Product, Category

        # Productos por categoría
        categories = Category.objects.filter(is_active=True).annotate(
            count=Count('products', filter=Q(products__is_active=True))
        ).filter(count__gt=0).values('name', 'count').order_by('-count')[:8]

        # Stock distribution
        out_of_stock = Product.objects.filter(is_active=True, stock=0).count()
        low_stock = Product.objects.filter(is_active=True, stock__gte=1, stock__lte=4).count()
        medium_stock = Product.objects.filter(is_active=True, stock__gte=5, stock__lte=20).count()
        high_stock = Product.objects.filter(is_active=True, stock__gte=21).count()

        return JsonResponse({
            'categories': list(categories),
            'stock': {
                'out_of_stock': out_of_stock,
                'low_stock': low_stock,
                'medium_stock': medium_stock,
                'high_stock': high_stock,
            }
        })