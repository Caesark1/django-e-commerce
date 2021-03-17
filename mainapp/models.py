from django.db import models
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.shortcuts import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class ProductAvailableManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_available = True)


class Vendor(models.Model):
    name_of_shop = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name_of_shop']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return f"{self.name_of_shop} created by {self.created_by.username} - {self.created_by.last_name} {self.created_by.first_name}"
    
    def get_absolute_url(self):
        return reverse("vendor_detail", kwargs={"slug": self.slug})
    


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь ', on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона пользователя', null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name='Адрес пользователя', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    orders = models.ManyToManyField('Order', related_name='related_customer')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self) -> str:
        return f'Покупатель: {self.user.username}'


class CartProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self) -> str:
        return f'Продукт: {self.product.title}'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(Customer, null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая Цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False) 

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return f'cart of {self.owner.user}' if self.owner else "cart of anonymous user"


class Product(models.Model):

    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True, related_name='vendor_products')
    title = models.CharField(max_length=255, verbose_name='Наименование Товара')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание товара', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена продукта')
    qty = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to = 'uploads/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    objects = models.Manager()
    available = ProductAvailableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_model_name(self):
        return self.__class__.__name__.lower()
    
    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return "./static/image/no_image.jpg"


class ProductImage(models.Model):

    description = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'Фотография - {self.product.title} продукта'


class ProductFeatureName(models.Model):

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product_feature_names')
    feature_key = models.CharField(max_length=200)
    feature_name = models.CharField(max_length=200)
    postfix_for_value = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f'Категория - "{self.category.name}" | Характеристика - "{self.feature_name}"'


class ProductFeatureValue(models.Model):
    feature = models.ForeignKey(ProductFeatureName, null=True, on_delete=models.CASCADE, related_name='features')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_features_values')
    feature_value = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return f'Характеристики - {self.feature.feature_name}' \
               f'Значение - {self.feature_value}'


class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name='Имя Категории', unique=True)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Order(models.Model):

    BUYING_TYPE_STATUS_CHOICES = (
        ('SELF', 'self'),
        ('DELIVERY', 'delivery')
    )

    STATUS_CHOICES = (
        ('NEW', 'new'),
        ('IN PROGRESS', 'In progress'),
        ('IS READY', 'Order is ready'),
        ('COMPLETED', 'Completed')
    )

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='related_orders')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='new')
    buying_type = models.CharField(max_length=255, choices=BUYING_TYPE_STATUS_CHOICES, default='self')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    order_date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.customer.user}s order"
