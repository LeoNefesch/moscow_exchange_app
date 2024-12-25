from django.db import models
from django.utils.translation import gettext_lazy as _


class Security(models.Model):
    """Информация о ценных бумагах"""
    id = models.BigIntegerField(primary_key=True)
    secid = models.CharField(max_length=17, unique=True, verbose_name='Код документа')
    regnumber = models.CharField(max_length=63, blank=True, null=True, verbose_name='Номер государственной регистрации')
    name = models.CharField(max_length=255, verbose_name='Полное наименование')
    emitent_title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.secid

    class Meta:
        verbose_name = _('Информация о ценных бумагах')
        verbose_name_plural = _('Информация о ценных бумагах')
        ordering = ['secid']


class History(models.Model):
    """История торгов за произвольную дату"""
    id = models.AutoField(primary_key=True)
    secid = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='history_records', to_field='secid')
    tradedate = models.DateField(verbose_name='Дата проведения торгов')
    numtrades = models.FloatField(verbose_name='Количество сделок за торговый день')
    open = models.FloatField(blank=True, null=True, verbose_name='Цена первой сделки')
    close = models.FloatField(blank=True, null=True, verbose_name='Цена послеторгового периода')

    def __str__(self):
        return f"{self.secid} - {self.tradedate}"

    class Meta:
        verbose_name = _('История торгов за произвольную дату')
        verbose_name_plural = _('История торгов за произвольную дату')
