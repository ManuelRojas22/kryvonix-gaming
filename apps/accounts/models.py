"""
Models for VEXOR GAMING Accounts app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Extended user model with additional fields."""
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(
        _('phone'),
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    newsletter = models.BooleanField(_('newsletter'), default=False)
    email_verified = models.BooleanField(_('email verified'), default=False)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username


class Address(models.Model):
    """User address for shipping/billing."""
    ADDRESS_TYPES = [
        ('shipping', _('Envío')),
        ('billing', _('Facturación')),
        ('both', _('Ambas')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('usuario')
    )
    type = models.CharField(_('tipo'), max_length=10, choices=ADDRESS_TYPES, default='shipping')
    is_default = models.BooleanField(_('predeterminada'), default=False)

    # Address fields
    full_name = models.CharField(_('nombre completo'), max_length=100)
    phone = models.CharField(_('teléfono'), max_length=20)
    address_line1 = models.CharField(_('dirección línea 1'), max_length=200)
    address_line2 = models.CharField(_('dirección línea 2'), max_length=200, blank=True)
    city = models.CharField(_('ciudad'), max_length=100)
    state = models.CharField(_('estado/departamento'), max_length=100)
    postal_code = models.CharField(_('código postal'), max_length=20)
    country = models.CharField(_('país'), max_length=100, default='Colombia')

    # Metadata
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        verbose_name = _('dirección')
        verbose_name_plural = _('direcciones')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.city}, {self.country}'

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, type=self.type, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def get_full_address(self):
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(parts)


class EmailVerificationToken(models.Model):
    """Token for email verification."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = _('token de verificación')
        verbose_name_plural = _('tokens de verificación')

    def __str__(self):
        return f'Token for {self.user.email}'

    def is_valid(self):
        from django.utils import timezone
        return self.expires_at > timezone.now()


class PasswordResetToken(models.Model):
    """Token for password reset."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('token de reset de contraseña')
        verbose_name_plural = _('tokens de reset de contraseña')

    def __str__(self):
        return f'Reset token for {self.user.email}'

    def is_valid(self):
        from django.utils import timezone
        return not self.used and self.expires_at > timezone.now()