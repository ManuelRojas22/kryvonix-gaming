"""
URLs for VEXOR GAMING Accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('registro/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Profile
    path('perfil/', views.profile, name='profile'),
    path('perfil/eliminar/', views.profile_delete, name='profile_delete'),
    path('perfil/password/', views.password_change, name='password_change'),

    # Addresses
    path('direcciones/', views.address_list, name='address_list'),
    path('direcciones/nueva/', views.address_create, name='address_create'),
    path('direcciones/<int:pk>/editar/', views.address_edit, name='address_edit'),
    path('direcciones/<int:pk>/eliminar/', views.address_delete, name='address_delete'),
    path('direcciones/<int:pk>/predeterminada/', views.address_set_default, name='address_set_default'),

    # Password reset
    path('password/reset/', views.password_reset_request, name='password_reset_request'),
    path('password/reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # Email verification
    path('verificar/<str:token>/', views.email_verify, name='email_verify'),

    # AJAX
    path('newsletter/toggle/', views.toggle_newsletter, name='toggle_newsletter'),
]