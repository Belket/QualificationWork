from django.db import models


class OfferedElement(models.Model):
    class Meta:
        verbose_name = "Offered Element"
        verbose_name_plural = "Offered Elements"
    name = models.CharField(max_length=100, blank=False)
    Company = models.CharField(max_length=100, blank=False)
    Class = models.CharField(max_length=100, blank=False)
    Group = models.CharField(max_length=100, blank=False)
    Subgroup = models.CharField(max_length=100, blank=False)
    T0 = models.FloatField(blank=False)
    Txp = models.FloatField(blank=False)
    Tp = models.FloatField(blank=False)
    TB = models.FloatField(blank=False)
    Info = models.TextField(blank=True)
    date_of_adding = models.DateField(blank=False)
    user_id = models.IntegerField(default=0)
