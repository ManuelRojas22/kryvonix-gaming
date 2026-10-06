from django import forms
from django.forms import inlineformset_factory

from apps.catalog.models import Category, Brand, Product, ProductImage, ProductSpec


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: gpu, cpu, ram, keyboard, mouse, monitor'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-cyan-500 border-gray-300 rounded focus:ring-cyan-500'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = 'Se genera automáticamente si se deja vacío'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-cyan-500 border-gray-300 rounded focus:ring-cyan-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = 'Se genera automáticamente si se deja vacío'


class ProductForm(forms.ModelForm):
    # Non-model field for easier discount management
    discount_percent = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=99,
        label='Descuento (%)',
        help_text='Ingrese un porcentaje (0-99) para calcular automáticamente el precio con descuento',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent',
            'min': '0',
            'max': '99',
            'placeholder': 'Ej: 15'
        })
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'category', 'brand',
            'price', 'discount_price', 'discount_percent', 'stock', 'warranty_months',
            'is_featured', 'is_active',
            'socket', 'ram_type', 'wattage', 'length_mm', 'form_factor'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'rows': 6, 'id': 'id_description'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'brand': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'step': '0.01', 'min': '0'}),
            'discount_price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0'}),
            'warranty_months': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-cyan-500 border-gray-300 rounded focus:ring-cyan-500'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-cyan-500 border-gray-300 rounded focus:ring-cyan-500'}),
            'socket': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: AM5, LGA1700'}),
            'ram_type': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: DDR5, DDR4'}),
            'wattage': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0', 'placeholder': 'Vatios'}),
            'length_mm': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0', 'placeholder': 'Largo en mm'}),
            'form_factor': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: ATX, Micro-ATX, Mini-ITX'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = 'Se genera automáticamente si se deja vacío'
        self.fields['discount_price'].required = False
        self.fields['discount_price'].help_text = 'Dejar vacío si no hay descuento (se calcula automáticamente con el %)'
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['brand'].queryset = Brand.objects.filter(is_active=True).order_by('name')
        
        # Set initial discount_percent from existing discount_price
        if self.instance and self.instance.pk and self.instance.has_discount:
            self.fields['discount_percent'].initial = self.instance.discount_percent

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        discount_percent = cleaned_data.get('discount_percent')
        
        # If discount_percent is provided, calculate discount_price
        if discount_percent is not None and price is not None:
            if 0 <= discount_percent <= 99:
                calculated_discount = round(price * (1 - discount_percent / 100), 2)
                cleaned_data['discount_price'] = calculated_discount
            elif discount_percent == 0:
                cleaned_data['discount_price'] = None
        
        # Validate discount_price is less than price
        if discount_price is not None and price is not None:
            if discount_price >= price:
                self.add_error('discount_price', 'El precio con descuento debe ser menor al precio original.')
            if discount_price < 0:
                self.add_error('discount_price', 'El precio con descuento no puede ser negativo.')
        
        return cleaned_data


# Inline formsets for ProductImage and ProductSpec
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=['image', 'order', 'alt_text'],
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent'}),
        'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0'}),
        'alt_text': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Texto alternativo'}),
    }
)

ProductSpecFormSet = inlineformset_factory(
    Product, ProductSpec,
    fields=['name', 'value', 'order'],
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: Memoria VRAM'}),
        'value': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'placeholder': 'Ej: 16 GB GDDR6'}),
        'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent', 'min': '0'}),
    }
)