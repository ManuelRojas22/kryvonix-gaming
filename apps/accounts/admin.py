"""
Admin for VEXOR GAMING Accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Address, EmailVerificationToken, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'get_full_name', 'phone', 'is_staff', 'is_active', 'newsletter', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'newsletter', 'email_verified', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'avatar')}),
        (_('Preferencias'), {'fields': ('newsletter', 'email_verified')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'type', 'is_default', 'created_at']
    list_filter = ['type', 'is_default', 'country', 'created_at']
    search_fields = ['user__email', 'full_name', 'city', 'address_line1']
    list_editable = ['is_default']
    raw_id_fields = ['user']
    ordering = ['-created_at']


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_valid']
    search_fields = ['user__email']
    readonly_fields = ['created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'used', 'is_valid']
    search_fields = ['user__email']
    readonly_fields = ['created_at']
    list_filter = ['used']