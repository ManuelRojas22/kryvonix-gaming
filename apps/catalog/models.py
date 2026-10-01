"""
Models for VEXOR GAMING Catalog app.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    """Abstract model with created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """Product category (GPU, CPU, RAM, etc.)."""
    name = models.CharField('Nombre', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    description = models.TextField('Descripción', blank=True)
    icon = models.CharField('Icono (clase CSS)', max_length=50, blank=True, help_text='Ej: gpu, cpu, ram, keyboard, mouse, monitor')
    is_active = models.BooleanField('Activo', default=True)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:shop_category', kwargs={'category_slug': self.slug})

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Brand(TimeStampedModel):
    """Product brand (NVIDIA, AMD, Intel, Corsair, etc.)."""
    name = models.CharField('Nombre', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    logo = models.ImageField('Logo', upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:shop') + f'?brand={self.slug}'


class Product(TimeStampedModel):
    """Main product model."""
    name = models.CharField('Nombre', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    description = models.TextField('Descripción')
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(
        'Precio con descuento',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Dejar vacío si no hay descuento'
    )
    stock = models.PositiveIntegerField('Stock', default=0)
    warranty_months = models.PositiveIntegerField('Garantía (meses)', default=12)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Marca'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Categoría'
    )
    is_featured = models.BooleanField('Destacado', default=False)
    is_active = models.BooleanField('Activo', default=True)
    units_sold = models.PositiveIntegerField('Unidades vendidas', default=0)

    # Optional fields for future PC Builder
    socket = models.CharField('Socket', max_length=50, blank=True, help_text='Ej: AM5, LGA1700')
    ram_type = models.CharField('Tipo de RAM', max_length=20, blank=True, help_text='Ej: DDR5, DDR4')
    wattage = models.PositiveIntegerField('Vatios', blank=True, null=True, help_text='Para fuentes de poder')
    length_mm = models.PositiveIntegerField('Largo (mm)', blank=True, null=True, help_text='Para tarjetas gráficas')
    form_factor = models.CharField('Factor de forma', max_length=50, blank=True, help_text='Ej: ATX, Micro-ATX, Mini-ITX')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            return round((1 - self.discount_price / self.price) * 100)
        return 0

    @property
    def current_price(self):
        return self.discount_price if self.has_discount else self.price

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def primary_image(self):
        return self.images.first()

    def get_related_products(self, limit=4):
        return Product.objects.filter(
            category=self.category,
            is_active=True
        ).exclude(pk=self.pk).select_related('brand', 'category').prefetch_related('images')[:limit]


class ProductImage(TimeStampedModel):
    """Product gallery images."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Producto'
    )
    image = models.ImageField('Imagen', upload_to='products/')
    order = models.PositiveIntegerField('Orden', default=0)
    alt_text = models.CharField('Texto alternativo', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de productos'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.product.name} - Imagen {self.order}'

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = self.product.name
        super().save(*args, **kwargs)


class ProductSpec(TimeStampedModel):
    """Key-value specifications for products."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specs',
        verbose_name='Producto'
    )
    name = models.CharField('Nombre', max_length=100)
    value = models.CharField('Valor', max_length=200)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'
        ordering = ['order', 'name']
        unique_together = ['product', 'name']

    def __str__(self):
        return f'{self.product.name}: {self.name} = {self.value}'