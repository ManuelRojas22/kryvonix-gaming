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