# Generated by Django 2.1.4 on 2019-01-05 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_remove_announcements_expirytime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcements',
            name='Creator_ID',
        ),
    ]
