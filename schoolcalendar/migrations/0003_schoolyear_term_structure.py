# Generated by Django 5.1.2 on 2024-11-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0002_historicalperiodtemplate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolyear',
            name='term_structure',
            field=models.CharField(choices=[('SEMESTER', 'Semester'), ('TRIMESTER', 'Trimester')], default='SEMESTER', max_length=10),
        ),
    ]
