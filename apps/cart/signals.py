"""
Signals for VEXOR GAMING Cart app.
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Cart, CartItem

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Create cart for new user."""
    if created:
        Cart.objects.get_or_create(user=instance)


@receiver(pre_delete, sender=CartItem)
def update_cart_timestamp(sender, instance, **kwargs):
    """Update cart timestamp when item is deleted."""
    if instance.cart_id:
        Cart.objects.filter(id=instance.cart_id).update(updated_at=timezone.now())