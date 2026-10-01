"""
Utility functions for VEXOR GAMING Wishlist app.
"""
from .models import Wishlist


def get_or_create_wishlist(request):
    """Get or create wishlist for current user."""
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return wishlist
    return None


def get_wishlist(request):
    """Get wishlist without creating if doesn't exist."""
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user).first()
    return None