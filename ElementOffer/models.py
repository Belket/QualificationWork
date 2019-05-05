from django.db import models


class OfferedElement(models.Model):
    class Meta:
        verbose_name = "Offered Element"
        verbose_name_plural = "Offered Elements"
    name = models.CharField(max_length=100, blank=False)
    Class = models.CharField(max_length=100, blank=False)
    Group = models.CharField(max_length=100, blank=False)
    Subgroup = models.CharField(max_length=100, blank=False)
    Company = models.CharField(max_length=100, blank=False)
    Maintainability = models.CharField(max_length=100, blank=False)
    MTBF = models.CharField(max_length=20, blank=False)
    Source = models.CharField(max_length=100, blank=False)
    Info = models.TextField(blank=True)
    user_id = models.IntegerField(default=0)
