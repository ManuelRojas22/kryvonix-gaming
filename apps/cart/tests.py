"""
Tests for VEXOR GAMING Cart app.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Brand, Product
from apps.cart.models import Cart, CartItem
from apps.cart.utils import get_or_create_cart

User = get_user_model()


class CartModelTests(TestCase):
    """Test cart models."""

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
            price=Decimal('1999.99'), stock=10,
            brand=self.brand, category=self.category
        )
        self.product2 = Product.objects.create(
            name='RTX 4080', slug='rtx-4080', description='GPU',
            price=Decimal('1199.99'), stock=5,
            brand=self.brand, category=self.category
        )

    def test_cart_creation_user(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.item_count, 0)
        self.assertEqual(cart.total_price, Decimal('0'))

    def test_cart_creation_session(self):
        cart = Cart.objects.create(session_key='abc123')
        self.assertEqual(cart.session_key, 'abc123')
        self.assertIsNone(cart.user)

    def test_cart_add_item(self):
        cart = Cart.objects.create(user=self.user)
        item = cart.add_item(self.product, 2)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(cart.item_count, 2)
        self.assertEqual(cart.total_price, Decimal('3999.98'))

    def test_cart_add_existing_item(self):
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.product, 1)
        cart.add_item(self.product, 2)
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.quantity, 3)

    def test_cart_merge(self):
        user_cart = Cart.objects.create(user=self.user)
        user_cart.add_item(self.product, 1)
        session_cart = Cart.objects.create(session_key='session123')
        session_cart.add_item(self.product2, 2)
        user_cart.merge_with(session_cart)
        self.assertEqual(user_cart.items.count(), 2)
        self.assertEqual(user_cart.item_count, 3)
        # Session cart should be deleted
        self.assertFalse(Cart.objects.filter(id=session_cart.id).exists())

    def test_cart_item_total_price(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(item.unit_price, self.product.current_price)
        self.assertEqual(item.total_price, Decimal('5999.97'))

    def test_cart_item_stock_validation(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem(cart=cart, product=self.product, quantity=15)  # More than stock
        with self.assertRaises(Exception):
            item.clean()


class CartViewTests(TestCase):
    """Test cart views."""

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

    def _get_cart_detail(self):
        return self.client.get(reverse('cart:detail'))

    def test_cart_detail_anonymous(self):
        response = self._get_cart_detail()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('cart', response.context)

    def test_cart_detail_authenticated(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self._get_cart_detail()
        self.assertEqual(response.status_code, 200)

    def test_cart_add_product(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('cart:add', args=[self.product.id]), {
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)
        cart = self.user.cart
        self.assertEqual(cart.item_count, 2)

    def test_cart_add_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(
            reverse('cart:add', args=[self.product.id]),
            {'quantity': 1},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'cart_count': 1,
            'cart_total': 1799.99,
            'message': 'RTX 4090 añadido al carrito'
        })

    def test_cart_add_insufficient_stock(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('cart:add', args=[self.product.id]), {
            'quantity': 15
        })
        self.assertEqual(response.status_code, 302)
        # Should not add to cart

    def test_cart_update_quantity(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        cart = self.user.cart
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse('cart:update', args=[item.id]), {
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_cart_update_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        cart = self.user.cart
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(
            reverse('cart:update', args=[item.id]),
            {'quantity': 2},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['item_total'], 3599.98)

    def test_cart_remove_item(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        cart = self.user.cart
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse('cart:remove', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_cart_clear(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        cart = self.user.cart
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        response = self.client.post(reverse('cart:clear'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)

    def test_cart_count_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        cart = self.user.cart
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        response = self.client.get(reverse('cart:count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)

    def test_cart_merge_on_login(self):
        # Create session cart
        session = self.client.session
        session.save()
        cart = Cart.objects.create(session_key=session.session_key)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Login
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.get(reverse('cart:detail'))

        # Check cart was merged
        user_cart = Cart.objects.get(user=self.user)
        self.assertEqual(user_cart.item_count, 2)
        # Session cart should be gone
        self.assertFalse(Cart.objects.filter(session_key=session.session_key).exists())