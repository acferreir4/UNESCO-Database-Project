# Generated by Django 2.1.5 on 2019-03-08 02:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_date_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_expire',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
