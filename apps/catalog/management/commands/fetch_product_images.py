import urllib.parse
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.catalog.models import Product, ProductImage


DUMMYIMAGE_BASE = "https://dummyimage.com/800x600/000/fff.png"


class Command(BaseCommand):
    help = 'Generate placeholder images with product name using dummyimage.com'

    def handle(self, *args, **options):
        products = Product.objects.filter(is_active=True).prefetch_related('images')
        added = 0
        for product in products:
            if product.images.exists():
                self.stdout.write(f'Skipping {product.name} (already has images)')
                continue

            text = urllib.parse.quote(product.name)
            url = f"{DUMMYIMAGE_BASE}&text={text}"
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                image_name = f"{product.slug}.png"
                product_image = ProductImage(product=product, order=0, alt_text=product.name)
                product_image.image.save(image_name, ContentFile(resp.content), save=True)
                self.stdout.write(self.style.SUCCESS(f'Added image to {product.name}'))
                added += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed for {product.name}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Added images to {added} products.'))