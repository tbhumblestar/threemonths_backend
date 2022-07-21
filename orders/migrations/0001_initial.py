# Generated by Django 4.0.6 on 2022-07-22 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('cafe', 'Cafe order'), ('package', 'Package order'), ('cake', 'Cake order')], max_length=100)),
                ('customer_name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('not_confirmed', 'not_confirmed'), ('confirmed', 'confirmed'), ("can't_cancel", "can't_cancel"), ('completed', 'completed')], max_length=50)),
                ('additional_explanation', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='PackageOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_location', models.CharField(max_length=100)),
                ('delivery_date', models.DateField()),
                ('is_packaging', models.BooleanField(default=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'package_orders',
            },
        ),
        migrations.CreateModel(
            name='OrderedProductsInPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.BigIntegerField()),
                ('order_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.packageorder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'ordered_products_in_packages',
            },
        ),
        migrations.CreateModel(
            name='OrderedCake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.BigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'ordered_cakes',
            },
        ),
        migrations.CreateModel(
            name='CakeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('want_pick_up_date', models.DateField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'cake_orders',
            },
        ),
        migrations.CreateModel(
            name='CafeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cafename', models.CharField(max_length=50)),
                ('cafe_owner_name', models.CharField(max_length=50)),
                ('cafe_location', models.CharField(max_length=50)),
                ('want_delivery_date', models.DateField()),
                ('product_explanation', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'cafe_orders',
            },
        ),
    ]
