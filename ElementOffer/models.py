from django.db import models


class OfferedElement(models.Model):
    class Meta:
        verbose_name = "Предложенный элемент"
        verbose_name_plural = "Предложенные элементы"
    name = models.CharField(max_length=100, blank=False, verbose_name="Название")
    Class = models.CharField(max_length=100, blank=False, verbose_name="Класс")
    Group = models.CharField(max_length=100, blank=False, verbose_name="Группа")
    Subgroup = models.CharField(max_length=100, blank=False, verbose_name="Подгруппа")
    Company = models.CharField(max_length=100, blank=False, verbose_name="Компания")
    Maintainability = models.CharField(max_length=100, blank=False, verbose_name="Ремонтопригодность")
    MTBF = models.CharField(max_length=20, blank=False, verbose_name="MTBF")
    Source = models.CharField(max_length=100, blank=False, verbose_name="Источник")
    Info = models.TextField(blank=True, verbose_name="Доп. Информация")
    user_id = models.IntegerField(default=0, verbose_name="Пользовательский id")
