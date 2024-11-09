# Generated by Django 5.1.2 on 2024-11-08 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0006_alter_periodcontent_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalperiodtemplate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalperiodtemplate',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalperiodtemplate',
            name='modified_by',
        ),
        migrations.AlterModelOptions(
            name='periodtemplate',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='periodtemplate',
            name='schoolcalen_effecti_5d3dc9_idx',
        ),
        migrations.RemoveIndex(
            model_name='periodtemplate',
            name='schoolcalen_name_da206d_idx',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='afternoon_periods',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='change_reason',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='deleted_by_cascade',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='effective_from',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='evening_periods',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='first_period',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='metadata',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='morning_periods',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='passing_time',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='period_length',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='schedule_type',
        ),
        migrations.RemoveField(
            model_name='periodtemplate',
            name='version',
        ),
        migrations.AddField(
            model_name='periodtemplate',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='periodtemplate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='periodtemplate',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='HistoricalPeriodTemplate',
        ),
    ]
