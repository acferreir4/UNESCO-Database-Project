# Generated by Django 2.2.6 on 2019-11-10 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamicforms', '0002_datatable_submitter_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datatable',
            options={'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterModelOptions(
            name='dynamicforms',
            options={'verbose_name_plural': 'Questionnaire Forms'},
        ),
    ]
