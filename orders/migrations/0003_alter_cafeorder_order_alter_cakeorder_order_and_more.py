# Generated by Django 4.0.6 on 2022-07-26 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_cafeorder_want_delivery_date_order_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafeorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
        migrations.AlterField(
            model_name='cakeorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
        migrations.AlterField(
            model_name='packageorder',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
