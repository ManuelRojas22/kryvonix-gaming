"""
Views for VEXOR GAMING Catalog app.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.conf import settings
from .models import Product, Category, Brand


def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)


def handler500(request):
    """Custom 500 error handler."""
    return render(request, '500.html', status=500)


def home(request):
    """Home page with hero, featured products, best sellers, new arrivals."""
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True
    ).select_related('brand', 'category').prefetch_related('images')[:settings.FEATURED_PRODUCTS_COUNT]

    best_sellers = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').prefetch_related('images').order_by('-units_sold')[:8]

    new_arrivals = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').prefetch_related('images').order_by('-created_at')[:8]

    categories = Category.objects.filter(is_active=True).annotate(
        products_count=Count('products', filter=Q(products__is_active=True))
    ).filter(products_count__gt=0)[:6]

    context = {
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'catalog/home.html', context)


def shop(request, category_slug=None):
    """Shop page with filtering, sorting, and pagination."""
    products = Product.objects.filter(is_active=True).select_related('brand', 'category').prefetch_related('images')

    # Category filter
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    # GET parameters
    query = request.GET.get('q', '').strip()
    brand_slug = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')
    sort = request.GET.get('sort', 'newest')

    # Text search
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Brand filter
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Price range filter
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Stock filter
    if in_stock == 'true':
        products = products.filter(stock__gt=0)

    # Sorting
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'best_sellers': '-units_sold',
        'newest': '-created_at',
        'discount': '-discount_price',  # Products with discount first
    }
    order_by = sort_options.get(sort, '-created_at')
    if sort == 'discount':
        # Custom ordering: has_discount first, then by discount percent
        products = products.extra(
            select={'has_discount': 'CASE WHEN discount_price IS NOT NULL AND discount_price < price THEN 1 ELSE 0 END'}
        ).order_by('-has_discount', '-discount_price')
    else:
        products = products.order_by(order_by)

    # Pagination
    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    # Get filter options for sidebar
    brands = Brand.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).filter(product_count__gt=0)

    all_categories = Category.objects.filter(is_active=True).annotate(
        products_count=Count('products', filter=Q(products__is_active=True))
    ).filter(products_count__gt=0)

    context = {
        'products': products_page,
        'category': category,
        'categories': all_categories,
        'brands': brands,
        'query': query,
        'selected_brand': brand_slug,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort': sort,
        'sort_options': [
            ('newest', 'Más recientes'),
            ('price_asc', 'Precio: menor a mayor'),
            ('price_desc', 'Precio: mayor a menor'),
            ('best_sellers', 'Más vendidos'),
            ('discount', 'Mayor descuento'),
        ],
    }
    return render(request, 'catalog/shop.html', context)


def product_detail(request, slug):
    """Product detail page with gallery, specs, and related products."""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category').prefetch_related('images', 'specs'),
        slug=slug,
        is_active=True
    )

    related_products = product.get_related_products(settings.RELATED_PRODUCTS_COUNT)

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)


def pc_builder(request):
    """PC Builder page: select compatible components and see approximate total price."""
    # Define the categories we need for a PC build
    category_slugs = [
        'procesadores',          # CPU
        'tarjetas-graficas',     # GPU
        'memoria-ram',           # RAM
        'placas-base',           # Motherboard
        'fuentes-poder',         # PSU
        'gabinetes',             # Case
        'almacenamiento',        # Storage (SSD/HDD)
    ]

    categories = Category.objects.filter(slug__in=category_slugs, is_active=True).prefetch_related(
        'products'
    )

    # Build a dict: category_slug -> list of active products (with price)
    components = {}
    for cat in categories:
        products = cat.products.filter(is_active=True).select_related('brand').order_by('price')
        components[cat.slug] = [
            {
                'id': p.id,
                'name': p.name,
                'brand': p.brand.name,
                'price': float(p.current_price),
                'slug': p.slug,
                'image': p.primary_image.image.url if p.primary_image else None,
            }
            for p in products
        ]

    context = {
        'components': components,
        'category_order': category_slugs,
    }
    return render(request, 'catalog/pc_builder.html', context)