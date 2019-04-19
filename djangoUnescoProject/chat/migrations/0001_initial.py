# Generated by Django 2.1.5 on 2019-03-19 01:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\d\\-_]*$', 'Only alphanumeric characters, _ and -  are allowed. No Space.')])),
                ('category', models.CharField(choices=[('G', 'Group Room'), ('P', 'Personal Room')], max_length=1)),
                ('display_line_1', models.CharField(max_length=50, null=True)),
                ('display_line_2', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Chat Rooms',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomName_RoomAccess', to='chat.ChatRooms')),
            ],
            options={
                'verbose_name_plural': 'Room Access',
            },
        ),
    ]
