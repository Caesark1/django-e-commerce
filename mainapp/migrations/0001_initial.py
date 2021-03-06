# Generated by Django 3.1.7 on 2021-03-14 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая Цена')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Имя Категории')),
                ('slug', models.SlugField(unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='mainapp.category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер телефона пользователя')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес пользователя')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование Товара')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена продукта')),
                ('qty', models.PositiveIntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='mainapp.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeatureName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(max_length=200)),
                ('feature_name', models.CharField(max_length=200)),
                ('postfix_for_value', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_shop', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Продавец',
                'verbose_name_plural': 'Продавцы',
                'ordering': ['name_of_shop'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='mainapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeatureValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_value', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='mainapp.productfeaturename')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features_values', to='mainapp.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.vendor'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('NEW', 'new'), ('IN PROGRESS', 'In progress'), ('IS READY', 'Order is ready'), ('COMPLETED', 'Completed')], default='new', max_length=255)),
                ('buying_type', models.CharField(choices=[('SELF', 'self'), ('DELIVERY', 'delivery')], default='self', max_length=255)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='mainapp.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_customer', to='mainapp.Order'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь '),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Покупатель')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='mainapp.CartProduct'),
        ),
    ]
