# Generated by Django 4.0.6 on 2022-07-29 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_packageorder_purpose'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproduct',
            name='count',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='buying',
            field=models.BooleanField(default=False),
        ),
    ]
