# Generated by Django 4.0.6 on 2022-07-28 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productimage_product'),
        ('orders', '0005_orderedproduct_orderedcake_cake_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cakeorder',
            name='count',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cakeorder',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='OrderedCake',
        ),
    ]
