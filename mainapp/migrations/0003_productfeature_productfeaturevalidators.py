# Generated by Django 3.1.7 on 2021-03-05 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210304_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(max_length=200)),
                ('feature_name', models.CharField(max_length=200)),
                ('postfix_for_value', models.CharField(blank=True, max_length=20, null=True)),
                ('user_in_filter', models.BooleanField(default=False)),
                ('filter_type', models.CharField(choices=[('РАДИОКНОПКА', 'Радиокнопка'), ('ЧЕКБОКС', 'Чекбокс')], default='Чекбокс', max_length=20)),
                ('filter_measure', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeatureValidators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_value', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.productfeature')),
            ],
        ),
    ]
