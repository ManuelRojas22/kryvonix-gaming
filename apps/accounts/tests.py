"""
Tests for VEXOR GAMING Accounts app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User, Address, EmailVerificationToken, PasswordResetToken

User = get_user_model()


class AccountsModelTests(TestCase):
    """Test accounts models."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test_model@example.com',
            username='testuser_model',
            password='TestPass123!',
            first_name='Juan',
            last_name='Pérez',
            phone='+57 300 123 4567'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('TestPass123!'))
        self.assertEqual(self.user.get_full_name(), 'Juan Pérez')
        self.assertEqual(self.user.get_short_name(), 'Juan')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_address_creation(self):
        address = Address.objects.create(
            user=self.user,
            type='shipping',
            full_name='Juan Pérez',
            phone='+57 300 123 4567',
            address_line1='Calle 123 #45-67',
            city='Bogotá',
            state='Cundinamarca',
            postal_code='110111',
            country='Colombia',
            is_default=True
        )
        self.assertEqual(address.user, self.user)
        self.assertTrue(address.is_default)
        self.assertIn('Bogotá', address.get_full_address())

    def test_address_default_single(self):
        """Only one default address per type per user."""
        Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 1',
            city='Bogotá', state='Cundinamarca', postal_code='110111',
            is_default=True
        )
        address2 = Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 2',
            city='Medellín', state='Antioquia', postal_code='050001',
            is_default=True
        )
        address2.refresh_from_db()
        # First address should no longer be default
        first = Address.objects.get(address_line1='Calle 1')
        self.assertFalse(first.is_default)
        self.assertTrue(address2.is_default)

    def test_email_verification_token(self):
        from django.utils import timezone
        from datetime import timedelta
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token='test-token-123',
            expires_at=timezone.now() + timedelta(hours=24)
        )
        self.assertTrue(token.is_valid())
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        self.assertFalse(token.is_valid())

    def test_password_reset_token(self):
        from django.utils import timezone
        from datetime import timedelta
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='reset-token-123',
            expires_at=timezone.now() + timedelta(hours=1)
        )
        self.assertTrue(token.is_valid())
        token.used = True
        token.save()
        self.assertFalse(token.is_valid())


class AccountsViewTests(TestCase):
    """Test accounts views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test_view@example.com',
            username='testuser_view',
            password='TestPass123!',
            first_name='Juan',
            last_name='Pérez'
        )

    def test_register_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_post_valid(self):
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'phone': '+57 300 111 2222',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
            'newsletter': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_post_invalid(self):
        response = self.client.post(reverse('accounts:register'), {
            'email': 'invalid-email',
            'username': 'ab',  # Too short
            'password1': 'short',
            'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Introduzca una dirección de correo electrónico válida.')

    def test_login_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_post_valid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test@example.com',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test@example.com',
            'password': 'WrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_post(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_get_authenticated(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['form'].instance, self.user)

    def test_profile_post_update(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez Gómez',
            'phone': '+57 300 999 8888',
            'newsletter': False
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Juan Carlos')
        self.assertEqual(self.user.last_name, 'Pérez Gómez')
        self.assertFalse(self.user.newsletter)

    # Address tests
    def test_address_list_requires_login(self):
        response = self.client.get(reverse('accounts:address_list'))
        self.assertEqual(response.status_code, 302)

    def test_address_list_authenticated(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 123',
            city='Bogotá', state='Cundinamarca', postal_code='110111'
        )
        response = self.client.get(reverse('accounts:address_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/address_list.html')
        self.assertContains(response, 'Calle 123')

    def test_address_create(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('accounts:address_create'), {
            'type': 'shipping',
            'full_name': 'Juan Pérez',
            'phone': '+57 300 123 4567',
            'address_line1': 'Calle 456 #78-90',
            'address_line2': 'Apto 201',
            'city': 'Medellín',
            'state': 'Antioquia',
            'postal_code': '050001',
            'country': 'Colombia',
            'is_default': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Address.objects.filter(address_line1='Calle 456 #78-90').exists())

    def test_address_edit(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        address = Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 123',
            city='Bogotá', state='Cundinamarca', postal_code='110111'
        )
        response = self.client.post(reverse('accounts:address_edit', args=[address.pk]), {
            'type': 'billing',
            'full_name': 'Juan Pérez',
            'phone': '+57 300 123 4567',
            'address_line1': 'Calle 789',
            'city': 'Cali',
            'state': 'Valle', 'postal_code': '760001',
            'country': 'Colombia',
            'is_default': False
        })
        self.assertEqual(response.status_code, 302)
        address.refresh_from_db()
        self.assertEqual(address.address_line1, 'Calle 789')
        self.assertEqual(address.type, 'billing')

    def test_address_delete(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        address = Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 123',
            city='Bogotá', state='Cundinamarca', postal_code='110111'
        )
        response = self.client.post(reverse('accounts:address_delete', args=[address.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Address.objects.filter(pk=address.pk).exists())

    def test_address_set_default_ajax(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        address1 = Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 1',
            city='Bogotá', state='Cundinamarca', postal_code='110111',
            is_default=True
        )
        address2 = Address.objects.create(
            user=self.user, type='shipping', full_name='Juan Pérez',
            phone='+57 300 123 4567', address_line1='Calle 2',
            city='Medellín', state='Antioquia', postal_code='050001'
        )
        response = self.client.post(reverse('accounts:address_set_default', args=[address2.pk]),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        address1.refresh_from_db()
        address2.refresh_from_db()
        self.assertFalse(address1.is_default)
        self.assertTrue(address2.is_default)

    # Password change
    def test_password_change(self):
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': 'TestPass123!',
            'new_password1': 'NewPass456!',
            'new_password2': 'NewPass456!',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))

    # Password reset
    def test_password_reset_request(self):
        response = self.client.post(reverse('accounts:password_reset_request'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())

    def test_password_reset_confirm(self):
        token = PasswordResetToken.objects.create(
            user=self.user, token='valid-token-123',
            expires_at=timezone.now() + timedelta(hours=1)
        )
        response = self.client.post(reverse('accounts:password_reset_confirm', args=[token.token]), {
            'new_password1': 'ResetPass789!',
            'new_password2': 'ResetPass789!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.check_password('ResetPass789!'))
        token.refresh_from_db()
        self.assertTrue(token.used)