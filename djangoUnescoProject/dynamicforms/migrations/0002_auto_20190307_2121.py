# Generated by Django 2.1.5 on 2019-03-07 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamicforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forms',
            options={'verbose_name_plural': 'Forms'},
        ),
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name_plural': 'Questions'},
        ),
    ]
