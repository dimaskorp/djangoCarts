# Generated by Django 4.1.5 on 2023-04-27 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartridge', '0015_alter_cartridges_col_alter_cartridges_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridges',
            name='col',
            field=models.IntegerField(blank=True, db_index=True, default=None, verbose_name='Перезаправки'),
        ),
        migrations.AlterField(
            model_name='cartridges',
            name='date',
            field=models.DateTimeField(default='27.04.2023 11:55', verbose_name='Дата изменения'),
        ),
    ]
