"""
Signals for VEXOR GAMING Catalog app.
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product, ProductImage


@receiver(post_save, sender=ProductImage)
def set_primary_image(sender, instance, created, **kwargs):
    """Ensure first image is primary when created."""
    if created and instance.order == 0:
        # Mark other images as non-primary (order > 0)
        ProductImage.objects.filter(product=instance.product).exclude(pk=instance.pk).update(order=1)


@receiver(pre_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    """Delete image file from storage when model is deleted."""
    if instance.image:
        instance.image.delete(save=False)