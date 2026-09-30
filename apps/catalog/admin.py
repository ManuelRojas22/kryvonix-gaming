"""
Admin configuration for VEXOR GAMING Catalog app.
"""
from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductSpec


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'order', 'alt_text']
    ordering = ['order']


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 1
    fields = ['name', 'value', 'order']
    ordering = ['order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'is_active', 'order', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']

    def product_count(self, obj):
        return obj.product_count
    product_count.short_description = 'Productos'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'logo_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

    def logo_preview(self, obj):
        if obj.logo:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'brand', 'category', 'price', 'discount_price',
        'stock', 'has_discount', 'discount_percent', 'is_featured',
        'is_active', 'units_sold', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'brand', 'category',
        'created_at', 'warranty_months'
    ]
    search_fields = ['name', 'description', 'brand__name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'units_sold']
    inlines = [ProductImageInline, ProductSpecInline]
    ordering = ['-created_at']
    list_per_page = 20

    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'description', 'category', 'brand')
        }),
        ('Precios y stock', {
            'fields': ('price', 'discount_price', 'stock', 'warranty_months')
        }),
        ('Estado', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Campos para PC Builder (opcional)', {
            'fields': ('socket', 'ram_type', 'wattage', 'length_mm', 'form_factor'),
            'classes': ('collapse',),
        }),
        ('Estadísticas', {
            'fields': ('units_sold', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_discount(self, obj):
        return obj.has_discount
    has_discount.boolean = True
    has_discount.short_description = 'Descuento'

    def discount_percent(self, obj):
        if obj.has_discount:
            return f'{obj.discount_percent}%'
        return '-'
    discount_percent.short_description = '% Desc.'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand', 'category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name']
    ordering = ['product', 'order']

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Vista previa'


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'order']
    list_filter = ['product__category', 'product__brand']
    search_fields = ['product__name', 'name', 'value']
    ordering = ['product', 'order']