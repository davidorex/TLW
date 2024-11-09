from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0007_remove_historicalperiodtemplate_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodtemplate',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
