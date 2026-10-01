"""
Utility functions for VEXOR GAMING Cart app.
"""
from django.conf import settings
from .models import Cart


CART_SESSION_KEY = 'vexor_cart_id'


def get_or_create_cart(request):
    """Get or create cart for current request (user or session)."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Merge session cart if exists
        session_cart_id = request.session.get(CART_SESSION_KEY)
        if session_cart_id and session_cart_id != cart.id:
            try:
                session_cart = Cart.objects.get(id=session_cart_id, user__isnull=True)
                cart.merge_with(session_cart)
                request.session[CART_SESSION_KEY] = cart.id
            except Cart.DoesNotExist:
                pass
        return cart
    else:
        cart_id = request.session.get(CART_SESSION_KEY)
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, user__isnull=True)
                return cart
            except Cart.DoesNotExist:
                pass

        cart = Cart.objects.create(session_key=request.session.session_key)
        request.session[CART_SESSION_KEY] = cart.id
        return cart


def get_cart(request):
    """Get cart without creating if doesn't exist."""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get(CART_SESSION_KEY)
        if cart_id:
            return Cart.objects.filter(id=cart_id, user__isnull=True).first()
    return None


def transfer_cart_to_user(session_cart, user):
    """Transfer anonymous cart to user on login."""
    user_cart, created = Cart.objects.get_or_create(user=user)
    user_cart.merge_with(session_cart)
    return user_cart