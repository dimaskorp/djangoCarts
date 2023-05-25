# Generated by Django 4.1.5 on 2023-05-11 11:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cartridge', '0021_alter_cartridges_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changelog',
            name='action_on_model',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='changed',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='data',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='model',
        ),
        migrations.RemoveField(
            model_name='changelog',
            name='record_id',
        ),

        migrations.AddField(
            model_name='changelog',
            name='cartName_h',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='cartridge.nameсartridge'),
        ),

        migrations.AddField(
            model_name='changelog',
            name='manufacturerName_h',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='cartridge.manufacturer'),
        ),
        migrations.AddField(
            model_name='changelog',
            name='status_h',
            field=models.CharField(db_index=True, default=1, max_length=50, unique=True, verbose_name='Статус'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartridges',
            name='date',
            field=models.DateTimeField(default='11.05.2023 11:29', verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='historicalcartridges',
            name='date',
            field=models.DateTimeField(default='11.05.2023 11:29', verbose_name='Дата изменения'),
        ),
    ]