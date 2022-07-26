# Generated by Django 4.0.6 on 2022-07-27 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productimage_product'),
        ('orders', '0004_cafeorder_corporate_registration_num_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.BigIntegerField()),
            ],
            options={
                'db_table': 'ordered_products',
            },
        ),
        migrations.AddField(
            model_name='orderedcake',
            name='cake_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderedcakes', to='orders.packageorder'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cafeorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cafeorders', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='cakeorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cakeorders', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='packageorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='packageorders', to='orders.order'),
        ),
        migrations.DeleteModel(
            name='OrderedProductsInPackage',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='package_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderedproducts', to='orders.packageorder'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
