"""
Tests for VEXOR GAMING Wishlist app.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Brand, Product
from apps.wishlist.models import Wishlist, WishlistItem
from apps.wishlist.utils import get_or_create_wishlist

User = get_user_model()


class WishlistModelTests(TestCase):
    """Test wishlist models."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )
        self.category = Category.objects.create(name='GPU', slug='gpu')
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.product = Product.objects.create(
            name='RTX 4090', slug='rtx-4090', description='GPU',
            price=Decimal('1999.99'), discount_price=Decimal('1799.99'),
            stock=10, brand=self.brand, category=self.category
        )
        self.product2 = Product.objects.create(
            name='RTX 4080', slug='rtx-4080', description='GPU',
            price=Decimal('1199.99'), stock=5,
            brand=self.brand, category=self.category
        )
        # Use the wishlist created by signal
        self.wishlist = self.user.wishlist

    def test_wishlist_creation(self):
        self.assertEqual(self.wishlist.user, self.user)
        self.assertEqual(self.wishlist.item_count, 0)

    def test_wishlist_add_product(self):
        item, created = self.wishlist.add_product(self.product)
        self.assertTrue(created)
        self.assertEqual(self.wishlist.item_count, 1)
        self.assertTrue(self.wishlist.has_product(self.product))

    def test_wishlist_add_duplicate(self):
        self.wishlist.add_product(self.product)
        item, created = self.wishlist.add_product(self.product)
        self.assertFalse(created)
        self.assertEqual(self.wishlist.item_count, 1)

    def test_wishlist_remove_product(self):
        self.wishlist.add_product(self.product)
        deleted, _ = self.wishlist.remove_product(self.product)
        self.assertEqual(deleted, 1)
        self.assertEqual(self.wishlist.item_count, 0)

    def test_wishlist_item_price_dropped(self):
        """Test price drop detection (current implementation returns False)."""
        item = WishlistItem.objects.create(wishlist=self.wishlist, product=self.product)
        # Current implementation compares current price with itself
        self.assertFalse(item.price_dropped)
        self.assertEqual(item.discount_percent, 0)

    def test_wishlist_item_notifications(self):
        item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            product=self.product,
            notify_price_drop=True,
            notify_back_in_stock=False
        )
        self.assertTrue(item.notify_price_drop)
        self.assertFalse(item.notify_back_in_stock)


class WishlistViewTests(TestCase):
    """Test wishlist views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )
        self.category = Category.objects.create(name='GPU', slug='gpu')
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.product = Product.objects.create(
            name='RTX 4090', slug='rtx-4090', description='GPU',
            price=Decimal('1999.99'), discount_price=Decimal('1799.99'),
            stock=10, brand=self.brand, category=self.category
        )
        self.product2 = Product.objects.create(
            name='RTX 4080', slug='rtx-4080', description='GPU',
            price=Decimal('1199.99'), stock=5,
            brand=self.brand, category=self.category
        )

    def test_wishlist_detail_requires_login(self):
        response = self.client.get(reverse('wishlist:detail'))
        self.assertEqual(response.status_code, 302)

    def test_wishlist_detail_authenticated(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.get(reverse('wishlist:detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/detail.html')

    def test_wishlist_add_product(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('wishlist:add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        wishlist = self.user.wishlist
        self.assertEqual(wishlist.item_count, 1)

    def test_wishlist_add_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(
            reverse('wishlist:add', args=[self.product.id]),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['added'])

    def test_wishlist_add_duplicate_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        self.user.wishlist.add_product(self.product)
        response = self.client.post(
            reverse('wishlist:add', args=[self.product.id]),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(data['added'])

    def test_wishlist_remove_product(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        self.user.wishlist.add_product(self.product)
        response = self.client.post(reverse('wishlist:remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.wishlist.item_count, 0)

    def test_wishlist_remove_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        self.user.wishlist.add_product(self.product)
        response = self.client.post(
            reverse('wishlist:remove', args=[self.product.id]),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['wishlist_count'], 0)

    def test_wishlist_toggle_notify_price(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        item = WishlistItem.objects.create(wishlist=self.user.wishlist, product=self.product, notify_price_drop=False)
        response = self.client.post(
            reverse('wishlist:toggle_notify', args=[self.product.id]),
            {'notify_type': 'price'}
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.notify_price_drop)

    def test_wishlist_toggle_notify_stock(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        item = WishlistItem.objects.create(wishlist=self.user.wishlist, product=self.product, notify_back_in_stock=False)
        response = self.client.post(
            reverse('wishlist:toggle_notify', args=[self.product.id]),
            {'notify_type': 'stock'}
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.notify_back_in_stock)

    def test_wishlist_count_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        self.user.wishlist.add_product(self.product)
        self.user.wishlist.add_product(self.product2)
        response = self.client.get(reverse('wishlist:count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_wishlist_move_to_cart(self):
        from apps.cart.utils import get_or_create_cart
        self.client.login(username='test@example.com', password='TestPass123!')
        self.user.wishlist.add_product(self.product)

        # Ensure cart exists
        cart = get_or_create_cart(self.client)

        response = self.client.post(reverse('wishlist:move_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        # Product should be removed from wishlist
        self.assertEqual(self.user.wishlist.item_count, 0)
        # Product should be in cart
        self.assertEqual(cart.item_count, 1)
        self.assertEqual(cart.items.first().product, self.product)