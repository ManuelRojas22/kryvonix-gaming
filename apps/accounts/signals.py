"""
Signals for VEXOR GAMING Accounts app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create related objects for new user."""
    if created:
        # Cart and Wishlist are created via their own signals
        pass