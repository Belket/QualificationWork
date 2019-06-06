from django.db import models
from HandBook.models import Company, Class, Group, SubGroup
from django.dispatch import receiver
from django.db.models.signals import post_save


class Element(models.Model):
    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
    name = models.CharField(max_length=100, blank=False, verbose_name="Название", unique=True)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Класс")
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    Subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE, verbose_name="Подгруппа")
    T0 = models.FloatField(blank=False, verbose_name="Средняя наработка на отказ")
    Txp = models.FloatField(blank=False, verbose_name="Средний срок сохраняемости")
    Tp = models.FloatField(blank=False, verbose_name="Средний ресурс (ч)")
    TB = models.FloatField(blank=False, verbose_name="Среднее время восстановления (ч)")
    Info = models.TextField(blank=True, verbose_name="Доп. Информация")
    date_of_adding = models.DateField(blank=False, verbose_name="Дата добавления")
    confirm_link = models.TextField(max_length=400, verbose_name="Подтверждающая ссылка")

    def save(self, *args, **kwargs):
        digits_after_comma = 2
        T0 = self.T0
        lambda0 = 1 / T0
        lambda_xp = lambda0 * 10 ** (-2)
        self.Txp = round(1 / (lambda_xp * 8760), digits_after_comma)
        self.Tp = round((1 - 0.15 * 0.253) * T0, digits_after_comma)
        super(Element, self).save(*args, **kwargs)


@receiver(post_save, sender=Element)
def calculate_means(sender, instance, **kwargs):
    subgroup = instance.Subgroup
    elements = Element.objects.filter(Subgroup=subgroup)
    amount_of_elements = len(elements)
    digits_after_comma = 2
    subgroup.midT0 = round(sum([element.T0 for element in elements]) / amount_of_elements, digits_after_comma)
    subgroup.midTxp = round(sum([element.Txp for element in elements]) / amount_of_elements, digits_after_comma)
    subgroup.midTp = round(sum([element.Tp for element in elements]) / amount_of_elements, digits_after_comma)
    subgroup.midTB = round(sum([element.TB for element in elements]) / amount_of_elements, digits_after_comma)
    subgroup.save()



