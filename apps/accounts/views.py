"""
Views for VEXOR GAMING Accounts app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import User, Address, EmailVerificationToken, PasswordResetToken
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm,
    AddressForm, PasswordChangeForm, PasswordResetRequestForm,
    PasswordResetConfirmForm
)
from apps.cart.utils import get_or_create_cart
from apps.wishlist.utils import get_or_create_wishlist


def register(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create verification token
            token = EmailVerificationToken.objects.create(
                user=user,
                token=secrets.token_urlsafe(32),
                expires_at=timezone.now() + timedelta(hours=24)
            )
            # TODO: Send verification email
            messages.success(request, '¡Cuenta creada! Revisa tu email para verificar tu cuenta.')
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Merge session cart with user cart
            cart = get_or_create_cart(request)
            messages.success(request, f'¡Bienvenido, {user.get_short_name()}!')
            next_url = request.GET.get('next', 'catalog:home')
            return redirect(next_url)
    else:
        form = UserLoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["POST"])
def user_logout(request):
    """User logout."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('catalog:home')


@login_required
def profile(request):
    """User profile page."""
    user = request.user
    addresses = user.addresses.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'addresses': addresses,
    })


@login_required
@require_http_methods(["POST"])
def profile_delete(request):
    """Delete user account."""
    user = request.user
    user.delete()
    messages.success(request, 'Tu cuenta ha sido eliminada.')
    return redirect('catalog:home')


# Address views
@login_required
def address_list(request):
    """List user addresses."""
    addresses = request.user.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_create(request):
    """Create new address."""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Dirección añadida correctamente.')
            return redirect('accounts:address_list')
    else:
        form = AddressForm()

    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Nueva dirección'})


@login_required
def address_edit(request, pk):
    """Edit address."""
    address = get_object_or_404(Address, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dirección actualizada.')
            return redirect('accounts:address_list')
    else:
        form = AddressForm(instance=address)

    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Editar dirección'})


@login_required
@require_http_methods(["POST"])
def address_delete(request, pk):
    """Delete address."""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Dirección eliminada.')
    return redirect('accounts:address_list')


@login_required
@require_http_methods(["POST"])
def address_set_default(request, pk):
    """Set address as default."""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    return JsonResponse({'success': True})


# Password views
@login_required
def password_change(request):
    """Change password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {'form': form})


def password_reset_request(request):
    """Request password reset."""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = PasswordResetToken.objects.create(
                    user=user,
                    token=secrets.token_urlsafe(32),
                    expires_at=timezone.now() + timedelta(hours=1)
                )
                # TODO: Send reset email
                messages.success(request, 'Si el email existe, recibirás instrucciones para resetear tu contraseña.')
            except User.DoesNotExist:
                messages.success(request, 'Si el email existe, recibirás instrucciones para resetear tu contraseña.')
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """Confirm password reset with token."""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Token inválido o expirado.')
        return redirect('accounts:password_reset_request')

    if not reset_token.is_valid():
        messages.error(request, 'Token inválido o expirado.')
        return redirect('accounts:password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(reset_token.user, request.POST)
        if form.is_valid():
            form.save()
            reset_token.used = True
            reset_token.save()
            messages.success(request, 'Contraseña restablecida correctamente.')
            return redirect('accounts:login')
    else:
        form = PasswordResetConfirmForm(reset_token.user)

    return render(request, 'accounts/password_reset_confirm.html', {'form': form, 'token': token})


# Email verification
def email_verify(request, token):
    """Verify email with token."""
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Token de verificación inválido.')
        return redirect('catalog:home')

    if not verification_token.is_valid():
        messages.error(request, 'Token de verificación expirado.')
        return redirect('catalog:home')

    user = verification_token.user
    user.email_verified = True
    user.save()
    verification_token.delete()

    messages.success(request, 'Email verificado correctamente.')
    return redirect('accounts:login')


# AJAX endpoints
@login_required
@require_http_methods(["POST"])
def toggle_newsletter(request):
    """Toggle newsletter subscription."""
    request.user.newsletter = not request.user.newsletter
    request.user.save(update_fields=['newsletter'])
    return JsonResponse({'subscribed': request.user.newsletter})