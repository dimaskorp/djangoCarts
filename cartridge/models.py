from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords
import datetime


class Manufacturer(models.Model):  # Производитель
    manufacturer = models.CharField("Производитель", max_length=50, unique=True, db_index=True)
    comments = models.CharField("Комментарии", max_length=100, blank=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return str(self.manufacturer)


class Placements(models.Model):  # Помещения
    barcode = models.IntegerField('Штрихкод', unique=True, db_index=True)
    name = models.CharField("Помещение", max_length=50, unique=True, db_index=True)
    branch = models.CharField("Корпус", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def __str__(self):
        return str(self.name)


class NameСartridge(models.Model):  # Названия картриджей
    name = models.CharField("Название картриджа", max_length=50, unique=True, db_index=True)
    comments = models.CharField("Комментарии", max_length=100, blank=True)

    class Meta:
        verbose_name = 'Название картриджа'
        verbose_name_plural = 'Названия картриджей'

    def __str__(self):
        return str(self.name)


class Cartridges(models.Model):  # Картриджи
    barcode = models.CharField('Штрихкод', unique=True, db_index=True, max_length=50)
    cartName = models.ForeignKey('NameСartridge', default=None, on_delete=models.PROTECT)
    placeName = models.ForeignKey('Placements', on_delete=models.PROTECT)
    manufacturerName = models.ForeignKey('Manufacturer', default=None, on_delete=models.PROTECT)
    date = models.DateTimeField("Дата изменения", default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    col = models.IntegerField('Перезаправки', db_index=True, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.barcode) + " | " + str(self.cartName)

    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'


class Status(models.Model):  # Помещения
    status = models.CharField("Статус", max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'

    def __str__(self):
        return str(self.status)


class ChangeLog(models.Model):
    barcode_h = models.CharField('Штрихкод', blank=True, null=True, max_length=50)
    cartName_h = models.CharField('Модель', max_length=250, blank=True, null=True)
    placeName_h = models.CharField('Помещение', max_length=50, blank=True, null=True)
    manufacturerName_h = models.CharField('Производитель', max_length=50, blank=True, null=True)
    date_h = models.DateTimeField("Дата изменения", null=True)
    comments_h = models.CharField('Комментарии', max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = _('Журнал изменений')
        verbose_name_plural = _('Журналы изменений')

    def __str__(self):
        return str(self.barcode_h) + " " + str(self.manufacturerName_h) + " " + str(self.cartName_h) + " " + str(self.date_h)

