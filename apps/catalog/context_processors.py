"""
Context processors for VEXOR GAMING Catalog app.
"""
from .models import Category


def categories(request):
    """Add active categories to all templates for navbar."""
    return {
        'nav_categories': Category.objects.filter(is_active=True).order_by('order', 'name')[:8]
    }