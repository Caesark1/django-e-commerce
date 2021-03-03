# Generated by Django 3.1.7 on 2021-02-21 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Покупатель', 'verbose_name_plural': 'Покупатели'},
        ),
        migrations.AlterModelOptions(
            name='laptop',
            options={'verbose_name': 'Ноутбук', 'verbose_name_plural': 'Ноутбуки'},
        ),
        migrations.AlterModelOptions(
            name='smartphone',
            options={'verbose_name': 'Смартфон', 'verbose_name_plural': 'Смартфоны'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['name'], 'verbose_name': 'Продавец', 'verbose_name_plural': 'Продавцы'},
        ),
        migrations.AlterField(
            model_name='laptop',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.vendor'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.vendor'),
        ),
    ]
