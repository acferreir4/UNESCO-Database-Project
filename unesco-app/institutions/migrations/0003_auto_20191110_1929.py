# Generated by Django 2.2.6 on 2019-11-10 19:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20190426_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='abbreviation',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='institution',
            name='environment',
            field=models.CharField(blank=True, choices=[('often', 'Often'), ('frequently', 'Frequently'), ('seldom', 'Seldom'), ('never', 'Never')], default='never', max_length=15),
        ),
        migrations.AlterField(
            model_name='institution',
            name='focus_pst',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('primary', 'Primary'), ('secondary', 'Secondary'), ('tertiary', 'Tertiary'), ('kindergarten', 'Kindergarten'), ('undefined', 'Not yet defined')], default='undefined', max_length=15, verbose_name='Focus on K/P/S/T'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='further',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Further levels of education'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='general',
            field=models.CharField(blank=True, choices=[('passive', 'Passive'), ('active', 'Active')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='institution',
            name='guest_lectures',
            field=models.CharField(blank=True, choices=[('often', 'Often'), ('frequently', 'Frequently'), ('seldom', 'Seldom'), ('never', 'Never')], default='never', max_length=15),
        ),
        migrations.AlterField(
            model_name='institution',
            name='internet_access',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('none', 'None'), ('seldom', 'Seldom')], default='yes', max_length=10),
        ),
        migrations.AlterField(
            model_name='institution',
            name='online',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('none', 'None'), ('seldom', 'Seldom'), ('often', 'Often')], default='yes', max_length=10, verbose_name='Use of online learning material'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='qualifications',
            field=models.CharField(blank=True, choices=[('bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PhD'), ('certificate', 'Certificate')], default='bachelor', max_length=15),
        ),
        migrations.AlterField(
            model_name='institution',
            name='role',
            field=models.CharField(choices=[('research', 'Research'), ('coordination', 'Coordination'), ('government', 'Government')], default='research', max_length=15),
        ),
        migrations.AlterField(
            model_name='institution',
            name='staff_count',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='institution',
            name='type_of_inst',
            field=models.CharField(choices=[('university', 'University'), ('ngo', 'NGO'), ('college', 'College'), ('rce', 'RCE')], default='university', max_length=15, verbose_name='Type of institution'),
        ),
        migrations.AlterField(
            model_name='researchinstitutecontact',
            name='degree',
            field=models.CharField(blank=True, choices=[('phd', 'PhD'), ('master', 'Master'), ('bachelor', 'Bachelor')], default='bachelor', max_length=10),
        ),
        migrations.AlterField(
            model_name='researchinstitutecontact',
            name='function',
            field=models.CharField(blank=True, default='', max_length=150),
            preserve_default=False,
        ),
    ]
