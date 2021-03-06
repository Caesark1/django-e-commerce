# Generated by Django 3.1.7 on 2021-03-06 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210306_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
