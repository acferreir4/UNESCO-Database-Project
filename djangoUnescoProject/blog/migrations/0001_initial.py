# Generated by Django 2.1.5 on 2019-03-19 01:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('fileAttachment', models.FileField(blank=True, null=True, upload_to='announcements/files')),
                ('imageAttachment', models.ImageField(blank=True, null=True, upload_to='announcements/images')),
            ],
        ),
    ]
