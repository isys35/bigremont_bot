# Generated by Django 3.2.7 on 2021-09-19 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigremont_app', '0003_auto_20210919_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(db_index=True, max_length=250, unique=True, verbose_name='Наименование материала'),
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, unique=True, verbose_name='Наименование')),
                ('materials', models.ManyToManyField(to='bigremont_app.Material')),
            ],
        ),
    ]
