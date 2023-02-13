from django.db import models
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
    barcode = models.IntegerField('Штрихкод', primary_key=True, unique=True, db_index=True)
    cartName = models.ForeignKey('NameСartridge', default=None, on_delete=models.PROTECT)
    placeName = models.ForeignKey('Placements', on_delete=models.PROTECT)
    manufacturerName = models.ForeignKey('Manufacturer', default=None, on_delete=models.PROTECT)
    date = models.DateTimeField("Дата изменения", default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

    def __str__(self):
        return str(self.barcode) + " | " + str(self.cartName)

    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'
