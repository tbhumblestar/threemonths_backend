# Generated by Django 4.0.6 on 2022-08-19 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_rename_qanda_qna_rename_qandacomment_qnacomment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qnacomment',
            old_name='q_and_a',
            new_name='qna',
        ),
    ]
