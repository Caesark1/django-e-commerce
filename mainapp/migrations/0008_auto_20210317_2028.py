# Generated by Django 3.1.7 on 2021-03-17 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20210317_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeaturevalue',
            name='feature_value',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
