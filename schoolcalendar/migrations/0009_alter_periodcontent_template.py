from django.db import migrations, models
import schoolcalendar.models.period_content


class Migration(migrations.Migration):

    dependencies = [
        ('schoolcalendar', '0008_add_is_default_to_periodtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodcontent',
            name='template',
            field=models.ForeignKey(
                default=schoolcalendar.models.period_content.get_default_template,
                null=True,
                on_delete=models.PROTECT,
                to='schoolcalendar.periodtemplate'
            ),
        ),
    ]
