"""
Signals for VEXOR GAMING Wishlist app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Wishlist

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    """Create wishlist for new user."""
    if created:
        Wishlist.objects.get_or_create(user=instance)