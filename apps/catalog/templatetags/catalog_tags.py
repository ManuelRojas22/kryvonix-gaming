"""
Custom template tags for VEXOR GAMING Catalog app.
"""
from django import template

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