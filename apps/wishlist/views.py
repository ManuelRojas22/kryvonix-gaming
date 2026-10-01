"""
Views for VEXOR GAMING Wishlist app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import Wishlist, WishlistItem
from .utils import get_or_create_wishlist, get_wishlist
from apps.catalog.models import Product


@login_required
def wishlist_detail(request):
    """Wishlist page."""
    wishlist = get_or_create_wishlist(request)
    return render(request, 'wishlist/detail.html', {'wishlist': wishlist})


@login_required
@require_http_methods(["POST"])
def wishlist_add(request, product_id):
    """Add product to wishlist."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)

    item, created = wishlist.add_product(product)

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'added': created,
            'wishlist_count': wishlist.item_count,
            'message': f'{product.name} {"añadido a" if created else "ya está en"} tu lista de deseos'
        })

    if created:
        messages.success(request, f'{product.name} añadido a tu lista de deseos.')
    else:
        messages.info(request, f'{product.name} ya está en tu lista de deseos.')

    return redirect('wishlist:detail')


@login_required
@require_http_methods(["POST"])
def wishlist_remove(request, product_id):
    """Remove product from wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request)

    deleted, _ = wishlist.remove_product(product)

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'wishlist_count': wishlist.item_count,
            'message': f'{product.name} eliminado de tu lista de deseos'
        })

    if deleted:
        messages.success(request, f'{product.name} eliminado de tu lista de deseos.')
    else:
        messages.error(request, 'El producto no estaba en tu lista de deseos.')

    return redirect('wishlist:detail')


@login_required
@require_http_methods(["POST"])
def wishlist_toggle_notify(request, product_id):
    """Toggle notification preferences for wishlist item."""
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request)

    item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)

    notify_type = request.POST.get('notify_type')
    if notify_type == 'price':
        item.notify_price_drop = not item.notify_price_drop
    elif notify_type == 'stock':
        item.notify_back_in_stock = not item.notify_back_in_stock
    item.save()

    return JsonResponse({
        'success': True,
        'notify_price_drop': item.notify_price_drop,
        'notify_back_in_stock': item.notify_back_in_stock
    })


@login_required
def wishlist_count(request):
    """Get wishlist item count (AJAX)."""
    wishlist = get_wishlist(request)
    count = wishlist.item_count if wishlist else 0
    return JsonResponse({'count': count})


@login_required
def wishlist_move_to_cart(request, product_id):
    """Move item from wishlist to cart."""
    from apps.cart.utils import get_or_create_cart

    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)
    cart = get_or_create_cart(request)

    # Remove from wishlist
    wishlist.remove_product(product)

    # Add to cart
    quantity = 1
    if quantity > product.stock:
        messages.error(request, 'No hay suficiente stock disponible.')
        return redirect('wishlist:detail')

    item, created = cart.items.get_or_create(
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, 'No hay suficiente stock disponible.')
            return redirect('wishlist:detail')
        item.quantity = new_quantity
        item.save()

    messages.success(request, f'{product.name} movido al carrito.')
    return redirect('cart:detail')