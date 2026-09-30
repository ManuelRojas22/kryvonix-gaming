"""
Tests for VEXOR GAMING Catalog app.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Brand, Product, ProductSpec


class ModelTests(TestCase):
    """Test catalog models."""

    def setUp(self):
        self.category = Category.objects.create(
            name='Tarjetas Gráficas',
            slug='tarjetas-graficas',
            description='GPUs para gaming'
        )
        self.brand = Brand.objects.create(
            name='NVIDIA',
            slug='nvidia'
        )
        self.product = Product.objects.create(
            name='RTX 4090',
            slug='rtx-4090',
            description='Tarjeta gráfica de alta gama',
            price=Decimal('1999.99'),
            discount_price=Decimal('1799.99'),
            stock=10,
            warranty_months=36,
            brand=self.brand,
            category=self.category,
            is_active=True
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Tarjetas Gráficas')

    def test_category_slug_auto_generation(self):
        cat = Category.objects.create(name='Procesadores')
        self.assertEqual(cat.slug, 'procesadores')

    def test_brand_str(self):
        self.assertEqual(str(self.brand), 'NVIDIA')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'RTX 4090')

    def test_product_has_discount_true(self):
        self.assertTrue(self.product.has_discount)

    def test_product_has_discount_false(self):
        product_no_discount = Product.objects.create(
            name='RTX 4080',
            slug='rtx-4080',
            description='Otra GPU',
            price=Decimal('1199.99'),
            stock=5,
            brand=self.brand,
            category=self.category
        )
        self.assertFalse(product_no_discount.has_discount)

    def test_product_discount_percent(self):
        self.assertEqual(self.product.discount_percent, 10)

    def test_product_discount_percent_no_discount(self):
        product_no_discount = Product.objects.create(
            name='RTX 4080',
            slug='rtx-4080',
            description='Otra GPU',
            price=Decimal('1199.99'),
            stock=5,
            brand=self.brand,
            category=self.category
        )
        self.assertEqual(product_no_discount.discount_percent, 0)

    def test_product_current_price_with_discount(self):
        self.assertEqual(self.product.current_price, Decimal('1799.99'))

    def test_product_current_price_without_discount(self):
        product_no_discount = Product.objects.create(
            name='RTX 4080',
            slug='rtx-4080',
            description='Otra GPU',
            price=Decimal('1199.99'),
            stock=5,
            brand=self.brand,
            category=self.category
        )
        self.assertEqual(product_no_discount.current_price, Decimal('1199.99'))

    def test_product_in_stock_true(self):
        self.assertTrue(self.product.in_stock)

    def test_product_in_stock_false(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)

    def test_product_slug_auto_generation(self):
        prod = Product.objects.create(
            name='Nueva GPU',
            description='Test',
            price=Decimal('500'),
            stock=1,
            brand=self.brand,
            category=self.category
        )
        self.assertTrue(prod.slug.startswith('nueva-gpu'))

    def test_product_spec_unique_together(self):
        ProductSpec.objects.create(product=self.product, name='VRAM', value='24 GB GDDR6X')
        with self.assertRaises(Exception):
            ProductSpec.objects.create(product=self.product, name='VRAM', value='12 GB GDDR6X')


class ViewTests(TestCase):
    """Test catalog views."""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Tarjetas Gráficas',
            slug='tarjetas-graficas'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.product = Product.objects.create(
            name='RTX 4090',
            slug='rtx-4090',
            description='Mejor GPU',
            price=Decimal('1999.99'),
            discount_price=Decimal('1799.99'),
            stock=10,
            brand=self.brand,
            category=self.category,
            is_active=True,
            is_featured=True
        )
        # Create more products for pagination tests
        for i in range(15):
            Product.objects.create(
                name=f'Producto {i}',
                slug=f'producto-{i}',
                description=f'Desc {i}',
                price=Decimal('100.00'),
                stock=5,
                brand=self.brand,
                category=self.category,
                is_active=True
            )

    def test_home_view(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')
        self.assertIn('featured_products', response.context)
        self.assertIn('best_sellers', response.context)
        self.assertIn('new_arrivals', response.context)

    def test_shop_view(self):
        response = self.client.get(reverse('catalog:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/shop.html')
        self.assertIn('products', response.context)

    def test_shop_view_with_category(self):
        response = self.client.get(reverse('catalog:shop_category', kwargs={'category_slug': 'tarjetas-graficas'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'], self.category)

    def test_shop_view_with_search(self):
        response = self.client.get(reverse('catalog:shop') + '?q=RTX')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RTX 4090')

    def test_shop_view_with_brand_filter(self):
        response = self.client.get(reverse('catalog:shop') + '?brand=nvidia')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RTX 4090')

    def test_shop_view_with_price_filter(self):
        response = self.client.get(reverse('catalog:shop') + '?min_price=1000&max_price=2000')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RTX 4090')

    def test_shop_view_with_stock_filter(self):
        response = self.client.get(reverse('catalog:shop') + '?in_stock=true')
        self.assertEqual(response.status_code, 200)

    def test_shop_view_with_sort(self):
        response = self.client.get(reverse('catalog:shop') + '?sort=price_asc')
        self.assertEqual(response.status_code, 200)

    def test_shop_view_pagination(self):
        response = self.client.get(reverse('catalog:shop') + '?page=2')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': 'rtx-4090'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertIn('related_products', response.context)

    def test_product_detail_404(self):
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': 'no-existe'}))
        self.assertEqual(response.status_code, 404)

    def test_product_detail_inactive_product_404(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': 'rtx-4090'}))
        self.assertEqual(response.status_code, 404)

    def test_404_handler(self):
        response = self.client.get('/pagina-que-no-existe/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')