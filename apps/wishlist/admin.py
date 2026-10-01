"""
Admin for VEXOR GAMING Wishlist app.
"""
from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ['product', 'added_at', 'current_price', 'price_when_added', 'notify_price_drop', 'notify_back_in_stock']
    fields = ['product', 'added_at', 'current_price', 'price_when_added', 'notify_price_drop', 'notify_back_in_stock']

    def current_price(self, obj):
        return f'${obj.current_price:.2f}'
    current_price.short_description = 'Precio actual'

    def price_when_added(self, obj):
        return f'${obj.price_when_added:.2f}'
    price_when_added.short_description = 'Precio al añadir'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'created_at', 'updated_at']
    search_fields = ['user__email']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [WishlistItemInline]
    ordering = ['-updated_at']

    def item_count(self, obj):
        return obj.item_count
    item_count.short_description = 'Items'


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product', 'added_at', 'current_price', 'price_when_added', 'price_dropped', 'discount_percent', 'notify_price_drop']
    list_filter = ['added_at', 'notify_price_drop', 'notify_back_in_stock']
    search_fields = ['wishlist__user__email', 'product__name']
    raw_id_fields = ['wishlist', 'product']
    readonly_fields = ['added_at', 'current_price', 'price_when_added', 'price_dropped', 'savings', 'discount_percent']

    def current_price(self, obj):
        return f'${obj.current_price:.2f}'
    current_price.short_description = 'Precio actual'

    def price_when_added(self, obj):
        return f'${obj.price_when_added:.2f}'
    price_when_added.short_description = 'Precio al añadir'

    def price_dropped(self, obj):
        return obj.price_dropped
    price_dropped.boolean = True
    price_dropped.short_description = 'Bajó precio'

    def discount_percent(self, obj):
        if obj.discount_percent:
            return f'{obj.discount_percent}%'
        return '-'
    discount_percent.short_description = '% Desc.'