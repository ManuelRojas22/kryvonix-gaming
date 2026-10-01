"""
Context processors for VEXOR GAMING Wishlist app.
"""
from .utils import get_wishlist


def wishlist(request):
    """Add wishlist info to all templates."""
    wishlist = get_wishlist(request)
    return {
        'wishlist': wishlist,
        'wishlist_count': wishlist.item_count if wishlist else 0,
    }