# Generated by Django 5.1.2 on 2024-11-08 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0003_schoolyear_term_structure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolyear',
            old_name='term_structure',
            new_name='term_type',
        ),
    ]