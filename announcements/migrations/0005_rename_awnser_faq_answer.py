# Generated by Django 4.0.6 on 2022-08-20 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0004_alter_qnacomment_qna'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faq',
            old_name='awnser',
            new_name='answer',
        ),
    ]
