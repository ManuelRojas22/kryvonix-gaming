"""
Context processors for VEXOR GAMING Cart app.
"""
from .utils import get_cart


def cart(request):
    """Add cart info to all templates."""
    cart = get_cart(request)
    return {
        'cart': cart,
        'cart_count': cart.item_count if cart else 0,
        'cart_total': cart.total_price if cart else 0,
    }