"""
Custom template tags for VEXOR GAMING Catalog app.
"""
from django import template
from django.templatetags.static import static
import os
from django.conf import settings

register = template.Library()


@register.inclusion_tag('partials/product_card.html')
def product_card(product, show_category=True, show_brand=True):
    """Render a product card."""
    return {
        'product': product,
        'show_category': show_category,
        'show_brand': show_brand,
    }


@register.simple_tag
def get_sort_label(sort_value):
    """Get human-readable label for sort option."""
    labels = {
        'newest': 'Más recientes',
        'price_asc': 'Precio: menor a mayor',
        'price_desc': 'Precio: mayor a menor',
        'best_sellers': 'Más vendidos',
        'discount': 'Mayor descuento',
    }
    return labels.get(sort_value, sort_value)


@register.simple_tag
def query_string(request, **kwargs):
    """Generate query string with updated parameters."""
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == '':
            query.pop(key, None)
        else:
            query[key] = value
    return query.urlencode()


@register.filter
def sub(value, arg):
    """Subtract arg from value."""
    try:
        return value - arg
    except Exception:
        return ''


@register.simple_tag
def static_v(path):
    """
    Return static URL with cache-busting query param based on file mtime.
    Usage: {% static_v 'css/output.css' %}
    """
    full_path = os.path.join(settings.STATIC_ROOT, path) if settings.STATIC_ROOT else ''
    # fallback to STATICFILES_DIRS search
    if not full_path or not os.path.exists(full_path):
        for static_dir in settings.STATICFILES_DIRS:
            candidate = os.path.join(static_dir, path)
            if os.path.exists(candidate):
                full_path = candidate
                break
    if full_path and os.path.exists(full_path):
        mtime = int(os.path.getmtime(full_path))
        return f"{static(path)}?v={mtime}"
    return static(path)