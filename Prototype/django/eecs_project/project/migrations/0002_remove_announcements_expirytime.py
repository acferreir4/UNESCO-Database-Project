# Generated by Django 2.1.4 on 2019-01-05 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcements',
            name='ExpiryTime',
        ),
    ]
