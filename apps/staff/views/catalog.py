from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify

from apps.staff.mixins import StaffRequiredMixin
from apps.staff.forms import CategoryForm, BrandForm, ProductForm, ProductImageFormSet, ProductSpecFormSet
from apps.catalog.models import Category, Brand, Product


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