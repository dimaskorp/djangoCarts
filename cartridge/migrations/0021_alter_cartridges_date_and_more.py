# Generated by Django 4.1.5 on 2023-05-02 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartridge', '0020_alter_cartridges_date_historicalcartridges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridges',
            name='date',
            field=models.DateTimeField(default='02.05.2023 15:42', verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='historicalcartridges',
            name='date',
            field=models.DateTimeField(default='02.05.2023 15:42', verbose_name='Дата изменения'),
        ),
    ]