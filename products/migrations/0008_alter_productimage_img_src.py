# Generated by Django 4.0.6 on 2022-08-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='img_src',
            field=models.CharField(max_length=500),
        ),
    ]
