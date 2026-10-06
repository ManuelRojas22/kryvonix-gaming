"""
Models for VEXOR GAMING Cart app.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.catalog.models import Product


class Cart(models.Model):
    """Shopping cart - can be tied to user or session."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name=_('usuario')
    )
    session_key = models.CharField(_('clave de sesión'), max_length=40, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        verbose_name = _('carrito')
        verbose_name_plural = _('carritos')

    def __str__(self):
        if self.user:
            return f'Carrito de {self.user.email}'
        return f'Carrito anónimo ({self.session_key[:8]})'

    @property
    def item_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.select_related('product'))

    @property
    def total_items(self):
        return self.items.count()

    def merge_with(self, other_cart):
        """Merge another cart into this one."""
        for item in other_cart.items.all():
            self.add_item(item.product, item.quantity)
        other_cart.delete()

    def add_item(self, product, quantity=1):
        """Add or update item in cart."""
        item, created = self.items.get_or_create(
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item


class CartItem(models.Model):
    """Individual item in a cart."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('carrito')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name=_('producto')
    )
    quantity = models.PositiveIntegerField(_('cantidad'), default=1)
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        verbose_name = _('item del carrito')
        verbose_name_plural = _('items del carrito')
        unique_together = ['cart', 'product']

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    @property
    def unit_price(self):
        return self.product.current_price

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.quantity > self.product.stock:
            raise ValidationError(_('No hay suficiente stock disponible.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update cart timestamp
        self.cart.save(update_fields=['updated_at'])


class Order(models.Model):
    """Order placed by a customer."""
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    # Order identification
    order_number = models.CharField(_('número de pedido'), max_length=20, unique=True, blank=True)
    
    # Customer info
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('usuario')
    )
    client_name = models.CharField(_('nombre del cliente'), max_length=200)
    client_email = models.EmailField(_('email del cliente'))
    client_phone = models.CharField(_('teléfono'), max_length=20, blank=True)
    
    # Shipping address
    shipping_address = models.TextField(_('dirección de envío'))
    shipping_city = models.CharField(_('ciudad'), max_length=100, blank=True)
    shipping_postal_code = models.CharField(_('código postal'), max_length=20, blank=True)
    shipping_country = models.CharField(_('país'), max_length=100, blank=True, default='Colombia')
    
    # Financial
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(_('costo de envío'), max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(_('impuestos'), max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(_('descuento'), max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(_('estado'), max_length=20, choices=STATUS_CHOICES, default='pendiente')
    payment_status = models.CharField(_('estado de pago'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pendiente')
    payment_method = models.CharField(_('método de pago'), max_length=50, blank=True)
    transaction_id = models.CharField(_('ID de transacción'), max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(_('notas internas'), blank=True)
    customer_notes = models.TextField(_('notas del cliente'), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)
    shipped_at = models.DateTimeField(_('enviado el'), null=True, blank=True)
    delivered_at = models.DateTimeField(_('entregado el'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('pedido')
        verbose_name_plural = _('pedidos')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f'Pedido #{self.order_number or self.pk}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXX
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            random_part = f'{random.randint(1000, 9999)}'
            self.order_number = f'ORD-{date_str}-{random_part}'
        super().save(*args, **kwargs)
    
    @property
    def items_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def is_paid(self):
        return self.payment_status == 'pagado'
    
    def can_ship(self):
        return self.status in ['procesando', 'pendiente'] and self.is_paid


class OrderItem(models.Model):
    """Individual item in an order."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('pedido')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('producto')
    )
    product_name = models.CharField(_('nombre del producto'), max_length=200)
    product_sku = models.CharField(_('SKU'), max_length=100, blank=True)
    brand_name = models.CharField(_('marca'), max_length=100, blank=True)
    
    quantity = models.PositiveIntegerField(_('cantidad'), default=1)
    unit_price = models.DecimalField(_('precio unitario'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_('precio con descuento'), max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('item del pedido')
        verbose_name_plural = _('items del pedido')
    
    def __str__(self):
        return f'{self.quantity}x {self.product_name}'
    
    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.unit_price
    
    @property
    def subtotal(self):
        return self.effective_price * self.quantity