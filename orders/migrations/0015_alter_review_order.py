# Generated by Django 4.0.6 on 2022-08-24 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='orders.order'),
        ),
    ]
