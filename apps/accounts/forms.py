"""
Forms for VEXOR GAMING Accounts app.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as BasePasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, Address


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Extended registration form with email as username."""
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-base',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email'
        })
    )
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-base',
            'placeholder': 'nombreusuario',
            'autocomplete': 'username'
        })
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-base',
            'placeholder': 'Juan',
            'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-base',
            'placeholder': 'Pérez',
            'autocomplete': 'family-name'
        })
    )
    phone = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-base',
            'placeholder': '+57 300 123 4567',
            'autocomplete': 'tel'
        })
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'input-base',
            'placeholder': '••••••••',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'input-base',
            'placeholder': '••••••••',
            'autocomplete': 'new-password'
        })
    )
    newsletter = forms.BooleanField(
        label='Suscribirme al boletín de ofertas',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-primary-600 border-gray-300 rounded'})
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'newsletter')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ya existe una cuenta con este email.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.username = self.cleaned_data['username'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.newsletter = self.cleaned_data['newsletter']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Login form using email."""
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-base',
            'placeholder': 'tu@email.com',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'input-base',
            'placeholder': '••••••••',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        label='Recordarme',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-primary-600 border-gray-300 rounded'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


class UserProfileForm(forms.ModelForm):
    """User profile form."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'birth_date', 'avatar', 'newsletter']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Juan'}),
            'last_name': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Pérez'}),
            'phone': forms.TextInput(attrs={'class': 'input-base', 'placeholder': '+57 300 123 4567'}),
            'birth_date': forms.DateInput(attrs={'class': 'input-base', 'type': 'date'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'input-base'}),
            'newsletter': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-primary-600 border-gray-300 rounded'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Teléfono',
            'birth_date': 'Fecha de nacimiento',
            'avatar': 'Avatar',
            'newsletter': 'Suscribirme al boletín',
        }


class AddressForm(forms.ModelForm):
    """Address form."""
    class Meta:
        model = Address
        fields = ['type', 'full_name', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'type': forms.Select(attrs={'class': 'input-base'}),
            'full_name': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Juan Pérez'}),
            'phone': forms.TextInput(attrs={'class': 'input-base', 'placeholder': '+57 300 123 4567'}),
            'address_line1': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Calle 123 #45-67'}),
            'address_line2': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Apto 302, Torre B (opcional)'}),
            'city': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Bogotá'}),
            'state': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Cundinamarca'}),
            'postal_code': forms.TextInput(attrs={'class': 'input-base', 'placeholder': '110111'}),
            'country': forms.TextInput(attrs={'class': 'input-base', 'placeholder': 'Colombia'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-primary-600 border-gray-300 rounded'}),
        }
        labels = {
            'type': 'Tipo',
            'full_name': 'Nombre completo',
            'phone': 'Teléfono',
            'address_line1': 'Dirección línea 1',
            'address_line2': 'Dirección línea 2',
            'city': 'Ciudad',
            'state': 'Estado/Departamento',
            'postal_code': 'Código postal',
            'country': 'País',
            'is_default': 'Dirección predeterminada',
        }


class PasswordChangeForm(BasePasswordChangeForm):
    """Password change form with custom widgets."""
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'input-base', 'placeholder': '••••••••', 'autocomplete': 'current-password'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-base', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-base', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )


class PasswordResetRequestForm(forms.Form):
    """Password reset request form."""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'input-base', 'placeholder': 'tu@email.com', 'autocomplete': 'email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not User.objects.filter(email=email).exists():
            # Don't reveal if email exists
            return email
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    """Password reset confirm form."""
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-base', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-base', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
    )