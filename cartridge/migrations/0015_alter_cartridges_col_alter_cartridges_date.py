# Generated by Django 4.1.5 on 2023-04-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartridge', '0014_remove_cartridges_choice_remove_placements_choice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridges',
            name='col',
            field=models.IntegerField(blank=True, db_index=True, verbose_name='Перезаправки'),
        ),
        migrations.AlterField(
            model_name='cartridges',
            name='date',
            field=models.DateTimeField(default='27.04.2023 11:53', verbose_name='Дата изменения'),
        ),
    ]
