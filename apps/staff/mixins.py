from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere que el usuario sea staff (is_staff=True)."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(self.request.get_full_path(), 'staff:login')
        return HttpResponseForbidden('Acceso denegado: se requieren permisos de staff.')


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere superusuario."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(self.request.get_full_path(), 'staff:login')
        return HttpResponseForbidden('Acceso denegado: se requieren permisos de superusuario.')