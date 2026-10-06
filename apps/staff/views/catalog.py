from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify

from apps.staff.mixins import StaffRequiredMixin
from apps.staff.forms import CategoryForm, BrandForm, ProductForm, ProductImageFormSet, ProductSpecFormSet
from apps.catalog.models import Category, Brand, Product
from apps.cart.models import Order, OrderItem


# ==================== CATEGORY VIEWS ====================

class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'staff/catalog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        queryset = Category.objects.annotate(products_count=Count('products')).order_by('order', 'name')
        search = self.request.GET.get('search')
        is_active = self.request.GET.get('is_active')

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['is_active_filter'] = self.request.GET.get('is_active', '')
        return context


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'staff/catalog/category_form.html'
    success_url = reverse_lazy('staff:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada correctamente.')
        return super().form_valid(form)


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'staff/catalog/category_form.html'
    success_url = reverse_lazy('staff:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada correctamente.')
        return super().form_valid(form)


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'staff/catalog/category_confirm_delete.html'
    success_url = reverse_lazy('staff:category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


# ==================== BRAND VIEWS ====================

class BrandListView(StaffRequiredMixin, ListView):
    model = Brand
    template_name = 'staff/catalog/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 20

    def get_queryset(self):
        queryset = Brand.objects.annotate(products_count=Count('products')).order_by('name')
        search = self.request.GET.get('search')
        is_active = self.request.GET.get('is_active')

        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['is_active_filter'] = self.request.GET.get('is_active', '')
        
        # Stats for overview cards
        base_qs = Brand.objects.all()
        context['brands_total'] = base_qs.count()
        context['brands_active'] = base_qs.filter(is_active=True).count()
        context['brands_inactive'] = base_qs.filter(is_active=False).count()
        context['brands_with_logo'] = base_qs.exclude(logo='').exclude(logo__isnull=True).count()
        
        return context


class BrandCreateView(StaffRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'staff/catalog/brand_form.html'
    success_url = reverse_lazy('staff:brand_list')

    def form_valid(self, form):
        messages.success(self.request, 'Marca creada correctamente.')
        return super().form_valid(form)


class BrandUpdateView(StaffRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'staff/catalog/brand_form.html'
    success_url = reverse_lazy('staff:brand_list')

    def form_valid(self, form):
        messages.success(self.request, 'Marca actualizada correctamente.')
        return super().form_valid(form)


class BrandDeleteView(StaffRequiredMixin, DeleteView):
    model = Brand
    template_name = 'staff/catalog/brand_confirm_delete.html'
    success_url = reverse_lazy('staff:brand_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Marca eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


# ==================== PRODUCT VIEWS ====================

class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = 'staff/catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand').order_by('-created_at')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        is_active = self.request.GET.get('is_active')
        is_featured = self.request.GET.get('is_featured')
        stock_status = self.request.GET.get('stock')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(category__name__icontains=search)
            )
        if category:
            queryset = queryset.filter(category_id=category)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')
        if is_featured:
            queryset = queryset.filter(is_featured=is_featured == 'true')
        if stock_status:
            if stock_status == 'out':
                queryset = queryset.filter(stock=0)
            elif stock_status == 'low':
                queryset = queryset.filter(stock__gte=1, stock__lte=4)
            elif stock_status == 'ok':
                queryset = queryset.filter(stock__gte=5)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        context['brands'] = Brand.objects.filter(is_active=True).order_by('name')
        context['search'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['brand_filter'] = self.request.GET.get('brand', '')
        context['is_active_filter'] = self.request.GET.get('is_active', '')
        context['is_featured_filter'] = self.request.GET.get('is_featured', '')
        context['stock_filter'] = self.request.GET.get('stock', '')
        return context


class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'staff/catalog/product_form.html'
    success_url = reverse_lazy('staff:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, prefix='images')
            context['spec_formset'] = ProductSpecFormSet(self.request.POST, prefix='specs')
        else:
            context['image_formset'] = ProductImageFormSet(prefix='images')
            context['spec_formset'] = ProductSpecFormSet(prefix='specs')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        spec_formset = context['spec_formset']

        if image_formset.is_valid() and spec_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            spec_formset.instance = self.object
            spec_formset.save()
            messages.success(self.request, 'Producto creado correctamente.')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'staff/catalog/product_form.html'
    success_url = reverse_lazy('staff:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='images')
            context['spec_formset'] = ProductSpecFormSet(self.request.POST, instance=self.object, prefix='specs')
        else:
            context['image_formset'] = ProductImageFormSet(instance=self.object, prefix='images')
            context['spec_formset'] = ProductSpecFormSet(instance=self.object, prefix='specs')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        spec_formset = context['spec_formset']

        if image_formset.is_valid() and spec_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            spec_formset.instance = self.object
            spec_formset.save()
            messages.success(self.request, 'Producto actualizado correctamente.')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductDetailView(StaffRequiredMixin, DetailView):
    model = Product
    template_name = 'staff/catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('category', 'brand').prefetch_related('images', 'specs')


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'staff/catalog/product_confirm_delete.html'
    success_url = reverse_lazy('staff:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# ==================== AJAX ENDPOINTS ====================

def generate_slug(request):
    """AJAX endpoint para generar slug automático."""
    name = request.GET.get('name', '')
    if name:
        slug = slugify(name)
        # Verificar unicidad
        model = request.GET.get('model', 'product')
        if model == 'category':
            from apps.catalog.models import Category
            base_slug = slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
        elif model == 'brand':
            from apps.catalog.models import Brand
            base_slug = slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
        else:
            from apps.catalog.models import Product
            base_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
        return JsonResponse({'slug': slug})
    return JsonResponse({'slug': ''})


def toggle_product_status(request, pk):
    """AJAX para activar/desactivar producto."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.is_active = not product.is_active
        product.save(update_fields=['is_active'])
        return JsonResponse({'success': True, 'is_active': product.is_active})
    return JsonResponse({'success': False}, status=400)


def toggle_product_featured(request, pk):
    """AJAX para destacar/quitar destacado."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.is_featured = not product.is_featured
        product.save(update_fields=['is_featured'])
        return JsonResponse({'success': True, 'is_featured': product.is_featured})
    return JsonResponse({'success': False}, status=400)


def bulk_action_products(request):
    """Acciones en lote para productos."""
    if request.method == 'POST':
        action = request.POST.get('action')
        ids = request.POST.getlist('ids')
        products = Product.objects.filter(pk__in=ids)

        if action == 'activate':
            products.update(is_active=True)
            messages.success(request, f'{products.count()} productos activados.')
        elif action == 'deactivate':
            products.update(is_active=False)
            messages.success(request, f'{products.count()} productos desactivados.')
        elif action == 'feature':
            products.update(is_featured=True)
            messages.success(request, f'{products.count()} productos marcados como destacados.')
        elif action == 'unfeature':
            products.update(is_featured=False)
            messages.success(request, f'{products.count()} productos quitados de destacados.')
        elif action == 'apply_discount':
            discount_percent = request.POST.get('discount_percent')
            try:
                pct = int(discount_percent)
                if 1 <= pct <= 99:
                    count = 0
                    for product in products:
                        if product.price:
                            product.discount_price = round(product.price * (1 - pct / 100), 2)
                            product.save(update_fields=['discount_price'])
                            count += 1
                    messages.success(request, f'Descuento del {pct}% aplicado a {count} productos.')
                else:
                    messages.error(request, 'Porcentaje de descuento inválido (1-99).')
            except (ValueError, TypeError):
                messages.error(request, 'Porcentaje de descuento inválido.')
        elif action == 'remove_discount':
            count = products.exclude(discount_price__isnull=True).update(discount_price=None)
            messages.success(request, f'Descuento quitado de {count} productos.')
        elif action == 'delete':
            count = products.count()
            products.delete()
            messages.success(request, f'{count} productos eliminados.')

    return redirect('staff:product_list')


# ==================== ORDER VIEWS ====================

class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'staff/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        date_range = self.request.GET.get('date_range')

        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(client_name__icontains=search) |
                Q(client_email__icontains=search) |
                Q(id__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        if date_range:
            from django.utils import timezone
            from datetime import timedelta
            now = timezone.now()
            if date_range == 'today':
                queryset = queryset.filter(created_at__date=now.date())
            elif date_range == 'week':
                queryset = queryset.filter(created_at__gte=now - timedelta(days=7))
            elif date_range == 'month':
                queryset = queryset.filter(created_at__gte=now - timedelta(days=30))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = Order.objects.all()
        context['orders_total'] = base_qs.count()
        context['orders_pendiente'] = base_qs.filter(status='pendiente').count()
        context['orders_procesando'] = base_qs.filter(status='procesando').count()
        context['orders_enviado'] = base_qs.filter(status='enviado').count()
        context['orders_completado'] = base_qs.filter(status='completado').count()
        context['orders_cancelado'] = base_qs.filter(status='cancelado').count()
        context['total_revenue'] = base_qs.filter(payment_status='pagado').aggregate(
            total=Sum('total')
        )['total'] or 0
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['date_filter'] = self.request.GET.get('date_range', '')
        return context


class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'staff/orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('items__product__brand', 'items__product__images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        return context


def order_update_status(request, pk):
    """AJAX endpoint para actualizar estado de pedido."""
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            if new_status == 'enviado' and not order.shipped_at:
                from django.utils import timezone
                order.shipped_at = timezone.now()
            elif new_status == 'completado' and not order.delivered_at:
                from django.utils import timezone
                order.delivered_at = timezone.now()
            order.save(update_fields=['status', 'shipped_at', 'delivered_at', 'updated_at'])
            messages.success(request, f'Estado actualizado de "{old_status}" a "{new_status}".')
        else:
            messages.error(request, 'Estado inválido.')
    return redirect('staff:order_detail', pk=pk)


def reports_data(request):
    """AJAX endpoint para datos de reportes."""
    from django.db.models import Sum, Count, Avg
    from django.utils import timezone
    from datetime import timedelta
    import json
    
    days = int(request.GET.get('days', 30))
    now = timezone.now()
    start_date = now - timedelta(days=days)
    prev_start = start_date - timedelta(days=days)
    
    # Current period orders
    current_orders = Order.objects.filter(created_at__gte=start_date)
    prev_orders = Order.objects.filter(created_at__gte=prev_start, created_at__lt=start_date)
    
    # Revenue
    current_revenue = current_orders.filter(payment_status='pagado').aggregate(total=Sum('total'))['total'] or 0
    prev_revenue = prev_orders.filter(payment_status='pagado').aggregate(total=Sum('total'))['total'] or 0
    revenue_trend = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    # Orders count
    current_orders_count = current_orders.count()
    prev_orders_count = prev_orders.count()
    orders_trend = ((current_orders_count - prev_orders_count) / prev_orders_count * 100) if prev_orders_count > 0 else 0
    
    # AOV
    current_aov = current_revenue / current_orders_count if current_orders_count > 0 else 0
    prev_aov = prev_revenue / prev_orders_count if prev_orders_count > 0 else 0
    aov_trend = ((current_aov - prev_aov) / prev_aov * 100) if prev_aov > 0 else 0
    
    # Conversion rate (simplified - orders / visits would need analytics)
    # Using a placeholder based on orders vs carts
    from apps.cart.models import Cart
    current_carts = Cart.objects.filter(created_at__gte=start_date).count()
    prev_carts = Cart.objects.filter(created_at__gte=prev_start, created_at__lt=start_date).count()
    current_conversion = (current_orders_count / current_carts * 100) if current_carts > 0 else 0
    prev_conversion = (prev_orders_count / prev_carts * 100) if prev_carts > 0 else 0
    conversion_trend = ((current_conversion - prev_conversion) / prev_conversion * 100) if prev_conversion > 0 else 0
    
    # Sales chart data (daily revenue)
    sales_by_day = current_orders.filter(payment_status='pagado').extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(total=Sum('total')).order_by('day')
    
    sales_labels = []
    sales_values = []
    for i in range(days):
        day = (start_date + timedelta(days=i)).date()
        sales_labels.append(day.strftime('%d/%m'))
        day_total = next((item['total'] for item in sales_by_day if item['day'] == day), 0)
        sales_values.append(float(day_total or 0))
    
    # Category chart
    category_sales = OrderItem.objects.filter(order__in=current_orders, order__payment_status='pagado').select_related('product__category').values('product__category__name').annotate(
        revenue=Sum('subtotal'),
        units=Sum('quantity')
    ).order_by('-revenue')[:8]
    
    cat_labels = [c['product__category__name'] or 'Sin categoría' for c in category_sales]
    cat_values = [float(c['revenue'] or 0) for c in category_sales]
    
    # Top products
    top_products = OrderItem.objects.filter(order__in=current_orders, order__payment_status='pagado').select_related('product__category', 'product__brand', 'product__images').values(
        'product__id', 'product__name', 'product__brand__name', 'product__category__name'
    ).annotate(
        units_sold=Sum('quantity'),
        revenue=Sum('subtotal')
    ).order_by('-units_sold')[:10]
    
    top_products_data = []
    for tp in top_products:
        # Get primary image
        from apps.catalog.models import ProductImage
        img = ProductImage.objects.filter(product_id=tp['product__id']).first()
        top_products_data.append({
            'name': tp['product__name'],
            'brand': tp['product__brand__name'] or '',
            'category': tp['product__category__name'] or 'Sin categoría',
            'units_sold': tp['units_sold'] or 0,
            'revenue': float(tp['revenue'] or 0),
            'aov': float(tp['revenue'] / tp['units_sold']) if tp['units_sold'] else 0,
            'image': img.image.url if img else None
        })
    
    # Recent orders
    recent_orders_qs = Order.objects.select_related('user').order_by('-created_at')[:10]
    recent_orders = []
    for o in recent_orders_qs:
        recent_orders.append({
            'id': o.id,
            'order_number': o.order_number,
            'client_name': o.client_name,
            'client_email': o.client_email,
            'total': float(o.total),
            'status': o.status,
            'created_at': o.created_at.isoformat()
        })
    
    # Low stock products
    from apps.catalog.models import Product
    low_stock = Product.objects.filter(is_active=True, stock__lte=5, stock__gt=0).select_related('category', 'brand', 'images')[:10]
    low_stock_data = []
    for p in low_stock:
        img = p.images.first()
        low_stock_data.append({
            'name': p.name,
            'brand': p.brand.name,
            'category': p.category.name,
            'stock': p.stock,
            'image': img.image.url if img else None
        })
    
    # Top categories table
    top_categories = OrderItem.objects.filter(order__in=current_orders, order__payment_status='pagado').select_related('product__category').values(
        'product__category__name'
    ).annotate(
        units_sold=Sum('quantity'),
        revenue=Sum('subtotal')
    ).order_by('-revenue')[:10]
    
    top_categories_data = []
    for tc in top_categories:
        top_categories_data.append({
            'name': tc['product__category__name'] or 'Sin categoría',
            'units_sold': tc['units_sold'] or 0,
            'revenue': float(tc['revenue'] or 0)
        })
    
    # Status chart
    status_counts = current_orders.values('status').annotate(count=Count('id')).order_by('-count')
    status_labels = [s['status'] for s in status_counts]
    status_values = [s['count'] for s in status_counts]
    
    # Top products chart
    top_products_chart = OrderItem.objects.filter(order__in=current_orders, order__payment_status='pagado').select_related('product').values(
        'product__name'
    ).annotate(
        units=Sum('quantity')
    ).order_by('-units')[:10]
    
    return JsonResponse({
        'revenue': float(current_revenue),
        'revenue_trend': round(revenue_trend, 1),
        'orders_count': current_orders_count,
        'orders_trend': round(orders_trend, 1),
        'aov': round(current_aov, 2),
        'aov_trend': round(aov_trend, 1),
        'conversion_rate': round(current_conversion, 2),
        'conversion_trend': round(conversion_trend, 1),
        'sales_chart': {'labels': sales_labels, 'values': sales_values},
        'category_chart': {'labels': cat_labels, 'values': cat_values},
        'top_products_chart': {
            'labels': [p['product__name'] for p in top_products_chart],
            'values': [p['units'] for p in top_products_chart]
        },
        'top_products': top_products_data,
        'recent_orders': recent_orders,
        'low_stock': low_stock_data,
        'top_categories': top_categories_data,
        'status_chart': {'labels': status_labels, 'values': status_values},
    })