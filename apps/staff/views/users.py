from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model

from apps.staff.mixins import StaffRequiredMixin
from apps.accounts.models import Address

User = get_user_model()


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'staff/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        queryset = User.objects.annotate(
            address_count=Count('addresses'),
            order_count=Count('orders'),
            wishlist_count=Count('wishlist__items')
        ).order_by('-date_joined')

        search = self.request.GET.get('search')
        is_active = self.request.GET.get('is_active')
        is_staff = self.request.GET.get('is_staff')
        email_verified = self.request.GET.get('email_verified')
        newsletter = self.request.GET.get('newsletter')

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')
        if is_staff:
            queryset = queryset.filter(is_staff=is_staff == 'true')
        if email_verified:
            queryset = queryset.filter(email_verified=email_verified == 'true')
        if newsletter:
            queryset = queryset.filter(newsletter=newsletter == 'true')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['is_active_filter'] = self.request.GET.get('is_active', '')
        context['is_staff_filter'] = self.request.GET.get('is_staff', '')
        context['email_verified_filter'] = self.request.GET.get('email_verified', '')
        context['newsletter_filter'] = self.request.GET.get('newsletter', '')
        return context


class UserDetailView(StaffRequiredMixin, DetailView):
    model = User
    template_name = 'staff/users/user_detail.html'
    context_object_name = 'user_obj'

    def get_queryset(self):
        return User.objects.prefetch_related('addresses', 'wishlist__items__product', 'cart__items__product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Direcciones
        context['addresses'] = user.addresses.all()

        # Carrito actual
        try:
            context['cart'] = user.cart
            context['cart_items'] = user.cart.items.select_related('product').all() if hasattr(user, 'cart') else []
        except:
            context['cart'] = None
            context['cart_items'] = []

        # Wishlist
        try:
            context['wishlist'] = user.wishlist
            context['wishlist_items'] = user.wishlist.items.select_related('product').all() if hasattr(user, 'wishlist') else []
        except:
            context['wishlist'] = None
            context['wishlist_items'] = []

        return context


def toggle_user_active(request, pk):
    """AJAX para activar/desactivar usuario."""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            return JsonResponse({'success': False, 'error': 'No puedes desactivar tu propia cuenta'}, status=400)
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return JsonResponse({'success': True, 'is_active': user.is_active})
    return JsonResponse({'success': False}, status=400)


def toggle_user_staff(request, pk):
    """AJAX para dar/quitar permisos de staff."""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            return JsonResponse({'success': False, 'error': 'No puedes cambiar tus propios permisos'}, status=400)
        user.is_staff = not user.is_staff
        user.save(update_fields=['is_staff'])
        return JsonResponse({'success': True, 'is_staff': user.is_staff})
    return JsonResponse({'success': False}, status=400)