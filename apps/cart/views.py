"""
Views for VEXOR GAMING Cart app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Cart, CartItem
from .utils import get_or_create_cart, get_cart
from apps.catalog.models import Product


def cart_detail(request):
    """Cart detail page."""
    cart = get_or_create_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_http_methods(["POST"])
def cart_add(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)

    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        if request.headers.get('HX-Request'):
            return JsonResponse({'success': False, 'error': 'Stock insuficiente'}, status=400)
        messages.error(request, 'No hay suficiente stock disponible.')
        return redirect('catalog:product_detail', slug=product.slug)

    item, created = cart.items.get_or_create(
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            if request.headers.get('HX-Request'):
                return JsonResponse({'success': False, 'error': 'Stock insuficiente'}, status=400)
            messages.error(request, 'No hay suficiente stock disponible.')
            return redirect('catalog:product_detail', slug=product.slug)
        item.quantity = new_quantity
        item.save()

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total_price),
            'message': f'{product.name} añadido al carrito'
        })

    messages.success(request, f'{product.name} añadido al carrito.')
    return redirect('cart:detail')


@require_http_methods(["POST"])
def cart_update(request, item_id):
    """Update cart item quantity."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        item.delete()
        message = 'Producto eliminado del carrito.'
    elif quantity > item.product.stock:
        if request.headers.get('HX-Request'):
            return JsonResponse({'success': False, 'error': 'Stock insuficiente'}, status=400)
        messages.error(request, 'No hay suficiente stock disponible.')
        return redirect('cart:detail')
    else:
        item.quantity = quantity
        item.save()
        message = 'Carrito actualizado.'

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total_price),
            'item_total': float(item.total_price),
            'message': message
        })

    messages.success(request, message)
    return redirect('cart:detail')


@require_http_methods(["POST"])
def cart_remove(request, item_id):
    """Remove item from cart."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.product.name
    item.delete()

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total_price),
            'message': f'{product_name} eliminado del carrito'
        })

    messages.success(request, f'{product_name} eliminado del carrito.')
    return redirect('cart:detail')


@require_http_methods(["POST"])
def cart_clear(request):
    """Clear entire cart."""
    cart = get_cart(request)
    if cart:
        cart.items.all().delete()

    if request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'cart_count': 0,
            'cart_total': 0,
            'message': 'Carrito vaciado'
        })

    messages.success(request, 'Carrito vaciado.')
    return redirect('cart:detail')


def cart_count(request):
    """Get cart item count (AJAX)."""
    cart = get_cart(request)
    count = cart.item_count if cart else 0
    total = float(cart.total_price) if cart else 0

    return JsonResponse({
        'count': count,
        'total': total
    })


def cart_drawer_content(request):
    """Return cart drawer HTML partial (for HTMX)."""
    cart = get_or_create_cart(request)
    return render(request, 'cart/partials/drawer_content.html', {'cart': cart})