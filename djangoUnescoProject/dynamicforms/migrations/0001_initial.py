# Generated by Django 2.1.5 on 2019-03-19 01:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('is_draft', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DynamicForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator_id', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(max_length=300, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_time', models.DateTimeField(default=datetime.date.today)),
                ('expiry_date', models.DateTimeField(default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': 'DynamicForms',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.IntegerField()),
                ('question_text', models.CharField(max_length=100000)),
                ('answer_type', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modification_time', models.DateTimeField(default=datetime.date.today)),
                ('form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamicforms.DynamicForms')),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.AddField(
            model_name='datatable',
            name='form_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamicforms.DynamicForms'),
        ),
        migrations.AddField(
            model_name='datatable',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamicforms.Questions'),
        ),
    ]
