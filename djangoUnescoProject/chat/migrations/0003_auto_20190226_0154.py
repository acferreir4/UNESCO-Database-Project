# Generated by Django 2.1.5 on 2019-02-26 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20190225_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatrooms',
            options={'verbose_name_plural': 'Chat Rooms'},
        ),
        migrations.AlterModelOptions(
            name='roomaccess',
            options={'verbose_name_plural': 'Room Accesses'},
        ),
    ]
