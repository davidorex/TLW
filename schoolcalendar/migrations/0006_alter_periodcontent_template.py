# Generated by Django 5.1.2 on 2024-11-08 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0005_alter_periodcontent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodcontent',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='schoolcalendar.periodtemplate'),
        ),
    ]
