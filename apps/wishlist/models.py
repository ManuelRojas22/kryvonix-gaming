"""
Models for VEXOR GAMING Wishlist app.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.catalog.models import Product


class Wishlist(models.Model):
    """User's wishlist."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist',
        verbose_name=_('usuario')
    )
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        verbose_name = _('lista de deseos')
        verbose_name_plural = _('listas de deseos')

    def __str__(self):
        return f'Wishlist de {self.user.email}'

    @property
    def item_count(self):
        return self.items.count()

    def has_product(self, product):
        return self.items.filter(product=product).exists()

    def add_product(self, product):
        """Add product to wishlist."""
        item, created = self.items.get_or_create(product=product)
        return item, created

    def remove_product(self, product):
        """Remove product from wishlist."""
        return self.items.filter(product=product).delete()


class WishlistItem(models.Model):
    """Individual item in a wishlist."""
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('lista de deseos')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        verbose_name=_('producto')
    )
    added_at = models.DateTimeField(_('añadido el'), auto_now_add=True)
    notify_price_drop = models.BooleanField(_('notificar bajada de precio'), default=True)
    notify_back_in_stock = models.BooleanField(_('notificar disponibilidad'), default=True)

    class Meta:
        verbose_name = _('item de lista de deseos')
        verbose_name_plural = _('items de lista de deseos')
        unique_together = ['wishlist', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.product.name} en wishlist de {self.wishlist.user.email}'

    @property
    def current_price(self):
        return self.product.current_price

    @property
    def price_when_added(self):
        # Could store historical price, for now return current
        return self.current_price

    @property
    def price_dropped(self):
        return self.current_price < self.price_when_added

    @property
    def savings(self):
        if self.price_dropped:
            return self.price_when_added - self.current_price
        return 0

    @property
    def discount_percent(self):
        if self.price_dropped and self.price_when_added > 0:
            return round((1 - self.current_price / self.price_when_added) * 100)
        return 0