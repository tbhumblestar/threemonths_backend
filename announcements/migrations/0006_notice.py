# Generated by Django 4.0.6 on 2022-08-24 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announcements', '0005_rename_awnser_faq_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('img1_url', models.CharField(max_length=500)),
                ('img1_s3_path', models.CharField(max_length=500)),
                ('img2_url', models.CharField(max_length=500, null=True)),
                ('img2_s3_path', models.CharField(max_length=500, null=True)),
                ('img3_url', models.CharField(max_length=500, null=True)),
                ('img3_s3_path', models.CharField(max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notices',
            },
        ),
    ]
