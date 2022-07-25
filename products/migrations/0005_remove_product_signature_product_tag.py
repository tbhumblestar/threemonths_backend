# Generated by Django 4.0.6 on 2022-07-23 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='signature',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]