# Generated by Django 3.2.7 on 2021-09-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigremont_app', '0004_auto_20210919_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worktype',
            options={'verbose_name': 'Вид работ', 'verbose_name_plural': 'Виды работ'},
        ),
        migrations.AlterField(
            model_name='material',
            name='unit_measurement',
            field=models.CharField(choices=[('шт', 'шт'), ('лист', 'лист'), ('пачка', 'пачка'), ('рулон', 'рулон'), ('мешок', 'мешок'), ('ведро', 'ведро'), ('м', 'м')], max_length=100, verbose_name='Единица измерения'),
        ),
    ]
