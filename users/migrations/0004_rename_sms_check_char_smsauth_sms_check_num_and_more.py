# Generated by Django 4.0.6 on 2022-11-11 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_smsauth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smsauth',
            old_name='sms_check_char',
            new_name='sms_check_num',
        ),
        migrations.AlterField(
            model_name='smsauth',
            name='phone_number',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
