"""
Admin for VEXOR GAMING Cart app.
"""
from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'unit_price', 'total_price', 'created_at']
    fields = ['product', 'quantity', 'unit_price', 'total_price']

    def unit_price(self, obj):
        return f'${obj.unit_price:.2f}'
    unit_price.short_description = 'Precio unitario'

    def total_price(self, obj):
        return f'${obj.total_price:.2f}'
    total_price.short_description = 'Total'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'item_count', 'total_price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'session_key']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at', 'item_count', 'total_price']
    inlines = [CartItemInline]
    ordering = ['-updated_at']

    def item_count(self, obj):
        return obj.item_count
    item_count.short_description = 'Items'

    def total_price(self, obj):
        return f'${obj.total_price:.2f}'
    total_price.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'unit_price', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__email', 'product__name']
    raw_id_fields = ['cart', 'product']
    readonly_fields = ['created_at', 'updated_at', 'unit_price', 'total_price']

    def unit_price(self, obj):
        return f'${obj.unit_price:.2f}'
    unit_price.short_description = 'Precio unitario'

    def total_price(self, obj):
        return f'${obj.total_price:.2f}'
    total_price.short_description = 'Total'